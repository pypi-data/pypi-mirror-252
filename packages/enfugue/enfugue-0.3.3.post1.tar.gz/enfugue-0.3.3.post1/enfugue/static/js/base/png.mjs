import{isEmpty}from"./helpers.mjs";function byteArrayToString(e){let t="";for(let r of e)t+=String.fromCharCode(r);return t}function stringToByteArray(e){return new Array(e.length).fill(null).map(((t,r)=>e.charCodeAt(r)))}function splitDataURL(e){let[t,r]=e.split(","),[a,n]=t.split(";"),[i,s]=a.split(":"),[o,f]=s.split("/");return[o,f,n,r]}function normalize(e){return`${e}`.normalize("NFD").replace(/[\u0300-\u036f]/g,"")}const CRCTable=new Int32Array(new Array(256).fill(null).map(((e,t)=>{let r=t;for(let e=0;e<8;e++)r=1&r?-306674912^r>>>1:r>>>1;return r})));function CRC(e){let t=e.length>1e4?8:4,r=-1,a=e.length-(t-1),n=0;for(;n<a;)for(let a=0;a<t;a++)r=r>>>8^CRCTable[255&(r^e[n++])];for(;n<a+(t-1);)r=r>>>8^CRCTable[255&(r^e[n++])];return-1^r}const byteBuffer=new Uint8Array(4),int32ByteBuffer=new Int32Array(byteBuffer.buffer),uint32ByteBuffer=new Uint32Array(byteBuffer.buffer),bufferAsSigned=e=>{if(isEmpty(e))return int32ByteBuffer[0];int32ByteBuffer[0]=e},bufferAsUnsigned=e=>{if(isEmpty(e))return uint32ByteBuffer[0];uint32ByteBuffer[0]=e};class PNG{static headerBytes=[137,80,78,71,13,10,26,10];constructor(e,t){this.name=e,this.buffer=t}get data(){return new Uint8Array(this.buffer)}static fromFile(e){return new Promise(((t,r)=>{try{let a=new FileReader;a.onload=a=>{let n=new PNG(e.name,a.target.result);try{n.chunks,t(n)}catch(a){let n=new FileReader;n.onerror=e=>r(n),n.onload=e=>{PNG.fromURL(e.target.result).then(t).catch(r)},n.readAsDataURL(e)}},a.onerror=e=>r(a),a.readAsArrayBuffer(e)}catch(e){r(e)}}))}static fromBase64(e,t){return new this(e,stringToByteArray(atob(t)))}static fromImageURL(e){let t=null;if(!e.startsWith("data")){let[r,a]=e.split("?"),n=r.split("/");t=n[n.length-1]}return new Promise(((r,a)=>{let n=new XMLHttpRequest;n.responseType="blob",n.addEventListener("load",(function(e){200===this.status?this.response.arrayBuffer().then((e=>{r(new PNG(t,e))})):a(this.response)})),n.open("GET",e),n.send()}))}static fromOtherImageURL(e){let t=null;if(!e.startsWith("data")){let[r,a]=e.split("?"),n=r.split("/");t=n[n.length-1]}return new Promise(((r,a)=>{let n=new Image;n.onload=e=>{let a=document.createElement("canvas");a.width=n.width,a.height=n.height,a.getContext("2d").drawImage(n,0,0);let[i,s,o,f]=splitDataURL(a.toDataURL());r(this.fromBase64(t,f))},n.src=e}))}static fromURL(e){return new Promise(((t,r)=>{if(e.startsWith("data")){let[a,n,i,s]=splitDataURL(e);"base64"===i&&"image"===a?"png"===n?t(this.fromBase64(null,s)):this.fromOtherImageURL(e).then(t).catch(r):r(`Bad data; must be base64 and an image. Got data format '${i}' and media type/format ${a}/${n}`)}else{let[a,n]=e.split("?");a.endsWith(".png")?this.fromImageURL(e).then(t).catch(r):this.fromOtherImageURL(e).then(t).catch(r)}}))}static fromChunks(e,t){let r=this.headerBytes.length;for(let e of t)r+=e.data.length+12;let a=new Uint8Array(r),n=0,i=(e,t)=>{let r=e.length;for(let i=0;i<r;i++){let s=t?r-i-1:i;a[n++]=e[s]}};i(this.headerBytes,!1);for(let e of t){let t=stringToByteArray(e.name);bufferAsUnsigned(e.data.length),i(byteBuffer,!0),i(t,!1),i(e.data,!1),bufferAsSigned(CRC(t.concat(Array.from(e.data)))),i(byteBuffer,!0)}return new PNG(e,a)}get chunks(){let e=new Uint8Array(this.buffer),t=0,r=[],a=!1,n=(r,a,n=!0,i=0)=>{let s=t;for(;t-s<a&&t<e.length;){r[n?a-(t-s)+i-1:t-s+i]=e[t++]}};for(;t<this.constructor.headerBytes.length;t++)if(e[t]!==this.constructor.headerBytes[t])throw`Invalid .png file header - expected ${this.constructor.headerBytes[t]} at index ${t}, but got ${e[t]} instead.`;for(;t<e.length;){let e=t;n(byteBuffer,4);let i=bufferAsUnsigned()+4,s=new Uint8Array(i);n(s,4,!1);let o=byteArrayToString(s.slice(0,4));if(!r.length&&"IHDR"!==o)throw`First chunk does not contain IHDR (got ${o}); malformed PNG file.`;if("IEND"===o){a=!0,r.push({name:o,data:new Uint8Array(0),offset:e});break}n(s,i-4,!1,4),n(byteBuffer,4);let f=bufferAsSigned(),l=CRC(s);if(f!==l)throw`CRC Values are incorrect for ${o} - expected ${l}, got ${f}`;r.push({name:o,data:new Uint8Array(s.buffer.slice(4)),offset:e})}if(!a)throw"No IEND header found, malformed PNG file.";return r}encodeTextData(e,t){let r=normalize(e).substring(0,79),a=normalize(t);return new Uint8Array(stringToByteArray(r).concat([0]).concat(stringToByteArray(a)))}decodeTextData(e){let t=e.indexOf(0);return-1===t?{keyword:byteArrayToString(e),text:""}:{keyword:byteArrayToString(e.slice(0,t)),text:byteArrayToString(e.slice(t+1))}}addMetadatum(e,t){return this.addMetadata({key:t})}addMetadata(e){let t=Object.getOwnPropertyNames(e).reduce(((t,r)=>(t[r]=this.encodeTextData(r,`${e[r]}`),t)),{}),r=this.chunks,a=[],n=0;for(let e of r){if("IDAT"===e.name)break;if("tEXt"===e.name){let r=this.decodeTextData(e.data);for(let a in t)if(a===r.key){e.data=t[a],delete t[a];break}}a.push(e),n++}for(let e in t)a.push({name:"tEXt",data:t[e]});a=a.concat(r.slice(n)),this.buffer=PNG.fromChunks(this.name,a).buffer}get metadata(){let e={};for(let t of this.chunks)if("tEXt"===t.name){let r=this.decodeTextData(t.data);e[r.keyword]=r.text}return e}get base64(){return`data:image/png;base64,${btoa(byteArrayToString(this.data))}`}get blob(){return new Blob([this.data],{type:"image/png"})}get image(){let e=new Image;return e.src=this.base64,e}}export{PNG};
