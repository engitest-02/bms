/** @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { Decomposition } from "../decomposition/decomposition";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService} from "@web/core/utils/hooks";

var core = require("web.core");
var rpc = require('web.rpc');
// var actionService = useService("action");

class FormWithDecompoController extends FormController {

    async saveButtonClicked(params={}){
        await super.saveButtonClicked(params);
        core.bus.trigger('maintainance_object_changed', null); // to refresh decomposition
    }

    async duplicateRecord() {
        await super.duplicateRecord();
        core.bus.trigger('maintainance_object_changed', null); // to refresh decomposition
    }

    async deleteRecord() {
        const objectIdToDelete = this.model.root.resId
        console.log("objectIdToDelete", objectIdToDelete)
        const decomposition_type_id = 1 // FIXME- decomposition_type_id is hardcoded
        console.warn("FIXME: deleteRecord uses hardcoded decomposition type.")
        const isNotDeletable = await this._hasChildren(objectIdToDelete, decomposition_type_id) 
        console.log("isNotDeletable", isNotDeletable)
        if (isNotDeletable) {
            await this.model.dialogService.add(AlertDialog,
                {
                    body: "The object you want to delete has still children.\nThe delete operation has not been performed.",
                    confirm: () => {}
                });
        }
        else {
            const [parent_id, sibling_id] = await this._getNearestObject(objectIdToDelete, decomposition_type_id)
            const decompositionObjectToActivate = sibling_id ? sibling_id : parent_id
            await this.model.root.delete();
            // console.log("root.resID", this.model.root.resId)
            console.log("deleteRecord", decompositionObjectToActivate, parent_id, sibling_id)
            //this._doActionForm(decompositionObjectToActivate)
            core.bus.trigger('maintainance_object_changed', decompositionObjectToActivate)
        }
    }


    async _hasChildren(object_id, decomposition_type_id){
        const hasChildren = rpc.query({
            model: 'bms.decomposition_relationship',
            method: 'has_children',
            args: [object_id, decomposition_type_id],
            });
        return hasChildren
    }

    async _getNearestObject(object_id, decomposition_type_id){
        const parentFirstSibling = rpc.query({
            model: 'bms.decomposition_relationship',
            method: 'get_nearest_object',
            args: [object_id, decomposition_type_id],
            });
        return parentFirstSibling
    }

    // _doActionForm(decompositionObjectToActivate){
    //     const action = {"type": "ir.actions.act_window",
    //                     "res_model": "bms.maintainance_object",
    //                     "views": [[false, "form"]],
    //                     "target": "current",
    //                     "res_id": decompositionObjectToActivate
    //                     };
    //     console.log("action", action);
        // actionService.doAction(action);
    // }

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