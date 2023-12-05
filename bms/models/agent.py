from odoo import models, fields, api


class Agent(models.Model):
    _name = "bms.agent"
    _description = """A resource that acts or has the power to act."""

    first_name = fields.Char("first name")
    surname = fields.Char("surname")
    phone_number = fields.Char("phone number")
    email = fields.Char("email")
    organisation = fields.Char("organisation")