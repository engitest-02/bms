/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart } = owl;


export class Decomposition extends Component {

    setup(){
        this.ormService = useService("orm");

        onWillStart(async () => {
            this.decompositionTypeRecords = await this._loadDecompositionTypes();
        })
    }

    _loadDecompositionTypes(){
        return this.ormService.searchRead("bms.decomposition_type", [], []);
    }

}

Decomposition.template = "bms.Decomposition";

// CustomerList.props = {
//     selectCustomer: {
//         type: Function,
//     },
// };