// /** @odoo-module */

import { registry } from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
const { Component,onWillStart } = owl;

export class ObjectTypeNotebook extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");


        this.object_id = this.props.record.data.id;
        this.otlTypes = this.getOtlTypes(this.props.record.data.object_type_ids.records);
        this.attrDefIdsbyType = this.getAttrDefByType(this.props.record.data.object_type_ids.records);

        onWillStart(async () => {	       
            this.attributes = await this.loadAttributes();       
        });

    }

    change_otl_and_type(otlId, objectTypeId){
        console.log("otl", otlId, "type", objectTypeId);
        this.actionService.doAction(
            {
                "type": "ir.actions.act_window",
                "res_model": "bms.otl_type",
                "views": [[false, "form"]],
                "target": "current",
                "context":
                    {'default_object_ids': this.object_id,
                     'default_otl': otlId,
                    'default_object_type': objectTypeId}  
            }
        );
    }

    getAttrDefByType(ObjectTypeRecords){
        const attrDefIdsbyType = [];

        Object.values(ObjectTypeRecords).forEach((ObjectType) => {
            const otlId = ObjectType.data.otl_id[0];
            const otl = ObjectType.data.otl_id[1];
            // const otl = ObjectType.data.otl_id[1];
            const objectTypeName = ObjectType.data.name;
            const objectTypeId = ObjectType.data.id;
            const attrDefIds = [];
            // console.log("object type records", ObjectTypeRecords);
            Object.values(ObjectType.data.attribute_ids.records).forEach((attrDef)=>{
                attrDefIds.push(attrDef.data.id);
            });

            attrDefIdsbyType.push({"otlId": otlId, "otl": otl, "objectTypeId": objectTypeId, "objectTypeName": objectTypeName, "attrDefIds": attrDefIds})
        });
        return attrDefIdsbyType;
    }

    getOtlTypes(ObjectTypeRecords) {
        const otlTypes = [];
        Object.values(ObjectTypeRecords).forEach((record) => {
            otlTypes.push(record.data.otl_id[1])
        });
        
        const otlTypesUnique = [...new Set(otlTypes)];

        const otlTypesUniqueIndexed = [];
        for (let i = 0; i < otlTypesUnique.length; i++) {
            otlTypesUniqueIndexed.push({'id':i, 'name': otlTypesUnique[i]});
        }

        return otlTypesUniqueIndexed; // return unique (Set) and indexed OTL array [{0: 'OTL_A', 1: 'OTL_B'}]

    }

    loadAttributes(){
        const domain = [["object_id", "=", this.object_id]] ;
        return this.orm.searchRead("bms.att_def_value_report", domain, []);        
        //return this.orm.call("bms.object_type", "get_object_type", [[1, 2, 3]], {})
    }

}

ObjectTypeNotebook.template = "bms.object_type_notebook";
registry.category("fields").add("object_type_notebook", ObjectTypeNotebook)