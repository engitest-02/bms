// /** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart } = owl;



export class ObjectTypeNotebook extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notificatonService = useService("notification");

        // get from props
        this.object_id = this.props.record.data.id;

        this.objectTypeRecords = this.props.record.data.object_type_ids.records;

        onWillStart(async () => {
            const attributeRecords = await this.loadAttributes(); // complex query on view
            const existingOtls = await this.loadOtls()
            this.attributes = this._jsonifyAttributes(existingOtls, attributeRecords);
            // get all OTL library existing (even if no type is assigned to the object)
            // tehn calculate attributes for to feed the template  
            // {"otlId": ...
            //  "otlName": ...
            //  "objectTypeId": ...
            //  "objectTypeName": ...
            //  "attrDefIds" : ...
            //  "attrDefRecords" : ...
            // }        
        });

    }


    changeOtlAndType(otlId = null, objectTypeId = null) {
        if (this.props.record.data.id == null) { // maintainance object is new => first must be saved
            var Dialog = require('web.Dialog')
            Dialog.alert(
                this,
                "You have to save your new asset first",
                {
                    onForceClose: function(){
                    },
                    confirm_callback: function(){
                    }
                }
             );
        }
        else {
            var context = { 'default_object_ids': this.props.record.data.id };
            if ((otlId) && (objectTypeId)) {
                context = {
                    'default_otl': otlId,
                    'default_object_type': objectTypeId,
                    ...context
                };
            }
            else if ((otlId)) {
                context = {
                    'default_otl': otlId,
                    ...context
                };
            }
            const action = {
                "type": "ir.actions.act_window",
                "res_model": "bms.otl_type",
                "views": [[false, "form"]],
                "target": "current",
                "context": context,
            }
            this.actionService.doAction(action);
        }
    }

    getValue(record) {
        if (typeof (record.value_type) == 'boolean') { // no type value_type defined
            return ""
        }
        switch (record.value_type) {
            case 'boolean':
                return record.value_boolean
            case "char":
                return typeof (record.value_char) == "boolean" ? "" : record.value_char
            case "date":
                return typeof (record.value_date) == "boolean" ? "" : record.value_date
            case "float":
                return typeof (record.value_float) == "boolean" ? "" : record.value_float
            case "integer":
                return typeof (record.value_integer) == "boolean" ? "" : record.valute_integer
            default:
                return ""
        }
    }

    changeAttrValue(record) {
        console.log("value changed", record);

        const context = {
            'default_attr_def_id': record.attr_def_id,
            'default_object_id': record.object_id,
            'default_object_type_id': record.object_type_id,
            'default_attr_value': record.attr_value,
            'default_value_boolean': record.value_boolean,
            'default_value_char': record.value_char,
            'default_value_date': record.value_date,
            'default_value_float': record.value_float,
            'default_value_integer': record.value_integer,
            'form_view_initial_mode': "edit",
        }

        const domain = [('id', '=', record.attr_value_id)]
        this.actionService.doAction(
            {
                "type": "ir.actions.act_window",
                "res_model": "bms.attribute_value",
                "views": [[false, "form"]],
                "target": "inline",
                "context": context,
                "res_id": record.attr_value_id,
                
            }
        );
    }



    _jsonifyAttributes(existingOtls, attributeRecords) {
        const attributes = [];

        Object.values(existingOtls).forEach((existingOtl) => {
            const ojbectTypeId = this._getObjectTypeIdForOtl(attributeRecords, existingOtl.id);
            attributes.push(
                {
                    "otlId": existingOtl.id,
                    "otlName": existingOtl.name,
                    "objectTypeId": ojbectTypeId,
                    "objectTypeName": this._getObjectTypeNameForOtl(attributeRecords, existingOtl.id),
                    "attrDefIds": this._getAttrDefIdsForOtlAndObjectType(attributeRecords, existingOtl.id, ojbectTypeId),
                    "attrDefRecords": this._getAttrDefRecordsForOtlAndObjectType(attributeRecords, existingOtl.id, ojbectTypeId),
                }
            )
        });

        return attributes;
    }

    _getObjectTypeIdForOtl(attributeRecords, existingOtlId) {
        const objectTypeId = null
        for (let i = 0; i < attributeRecords.length; i++) {
            const record = attributeRecords[i];
            if (record['otl_id'] == existingOtlId) {
                return record['object_type_id'];
            }
        }
        return objectTypeId;
    }

    _getObjectTypeNameForOtl(attributeRecords, existingOtlId) {
        for (let i = 0; i < attributeRecords.length; i++) {
            const record = attributeRecords[i];
            if (record['otl_id'] == existingOtlId) {
                return record['object_type_name'];
            }
        }
        return null;
    }

    _getAttrDefIdsForOtlAndObjectType(attributeRecords, OtlId, objectTypeId) {
        const attributeDefIds = [];
        for (let i = 0; i < attributeRecords.length; i++) {
            const record = attributeRecords[i];
            if ((record['otl_id'] == OtlId) && (record['object_type_id'] == objectTypeId)) {
                attributeDefIds.push(record['att_def_id']);
            }
        }
        return attributeDefIds;
    }

    _getAttrDefRecordsForOtlAndObjectType(attributeRecords, OtlId, objectTypeId) {
        const attributeDefRecords = [];
        for (let i = 0; i < attributeRecords.length; i++) {
            const record = attributeRecords[i];
            if ((record['otl_id'] == OtlId) && (record['object_type_id'] == objectTypeId)) {
                attributeDefRecords.push(record);
            }
        }
        return attributeDefRecords;
    }

    loadAttributes() {
        const domain = [["object_id", "=", this.object_id]];
        return this.orm.searchRead("bms.attributes", domain, []);
    }

    loadOtls() {
        return this.orm.searchRead("bms.object_type_library", [], []);
    }

}

ObjectTypeNotebook.template = "bms.object_type_notebook";
registry.category("fields").add("object_type_notebook", ObjectTypeNotebook)