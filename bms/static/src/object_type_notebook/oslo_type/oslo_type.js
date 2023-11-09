// /** @odoo-module */

import { useService, useBus } from "@web/core/utils/hooks";
const { Component, onWillStart, onWillPatch } = owl;
import { OsloDatatypePrimitiveEnumeration } from "./oslo_datatype_primitive_enumeration";
import { OsloDatatypeIterative } from "./oslo_datatype_iterative";
var rpc = require('web.rpc');



export class OsloType extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.otlId = this.props.otlId;
        this.classUri = this.props.classUri;
        this.className = this.props.className;
        this.objectTypeId = this.props.objectTypeId; // TODO: same as classUri ???
        this.objectId = this.props.objectId;

        this.currentObjectId = this.objectId;
        this.attrDefValueRecs;

        onWillStart(async () => {
            this.attrDefRecs = await this._loadAttrPrimitiveDatatype(this.classUri);
            this.attrValueRecs = await this._loadAttrValue(this.objectId, this.objectTypeId);
            this.attrDefValueRecs = this._mergeAttrDefsAndValues(this.attrDefRecs, this.attrValueRecs);

            // new code
            const d = await this._loadAttrDefintion(this.classUri);
            this.attrDefs = JSON.parse(d)
            console.log("attributes", this.attrDefs);
        })

        onWillPatch(async () => {
            this.otlId = this.props.otlId;
            this.classUri = this.props.classUri;
            this.className = this.props.className;
            this.objectTypeId = this.props.objectTypeId;
            this.objectId = this.props.objectId;

            if (this.currentObjectId != this.objectId) {// rerender OTL notebook if parent object has changed
                this.attrDefRecs = await this._loadAttrPrimitiveDatatype(this.classUri);
                this.attrValueRecs = await this._loadAttrValue(this.objectId, this.objectTypeId);
                this.attrDefValueRecs = this._mergeAttrDefsAndValues(this.attrDefRecs, this.attrValueRecs);
                // console.log("onWillPatch", this.classUri, this.attrDefRecs, this.attrValueRecs, this.attrDefValueRecs);
                
                // new code
                const d = await this._loadAttrDefintion(this.classUri);
                this.attrDefs = JSON.parse(d)
                console.log("attributes", this.attrDefs);
                

                // end new code 
                this.render();
                this.currentObjectId = this.objectId;
                
            }
            

        })

    }

    _loadAttrPrimitiveDatatype(osloclass_uri) {
        const domain = [["osloclass_uri", "=", osloclass_uri]];
        return this.orm.searchRead("bms.awv_attributen_primitive_datatype", domain);
    }

    _loadAttrDefintion(osloclass_uri){
        console.log('osloclass_uri', osloclass_uri)
        const attrDefs = rpc.query({
            model: 'bms.attribute_definition_',
            method: 'get_att_def',
            args: [osloclass_uri],
            }
        )
        return attrDefs   
        // ).then((data) => {return JSON.parse(data)})  

    }

    _loadAttrValue(objectId, objectTypeId, osloclass_uri){
        const domain = [["object_id", "=", objectId], ["object_type_id", "=", objectTypeId]];
        return this.orm.searchRead("bms.oslo_attributen_value", domain);
    }

    _mergeAttrDefsAndValues(attrDefRecs, attrValueRecs){
        var merge = [];
        Object.values(attrDefRecs).forEach((attrDefRec) => {
            let attr = attrDefRec;        
            Object.values(attrValueRecs).forEach((attrValueRec) => {
                if (attrDefRec.osloattributen_uri == attrValueRec.oslo_attributen_uri){
                attr = {...attr, ...attrValueRec};        
                }        
            })
            merge.push(attr);
        })
        return merge;
    }

    changeOtlAndType() {
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
            var context = {
                'default_object_ids': this.objectId,
                'default_otl': this.otlId
            };
            if (this.objectTypeId) {
                context = {
                    'default_object_type': this.objectTypeId,
                    ...context
                };
            };
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

    changeAttrValue(attrDefValueRec) {
        console.log("record", attrDefValueRec);
        const context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            'default_oslo_attributen_uri': attrDefValueRec.osloattributen_uri,
            'default_attr_name': attrDefValueRec.osloattributen_name,
            'default_attr_def': attrDefValueRec.osloattributen_definition,
            'default_att_def_value_type_definition': attrDefValueRec.oslodatatype_primitive_definition_nl,
            'default_attr_def_value_type': attrDefValueRec.value_type,
            'default_value_char': attrDefValueRec.value_char,
            'default_value_boolean': attrDefValueRec.value_boolean,
            'default_value_date': attrDefValueRec.value_date,
            'default_value_datetime': attrDefValueRec.value_datetime,
            'default_value_float': attrDefValueRec.value_float,
            'default_value_integer': attrDefValueRec.value_integer,
            'form_view_initial_mode': "edit",
        }
        this.actionService.doAction(
            {
                "type": "ir.actions.act_window",
                "res_model": "bms.oslo_attributen_value_edit",
                "views": [[false, "form"]],
                "target": "inline",
                "context": context,
            }
        );
    }

    formatUnit(datatype_attr_unit_constraints) {
        if (datatype_attr_unit_constraints) {
            const r = RegExp(/(")(.*)(")/);
            const unit = r.exec(datatype_attr_unit_constraints)[2]
            return "[" + unit + "]";
        }
        else {
            return ""
        }
    }

    getValue(attrDefValueRec){
        const key = 'value_' + attrDefValueRec.value_type
        if (key in attrDefValueRec){
            return attrDefValueRec[key];
        }
        else {
            return "";
        }
    }

}

OsloType.template = "bms.oslo_type";
OsloType.components={OsloDatatypePrimitiveEnumeration, OsloDatatypeIterative};

class JSONAttrDefParser{
    constructor(JSONAttrDef){
        const attrs = JSONAttrDef.attributes
        Object.values(attrs).forEach((attr) => {
            
    })
}
}