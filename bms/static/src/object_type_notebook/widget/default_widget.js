// /** @odoo-module */
const { Component,  onWillStart, onWillUpdateProps } = owl;
import { OsloDatatypePrimitiveEnumeration } from "../oslo_type/oslo_datatype_primitive_enumeration";
import { OsloDatatypeIterative } from "../oslo_type/oslo_datatype_iterative";

export class DefaultWidget extends Component {
    setup(){
        // _this._asssign_props_value(this.props)
        onWillStart(async () => {
            this._asssign_props_value(this.props)
        })
        onWillUpdateProps(async (nextProps) => {  
            this._asssign_props_value(nextProps)
        })

    }

    _asssign_props_value(props){
        this.attr_defs = props.attr_defs
        this.objectId = props.objectId
        this.objectTypeId = props.objectTypeId
    }

}

DefaultWidget.template = "bms.default_widget"
DefaultWidget.components = {OsloDatatypePrimitiveEnumeration, OsloDatatypeIterative }

