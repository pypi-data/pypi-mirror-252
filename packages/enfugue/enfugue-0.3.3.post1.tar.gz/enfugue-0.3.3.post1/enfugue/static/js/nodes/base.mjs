import{View}from"../view/base.mjs";import{FormView}from"../forms/base.mjs";import{InputView,ListInputView}from"../forms/input.mjs";import{ElementBuilder}from"../base/builder.mjs";import{Point,Drawable}from"../graphics/geometry.mjs";import{merge,sleep,isEmpty,camelCase,bindPointerUntilRelease,getPointerEventCoordinates}from"../base/helpers.mjs";const E=new ElementBuilder({nodeContainer:"enfugue-node-container",nodeContents:"enfugue-node-contents",nodeHeader:"enfugue-node-header",nodeName:"enfugue-node-name",nodeButton:"enfugue-node-button",nodeOptionsContents:"enfugue-node-options-contents",nodeOptionsInputsOutputs:"enfugue-node-options-inputs-outputs",nodeOptions:"enfugue-node-options",nodeInputs:"enfugue-node-inputs",inputModes:"enfugue-node-input-modes",nodeOutputs:"enfugue-node-outputs",nodeInput:"enfugue-node-input",nodeInputGroup:"enfugue-node-input-group",nodeOutput:"enfugue-node-output",nodeOutputGroup:"enfugue-node-output-group"});class NodeCursorMode{static NONE=0;static MOVE=1;static RESIZE_N=2;static RESIZE_NE=3;static RESIZE_E=4;static RESIZE_SE=5;static RESIZE_S=6;static RESIZE_SW=7;static RESIZE_W=8;static RESIZE_NW=9}class NodeView extends View{static tagName="enfugue-node";static edgeHandlerTolerance=10;static canClose=!0;static canResizeX=!0;static canResizeY=!0;static canMove=!0;static canRename=!0;static canCopy=!0;static canFlipHeader=!1;static minWidth=150;static minHeight=100;static headerHeight=30;static snapSize=10;static padding=10;static defaultCursor="default";static fixedHeight=!1;static hideHeader=!1;static nodeButtons={};static copyText="Copy";static closeText="Close";static headerBottomText="Flip Header to Bottom";static headerTopText="Flip Header to Top";static headerBottomIcon="fa-solid fa-arrow-turn-down";static headerTopIcon="fa-solid fa-arrow-turn-up";constructor(t,e,s,o,i,r,n){super(t.config),this.editor=t,this.name=isEmpty(e)?this.constructor.name:e,this.content=s,this.left=isEmpty(o)?0:o,this.top=isEmpty(i)?0:i,this.left-=this.constructor.padding,this.top-=this.constructor.padding,this.width=isEmpty(r)?this.constructor.minWidth:r,this.width+=2*this.constructor.padding,this.height=isEmpty(n)?this.constructor.minHeight:n,this.height+=2*this.constructor.padding,this.setDimension(this.left,this.top,this.width,this.height,!0,!1),this.removed=!1,this.fixed=!1,this.canMerge=this.constructor.canMerge,this.closeCallbacks=[],this.resizeCallbacks=[],this.nameChangeCallbacks=[]}async getContent(){let t=this.content;return t instanceof View?await t.getNode():t}async setContent(t){return this.content=t,void 0!==this.node&&this.node.find(E.getCustomTag("nodeContents")).content(await this.getContent()),this}onClose(t){this.closeCallbacks.push(t)}async closed(){for(let t of this.closeCallbacks)await t()}onResize(t){this.resizeCallbacks.push(t)}async resized(){this.content instanceof View&&this.content.resize();for(let t of this.resizeCallbacks)await t()}get drawable(){return new Drawable([new Point(this.visibleLeft,this.visibleTop),new Point(this.visibleLeft+this.visibleWidth,this.visibleTop),new Point(this.visibleLeft+this.visibleWidth,this.visibleTop+this.visibleHeight),new Point(this.visibleLeft,this.visibleTop+this.visibleHeight)])}get x(){return this.left+this.constructor.padding}get y(){return this.top+this.constructor.padding}get w(){return this.width-2*this.constructor.padding}get h(){return this.height-2*this.constructor.padding}getState(){return{name:this.getName(),classname:this.constructor.name,x:this.x,y:this.y,w:this.w,h:this.h}}async setState(t){return this.name=t.name,this.setDimension(t.x-this.constructor.padding,t.y-this.constructor.padding,t.w+2*this.constructor.padding,t.h+2*this.constructor.padding,!0,!1),void 0!==this.node&&this.node.find(E.getCustomTag("nodeName")).content(this.name),this}setName(t,e=!0,s=!0){if(this.name=t,e&&void 0!==this.node&&this.node.find(E.getCustomTag("nodeName")).content(t),s)for(let e of this.nameChangeCallbacks)e(t)}onNameChange(t){this.nameChangeCallbacks.push(t)}getName(){return void 0===this.node?this.name:this.node.find(E.getCustomTag("nodeName")).getText()}remove(t=!0){this.removed=!0,this.editor.removeNode(this),t&&this.closed()}focus(){this.editor.focusNode(this)}static getNearestSnap(t,e,s){return isEmpty(e)&&(e=-this.padding),isEmpty(s)&&(s=1/0),Math.min(Math.max(Math.round(t/this.snapSize)*this.snapSize,e),s)}getLeftSnap(t){return this.constructor.getNearestSnap(t,-this.constructor.padding,this.editor.width+this.constructor.padding-this.width)}getTopSnap(t){return this.constructor.getNearestSnap(t,-this.constructor.padding,this.editor.height+this.constructor.padding-this.height)}getWidthSnap(t,e){return this.constructor.getNearestSnap(t,this.constructor.minWidth+2*this.constructor.padding,this.editor.width+this.constructor.padding-e)}getHeightSnap(t,e){return this.constructor.getNearestSnap(t,this.constructor.minHeight+2*this.constructor.padding,this.editor.height+this.constructor.padding-e)}resetDimension(){return this.setDimension(this.left,this.top,this.width,this.height,!0)}setDimension(t,e,s,o,i,r=!0){if(t=this.constructor.getNearestSnap(t),e=this.constructor.getNearestSnap(e),s=this.getWidthSnap(s,t),e+(o=this.getHeightSnap(o,e))>this.editor.height+this.constructor.padding){(e+=this.editor.height-e-o-this.constructor.padding)<0&&(o+=e,e=0)}if(t+s>this.editor.width+this.constructor.padding){(t+=this.editor.width-t-s-this.constructor.padding)<0&&(s+=t,t=0)}return void 0!==this.node&&this.node.css({left:`${t}px`,top:`${e}px`,width:`${s}px`,height:`${o}px`}),i&&(this.left=t,this.top=e,this.width=s,this.height=o),this.visibleLeft=t,this.visibleTop=e,this.visibleWidth=s,this.visibleHeight=o,r&&(i?this.editor.nodePlaced(this):this.editor.nodeMoved(this)),[t,e,s,o]}flipHeader(){!0===this.flipped?(this.flipped=!1,this.removeClass("flipped"),this.buttons.flip.tooltip=this.constructor.headerBottomText,this.buttons.flip.icon=this.constructor.headerBottomIcon):(this.flipped=!0,this.addClass("flipped"),this.buttons.flip.tooltip=this.constructor.headerTopText,this.buttons.flip.icon=this.constructor.headerTopIcon),this.rebuildHeaderButtons()}buildHeaderButtons(t,e){for(let s in e){let o=e[s];if(!0===o.disabled)continue;let i=E.nodeButton().class(`node-button-${camelCase(s)}`).content(E.i().class(o.icon)).on("click,touchstart",(t=>{o.callback.call(o.context||this,t)}));o.tooltip&&i.data("tooltip",o.tooltip),t.append(i)}}getButtons(){return isEmpty(this.buttons)?this.constructor.buttons:this.buttons}rebuildHeaderButtons(){void 0!==this.node&&this.lock.acquire().then((t=>{let e=this.node.find(E.getCustomTag("nodeHeader"));for(let t of e.children())if(t.tagName==E.getCustomTag("nodeButton"))try{e.remove(t)}catch(t){}this.buildHeaderButtons(e,this.buttons),e.render(),t()}))}async build(){let t,e,s=await super.build(),o=E.nodeContainer(),i=NodeCursorMode.NONE,r=NodeCursorMode.NONE,n=E.nodeName().content(this.name),d=E.nodeHeader().content(n).css({height:`${this.constructor.headerHeight}px`,"line-height":`${this.constructor.headerHeight}px`});this.constructor.canRename&&(n.editable().on("input",(()=>{this.setName(n.getText(),!1)})),d.on("dblclick",(t=>{t.preventDefault(),t.stopPropagation(),n.focus()}))),this.constructor.hideHeader&&s.addClass("hide-header");let c,h={};for(let t in this.constructor.nodeButtons)h[t]={...this.constructor.nodeButtons[t]},h[t].context=this;this.constructor.canCopy&&(h.copy={icon:"fa-solid fa-copy",tooltip:this.constructor.copyText,shortcut:"p",context:this,callback:()=>{this.editor.copyNode(this)}}),this.constructor.canFlipHeader&&(h.flip={shortcut:"b",icon:this.constructor.headerBottomIcon,tooltip:this.constructor.headerBottomText,context:this,callback:()=>{this.flipHeader()}}),this.constructor.canClose&&(h.close={shortcut:"v",icon:"fa-solid fa-window-close",tooltip:this.constructor.closeText,context:this,callback:()=>{this.closed(),this.editor.removeNode(this)}}),this.buildHeaderButtons(d,h),this.buttons=h;let a=(s,o)=>{isEmpty(s)&&(s=c);let r=!1,n=this.left,d=this.top,h=this.width,a=this.height,[u,p]=[0,0],[l,E]=[0,0];switch(isEmpty(s)||([l,E]=getPointerEventCoordinates(s),isEmpty(t)||isEmpty(e)||([u,p]=[l-t,E-e],u*=1/this.editor.zoom,p*=1/this.editor.zoom)),i){case NodeCursorMode.MOVE:n+=u,d+=p,r=!0;break;case NodeCursorMode.RESIZE_N:d+=p,a-=p,r=!0;break;case NodeCursorMode.RESIZE_NE:d+=p,a-=p,h+=u,r=!0;break;case NodeCursorMode.RESIZE_E:h+=u,r=!0;break;case NodeCursorMode.RESIZE_SE:h+=u,a+=p,r=!0;break;case NodeCursorMode.RESIZE_S:a+=p,r=!0;break;case NodeCursorMode.RESIZE_SW:a+=p,n+=u,h-=u,r=!0;break;case NodeCursorMode.RESIZE_W:n+=u,h-=u,r=!0;break;case NodeCursorMode.RESIZE_NW:d+=p,a-=p,n+=u,h-=u,r=!0}c=s,r&&(this.setDimension(n,d,h,a,o),this.editor.decorations.recalculate(),this.editor.decorations.draw(),this.resized())},u=t=>{let e=s.element.getBoundingClientRect(),o=this.constructor.edgeHandlerTolerance*this.editor.zoom,i=this.constructor.headerHeight*this.editor.zoom,[r,n]=getPointerEventCoordinates(t,s.element),d=n<o,c=r<o,h=r>e.width-o,a=n>e.height-o,u=!0===this.flipped?!a&&n>=e.height-i-o:!d&&n<o+i;return d&&c&&this.constructor.canResizeX&&this.constructor.canResizeY?NodeCursorMode.RESIZE_NW:d&&h&&this.constructor.canResizeX&&this.constructor.canResizeY?NodeCursorMode.RESIZE_NE:d&&this.constructor.canResizeY?NodeCursorMode.RESIZE_N:a&&c&&this.constructor.canResizeX&&this.constructor.canResizeY?NodeCursorMode.RESIZE_SW:a&&h&&this.constructor.canResizeX&&this.constructor.canResizeY?NodeCursorMode.RESIZE_SE:a&&this.constructor.canResizeY?NodeCursorMode.RESIZE_S:c&&this.constructor.canResizeX?NodeCursorMode.RESIZE_W:h&&this.constructor.canResizeX?NodeCursorMode.RESIZE_E:u&&this.constructor.canMove&&!c&&!h?NodeCursorMode.MOVE:NodeCursorMode.NONE},p=t=>{if(!this.fixed&&i==NodeCursorMode.NONE)switch(r=u(t),r){case NodeCursorMode.MOVE:s.css("cursor","grab");break;case NodeCursorMode.RESIZE_NE:case NodeCursorMode.RESIZE_SW:s.css("cursor","nesw-resize");break;case NodeCursorMode.RESIZE_N:case NodeCursorMode.RESIZE_S:s.css("cursor","ns-resize");break;case NodeCursorMode.RESIZE_E:case NodeCursorMode.RESIZE_W:s.css("cursor","ew-resize");break;case NodeCursorMode.RESIZE_NW:case NodeCursorMode.RESIZE_SE:s.css("cursor","nwse-resize");break;default:s.css("cursor",this.constructor.defaultCursor)}};o.append(d),s.append(o).css({left:`${this.left}px`,top:`${this.top}px`,width:`${this.width}px`,height:`${this.height}px`,padding:`${this.constructor.padding}px`}).on("mousemove",(t=>{this.fixed||i!==NodeCursorMode.NONE||p(t)})).on("mousedown,touchstart",(s=>{if(!(this.fixed||"mousedown"===s.type&&1!==s.which||i!==NodeCursorMode.NONE)&&(p(s),r!==NodeCursorMode.NONE))switch(s.preventDefault(),s.stopPropagation(),this.editor.focusNode(this),p(s),r){case NodeCursorMode.MOVE:case NodeCursorMode.RESIZE_NE:case NodeCursorMode.RESIZE_SW:case NodeCursorMode.RESIZE_N:case NodeCursorMode.RESIZE_S:case NodeCursorMode.RESIZE_E:case NodeCursorMode.RESIZE_W:case NodeCursorMode.RESIZE_NW:case NodeCursorMode.RESIZE_SE:switch([t,e]=getPointerEventCoordinates(s),i=r,i){case NodeCursorMode.MOVE:this.editor.node.css("cursor","grab");break;case NodeCursorMode.RESIZE_NE:case NodeCursorMode.RESIZE_SW:this.editor.node.css("cursor","nesw-resize");break;case NodeCursorMode.RESIZE_N:case NodeCursorMode.RESIZE_S:this.editor.node.css("cursor","ns-resize");break;case NodeCursorMode.RESIZE_E:case NodeCursorMode.RESIZE_W:this.editor.node.css("cursor","ew-resize");break;case NodeCursorMode.RESIZE_NW:case NodeCursorMode.RESIZE_SE:this.editor.node.css("cursor","nwse-resize");break;default:this.editor.node.css("cursor",this.constructor.defaultCursor)}let o=s=>{"touchend"===s.type?a(null,!0):a(s,!0),i=NodeCursorMode.NONE,[t,e]=[null,null],this.editor.node.css("cursor",this.constructor.defaultCursor),this.editor.constructor.disableCursor&&this.editor.node.css("pointer-events","none")};bindPointerUntilRelease((t=>a(t,!1)),(t=>o(t,!0))),this.editor.constructor.disableCursor&&this.editor.node.css("pointer-events","all")}}));let l=await this.getContent(),g=E.nodeContents();return isEmpty(l)||(l instanceof View&&(l=await l.getNode()),g.content(l)),g.on("mousedown,touchstart",(t=>{this.fixed||this.editor.focusNode(this)})),this.constructor.fixedHeight||(this.constructor.hideHeader||this.constructor.fixedHeader?g.css("height","100%"):g.css("height",`calc(100% - ${this.constructor.headerHeight}px)`)),o.append(g),s}}export{NodeView};
