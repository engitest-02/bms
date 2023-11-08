// /** @odoo-module */

import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart } = owl


export class OsloDatatypePrimitiveEnumeration extends Component {
    setup(){
        this.actionService = useService("action")
        this.ormService = useService("orm")

        this.attrName = this.props.attr.attr_name;
        this.unit = this._format_unit(this.props.attr.attr_datatype_def.unit)
        
        this.objectId = this.props.objectId
        this.objectTypeId = this.props.objectTypeId
        this.attrDefId = this.props.attr.attr_datatype_def.attr_def_id
        this.attrType = this.props.attr.attr_datatype_def.attr_type
        this.attrDefinitionNl = this.props.attr.attr_definition_nl
        this.attrDefDatatypeDef= this.props.attr.attr_datatype_def.datatype_label_nl
        this.attrDefValueType = this.props.attr.attr_datatype_def.attr_value_type
        this.attrOsloDatatype = this.props.attr.attr_datatype_def.oslo_datatype
        
        this.attrValueToDisplay;

        onWillStart(async () => {
            var valueField = "value_" + this.attrDefValueType

            const attrValueRecs = await this._load_attribute_value()
            if (attrValueRecs){ this.attrValueRec = attrValueRecs[0]}   
            this.attrValueToDisplay = this.attrValueRec? this.attrValueRec[valueField]: ""
            
            if (this.attrOsloDatatype == "OSLOEnumeration"){// create selectionValues list useful for the form + notation to display
                var selectionValues = []
                Object.values(this.props.attr.attr_datatype_def.selection_values).forEach(
                    (selection_value) => {                        
                        selectionValues.push([selection_value.selection_id, selection_value.notation]) 
                        if (this.attrValueToDisplay === selection_value.selection_id){
                            // don't display the selection_id of the existing value but its notation
                            this.attrValueToDisplay = selection_value.notation
                        }
                })
                this.selectionValues = selectionValues
            }  
        })
    }

    changeAttrValue(){
        var context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            'default_attr_def_id': this.attrDefId,
            'default_attr_name': this.attr_name,
            'default_attr_def': this.attrDefinitionNl,
            'default_attr_def_datatype_definition': this.attrDefDatatypeDef,
            'default_attr_def_value_type': this.attrDefValueType,
            // "default_enumeration_selection_values": [],
            'form_view_initial_mode': "new",
        }
        if (this.attrValueRec) { //attribute has already a value
            context = {...context,
                    'default_value_char': this.attrValueRec.value_char,
                    'default_value_boolean': this.attrValueRec.value_boolean,
                    'default_value_date': this.attrValueRec.value_date,
                    'default_value_datetime': this.attrValueRec.value_datetime,
                    'default_value_float': this.attrValueRec.value_float,
                    'default_value_non_negative_integer': this.attrValueRec.value_non_negative_integer,
                    'default_enumeration_value_id':  this.attrValueRec.enumeration_value_id? this.attrValueRec.enumeration_value_id[0]:false}
        }

        // if (this.attrOsloDatatype == "OSLOEnumeration"){ // assign selection list

        //     context['default_enumeration_selection_values'] = this.selectionValues
        // }
        console.log('context', context)
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
        const attValueRec = this.ormService.searchRead("bms.oslo_attributen_value", domain) 
        return attValueRec
    }
}

OsloDatatypePrimitiveEnumeration.template = "bms.oslo_datatype_primitive_enumeration"