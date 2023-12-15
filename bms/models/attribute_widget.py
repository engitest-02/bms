from odoo import models, fields


class AttributeWidget(models.Model):
    _name = "bms.attribute_widget"
    _description = """ 
                    List of custom widgets appliable on attribute to modify the way they are displayed.
                    """
    
    name = fields.Char(string="name")#for the user
    js_component_name = fields.Char(string="JS component")# name of the Javascript component which will be used by the front-end JS code
    description = fields.Char(string="description")
