import{isEmpty}from"../../base/helpers.mjs";import{ImageView}from"../../view/image.mjs";import{InputView}from"./base.mjs";class FileInputView extends InputView{static inputType="file";inputted(e){super.inputted(e),this.node.css({"background-size":"0% 100%"})}getValue(){if(void 0!==this.node&&this.node.element.files&&this.node.element.files.length>0)return this.node.element.files[0]}setProgress(e){this.progress=e,void 0!==this.node&&this.node.css({"background-size":100*this.progress+"% 100%"})}async build(){let e=await super.build(),t=isEmpty(this.progress)?0:this.progress;return e.css({"background-size":100*t+"% 100%"}).on("drop",(e=>{e.dataTransfer.files&&e.stopPropagation()})),e}}class ImageFileInputView extends FileInputView{getValue(){return isEmpty(this.data)?super.getValue():this.data}changed(){if(this.data=null,void 0!==this.node){let e=this.node.element.parentElement;if(!isEmpty(e)){let t=e.querySelector("img");isEmpty(t)||e.removeChild(t)}}return new Promise((async(e,t)=>{let i=this.getValue();if(i instanceof File){let s=new FileReader;s.addEventListener("load",(async()=>{if(!s.result.substring(5,s.result.indexOf(";")).startsWith("image"))return this.setValue(null),void t("File must be an image.");this.data=s.result;let i=new ImageView(this.config,this.data);this.node.element.parentElement.insertBefore(await i.render(),this.node.element.parentElement.children[0]),await super.changed(),e()})),s.readAsDataURL(i)}else await super.changed(),e()}))}}export{FileInputView,ImageFileInputView};
