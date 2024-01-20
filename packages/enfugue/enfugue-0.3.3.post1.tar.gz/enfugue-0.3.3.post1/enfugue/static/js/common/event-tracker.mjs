import{DOMWatcher}from"../base/watcher.mjs";import{uuid}from"../base/helpers.mjs";const eventTrackingConfig={childList:!0,subtree:!0,attributes:!0};let trackers=[];class UserEventTracker extends DOMWatcher{constructor(e){super(e),this.filterFunction=this.nodeFilter,this.initializeFunction=this.nodeInitialize,this.uninitializeFunction=this.nodeUninitialize,this.eventTrackerCallbacks=e.eventTrackerCallbacks,this.boundEvents={}}nodeFilter(e){return void 0!==this.getTrackingProperties(e)}nodeInitialize(e){let t=this.getTrackingProperties(e);this.boundEvents[t.id]={};for(let n of t.events){let i=function(e,t,n){return function(e){let i=t.value;"function"==typeof i&&(i=i());for(let r of n)r(e,t.category,i)}}(0,t,this.eventTrackerCallbacks);this.boundEvents[t.id][n]=i,e.addEventListener(n,i)}}nodeUninitialize(e){let t=e.getAttribute("data-tracking-id");for(let n in this.boundEvents[t])e.removeEventListener(n,this.boundEvents[t][n]);delete this.boundEvents[t]}addTrackedNode(e){e.setAttribute("data-tracking-id",uuid()),super.addTrackedNode(e)}getTrackingProperties(node){try{let events=node.getAttribute("data-tracking-events"),id=node.getAttribute("data-tracking-id");if(null!=events){let valueType=node.getAttribute("data-tracking-value-type");null===valueType&&(valueType="static");let value=node.getAttribute("data-tracking-value");return"function"===valueType&&(value=function(node,value){return function(){return function(value){return eval(value)}.call(node,value)}}(node,value)),{id:id,events:events.split(","),category:node.getAttribute("data-tracking-category"),value:value}}}catch(e){}}}let createTracker=function(e,t){let n={node:e,eventTrackerCallbacks:Array.from(arguments).slice(2),debug:t},i=new UserEventTracker(n);return trackers.push(i),i};export let EventTracking={track:createTracker};
