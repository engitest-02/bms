from odoo import models, fields, api


class DecompositionRelationship(models.Model):
    """ """

    _name = "bms.decomposition_relationship"
    _description = "bms.decompostion_relationship: describes relationships of object in the different relationship types. (parent, sibling order, ...) "

    tree_level = fields.Integer("tree level")
    sibling_order = fields.Integer("sibling order", default=0)

    # object_name = fields.Char(related='object_id.name')

    object_id = fields.Many2one(
        comodel_name="bms.maintainance_object", ondelete="set null"
    )
    parent_object_id = fields.Many2one(
        comodel_name="bms.maintainance_object", ondelete="set null"
    )
    decomposition_type = fields.Many2one(
        comodel_name="bms.decomposition_type", ondelete="set null"
    )

    @api.model
    def getTree(self):
        """
        source: [
                {title: "Node 1", key: "1"},
                {title: "Folder 2", key: "2",
                    folder: true, children: [
                            {title: "Node 2.1", key: "3", myOwnAttr: "abc"},
                 get           {title: "Node 2.2", key: "4"}
                        ]}
                ]
        """
        tree = []

        level1_records = self._get_records(1)
        for record in level1_records:
            node = self._record2node(record)
            import pdb
       
            children_nodes = self._get_children(node)
            if children_nodes:
                node["folder"] = True
                node["children"] = children_nodes
            tree.append(node)
        import json
        import pprint
        # pprint.pprint(json.dumps(tree))   
        return json.dumps(tree)

    def _get_records(self, tree_level):
        domain = [("tree_level", "=", 1)]
        # domain = [("tree_level", "=", 4),('object_id.lantis_unique_id','=', 3675)]
        return self.env["bms.decomposition_relationship"].search(domain)

    def _record2node(self, record):
        return {"title": record.object_id.name, "key": record.object_id.id}

    def _get_children(self, node):
        parent_id = node["key"]

        domain = [("parent_object_id", "=", parent_id)]
        children_records = self.env["bms.decomposition_relationship"].search(domain)

        children_nodes = []
        for record in children_records:
            child_node = self._record2node(record)
            # import pdb; pdb.set_trace()
            little_children_nodes = self._get_children(child_node)
            
            if not little_children_nodes:
                children_nodes.append(child_node)
            else:
                child_node["folder"] = True
                child_node["children"] = little_children_nodes
            
            children_nodes.append(child_node)
        
        return children_nodes
