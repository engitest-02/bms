from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError


class OsloaAttributenValueEdit(models.TransientModel):
    _name = "bms.oslo_attributen_value_edit"
    _description = "Transient model for the assignation of a value to an Oslo attribute linked to an existing object."

    object_id = fields.Many2one("bms.maintainance_object", string="maintainance object")
    object_type_id = fields.Many2one("bms.object_type", string="object type")
    attr_def_id = fields.Many2one("bms.attribute_definition_", string="attribute definition id")
    
    
    attr_def_id_id = fields.Integer(related="attr_def_id.id")
    attr_def_uri = fields.Char(related="attr_def_id.uri")


    attr_name = fields.Char("attribute name")
    attr_def = fields.Char("attribute definition")
    attr_def_datatype_definition = fields.Char("value definition")
    attr_def_value_type = fields.Char(related="attr_def_id.value_type", string="value type")

    value_char = fields.Char("value", default=None)
    value_boolean = fields.Boolean("value", default=False)
    value_date = fields.Date("value", default=None)
    value_datetime = fields.Datetime("value", default=None)
    value_float = fields.Float("value", default=None)
    value_non_negative_integer = fields.Integer("value", default=None)
    value_enumeration = fields.Selection(selection="_compute_selection", string="value", default="_get_selection_default")

  
    @api.constrains('value_non_negative_integer')
    def _check_description(self):
        for rec in self:
            if rec.value_non_negative_integer < 0:
                raise ValidationError("The expected value has to be a non negative integer")

    def _compute_selection(self):
        return self._context["default_enumeration_selection_values"]
    
    @api.model
    def _get_selection_default(self):
        print("value enumeration", self._context["default_value_enumeration"])
        return self._context["default_value_enumeration"]

    @api.model
    def create(self, vals):
        self._change_attribute_value(vals)
        return super(OsloaAttributenValueEdit, self).create(vals)

    def write(self, vals):
        self._change_attribute_value(vals)
        return super(OsloaAttributenValueEdit, self).write(vals)

    def _change_attribute_value(self, vals):
        vals = {
            **vals,
            "object_id": self._context["default_object_id"],
            "object_type_id": self._context["default_object_type_id"],
            "attr_def_id": self._context["default_attr_def_id"],
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
            ("attr_def_id", "=", vals["attr_def_id"]),
        ]
        return self.env["bms.oslo_attributen_value"].search(domain)

    def _custom_update(self, record, vals):
        print("_update called")
        key = "value_" + vals["attr_def_value_type"]
        values = {key: vals[key]}
        record.write(values)
        return True

    def _custom_create(self, vals):
        print("_create called", vals, type(vals))
        key = "value_" + vals["attr_def_value_type"]
        values = {
            "object_id": vals["object_id"],
            "object_type_id": vals["object_type_id"],
            "attr_def_id": vals["attr_def_id"],
            key: vals[key]
        }
        print(values)
        new_att_value = self.env["bms.oslo_attributen_value"].create([values])
        return True
