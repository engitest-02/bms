// /** @odoo-module */

import { registry } from "@web/core/registry";

import {Address} from "./address"
import {DefaultWidget} from "./default_widget"

const widgets = [
    {
        id: "Address",
        Component: Address,
    },
    {
        id: "DefaultWidget",
        Component: DefaultWidget,
    } 
];

// register classes to make them retrievable in object_type.js  and usable in the template: t.component= "myCustomWidget"
widgets.forEach(widget => {
    registry.category("attribute_widget").add(widget.id, widget);
});