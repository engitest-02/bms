    // /** @odoo-module */

import { registry } from "@web/core/registry";
import { useService, useBus } from "@web/core/utils/hooks";
import { OsloType } from "./oslo_type/oslo_type";
const { Component, onWillStart, onWillPatch } = owl;


export class ObjectTypeNotebook extends Component {
    // only 1 type admitted and of AWV OTL. IF more than one type nothing is displayed !!!
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        
        this.objectId = this.props.record.data.id;
        this._setup_objectType(this.props.record.data.object_type_ids.records)
      
        this.currentObjectId = this.objectId //keep delta in case of change of object_id
        this.existingOtls;

        onWillPatch(async () => {
            this.objectId = this.props.record.data.id;
            if (this.currentObjectId != this.objectId) {// rerender OTL notebook if parent object has changed
                this._setup_objectType(this.props.record.data.object_type_ids.records)
                this.render()
                this.currentObjectId = this.objectId
            }
        })
    }

    changeOtlAndType() {
        console.log("changeOtlAndType called");
        if (this.objectId == null) { // maintainance object is new => first must be saved
            var Dialog = require('web.Dialog')
            Dialog.alert(
                this,
                "You have to save your new asset first",
                {
                    onForceClose: function () {
                    },
                    confirm_callback: function () {
                    }
                }
            );
        }
        else {
            var context = { 'default_object_ids': this.objectId };
            if ((this.otlId) && (this.objectTypeId)) {
                context = {'default_otl': this.otlId,
                           'default_object_type': this.objectTypeId,
                            ...context};
            }
            else if ((this.otlId)) {
                context = { 'default_otl': this.otlId,
                            ...context};
            }
            console.log("this", this)
            const action = {"type": "ir.actions.act_window",
                            "res_model": "bms.otl_type",
                            "views": [[false, "form"]],
                            "target": "current",
                            "context": context,}

            this.actionService.doAction(action);
        }
    }

    _setup_objectType(objectTypeIds){
        this.only1AWVtype = true
        this.hasAWVtype = true
        if (objectTypeIds.length > 1) {this.only1AWVtype = false }
        if (objectTypeIds.length == 0) {
            this.hasAWVtype = false 
            console.warn("use of hard coded OTL ID for AWV library !!!")
            this.otlId = 1
        }
        if (objectTypeIds.length == 1) {
            this.otlId = objectTypeIds[0].data.otl_id[0]
            this.objectTypeId = objectTypeIds[0].data.id
            this.classUri = objectTypeIds[0].data.otl_type_internal_id
            this.className = objectTypeIds[0].data.name
        }
    }
    // getValue(record) {
    //     if (typeof (record.value_type) == 'boolean') { // no type value_type defined
    //         return ""
    //     }
    //     switch (record.value_type) {
    //         case 'boolean':
    //             return record.value_boolean
    //         case "char":
    //             return typeof (record.value_char) == "boolean" ? "" : record.value_char
    //         case "date":
    //             return typeof (record.value_date) == "boolean" ? "" : record.value_date
    //         case "float":
    //             return typeof (record.value_float) == "boolean" ? "" : record.value_float
    //         case "integer":
    //             return typeof (record.value_integer) == "boolean" ? "" : record.valute_integer
    //         default:
    //             return ""
    //     }
    // }

    // changeAttrValue(record) {

    //     const context = {
    //         'default_attr_def_id': record.attr_def_id,
    //         'default_object_id': record.object_id,
    //         'default_object_type_id': record.object_type_id,
    //         'default_attr_value': record.attr_value,
    //         'default_value_boolean': record.value_boolean,
    //         'default_value_char': record.value_char,
    //         'default_value_date': record.value_date,
    //         'default_value_float': record.value_float,
    //         'default_value_integer': record.value_integer,
    //         'form_view_initial_mode': "edit",
    //     }

    //     const domain = [('id', '=', record.attr_value_id)]
    //     this.actionService.doAction(
    //         {
    //             "type": "ir.actions.act_window",
    //             "res_model": "bms.attribute_value",
    //             "views": [[false, "form"]],
    //             "target": "inline",
    //             "context": context,
    //             "res_id": record.attr_value_id,

    //         }
    //     );
    // }

    // _jsonifyAttributes(existingOtls, attributeRecords) {
    //     const attributes = [];

    //     Object.values(existingOtls).forEach((existingOtl) => {
    //         const ojbectTypeId = this._getObjectTypeIdForOtl(attributeRecords, existingOtl.id);
    //         attributes.push(
    //             {
    //                 "otlId": existingOtl.id,
    //                 "otlName": existingOtl.name,
    //                 "objectTypeId": ojbectTypeId,
    //                 "objectTypeName": this._getObjectTypeNameForOtl(attributeRecords, existingOtl.id),
    //                 "objectTypeInternalId": this._getObjectTypeInternalId(attributeRecords, existingOtl.id),
    //                 "attrCplxDef": null, //todo {CplxDef:[attrDefIds]}
    //                 "attrDefIds": this._getAttrDefIdsForOtlAndObjectType(attributeRecords, existingOtl.id, ojbectTypeId),
    //                 "attrDefRecords": this._getAttrDefRecordsForOtlAndObjectType(attributeRecords, existingOtl.id, ojbectTypeId),
    //             }
    //         )
    //     });

    //     return attributes;
    // }

    // _getObjectTypeIdForOtl(attributeRecords, existingOtlId) {
    //     const objectTypeId = null
    //     for (let i = 0; i < attributeRecords.length; i++) {
    //         const record = attributeRecords[i];
    //         if (record['otl_id'] == existingOtlId) {
    //             return record['object_type_id'];
    //         }
    //     }
    //     return objectTypeId;
    // }

    // _getObjectTypeNameForOtl(attributeRecords, existingOtlId) {
    //     for (let i = 0; i < attributeRecords.length; i++) {
    //         const record = attributeRecords[i];
    //         if (record['otl_id'] == existingOtlId) {
    //             return record['object_type_name'];
    //         }
    //     }
    //     return null;
    // }

    // _getAttrDefIdsForOtlAndObjectType(attributeRecords, OtlId, objectTypeId) {
    //     const attributeDefIds = [];
    //     for (let i = 0; i < attributeRecords.length; i++) {
    //         const record = attributeRecords[i];
    //         if ((record['otl_id'] == OtlId) && (record['object_type_id'] == objectTypeId)) {
    //             attributeDefIds.push(record['att_def_id']);
    //         }
    //     }
    //     return attributeDefIds;
    // }

    // _getAttrDefRecordsForOtlAndObjectType(attributeRecords, OtlId, objectTypeId) {
    //     const attributeDefRecords = [];
    //     for (let i = 0; i < attributeRecords.length; i++) {
    //         const record = attributeRecords[i];
    //         if ((record['otl_id'] == OtlId) && (record['object_type_id'] == objectTypeId)) {
    //             attributeDefRecords.push(record);
    //         }
    //     }
    //     return attributeDefRecords;
    // }

    // _getObjectTypeInternalId(attributeRecords, existingOtlId) {
    //     for (let i = 0; i < attributeRecords.length; i++) {
    //         const record = attributeRecords[i];
    //         if (record['otl_id'] == existingOtlId) {
    //             return record['otl_type_internal_id'];
    //         }
    //     }
    //     return null;
    // }

    // loadAttributes(objectId) {
    //     // complex query on a vie
    //     const domain = [["object_id", "=", objectId]];
    //     return this.orm.searchRead("bms.attributes", domain, []);
    // }

    // loadOtls() {
    //     return this.orm.searchRead("bms.object_type_library", [], []);
    // }

}

ObjectTypeNotebook.template = "bms.object_type_notebook";
ObjectTypeNotebook.components = { OsloType };
registry.category("fields").add("object_type_notebook", ObjectTypeNotebook)


