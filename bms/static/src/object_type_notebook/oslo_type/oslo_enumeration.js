// /** @odoo-module */

import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart } = owl


export class OsloEnumeration extends Component {
    setup(){
        this.actionService = useService("action")
        this.ormService = useService("orm")

        this.attrName = this.props.attr.attr_name;
        // this.unit = this._format_unit(this.props.attr.attr_datatype_def.unit)
        
        this.objectId = this.props.objectId
        this.objectTypeId = this.props.objectTypeId
        this.attrDefId = this.props.attr.attr_datatype_def.attr_def_id
        this.attrType = this.props.attr.attr_datatype_def.attr_type
        this.attrDefinitionNl = this.props.attr.attr_definition_nl
        this.attrDefDatatypeDef= this.props.attr.attr_datatype_def.datatype_label_nl
        this.attrDefValueType = this.props.attr.attr_datatype_def.attr_value_type

        this.valueField = "value_" + this.attrDefValueType
        this.attrValue;

        onWillStart(async () => {
            const [attrValue, valueField] = await this._load_attribute_value()
            this.attrValue = attrValue ? attrValue[this.valueField] : ""
        })
    }

    changeAttrValue(){

        const context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            'default_attr_def_id': this.attrDefId,
            'default_attr_name': this.attr_name,
            'default_attr_def': this.attrDefinitionNl,
            'default_attr_def_datatype_definition': this.attrDefDatatypeDef,
            'default_attr_def_value_type': this.attrDefValueType,
            'default_value_char': attrDefValueRec.value_char,
            'default_value_boolean': attrDefValueRec.value_boolean,
            'default_value_date': attrDefValueRec.value_date,
            'default_value_datetime': attrDefValueRec.value_datetime,
            'default_value_float': attrDefValueRec.value_float,
            'default_value_non_negative_integer': attrDefValueRec.value_integer,
            'default_value_enumeration': attrDefValueRec.value_enumerator,
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

    _load_attribute_value(){
        const domain=[["object_id", "=", this.objectId], 
                ["object_type_id","=",this.objectTypeId],
                ["attr_def_id", "=", this.attrDefId]];
        const value = this.ormService.searchRead("bms.oslo_attributen_value", domain, [this.valueField]) 
        return value
    }
}

OsloEnumeration.template = "bms.oslo_enumeration"