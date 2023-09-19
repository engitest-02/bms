// ** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { KeepLast } from "@web/core/utils/concurrency";
import { registry } from "@web/core/registry";

const { Component, onWillStart, useState } = owl;

export class ObjectType extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        //this.object_types = useState({ data: [] });
        this.domain = [["object_ids", "in", [this.props.maintainance_object_id]]];
        this.keepLast = new KeepLast();
        this.filterName = "";
        onWillStart(async () => {
            this.object_types = await this.keepLast.add(this.loadObjectTypes()); // keeplast cancels loadObjecTypes if user changes action
        });
        // this.reg = registry.category("fields");
    }

    loadObjectTypes() {
        // return this.orm.browse("bms.object_type", this.domain); // ... , ["fields_name,"]
        //return this.orm.read("bms.object_type", [this.props.maintainance_object_id],["name", "description"]);
        return this.orm.call("bms.object_type", "fields_get", [], {});
        // return this.orm.call("bms.object_type","get_object_type", [[1], 2 ],{})
        // return this.orm.call("bms.object_type","get_object_type", [[this.props.maintainance_object_id],], {});
        // await this.orm.call(this.props.record.resModel, 'js_remove_outstanding_partial', [moveId, partialId], {});
    }

}

ObjectType.props = ["maintainance_object_id"];
ObjectType.template = "bms.object_type";