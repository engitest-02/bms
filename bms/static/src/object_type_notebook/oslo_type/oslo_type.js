// /** @odoo-module */

import { useService, useBus } from "@web/core/utils/hooks";
const { Component, onWillStart, onWillPatch } = owl;



export class OsloType extends Component {
    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.otlId = this.props.otlId;
        this.classUri = this.props.classUri;
        this.className = this.props.className;
        this.objectTypeId = this.props.objectTypeId;
        this.objectId = this.props.objectId;

        this.currentObjectId = this.objectId;
        this.attrPrimitiveDatatypeRecs;

        onWillStart(async () => {
            this.attrPrimitiveDatatypeRecs = await this._loadAttrPrimitiveDatatype(this.classUri);
        })

        onWillPatch(async () => {
            this.otlId = this.props.otlId;
            this.classUri = this.props.classUri;
            this.className = this.props.className;
            this.objectTypeId = this.props.objectTypeId;
            this.objectId = this.props.objectId;

            if (this.currentObjectId != this.objectId) {// rerender OTL notebook if parent object has changed
                this.attrPrimitiveDatatypeRecs = await this._loadAttrPrimitiveDatatype(this.classUri);
                this.render();
                this.currentObjectId = this.objectId;
            }
        })

    }

    _loadAttrPrimitiveDatatype(osloclass_uri) {
        const domain = [["osloclass_uri", "=", osloclass_uri]];
        const result = this.orm.searchRead("bms.awv_attributen_primitive_datatype", domain)
        return result;  
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

    changeAttrValue(record) {
        console.log("record", record);
        const context = {
            'default_object_id': this.objectId,
            'default_object_type_id': this.objectTypeId,
            'default_oslo_attributen_uri': record.osloattributen_uri,
            'default_attr_name': record.osloattributen_name,
            'default_attr_def': record.osloattributen_definition,
            'default_att_def_value_type_definition': record.oslodatatype_primitive_definition_nl,
            'default_attr_def_value_type': record.value_type,
            'default_value_char': record.value_char,
            'default_value_boolean': record.value_boolean,
            'default_value_date': record.value_date,
            'default_value_datetime': record.value_datetime,
            'default_value_float': record.value_float,
            'default_value_integer': record.value_integer,
            'form_view_initial_mode': "edit",
        }
        this.actionService.doAction(
            {
                "type": "ir.actions.act_window",
                "res_model": "bms.wz_oslo_attributen_value",
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

}

OsloType.template = "bms.oslo_type";

