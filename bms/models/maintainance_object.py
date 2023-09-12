from odoo import models, fields, api


class MaintainanceObject(models.Model):
    """
    Maintenance object table
    """

    _name = "bms.maintainance_object"
    _description = "Maintenance object"

    name = fields.Char("name", required=True)
    lantis_unique_id = fields.Char("Lantis ID", required=True)
    is_active = fields.Boolean("Is active")
    is_asset = fields.Boolean("IS asset")

    # type_name = fields.Char(related="object_type_ids.name")
    # attr_def = fields.Char(related="attr_value_ids.attr_def_name")
    # value_type = fields.Char(compute="_get_value_type")

    # relational fields
    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )
    attr_value_ids = fields.One2many(
        comodel_name="bms.attribute_value",
        inverse_name="object_id"
    )

    # @api.depends("attr_def")
    # def _get_value_field(self):
    #     for record in self:
    #         value_type = dict(record._fields["selection_field"].selection).get(
    #             record.selection_field
    #         )
    #     return value_type

    #     match value_type:
    #         case "string":
    #             return fields.Char("string value")
    #         case "boolean":
    #             return fields.Boolean("boolean value")
    #         case "date":
    #             return fields.Date("date value")
    #         case "float":
    #             return fields.Float("float value")
    #         case "binary":
    #             return fields.Binary("binary value")
    #         case "integer":
    #             return fields.Integer("integer value")
