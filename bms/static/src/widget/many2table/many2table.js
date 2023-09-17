/** @odoo-module */

import { registry } from "@web/core/registry";
import { Field } from "@web/views/fields/field";  
// import { X2ManyField } from "@web/fields/x2many/x2many_field";

const { Component } = owl;

export class Many2ManyTable extends Component {}


Many2ManyTable.template = "bms.Many2ManyTable";
Many2ManyTable.components = { Field };
// Many2ManyTable.supportedTypes = ["many2many"];
// Many2ManyTable.useSubView = true;

registry.category("fields").add("Many2Many_table", Many2ManyTable);



