from odoo import models, fields


class MaintainanceObject(models.Model):
    """
    Maintenance object table
    """

    _name = "bms.maintainance_object"
    _description = "Maintenance object"

    name = fields.Char("name", required=True)
    lantis_unique_id = fields.Char("Lantis ID", required=True)
    # is_active = fields.Boolean("Is active")
    # is_asset = fields.Boolean("Is asset")

    awv_type_not_found = fields.Boolean()
    bo_temporary_type = fields.Char()

    # relational fields
    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )
    # attr_value_ids = fields.One2many(
    #     comodel_name="bms.attribute_value", inverse_name="object_id"
    # )
    parent_object_ids = fields.One2many(comodel_name="bms.decomposition_relationship", inverse_name="parent_object_id")
    decomposition_ids = fields.One2many(
        comodel_name="bms.decomposition_relationship", inverse_name="object_id"
    )  
    oslo_attributen_value_id = fields.One2many(comodel_name="bms.oslo_attributen_value", inverse_name="object_id")
