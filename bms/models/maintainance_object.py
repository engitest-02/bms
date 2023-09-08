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
    # otl_ids = fields.Many2many(
    #     comodel_name="bms.object_type_library",
    #     relation="objects_to_otl",
    #     column1="maintainance_object_id",
    #     column2="maintainance_otl_id",
    # )
