import{ElementBuilder}from"../../base/builder.mjs";import{Controller}from"../base.mjs";import{View}from"../../view/base.mjs";import{ListInputView}from"../../forms/input.mjs";import{isEmpty,kebabCase,getPointerEventCoordinates,bindPointerUntilRelease}from"../../base/helpers.mjs";const E=new ElementBuilder,leftMargin=250,rightMargin=250,topMargin=96,bottomMargin=80;let currentHeight=window.innerHeight-176,currentWidth=window.innerWidth-500;class DragLayoutInputView extends View{static minimumRatio=.1;static tagName="enfugue-drag-layout";constructor(t){super(t),this.onChangeCallbacks=[],this.mode="horizontal",this.ratio=.5}onChange(t){this.onChangeCallbacks.push(t)}setMode(t,i){this.mode=t,this.setRatio(i,!1)}setRatio(t,i=!0){if(this.ratio=t,i)for(let t of this.onChangeCallbacks)t(this.ratio);isEmpty(this.node)||("horizontal"===this.mode?this.node.css({top:"120px",bottom:"80px",right:"auto",left:250+this.ratio*currentWidth+"px"}):this.node.css({top:96+this.ratio*currentHeight+"px",bottom:"auto",left:"250px",right:"250px"}))}async build(){let t=await super.build();return t.on("mousedown,touchstart",(t=>{"mousedown"===t.type&&1!==t.which||(t.preventDefault(),t.stopPropagation(),bindPointerUntilRelease((t=>{let[i,a]=getPointerEventCoordinates(t);i-=250,a-=96;let e=Math.min(Math.max(i,0),currentWidth)/currentWidth,s=Math.min(Math.max(a,0),currentHeight)/currentHeight;e=Math.max(this.constructor.minimumRatio,Math.min(e,1-this.constructor.minimumRatio)),s=Math.max(this.constructor.minimumRatio,Math.min(s,1-this.constructor.minimumRatio)),"horizontal"===this.mode?this.setRatio(e):this.setRatio(s)})))})),t}}class CurrentViewInputView extends ListInputView{static className="list-input-view current-view-input-view";static defaultValue="canvas";static defaultOptions={canvas:"Canvas"};static tooltip="This is your current view. By default you will always view the input canvas. When there are results from your generations, the sample canvas will be available."}class LayoutController extends Controller{static layouts=["dynamic","vertical","horizontal"];get layout(){let t=this.application.session.getItem("layout");return isEmpty(t)?"dynamic":t}set layout(t){this.application.session.setItem("layout",t),this.setLayout(t)}get horizontalRatio(){let t=this.application.session.getItem("horizontalRatio");return isEmpty(t)?.5:t}set horizontalRatio(t){this.application.session.setItem("horizontalRatio",t)}get verticalRatio(){let t=this.application.session.getItem("verticalRatio");return isEmpty(t)?.5:t}set verticalRatio(t){this.application.session.setItem("verticalRatio",t)}setLayout(t){window.requestAnimationFrame((()=>{for(let i of this.constructor.layouts)t===i?this.application.container.classList.add(`enfugue-layout-${i}`):this.application.container.classList.remove(`enfugue-layout-${i}`);"dynamic"===t?(this.hideSamples(),this.dragLayoutView.hide()):(this.showSamples(),this.dragLayoutView.show(),this.dragLayoutView.setMode(t,"horizontal"===t?this.horizontalRatio:this.verticalRatio)),this.updateRatios()}))}showSamples(t=!0){t&&(this.currentViewInput.setOptions({canvas:"Canvas",samples:"Samples"}),this.currentViewInput.setValue("samples",!1)),this.application.images.show()}hideSamples(t=!0){t&&(this.currentViewInput.setOptions({canvas:"Canvas"}),this.currentViewInput.setValue("canvas",!1)),this.application.images.hide()}checkHideSamples(t=!0){"dynamic"===this.layout&&this.hideSamples(t)}checkShowSamples(t=!0){"dynamic"!==this.layout&&this.showSamples(t)}updateRatios(t=!1){"vertical"===this.layout?(this.canvas.node.css({left:"250px",right:"250px",bottom:76+(1-this.verticalRatio)*currentHeight+"px",top:"96px"}),this.images.node.css({left:"250px",right:"250px",top:75+this.verticalRatio*currentHeight+"px",bottom:"80px"}),t&&this.dragLayoutView.setRatio(this.verticalRatio,!1)):"horizontal"===this.layout?(this.canvas.node.css({left:"250px",bottom:"80px",top:"96px",right:248+(1-this.horizontalRatio)*currentWidth+"px"}),this.images.node.css({left:252+this.horizontalRatio*currentWidth+"px",right:"250px",top:"96px",bottom:"80px"}),t&&this.dragLayoutView.setRatio(this.horizontalRatio,!1)):(this.canvas.node.css({left:null,right:null,top:null,bottom:null}),this.images.node.css({left:null,right:null,top:null,bottom:null}))}async initialize(){let t=this.application.menu.getCategory("Layout"),i=await t.addItem("Dynamic","fa-solid fa-arrows-rotate"),a=await t.addItem("Split Horizontally","fa-solid fa-arrows-left-right"),e=await t.addItem("Split Vertically","fa-solid fa-arrows-up-down"),s=await t.addItem("Tile Horizontally","fa-solid fa-ellipsis"),o=await t.addItem("Tile Vertically","fa-solid fa-ellipsis-vertical");i.onClick((()=>{this.layout="dynamic"})),a.onClick((()=>{this.layout="horizontal"})),e.onClick((()=>{this.layout="vertical"})),s.onClick((()=>{let t=s.hasClass("active");this.application.samples.setTileHorizontal(!t),s.toggleClass("active")})),o.onClick((()=>{let t=o.hasClass("active");this.application.samples.setTileVertical(!t),o.toggleClass("active")})),this.currentViewInput=new CurrentViewInputView(this.config),this.currentViewInput.onChange(((t,i)=>{"samples"===i?this.showSamples(!1):(this.application.samples.setPlay(!1),setTimeout((()=>{this.hideSamples(!1)}),100))})),this.application.container.appendChild(await this.currentViewInput.render()),this.dragLayoutView=new DragLayoutInputView(this.config),this.dragLayoutView.onChange((t=>{"horizontal"===this.layout?this.horizontalRatio=t:this.verticalRatio=t,this.updateRatios()})),this.dragLayoutView.hide(),this.application.container.appendChild(await this.dragLayoutView.render()),this.setLayout(this.layout),this.application.images.addClass("samples"),this.checkHideSamples(),window.addEventListener("resize",(()=>{currentHeight=window.innerHeight-176,currentWidth=window.innerWidth-500,this.updateRatios(!0)}))}}export{LayoutController};
