from odoo import models, fields


class ObjectType(models.Model):
    """
    Type of an object
    """

    _name = "bms.object_type"
    _description = "maintenance object type"

    type_name = fields.Char("type name")
    description = fields.Char("description")
    # attribute_name = fields.Char("attribute name")
    # attribute_value_type = fields.Char("attribute value type")

    otl_id = fields.Many2one(comodel_name="bms.object_type_library", ondelete="cascade")
    attribute_ids = fields.Many2many(
        comodel_name="bms.attribute_definition",
        relation="bms_attributes_to_types",
        column1="type_id",
        column2="attribute_id",
    )

    # maintaintance_object_ids = fields.Many2many(
    #     comodel_name="bms.maintainance_object",
    #     relation="objects_to_types",
    #     column1="object_type_id",
    #     column2="maintainance_object_id")
