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
    is_asset = fields.Boolean("Is asset")

    awv_type_not_found = fields.Boolean()
    bo_temporary_type = fields.Char()

    # relational fields
    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )
    attr_value_ids = fields.One2many(
        comodel_name="bms.attribute_value", inverse_name="object_id"
    )
    parent_object_ids = fields.One2many(comodel_name="bms.decomposition_relationship", inverse_name="parent_object_id")
    decomposition_ids = fields.One2many(
        comodel_name="bms.decomposition_relationship", inverse_name="object_id"
    )
    
    #demo agent
    agent_name = fields.Char(related="agent_id.name", readonly=True)
    agent_description = fields.Char(related="agent_id.description", readonly=True)
    agent_email = fields.Char(related="agent_id.email", readonly=True)
    agent_phone_number = fields.Char(related="agent_id.phone_number", readonly=True)
    
    agent_id = fields.Many2one(comodel_name="bms.my_demo_agent", readonly=False)

