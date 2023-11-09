// /** @odoo-module */

import { OsloDatatypePrimitiveEnumeration } from "./oslo_datatype_primitive_enumeration"
const { Component } = owl


export class OsloDatatypeIterative extends Component {
    setup(){
        this.attrName = this.props.attr.attr_name
        this.iterativeAttributes = this.props.attr.attr_datatype_def.iterative_attributes
        this.objectId = this.props.objectId
        this.objectTypeId = this.props.objectTypeId
    }
}

OsloDatatypeIterative.template = "bms.oslo_datatype_iterative"
OsloDatatypeIterative.components = {OsloDatatypePrimitiveEnumeration, OsloDatatypeIterative}