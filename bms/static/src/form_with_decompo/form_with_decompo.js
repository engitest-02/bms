/** @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { Decomposition } from "../decomposition/decomposition";
const { onWillUpdateProps } = owl;
var core = require("web.core");

class FormWithDecompoController extends FormController {

    async saveButtonClicked(params={}){
        await super.saveButtonClicked(params);
        core.bus.trigger('maintainance_object_changed', null); // used by decomposition
    }

}

FormWithDecompoController.template = "bms.decompositionRenderer";
FormWithDecompoController.components = {
     ...FormWithDecompoController.components, Decomposition
 };

export const formWithDecompoController = {
    ...formView,
    Controller: FormWithDecompoController,
};

registry.category("views").add("bms_form_with_decompo", formWithDecompoController);