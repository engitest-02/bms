from odoo import models, fields


class AttributeDefinition(models.Model):
    """ """

    _name = "bms.attribute_definition"
    _description = "Attribute definition"

    name = fields.Char("name")
    description = fields.Char("description")
    value_type = fields.Selection(
        [
            ("string", "string"),
            ("boolean", "boolean"),
            ("date", "date"),
            ("float", "float"),
            ("binary", "binary"),
            ("integer", "integer"),
        ],
        string="value type",
    )

    type_id = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_attributes_to_types",
        column1="attribute_id",
        column2="type_id",
    )
    attr_value_id = fields.One2many(
        comodel_name="bms.attribute_value", inverse_name="attr_def_id"
    )
