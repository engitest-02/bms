from odoo import models, fields

class DecompositionRelationship(models.Model):
    """
    """

    _name = "bms.decomposition_relationship"
    _description = "bms.decompostion_relationship: describes relationships of object in the different relationship types. (parent, sibling order, ...) "
    
  
    sibling_order = fields.Integer("sibling order", default=0)
    
    object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete="set null")
    parent_object_id = fields.Many2one(comodel_name="bms.maintainance_object", ondelete="set null")
    decomposition_type = fields.Many2one(comodel_name="bms.decomposition_type", ondelete="set null")
