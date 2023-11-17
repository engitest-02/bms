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
            loadJS("/bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js")
            loadJS("/bms/static/lib/fancytree/js/jquery.fancytree.dnd5.js")
            loadCSS(["/bms/static/lib/fancytree/css/skin-odoo-bms/ui.fancytree.css"]);

            this.decompositionTypeRecords = await this._loadDecompositionTypes();
            this.lazyTreeString = await this._loadLazyTree(this.resId);            
            this.lazyTreeJson = JSON.parse(this.lazyTreeString);

        })
        
        onMounted(async () => {
            this.decompositionTree1 = $.ui.fancytree.createTree(
                '#decompositionTree_1',
                {extensions: ["dnd5"], //'edit', 'filter',
                 source: this.lazyTreeJson, 
                 click: this.loadClickedObjectId.bind(this),
                 autoScroll: true,
                 lazyLoad: (event, data) => {this._lazyLoad(event, data)},
                 dnd5:{
                    autoExpandMS: 1500,
                    preventRecursion: true, // Prevent dropping nodes on own descendants
                    preventVoidMoves: true,
                    // autoExpandMS: 1000,
                    // dropEffectDefault: "move",
                    // preventForeignNodes: false,   // Prevent dropping nodes from another Fancytree
                    // preventLazyParents: false,     // Prevent dropping items on unloaded lazy Fancytree nodes
                    // preventNonNodes: false,       // Prevent dropping items other than Fancytree nodes
                    // preventRecursion: false,       // Prevent dropping nodes on own descendants when in move-mode
                    // preventSameParent: false,     // Prevent dropping nodes under same direct parent
                    // preventVoidMoves: false,       // Prevent moving nodes 'before self', etc.
                    // multiSource: true,  // drag all selected nodes (plus current node)
                    dragStart: (sourceNode, data) => {this._dragStart(sourceNode, data)}, // must return true to enable draggin
                    dragEnd: (sourceNode, data) => {this._dragEnd(sourceNode, data)},
                    dragEnter: (targetNode, data) => {this._dragEnter(targetNode, data)}, // must return true to enable dropping
                    dragOver: (targetNode, data) => {this._dragOver(targetNode, data)},
                    dragDrop: (targetNode, data) => {this._dragDrop(targetNode, data)}
                 }

                }
            );
            this.decompositionTree1.activateKey(this.resId);

        })
    }

    loadClickedObjectId(ev, data){
        //console.log("decompostion click objectId", data.node.key)
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

    // function for drag&drop support on the treeview
    // --- Drag Support --------------------------------------------------------

    _dragStart(node, data){
        // Called on source node when user starts dragging `node`.
        // This method MUST be defined to enable dragging for tree nodes!
        // We can
        //   - Add or modify the drag data using `data.dataTransfer.setData()`.
        //   - Call `data.dataTransfer.setDragImage()` and set `data.useDefaultImage` to false.
        //   - Return false to cancel dragging of `node`.
  
        // Set the allowed effects (i.e. override the 'effectAllowed' option)
        data.effectAllowed = "all";  // or 'copyMove', 'link'', ...
  
        // Set a drop effect (i.e. override the 'dropEffectDefault' option)
        // One of 'copy', 'move', 'link'.
        // In order to use a common modifier key mapping, we can use the suggested value:
        data.dropEffect = data.dropEffectSuggested;
  
        // We could also define a custom image here (not on IE though):
        //data.dataTransfer.setDragImage($("<div>TEST</div>").appendTo("body")[0], -10, -10);
        //data.useDefaultImage = false;
  
        // Return true to allow the drag operation
        if( node.isFolder() ) { return false; }
        console.log("dragStart", data.dropEffectSuggested, data)
        return true; 
      }

    // --- Drop Support --------------------------------------------------------
    _dragEnter(node, data) {
        // Called on target node when s.th. is dragged over `node`.
        // `data.otherNode` may be a Fancytree source node or null for 
        // non-Fancytree droppables.
        // This method MUST be defined to enable dropping over tree nodes!
        //
        // We may
        //   - Set `data.dropEffect` (defaults to '')
        //   - Call `data.setDragImage()`
        //
        // Return
        //   - true to allow dropping (calc the hitMode from the cursor position)
        //   - false to prevent dropping (dragOver and dragLeave are not called)
        //   - a list (e.g. ["before", "after"]) to restrict available hitModes
        //   - a string "over", "before, or "after" to force a hitMode
        //   - Any other return value will calc the hitMode from the cursor position.
  
        // Example:
        // Prevent dropping a parent below another parent (only sort nodes under
        // the same parent):
        //if(node.parent !== data.otherNode.parent){
        //  return false;
        //}
        // Example:
        // Don't allow dropping *over* a node (which would create a child). Just
        // allow changing the order:
        //return ["before", "after"];
  
        // Accept everything:
        // data.node.info("dragEnter", data, true);
        console.log("_dragEnter");
        // data.dropEffect = "move";
        return true;
      }
    
    _dragOver(node, data) {
        // Called on target node every few milliseconds while some source is 
        // dragged over it.
        // `data.hitMode` contains the calculated insertion point, based on cursor
        // position and the response of `dragEnter`.
        //
        // We may
        //   - Override `data.hitMode`
        //   - Set `data.dropEffect` (defaults to the value that of dragEnter)
        //     (Note: IE will ignore this and use the value from dragenter instead!)
        //   - Call `data.dataTransfer.setDragImage()`
  
        // Set a drop effect (i.e. override the 'dropEffectDefault' option)
        // One of 'copy', 'move', 'link'.
        // In order to use a common modifier key mapping, we can use the suggested value:
        // data.dropEffect = data.dropEffectSuggested;
        data.node.info("dragOver", data)
        data.dropEffect = data.dropEffectSuggested;
      }
    _dragEnd(node, data) {
        data.node.info("dragEnd", data);
        // return true
    }
     _dragDrop(node, data) {
        // This function MUST be defined to enable dropping of items on the tree.
        //
        // The source data is provided in several formats:
        //   `data.otherNode` (null if it's not a FancytreeNode from the same page)
        //   `data.otherNodeData` (Json object; null if it's not a FancytreeNode)
        //   `data.dataTransfer.getData()`
        //
        // We may access some meta data to decide what to do:
        //   `data.hitMode` ("before", "after", or "over").
        //   `data.dataTransfer.dropEffect`,`.effectAllowed`
        //   `data.originalEvent.shiftKey`, ...
        //
        // Example:
        console.log("dragDrop")
        var transfer = data.dataTransfer;

        node.debug("dragDrop", data);
  
        if( data.otherNode ) {
          // Drop another Fancytree node from same frame
          // (maybe from another tree however)
          var sameTree = (data.otherNode.tree === data.tree);
  
          data.otherNode.moveTo(node, data.hitMode);
        } else if( data.otherNodeData ) {
          // Drop Fancytree node from different frame or window, so we only have
          // JSON representation available
          node.addChild(data.otherNodeData, data.hitMode);
        } else {
          // Drop a non-node
          node.addNode({
            title: transfer.getData("text")
          }, data.hitMode);
        }
        // Expand target node when a child was created:
        node.setExpanded();
      }
}

Decomposition.template = "bms.Decomposition";


