from odoo import models, fields


class ObjectType(models.Model):
    """
    Type of an object
    """

    _name = "bms.object_type"
    _description = "maintenance object type"

    name = fields.Char("type name")
    value_type = fields.Char("value type")


    otl_id = fields.Many2one(comodel_name="bms.object_type_library",
                             ondelete="cascade")