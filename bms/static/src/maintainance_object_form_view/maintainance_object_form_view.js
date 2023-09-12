/** @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { MaintainanceObject } from "../maintenance_object/maintainance_object"

class MaintainanceObjectController extends FormController {
    setup() {
        super.setup();
        this.archInfo = { ...this.props.archInfo }; // so that the archInfo are available in the component via props
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