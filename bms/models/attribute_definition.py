from odoo import models, fields


class AttributeDefinition(models.Model):
    """ """

    _name = "bms.attribute_definition"
    _description = "Attribute definition"

    name = fields.Char("name")
    description = fields.Char("description")
    value_type = fields.Selection(
        [
            ("char", "char"),
            ("boolean", "boolean"),
            ("date", "date"),
            ("float", "float"),
            ("binary", "binary"),
            ("integer", "integer"),
        ],
        string="value type",
    )

    value_char = fields.Char("string_value", related="attr_value_id.value_char")
    value_boolean = fields.Boolean(
        "boolean value", related="attr_value_id.value_boolean"
    )
    value_date = fields.Date("date value", related="attr_value_id.value_date")
    value_float = fields.Float("float value", related="attr_value_id.value_float")
    value_integer = fields.Integer(
        "integer value", related="attr_value_id.value_integer"
    )

    otl_name = fields.Char(related="object_type_id.name")

    object_type_id = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_attributes_to_types",
        column1="attribute_id",
        column2="object_type_id",
    )
    attr_value_id = fields.One2many(comodel_name="bms.attribute_value", inverse_name="attr_def_id")
