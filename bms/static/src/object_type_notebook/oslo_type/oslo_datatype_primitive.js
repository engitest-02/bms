// /** @odoo-module */

import { useService, useBus } from "@web/core/utils/hooks";
const { Component, onWillStart, onWillPatch } = owl;
var rpc = require('web.rpc');


export class OsloDatatypePrimitive extends Component {
    setup(){
        this.attr_name = this.props.attr.attr_name;
        this.unit = this._format_unit(this.props.attr.attr_datatype_def.unit);
        this.attrDefId = this.props.attr.attr_datatype_def.attr_def_id;
        this.objectId = this.props.objectId;
        this.objectTypeId = this.objectTypeId;
    }

    changeAttrValue(){
        console.log("attribute value changed!", this.attrDefId);
        const context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            // 'default_oslo_attributen_uri': attrDefValueRec.osloattributen_uri,
            // 'default_attr_name': attrDefValueRec.osloattributen_name,
            // 'default_attr_def': attrDefValueRec.osloattributen_definition,
            // 'default_att_def_value_type_definition': attrDefValueRec.oslodatatype_primitive_definition_nl,
            'default_attr_def_id': this.attrDefId,
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

    _format_unit(unit){
        if(unit){
            const r = RegExp(/(")(.*)(")/);
            const formatted_unit = r.exec(unit)[2]
            return "[" + formatted_unit + "]";
        }
        else{
            return ""
        }
        
    }

}
OsloDatatypePrimitive.template = "bms.oslo_datatype_primitive"