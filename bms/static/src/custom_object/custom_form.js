/** @odoo-module */

import { registry } from "@web/core/registry";
import { Field } from "@web/views/fields/field";  
// import { X2ManyField } from "@web/fields/x2many/x2many_field";

const { Component } = owl;

export class CustomForm extends Component {}


CustomForm.template = "bms.custom_form";
CustomForm.components = { Field };


registry.category("fields").add("CustomForm", CustomForm);


