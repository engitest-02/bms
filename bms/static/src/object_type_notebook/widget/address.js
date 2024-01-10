// /** @odoo-module */
const { Component, onWillStart, onWillUpdateProps } = owl;

export class Address extends Component {
    setup(){
        
        onWillStart(()=>{
            console.log("Address props", this.props)
        })
    }
}

Address.template = "bms.address"

