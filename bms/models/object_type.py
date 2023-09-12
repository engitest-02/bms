from odoo import models, fields


class ObjectType(models.Model):
    """
    Type of an object
    """

    _name = "bms.object_type"
    _description = "maintenance object type"

    name = fields.Char("type name")
    description = fields.Char("description")

    otl_id = fields.Many2one(comodel_name="bms.object_type_library")
    object_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_type_id",
        column2="object_id"
    )

    attribute_ids = fields.Many2many(
        comodel_name="bms.attribute_definition",
        relation="bms_attributes_to_types",
        column1="type_id",
        column2="attribute_id",
    )
