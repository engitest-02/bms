/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { loadCSS, loadJS } from "@web/core/assets";
import { memoize } from "@web/core/utils/functions";
var core = require("web.core");
var rpc = require('web.rpc');

const { Component, onMounted, onWillStart, useRef } = owl;

export class Decomposition extends Component {

    setup() {
        this.ormService = useService("orm");
        this.rpcService = useService("rpc");
        this.decompositionTree;
        this.model = this.props.model;
        this.resId = this.props.resId;
        this.core = core;

        onWillStart(async () => {
            loadJS(["/bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js"]);
            loadCSS(["/bms/static/lib/fancytree/css/skin-odoo-bms/ui.fancytree.css"]);

            this.decompositionTypeRecords = await this._loadDecompositionTypes();
            this.lazyTreeString = await this._loadLazyTree(this.resId);            
            this.lazyTreeJson = JSON.parse(this.lazyTreeString);

        })
        
        onMounted(async () => {
            this.decompositionTree1 = $.ui.fancytree.createTree(
                '#decompositionTree_1',
                {extensions: ['edit', 'filter'],
                 source: this.lazyTreeJson, 
                 click: this.loadClickedObjectId.bind(this),
                 autoScroll: true,
                 lazyLoad: (event, data) => {this._lazyLoad(event, data)}
                }
            );
            this.decompositionTree1.activateKey(this.resId);

        })
    }

    loadClickedObjectId(ev, data){
        this.model.load({resId: parseInt(data.node.key)});
     }

    _loadDecompositionTypes() {
        return this.ormService.searchRead("bms.decomposition_type", [], []);
    }

    _loadLazyTree(object_id){
        return rpc.query({model: 'bms.decomposition_relationship',
                                   method: 'get_lazy_tree_for_object',
                                   args: [object_id], });
               
    }
    
    _lazyLoad(event, data){
        var node = data.node
        var nextTree = rpc.query({
            model: 'bms.decomposition_relationship',
            method: 'get_lazy_tree',
            args: [node.key],
            }).then((tree) => {return JSON.parse(tree);});
        data.result = nextTree

    }

}

Decomposition.template = "bms.Decomposition";


