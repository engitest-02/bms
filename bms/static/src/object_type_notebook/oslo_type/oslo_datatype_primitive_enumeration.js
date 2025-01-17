// /** @odoo-module */

import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart,onWillUpdateProps } = owl

var rpc = require('web.rpc');
var Dialog = require('web.Dialog');

export class OsloDatatypePrimitiveEnumeration extends Component {
    setup(){
        this.actionService = useService("action")
        this.ormService = useService("orm")
        this.attrValueToDisplay;       

        onWillStart(async () =>{
            this._asssign_props_value(this.props)
            const attrValueRecs = await this._load_attribute_value()
            this._setup_value(this.props, attrValueRecs)
            this.currentObjectId = this.objectId
            
        })
        onWillUpdateProps(async (nextProps) => {         
            this._asssign_props_value(nextProps)
            // console.log("primitive onWillUpdateProps", "current_object", this.currentObjectId, "objectID", this.objectId, this.currentObjectId != this.objectId)
            if (this.currentObjectId != this.objectId){
                this.currentObjectId = this.objectId
                const attrValueRecs = await this._load_attribute_value()
                this._setup_value(this.props, attrValueRecs)
                this.render()
            }
        })
    }

    changeAttrValue(){
        console.log("changeAttrValue called")
        var context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            'default_attr_def_id': this.attrDefId,
            'default_attr_name': this.attrName,
            'default_attr_def': this.attrDefinitionNl,
            'default_attr_def_datatype_definition': this.attrDefDatatypeDef,
            'default_attr_def_value_type': this.attrDefValueType,
            'form_view_initial_mode': "edit",
        }
        if (this.attrValueRec) { //attribute has already a value
            context = {...context,
                    'default_value_char': this.attrValueRec.value_char,
                    'default_value_boolean': this.attrValueRec.value_boolean,
                    'default_value_date': this.attrValueRec.value_date,
                    'default_value_datetime': this.attrValueRec.value_datetime,
                    'default_value_float': this.attrValueRec.value_float,
                    'default_value_non_negative_integer': this.attrValueRec.value_non_negative_integer,
                    'default_enumeration_value_id':  this.attrValueRec.enumeration_value_id? this.attrValueRec.enumeration_value_id[0]:false,
                    'form_view_initial_mode': "edit"
                }
        }
        // console.log("oslo_datatype_primitive_enumeration context", context)
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

    copyAttrValueToSiblings(){
        
      
        console.log("copy to attribute to siblings", this.objectId)
        //   [object_id, object_type_id, attr_def_id, 
        // value_char, value_boolean, value_date, value_datetime, value_float, value_non_negative_integer, enumeration_value_id ]    
        // if attr is empty => value = false
        console.log("this", this)
        if (this.attrValueRec == null){
            var value_char = null;
            var value_boolean = null;
            var value_date = null;
            var value_datetime = null;
            var value_float = null;
            var value_non_negative_integer = null;
            var value_enumeration = null;
            var enumeration_value_id = null;
        }
        else{
            var value_char = this.attrValueRec.value_char
            var value_boolean = this.attrValueRec.value_boolean
            var value_date = this.attrValueRec.value_date
            var value_datetime = this.attrValueRec.value_datetime
            var value_float =  this.attrValueRec.value_float
            var value_non_negative_integer =  this.attrValueRec.value_non_negative_integer
            var value_enumeration = this.attrValueRec.value_enumeration
            var enumeration_value_id = this.attrValueRec.enumeration_value_id == false?  this.attrValueRec.enumeration_value_id : this.attrValueRec.enumeration_value_id[0]               
        }
        const args = [this.objectId, this.objectTypeId ,this.attrDefId,
                      value_char, value_boolean, value_date, value_datetime, value_float,
                      value_non_negative_integer, value_enumeration, enumeration_value_id , this.attrDefValueType];
        console.log("arg", this, args)
        

        Dialog.confirm(this,
            "Do you confim you want to copy this attribute value to all the siblings maintainance objec of the same type. You cannot undo this operation. ",
             {
           title: "Copy attribute value to siblings",
           async confirm_callback() {
               const attrDefs = rpc.query({
                model: 'bms.oslo_attributen_value',
                method: 'copy_attr_value_to_siblings',
                args: [args],
                }
            )
           },
           async cancel_callback(){
            // do nothing
           },
           async onForceClose(){
            //  do nothing
           }
       });

       
    }

    highlightValueField(event){
        // use in combinaison with on-mousevover to highlight the row related to the edit button
        $(event.target).closest('div[class="o_bms_hover p-0"]').addClass("o_bms_hover_triggered");
    }

    unhighlightValueField(event){
        // use in combinaison with on-mouseout to unhighlight the row related to the edit button
        $(event.target).closest('div[class="o_bms_hover p-0 o_bms_hover_triggered"]').removeClass("o_bms_hover_triggered");
    }

    _asssign_props_value(props){
        this.objectId = props.objectId
        this.objectTypeId = props.objectTypeId
        this.attrDefId = props.attr.attr_datatype_def.attr_def_id

        this.attrName = props.attr.attr_name
        this.attrDefinitionNl = props.attr.attr_definition_nl
        this.unit = this._format_unit(props.attr.attr_datatype_def.unit) 
       
        this.attrDefDatatypeDef = props.attr.attr_datatype_def.attr_name
        this.attrDefValueType = props.attr.attr_datatype_def.attr_value_type
        this.attrOsloDatatype = props.attr.attr_datatype_def.attr_datatype
    }

    _setup_value(props, attrValueRecs){

        var valueField = "value_" + this.attrDefValueType
       
        if (attrValueRecs){ 
            this.attrValueRec = attrValueRecs[0]
            if (this.attrValueRec && this.attrDefValueType != "boolean" && this.attrValueRec[valueField] == false){
                this.attrValueRec[valueField] = ""
            }// treat case of value is false (null) in field other than boolean
        }   
        this.attrValueToDisplay = this.attrValueRec? this.attrValueRec[valueField]: ""
        
        if (this.attrOsloDatatype == "OSLOEnumeration"){// create selectionValues list useful for the form + notation to display
            Object.values(this.props.attr.attr_datatype_def.selection_values).forEach(
                (selection_value) => {                        
                    if (this.attrValueToDisplay === selection_value.selection_id){
                        // don't display the selection_id of the existing value but its notation
                        this.attrValueToDisplay = selection_value.notation
                    }
            })
        } 
    }
    
    _format_unit(unit){
        if(unit){
            const r = RegExp(/(")(.*)(")/);
            const formatted_unit = r.exec(unit)[2]
            return " [" + formatted_unit + "]";
        }
        else{
            return ""
        }
    }

    async _load_attribute_value(){ //explicit objectId even if this.objectId to avoid caching side effects
        const domain=[["object_id", "=", this.objectId], 
                ["object_type_id","=",this.objectTypeId],
                ["attr_def_id", "=", this.attrDefId]];
        const attValueRec = await this.ormService.searchRead("bms.oslo_attributen_value", domain) 
        return attValueRec
    }
}

OsloDatatypePrimitiveEnumeration.template = "bms.oslo_datatype_primitive_enumeration"