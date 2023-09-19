/** @odoo-module */
import { Field } from "@web/views/fields/field";
import {ObjectType} from "../object_type/object_type";

const { Component } = owl;

export class MaintainanceObject extends Component {
    setup() {

        this.fieldsProps = [];

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


        this.maintainance_object_id = this.propsValue.record.data.id;


    }

    _getFieldInfo(archInfo) {

    }
}

MaintainanceObject.components = { Field, ObjectType };
MaintainanceObject.props = ["value"];
MaintainanceObject.template = "bms.maintainance_object";

