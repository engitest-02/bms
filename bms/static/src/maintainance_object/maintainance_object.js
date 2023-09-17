/** @odoo-module */
import { Field } from "@web/views/fields/field";

const { Component } = owl;

export class MaintainanceObject extends Component {
    setup() {

        // this.fieldsProps = {};
        // // for (const [key, value] of Object.entries(obj)) {
        // //     console.log(key, value);
        // // }
        // let counter = 0;
        // for (const [key, activeField] of Object.entries(this.props.value.record.activeFields))
        // {
        //     counter = counter + 1;
        //     this.fieldsProps[activeField.name] = {};        
        //     this.fieldsProps[activeField.name]['id'] = counter;
        //     this.fieldsProps[activeField.name]['fieldName'] = activeField.name;
        //     this.fieldsProps[activeField.name]['fieldInfo'] = { 'FieldComponent': activeField.FieldComponent };
        //     this.fieldsProps[activeField.name]['fieldClass'] = activeField.FieldComponent.name;
        //     this.fieldsProps[activeField.name]['setDirty'] = this.props.value.setFieldAsDirty;

        //     this.fieldsProps[activeField.name]['fieldRecord'] = this.props.value.record;
        // };

        this.fieldsProps = [];
        // for (const [key, value] of Object.entries(obj)) {
        //     console.log(key, value);
        // }
        let counter = -1;
        for (const [key, activeField] of Object.entries(this.props.value.record.activeFields)) {
            counter = counter + 1;
            let fieldsProp = {};
            fieldsProp['id'] = counter;
            fieldsProp['fieldName'] = activeField.name;
            fieldsProp['fieldInfo'] = { 'FieldComponent(': activeField.FieldComponent };
            fieldsProp['fieldClass'] = activeField.FieldComponent.name;
            fieldsProp['setDirty'] = this.props.value.setFieldAsDirty;
            fieldsProp['fieldRecord'] = this.props.value.record;
            this.fieldsProps.push(fieldsProp);
        };


        this.propsValue = this.props.value;
        this.fieldInfo = { 'FieldComponent': this.propsValue.record.activeFields.name.FieldComponent };
        this.fieldRecord = this.propsValue.record;
        this.fieldName = this.propsValue.record.activeFields.name.name;
        this.fieldClass = this.propsValue.record.activeFields.name.FieldComponent.name;
        this.setDirty = this.propsValue.setFieldAsDirty;


        this.object_id = this.propsValue.record.data.id;


    }

    _getFieldInfo(archInfo) {

    }
}

MaintainanceObject.components = { Field };
MaintainanceObject.props = ["value"];
MaintainanceObject.template = "bms.maintainance_object";

