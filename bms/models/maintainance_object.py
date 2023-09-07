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
    # maintainance_object_type_ids = fields.Many2many(
    #     comodel_name="bms.maintainance_object_type",
    #     relation="objects_to_types",
    #     column1="maintainance_object_id",
    #     column2="maintainance_object_type_id",
    # )
