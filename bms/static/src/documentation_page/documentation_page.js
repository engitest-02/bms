/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class DocumentationPage extends Component {}

DocumentationPage.template="bms.documentation_page_action";
registry.category("actions").add("bms.DocumentationPageAction", DocumentationPage );
