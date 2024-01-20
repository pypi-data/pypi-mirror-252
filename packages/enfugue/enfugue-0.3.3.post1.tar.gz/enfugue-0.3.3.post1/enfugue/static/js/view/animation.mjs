import{isEmpty,waitFor}from"../base/helpers.mjs";import{View}from"./base.mjs";import{ImageView}from"./image.mjs";class AnimationView extends View{static tagName="enfugue-animation-view";constructor(i,t=[]){super(i),this.canvas=document.createElement("canvas"),this.loadedCallbacks=[],this.setImages(t)}onLoad(i){this.loaded?i(this):this.loadedCallbacks.push(i)}setImages(i){this.images=i,isEmpty(i)?(this.loaded=!0,this.clearCanvas()):(this.loaded=!1,this.imageViews=i.map((i=>new ImageView(this.config,i,!1))),Promise.all(this.imageViews.map((i=>i.waitForLoad()))).then((()=>this.imagesLoaded())))}async imagesLoaded(){if(this.loaded=!0,!isEmpty(this.imageViews)){this.width=this.imageViews[0].width,this.height=this.imageViews[0].height,this.canvas.width=this.width,this.canvas.height=this.height,this.canvas.getContext("2d").drawImage(this.imageViews[0].image,0,0),void 0!==this.node&&this.node.css({width:this.width,height:this.height})}for(let i of this.loadedCallbacks)await i()}waitForLoad(){return waitFor((()=>this.loaded))}setFrame(i){if(isEmpty(i)&&(i=0),i>=this.imageViews.length&&(i=this.imageViews.length-1),this.frame=i,this.loaded){this.canvas.getContext("2d").drawImage(this.imageViews[this.frame].image,0,0)}else this.waitForLoad().then((()=>this.setFrame(i)))}clearCanvas(){this.canvas.getContext("2d").clearRect(0,0,this.canvas.width,this.canvas.height)}async build(){let i=await super.build();return i.content(this.canvas),this.loaded&&i.css({width:this.width,height:this.height}),i}}export{AnimationView};
