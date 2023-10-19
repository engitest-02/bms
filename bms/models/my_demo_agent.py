from odoo import api, models, fields


class MyDemoAgent(models.Model):
    _name = "bms.my_demo_agent"
    _description = "demo table to delete "

    name = fields.Char("Agent name")
    description = fields.Char("description")
    email = fields.Char("email")
    phone_number = fields.Char("phone number")


    object_ids = fields.One2many(comodel_name="bms.maintainance_object", inverse_name="agent_id")