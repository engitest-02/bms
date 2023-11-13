from odoo import models, fields


class AttributeValue(models.Model):
    """
    As the attributes are function of the object type, creatie of mechanism of
    attribute definition <-> attibute value to store in the database with the
    right native primary field type (string, float, date, ....)
    Cardinality chain
    object 1 <-> * type 1 <-> * attributes_def 1 <-> * attributes values 1 <-> 1 object
    """

    _name = "bms.attribute_value"
    _description = "bms.attribute_value: store values of attribute of an object type"
   

    value_char = fields.Char("value", default=None)
    value_boolean = fields.Boolean("value", default=False)
    value_date = fields.Date("value", default=None)
    value_float = fields.Float("value", default=None)
    value_integer = fields.Integer("value", default=None)

    # attr_def_name = fields.Char(related="attr_def_id.name", readonly=True, string="attribute name")
    # attr_def_value_type = fields.Selection(related="attr_def_id.value_type", readonly=True)
    object_name = fields.Char(related="object_id.name", string="object name")

    object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="Maintainance Object", required=True, ondelete="cascade")
    object_type_id = fields.Many2one(comodel_name="bms.object_type", required=True, ondelete="cascade")
    # attr_def_id = fields.Many2one(comodel_name="bms.attribute_definition", required=True, ondelete="cascade")
    
    