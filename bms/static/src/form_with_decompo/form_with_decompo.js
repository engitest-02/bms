/** @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { Decomposition } from "../decomposition/decomposition";
const { onWillUpdateProps } = owl;

class FormWithDecompoController extends FormController {

    setup() {
        super.setup();
        
//         onWillUpdateProps(async nextProps => {
            
//             console.log("FormWithDecompoController nextProps", this.model.data)})
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