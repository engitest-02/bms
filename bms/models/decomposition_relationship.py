from odoo import models, fields, api


import logging
logger = logging.getLogger(__name__)
logger.critical("Method _get_records() is in demo mode. It has been hardcoded. It has to be modified.")

class DecompositionRelationship(models.Model):
    """ """

    _name = "bms.decomposition_relationship"
    _description = "bms.decompostion_relationship: describes relationships of object in the different relationship types. (parent, sibling order, ...) "

    tree_level = fields.Integer("tree level")
    sibling_order = fields.Integer("sibling order", default=0)

    # object_name = fields.Char(related='object_id.name')
    object_awv_type_not_found = fields.Boolean(related="object_id.awv_type_not_found")
    object_id_id = fields.Integer(related="object_id.id", string="object_id")

    object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete="set null")
    parent_object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete="set null")
    decomposition_type_id = fields.Many2one(comodel_name="bms.decomposition_type", ondelete="set null")


    # @api.model
    # def getTree(self, decomposition_type_id=1):
    #     """
    #     source: [
    #             {title: "Node 1", key: "1"},
    #             {title: "Folder 2", key: "2",
    #                 folder: true, children: [
    #                         {title: "Node 2.1", key: "3", myOwnAttr: "abc"},
    #              get           {title: "Node 2.2", key: "4"}
    #                     ]}
    #             ]
    #     """
    #     tree = []
    #     level1_records = self._get_records(None, decomposition_type_id)#TODO: change with 1
    #     for record in level1_records:
    #         node = self._record2node(record.object_id)
    #         children_nodes = self._get_all_children(node, decomposition_type_id)
    #         if children_nodes:
    #             node["folder"] = True
    #             node["children"] = children_nodes
    #         tree.append(node)
    #     import json
    #     return json.dumps(tree)

    @api.model
    def get_lazy_tree(self, parent_id, decomposition_type_id=1):
        "return children tree"
        tree = []
        # if parent_id is None:
        #     records = self._get_records(1, decomposition_type_id=1)
        # else:
        node = {"title": "", "key": int(parent_id), "lazy": False}
        records = self._get_children(node, decomposition_type_id)
        for record in records:
            hasChildren = self._has_children(record.object_id.id, decomposition_type_id )
            node = self._record2node(record.object_id, folder=hasChildren, lazy=hasChildren)
            tree.append(node)
        import json
        print("get_lazy_tree", json.dumps(tree))
        return json.dumps(tree)

    @api.model
    def get_lazy_tree_for_object(self, object_id, decomposition_type_id=1):
        "Return the lineage tree of object_id for a decompostin type"
        object_id_rec = self._get_maintainance_object(object_id)
        has_children = self._has_children(object_id, decomposition_type_id)
        tree = self._record2node(object_id_rec, folder=has_children, lazy=has_children)
        
        parent = self._get_parent(object_id, decomposition_type_id)
        
        previous_parent_id = object_id
        lazy_tree=[]

        # create parents and sibling lineage of child_id
        while parent:

            parent_node = self._record2node(parent, folder=True, lazy=False)
            children_nodes = self._get_children_nodes(parent.id, decomposition_type_id)
            print("while parent", parent, children_nodes, tree)            
            for idx, child in enumerate(children_nodes):
                if child["key"] == previous_parent_id:
                    children_nodes[idx] = tree
                    print("if child", idx, previous_parent_id)
                    break
            parent_node["children"] = children_nodes
            tree = parent_node
            previous_parent_id = parent.id
            parent = self._get_parent(parent.id, decomposition_type_id)
        

        if not parent: # get sibling top = level 1
            level1_records = self._get_records(1, decomposition_type_id)
            for idx, sibling in enumerate(level1_records):
                has_children = self._has_children(sibling.object_id.id, decomposition_type_id)
                node = self._record2node(sibling.object_id, folder=has_children, lazy=has_children)
                if node["key"] == previous_parent_id:
                    node = tree
                lazy_tree.append(node)    
        import json
        print(json.dumps(lazy_tree))
        return json.dumps(lazy_tree)


    def _get_records(self, tree_level, decomposition_type_id):
        domain = [("tree_level", "=", tree_level),("decomposition_type_id", "=", decomposition_type_id )]
        if tree_level is None: #TODO to delete - only for demo
            domain = [("tree_level", "=", 4),('object_id.lantis_unique_id','=', 3675)]
        return self.env["bms.decomposition_relationship"].search(domain)

    def _record2node(self, record, folder=False, lazy=False):
        node = {"title": record.name, "key": record.id, "folder":folder,  "lazy": lazy}
        if record.awv_type_not_found:
            node = {**node, "extraClasses": "has_no_awv_type"}
        return node

    def _get_children_nodes(self, parent_id, decomposition_type_id):
        children_nodes = []
        children = self._get_children({'key':parent_id}, decomposition_type_id)
        for child in children:
            has_children = self._has_children(child.object_id.id, decomposition_type_id)
            if has_children:
                node = self._record2node(child.object_id, folder=has_children, lazy=has_children )
            else:
                node = self._record2node(child.object_id)
            children_nodes.append(node)
        return children_nodes


    def _has_children(self, object_id, decomposition_type_id):
        domain=[("parent_object_id", "=", object_id), ("decomposition_type_id", "=", decomposition_type_id)]
        records = self.env["bms.decomposition_relationship"].search(domain)
        if len(records) > 0:
            return True
        else: 
            return False

    def _get_maintainance_object(self, object_id):
        domain=[("id", "=", object_id)]
        record = self.env["bms.maintainance_object"].search(domain)
        return record


    def _get_children(self, node, decomposition_type_id):
        parent_id = node["key"]
        domain = [("parent_object_id", "=", parent_id),("decomposition_type_id", "=", decomposition_type_id)]
        children_records = self.env["bms.decomposition_relationship"].search(domain)
        return children_records

    def _get_parent(self, child_id, decomposition_type_id):
        domain = [("object_id", "=" , child_id), ("decomposition_type_id", "=", decomposition_type_id)]
        rec = self.env["bms.decomposition_relationship"].search(domain, [])
        return rec.parent_object_id

    def _get_all_children(self, node, decomposition_type_id):
        parent_id = node["key"]

        domain = [("parent_object_id", "=", parent_id), ("decomposition_type_id", "=", decomposition_type_id)]
        children_records = self.env["bms.decomposition_relationship"].search(domain)

        children_nodes = []
        for record in children_records:
            child_node = self._record2node(record.object_id)
            # import pdb; pdb.set_trace()
            little_children_nodes = self._get_all_children(child_node, decomposition_type_id )
            
            if little_children_nodes:
                child_node["folder"] = True
                child_node["children"] = little_children_nodes
            
            children_nodes.append(child_node)
        
        return children_nodes
