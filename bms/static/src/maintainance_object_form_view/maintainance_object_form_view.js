/** @odoo-module */
// import { FormController } from "@web/views/form/form_controller";
import { FormRenderer } from "@web/views/form/form_renderer";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { MaintainanceObject } from "../maintainance_object/maintainance_object"

const {useState} = owl;

class MaintainanceObjectRenderer extends FormRenderer {


    setup() {
        super.setup();
    }


}

MaintainanceObjectRenderer.template = "bms.MaintainanceObjectFormView";
MaintainanceObjectRenderer.components = {
    ...MaintainanceObjectRenderer.components, MaintainanceObject
};

export const maintainanceObjectView = {
    ...formView,
    Renderer: MaintainanceObjectRenderer,
};

registry.category("views").add("maintainance_object_form", maintainanceObjectView);