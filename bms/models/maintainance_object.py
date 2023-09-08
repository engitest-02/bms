from odoo import models, fields


class MaintainanceObject(models.Model):
    """
    Maintenance object table
    """

    _name = "bms.maintainance_object"
    _description = "Maintenance object"

    name = fields.Char("name", required=True)
    lantis_unique_id = fields.Char("Lantis ID", required=True)
    is_active = fields.Boolean("Is active")
    is_asset = fields.Boolean("IS asset")

    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )
    attr_value_ids = fields.Many2many(
        comodel_name="bms.attribute_value",
        relation="bms_objects_to_attr_values",
        column1="object_id",
        column2="attr_value_id",
    )
