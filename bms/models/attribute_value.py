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

    attr_def_name = fields.Char(
        related="attr_def_id.name", readonly=True, string="attribute name"
    )
    attr_def_value_type = fields.Selection(
        related="attr_def_id.value_type", readonly=True
    )
    object_name = fields.Char(related="object_id.name", string="object name")

    # object_name = fields.Selection(related="object_ids.name")
    # object_type = fields.Char(related="object_ids.type_name")
    # object_is_active = fields.Boolean(ralaed)

    attr_def_id = fields.Many2one(comodel_name="bms.attribute_definition")
    object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="Maintainance Object")
