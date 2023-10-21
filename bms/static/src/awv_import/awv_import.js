/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";

class AwvImportAction extends Component {
    setup(){
        this.orm = useService("orm");
        this.nbr_enumerations;
        this.state = useState({processed: 0, total_to_process: 0});
    }

    async import_awv_enumeration_values() {
        this.state.processed = 0;
        this.state.total_to_process = await this.orm.searchCount("bms.oslo_enumeration", []);
        const enumeration_ids = await this.orm.searchRead("bms.oslo_enumeration",[],["id"]);
        var rpc = require('web.rpc');
        
        Object.values(enumeration_ids).forEach((enumeration_id) => {
        const is_done = rpc.query({
            model: 'bms.oslo_enumeration_values',
            method: 'import_value_list',
            args: [enumeration_id.id],
        }).then(() => {this.state.processed += 1}) // }
    })
    }
}   

AwvImportAction.template = "bms.awv_import_action";

// remember the tag name we put in the first step
registry.category("actions").add("bms.AwvImportAction", AwvImportAction);