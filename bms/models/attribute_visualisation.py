from odoo import models, fields, api


class AttributeVisualisation(models.Model):
    _name = "bms.attribute_visualisation" 
    _description = """ Let the user define how an attribute should be displayed on the maintainance object screens
                       - invisible is true: the attribute is not displayed 
                       - widget: the javascript component to use to display this attribute (several attributes can share a same widget. 
                       They are given as Owl props to the widget.)
         """
    
    label_nl = fields.Char(string="attribute")
    uri = fields.Char(string="uri")
    invisible = fields.Boolean(string="invisible", default=False)

    #relationship
    widget_id = fields.Many2one(comodel_name="bms.attribute_widget", string="widget")

