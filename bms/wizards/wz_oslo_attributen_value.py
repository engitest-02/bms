from odoo import models, fields, api, Command


class WzOsloaAttributenValue(models.TransientModel):
    _name = "bms.wz_oslo_attributen_value"
    _description = "Transient model for the assignation of a value to an Oslo attribute linked to an existing object."

    object_id = fields.Many2one("bms.maintainance_object", string="maintainance object")
    object_type_id = fields.Many2one("bms.object_type", string="object type")

    attr_name = fields.Char("attribute name")
    attr_def = fields.Char("attribute definition")
    att_def_value_type_definition = fields.Char("value definition")
    attr_def_value_type = fields.Char("value type")

    value_char = fields.Char("value", default=None)
    value_boolean = fields.Boolean("value", default=False)
    value_date = fields.Date("value", default=None)
    value_datetime = fields.Datetime("value", default=None)
    value_float = fields.Float("value", default=None)
    value_integer = fields.Integer("value", default=None)

    oslo_datatype_xxx_attributen_uri = fields.Char(
        "oslo_datatype_xxx_attributen_uri", default=None
    )
    oslodatatype_primitive_uri = fields.Char("oslodatatype_primitive_uri")

    @api.model
    def create(self, vals):
        self._change_attribute_value(vals)
        return super(WzOsloaAttributenValue, self).create(vals)

    def write(self, vals):
        self._change_attribute_value(vals)
        return super(WzOsloaAttributenValue, self).write(vals)

    def _change_attribute_value(self, vals):
        vals = {
            **vals,
            "object_id": self._context["default_object_id"],
            "object_type_id": self._context["default_object_type_id"],
            "oslo_attributen_uri": self._context["default_oslo_attributen_uri"],
            "attr_def_value_type": self._context["default_attr_def_value_type"]
        }
        record = self._get_existing_item(vals)
        if record:
            return self._custom_update(record, vals)
        else:
            return self._custom_create(vals)

    def _get_existing_item(self, vals):
        domain = [
            ("object_id", "=", vals["object_id"]),
            ("object_type_id", "=", vals["object_type_id"]),
            ("oslo_attributen_uri", "=", vals["oslo_attributen_uri"]),
        ]
        return self.env["bms.oslo_attributen_value"].search(domain)


    def _custom_update(self, record, vals):
        print("_update called")
        key = "value_" + vals["attr_def_value_type"]
        values = {key: vals[key]}
        record.write(values)
        breakpoint()
        return True

    def _custom_create(self, vals):
        print("_create called", vals, type(vals))
        values = {
            "object_id": vals["object_id"],
            "object_type_id": vals["object_type_id"],
            "oslo_attributen_uri": vals["oslo_attributen_uri"]
        }
        key = "value_" + vals["attr_def_value_type"]
        values = {**values, key: vals[key]}
        print(values)

        new_att_value = self.env["bms.oslo_attributen_value"].create([values])
        return True
