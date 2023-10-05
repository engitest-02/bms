/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
const { Component, onMounted, onWillStart } = owl;
import { loadCSS, loadJS } from "@web/core/assets";


export class Decomposition extends Component {

    setup() {
        this.ormService = useService("orm");
        this.rpcService = useService("rpc");
        this.decompositionTree;

        onWillStart(async () => {
            this.decompositionTypeRecords = await this._loadDecompositionTypes();
            loadJS(["/bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js"]);
            loadCSS(["bms/static/lib/fancytree/css/skin-win8/ui.fancytree.min.css"])
            //await loadJS("//code.jquery.com/jquery-3.6.0.min.js");
            //loadCSS("//cdn.jsdelivr.net/npm/jquery.fancytree@2.27/dist/skin-win8/ui.fancytree.min.css");
            //await loadJS("//cdn.jsdelivr.net/npm/jquery.fancytree@2.27/dist/jquery.fancytree-all-deps.min.js");

            this.treeString = await this._loadJsonTree();
            this.treeJson = JSON.parse(this.treeString);
        })
        onMounted(async () => {
            
            this.decompositionTree = $.ui.fancytree.createTree('#tree', {
                extensions: ['edit', 'filter'],
                source: this.treeJson});
            // $('#tree').fancytree({
            //     // extensions: ['edit', 'filter'],
            //     source: this.treeJson,
            // });
            // this.decompositionTree = fancytree.getTree('#tree');
        })
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