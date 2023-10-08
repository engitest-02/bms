/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { loadCSS, loadJS } from "@web/core/assets";
var core = require("web.core");

const { Component, onMounted, onWillStart, useRef } = owl;

export class Decomposition extends Component {
    loadObjectId(objectId){
        this.model.load({resId: objectId});
    }

    setup() {
        this.ormService = useService("orm");
        this.rpcService = useService("rpc");
        this.decompositionTree;
        this.model = this.props.model;
        this.resId = this.props.resId;
        this.core = core;

        onWillStart(async () => {
            loadJS(["/bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js"]);
            loadCSS(["bms/static/lib/fancytree/css/skin-odoo-bms/ui.fancytree.css"])

            this.decompositionTypeRecords = await this._loadDecompositionTypes();
            this.treeString = await this._loadJsonTree();
            this.treeJson = JSON.parse(this.treeString);
        })
        
        onMounted(async () => {
            this.decompositionTree = $.ui.fancytree.createTree('#decompositionTree_1', {
                extensions: ['edit', 'filter'],
                source: this.treeJson, 
                click: this.loadClickedObjectId.bind(this),
                autoScroll: true,
            }
            );
            this.decompositionTree.activateKey(this.resId);

            console.log("decompostion.js: TODO: review toggleDecomposition which is in demo mode");
        })

    }

    loadClickedObjectId(ev, data){
        this.model.load({resId:  parseInt(data.node.key)});
     }

    toggleDecomposition(event) {
        // TODO: adapt the logica !!!! not generic. 
        if (event.target.id === "decomposition_1") {
            document.getElementById("decompositionTree_1").style.visibility = "visible";
            document.getElementById("decompositionTree_2").style.visibility = "hidden";
        } else {
            document.getElementById("decompositionTree_1").style.visibility = "hidden";
            document.getElementById("decompositionTree_2").style.visibility = "visible";
        }
    }

    _loadObjectId(objectId){
        this.model.load({resId: objectId});
        this.core.bus.trigger("decomposition_upload");
    }

    _loadDecompositionTypes() {
        return this.ormService.searchRead("bms.decomposition_type", [], []);
    }

    _loadJsonTree() {
        var rpc = require('web.rpc');
        return rpc.query({
            model: 'bms.decomposition_relationship',
            method: 'getTree',
            args: [],
        });
    }

}

Decomposition.template = "bms.Decomposition";

// CustomerList.props = {
//     selectCustomer: {
//         type: Function,
//     },
// };

