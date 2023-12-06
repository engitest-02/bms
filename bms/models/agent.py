from odoo import models, fields, api


class Agent(models.Model):
    _name = "bms.agent"
    _description = """A human resource that acts or has the power to act."""

    
    name = fields.Char(default=lambda self: self._default_name(), store=False)
    first_name = fields.Char("first name", required=True)
    surname = fields.Char("surname", required=True)
    phone_number = fields.Char("phone number")
    email = fields.Char("email")
    organisation = fields.Many2one(comodel_name="bms.organisation", string="organisation", required=True)

    def _default_name(self):
        if self:
            return self.first_name + " " + self.surname
        else: 
            return " empty {0}".format(str(self.id))

class Organisation(models.Model):
    _name = "bms.organisation"
    _description ="""A legal entity involves in the asset management"""

    name = fields.Char("name")
    street = fields.Char("street")
    number = fields.Char("number")
    box_number = fields.Char("box numer")
    postcode = fields.Char("postcode")
    city = fields.Char("city")
    country = fields.Char("country")
    vat = fields.Char("vat number")
    contact_person = fields.Many2one(comodel_name="bms.agent", string="contact person")
