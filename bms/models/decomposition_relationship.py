from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError


class DecompositionRelationship(models.Model):
    _name = "bms.decomposition_relationship"
    _description = "Describes relationships between objects to create decomposition trees (parent, sibling order, ...) "

    tree_level = fields.Integer("tree level")
    sibling_order = fields.Integer("sibling order", default=0)

    object_awv_type_not_found = fields.Boolean(related="object_id.awv_type_not_found")
    object_id_id = fields.Integer(related="object_id.id", string="object_id")

    parent_object_id_id = fields.Char(related="parent_object_id.mo_id", string="parent id")
    
    object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete='cascade')
    parent_object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete="set null", string="parent name")
    decomposition_type_id = fields.Many2one(comodel_name="bms.decomposition_type", ondelete="set null", string="Decomposition name", default=1)


    @api.constrains("object_id","decomposition_type_id","parent_object_id")
    def _constraint_object_id(self):
        for rec in self:
            results = self.env["bms.decomposition_relationship"].read_group(
                domain=[("object_id", "=", rec.object_id.id)],
                fields=["object_id:count"],
                groupby=["decomposition_type_id"])
            for result in results:
                if result.get('decomposition_type_id_count') > 1:
                    msg = "You cannot assign more than one parent to this object for the decomposition '{0}'.".format(result.get("decomposition_type_id")[1])
                    raise ValidationError(msg)
                
    @api.model
    def get_lazy_tree(self, parent_id, decomposition_type_id=1):
        """return children tree"""

        tree = []
        node = {"title": "", "key": int(parent_id), "lazy": False}
        records = self._get_children(node, decomposition_type_id)
        for record in records:
            hasChildren = self.has_children(record.object_id.id, decomposition_type_id )
            node = self._record2node(record.object_id, folder=hasChildren, lazy=hasChildren)
            tree.append(node)
        import json
        
        return json.dumps(tree)

    @api.model
    def get_lazy_tree_for_object(self, object_id, decomposition_type_id=1):
        "Return the lineage tree of object_id for a decompostin type"
        object_id_rec = self._get_maintainance_object(object_id)
        has_children = self.has_children(object_id, decomposition_type_id)

        tree = self._record2node(object_id_rec, folder=has_children, lazy=has_children)
        
        parent = self.get_parent(object_id, decomposition_type_id)
        
        previous_parent_id = object_id
        lazy_tree=[]

        # create parents and sibling lineage of child_id
        while parent:
            parent_node = self._record2node(parent, folder=True, lazy=False)
            children_nodes = self._get_children_nodes(parent.id, decomposition_type_id)
       
            for idx, child in enumerate(children_nodes):
                if child["key"] == previous_parent_id:
                    children_nodes[idx] = tree
                    break
            parent_node["children"] = children_nodes
            tree = parent_node
            previous_parent_id = parent.id
            parent = self.get_parent(parent.id, decomposition_type_id)
        
        if not parent: # get sibling top = level 1
            level1_records = self._get_top_objects(decomposition_type_id)
            for idx, sibling in enumerate(level1_records):
                has_children = self.has_children(sibling.object_id.id, decomposition_type_id)
                node = self._record2node(sibling.object_id, folder=has_children, lazy=has_children)
                if node["key"] == previous_parent_id:
                    node = tree
                lazy_tree.append(node)    
        import json
       
        return json.dumps(lazy_tree)

    @api.model
    def update_sibling_order(self, object_id, parent_id, sibling_order,  decomposition_type_id=1):
        domain = [("object_id", "=", object_id), ("decomposition_type_id", "=", decomposition_type_id )]
        rec = self.env['bms.decomposition_relationship'].search(domain)
        
        vals = {'sibling_order': sibling_order, 'parent_object_id': parent_id }
        result = rec.write(vals)


    @api.model
    def has_children(self, object_id, decomposition_type_id):
        domain=[("parent_object_id", "=", object_id), ("decomposition_type_id", "=", decomposition_type_id)]
        records = self.env["bms.decomposition_relationship"].search(domain)
        if len(records) > 0:
            return True
        else: 
            return False

    @api.model
    def get_parent(self, object_id, decomposition_type_id):
        domain = [("object_id", "=" , object_id), ("decomposition_type_id", "=", decomposition_type_id)]
        rec = self.env["bms.decomposition_relationship"].search(domain)
        return rec.parent_object_id
    
    @api.model
    def get_siblings(self, object_id):
        """ Returns: list maintainance object of siblings for object_id (without object_id). 
            Params: internal id of a maintainance object
            !!! decomposition type id = 1 !!!
        """
        parent_obj_rec = self.get_parent(object_id, decomposition_type_id=1)
              
        domain = [("parent_object_id", "=", parent_obj_rec.id), ("object_id", "!=", object_id)]
        siblings_obj_rel_recs = self.env["bms.decomposition_relationship"].search(domain)
        sibling_obj_recs = [rec.object_id for rec in siblings_obj_rel_recs]
        print("get_parent:obj; parent_obj", object_id, parent_obj_rec)
        print("children", sibling_obj_recs)
        return sibling_obj_recs
    

    @api.model
    def get_nearest_object(self, object_id, decomposition_type_id):
        """return the next sibling of the object, if not, the parent, if not (root), the sibling of the parent"""
        parent_id = self.get_parent(object_id, decomposition_type_id)
        domain = [("parent_object_id", "=" , parent_id.id),
                  ("decomposition_type_id", "=", decomposition_type_id),
                  ("object_id", "!=", object_id)]
        rec = self.env["bms.decomposition_relationship"].search(domain, limit=1, order="sibling_order ASC")
        return [parent_id.id, rec.object_id.id]

    @api.model
    def has_children(self, object_id, decomposition_type_id):
        domain=[("parent_object_id", "=", object_id), ("decomposition_type_id", "=", decomposition_type_id)]
        records = self.env["bms.decomposition_relationship"].search(domain)
        if len(records) > 0:
            return True
        else: 
            return False

    @api.model
    def get_parent(self, object_id, decomposition_type_id):
        domain = [("object_id", "=" , object_id), ("decomposition_type_id", "=", decomposition_type_id)]
        rec = self.env["bms.decomposition_relationship"].search(domain)
        return rec.parent_object_id
    
    @api.model
    def get_nearest_object(self, object_id, decomposition_type_id):
        """return the next sibling of the object, if not, the parent, if not (root), the sibling of the parent"""
        parent_id = self.get_parent(object_id, decomposition_type_id)
        domain = [("parent_object_id", "=" , parent_id.id),
                  ("decomposition_type_id", "=", decomposition_type_id),
                  ("object_id", "!=", object_id)]
        rec = self.env["bms.decomposition_relationship"].search(domain, limit=1, order="sibling_order ASC")
        return [parent_id.id, rec.object_id.id]

    def _get_top_objects(self, decomposition_type_id):
        domain = [("parent_object_id", "=", None),("decomposition_type_id", "=", decomposition_type_id )]
        order = "sibling_order"
        return self.env["bms.decomposition_relationship"].search(domain, order=order)

    def _record2node(self, record, folder=False, lazy=False):
        IS_MANAGING_LEVEL_ICON = """<i class="fa fa-handshake-o" aria-hidden="true"></i>"""
        MISSING_OTL_TYPE_ICON = """<span class="fa-stack o_bms_fa_small">
                                        <i class="fa fa-tag fa-stack-1x"></i>
                                        <i class="fa fa-ban fa-stack-2x"></i>
                                </span>"""
        title = record.name
        if record.is_managing_level:
            title += " " + IS_MANAGING_LEVEL_ICON 
        if not record.has_object_type_ids:
            title += " " + MISSING_OTL_TYPE_ICON 
        node = {"title": title, "key": record.id, "folder":folder,  "lazy": lazy}
        return node

    def _get_children_nodes(self, parent_id, decomposition_type_id):
        children_nodes = []
        children = self._get_children({'key':parent_id}, decomposition_type_id)
        for child in children:
            has_children = self.has_children(child.object_id.id, decomposition_type_id)
            if has_children:
                node = self._record2node(child.object_id, folder=has_children, lazy=has_children )
            else:
                node = self._record2node(child.object_id)
            children_nodes.append(node)
        return children_nodes

    def _get_maintainance_object(self, object_id):
        domain=[("id", "=", object_id)]
        record = self.env["bms.maintainance_object"].search(domain)
        return record

    def _get_children(self, node, decomposition_type_id):
        parent_id = node["key"]
        domain = [("parent_object_id", "=", parent_id),("decomposition_type_id", "=", decomposition_type_id)]
        order = "sibling_order"
        children_records = self.env["bms.decomposition_relationship"].search(domain, order=order)
        return children_records
  
    def _get_all_children(self, node, decomposition_type_id):
        parent_id = node["key"]
        
        domain = [("parent_object_id", "=", parent_id), ("decomposition_type_id", "=", decomposition_type_id)]
        order = "sibling_order"
        children_records = self.env["bms.decomposition_relationship"].search(domain, order=order)

        children_nodes = []
        for record in children_records:
            child_node = self._record2node(record.object_id)
            little_children_nodes = self._get_all_children(child_node, decomposition_type_id )
            
            if little_children_nodes:
                child_node["folder"] = True
                child_node["children"] = little_children_nodes
            
            children_nodes.append(child_node)
        
        return children_nodes
