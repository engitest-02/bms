// /** @odoo-module */

import { useService} from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
const { Component, onWillStart, onWillUpdateProps } = owl;

var rpc = require('web.rpc');

export class OsloType extends Component {
    // customized the visualisation and editing of the object_types and its attributes

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.objectId = this.props.objectId;
        this._assign_props_value(this.props);

        onWillStart(async () => {
            this.attrDefs = await this._getAttrDefs(this.classUri)
        })

        onWillUpdateProps(async (nextProps) => {  
            this.objectId = nextProps.objectId;
            if (this.currentObjectId != this.objectId) {// rerender OTL notebook if parent object has changed
                this._assign_props_value(nextProps);
                this.attrDefs = await this._getAttrDefs(this.classUri)           
            }
        })      
    }

    changeOtlAndType() {
        if (this.objectId == null) { // maintainance object is new => first must be saved
            var Dialog = require('web.Dialog')
            Dialog.alert(
                this,
                "You have to save your new asset first",
                {onForceClose: function () {},confirm_callback: function () {}}
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

    _assign_props_value(props){
        this.otlId = props.otlId;
        this.objectTypeId = props.objectTypeId; 
        this.classUri = props.classUri;
        this.className = props.className;
        this.currentObjectId = props.objectId;
    }

    async _getAttrDefs(classUri){
        const data = await this._loadAttrDefinition(classUri);
        let attrDefs = JSON.parse(data)
        attrDefs = this._insertWidgetComponent(attrDefs)
        return attrDefs
    }

    _loadAttrDefinition(osloclass_uri){
        const attrDefs = rpc.query({
            model: 'bms.attribute_definition',
            method: 'get_att_def',
            args: [osloclass_uri],
            }
        )
        return attrDefs   
    }
    
    _insertWidgetComponent(attrDefs){ // add the Widget Component Classes to make them available in the template
        attrDefs["widget_attrs"].forEach(attrDef =>{
             const widget =  registry.category("attribute_widget").get(attrDef.widget_name)
             attrDef.Component = widget.Component
        })
        return attrDefs
    }


}

OsloType.template = "bms.oslo_type";

