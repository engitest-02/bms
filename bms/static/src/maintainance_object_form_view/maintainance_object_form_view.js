/** @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { MaintainanceObject } from "../maintainance_object/maintainance_object"

const {useState} = owl;

class MaintainanceObjectController extends FormController {
    
     // this.props.model.root.data.attr_value_ids;

    setup() {
        super.setup();
    }


}

MaintainanceObjectController.template = "bms.MaintainanceObjectFormView";
MaintainanceObjectController.components = {
    ...MaintainanceObjectController.components, MaintainanceObject
};

export const maintainanceObjectView = {
    ...formView,
    Controller: MaintainanceObjectController,
};

registry.category("views").add("maintainance_object_form", maintainanceObjectView);