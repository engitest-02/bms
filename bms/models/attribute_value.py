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
    _description = "store values of attribute of an object type"

    value_string = fields.Char("string_value")
    value_boolean = fields.Boolean("boolean value")
    value_date = fields.Date("date value")
    value_float = fields.Float("float value")
    value_binary = fields.Binary("binary value")
    value_integer = fields.Integer("integer value")

    attr_def_id = fields.Many2one(comodel_name="bms.attribute_definition")
    object_ids = fields.Many2many(
        comodel_name="bms.maintainance_object",
        relation="bms_objects_to_attr_values",
        column1="attr_value_id",
        column2="object_id",
    )
