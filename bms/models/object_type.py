from odoo import api, models, fields


class ObjectType(models.Model):
    """
    Type of an object
    """

    _name = "bms.object_type"
    _description = "maintenance object type"

    name = fields.Char("type name")
    definition = fields.Char("definition")
    otl_type_internal_id = fields.Char("internal id")

    otl_name = fields.Char(related="otl_id.name")

    otl_id = fields.Many2one(comodel_name="bms.object_type_library")
    oslo_attributen_value_id = fields.One2many(comodel_name="bms.oslo_attributen_value", inverse_name="object_type_id")

    object_id = fields.Many2many(
        comodel_name="bms.maintainance_object",
        relation="bms_objects_to_types",
        column1="object_type_id",
        column2="object_id"
    )


