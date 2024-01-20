import{View}from"../view/base.mjs";import{ElementBuilder}from"../base/builder.mjs";import{isEmpty,kebabCase,set}from"../base/helpers.mjs";const E=new ElementBuilder;class FormView extends View{static tagName="form";static fieldSets={};static fieldSetConditions={};static autoSubmit=!1;static noSubmit=!1;static disableOnSubmit=!0;static autoComplete="off";static submitLabel="Submit";static showCancel=!1;static cancelLabel="Cancel";static collapseFieldSets=!1;constructor(t,e){super(t),this.values=e||{},this.errors={},this.submitCallbacks=[],this.cancelCallbacks=[],this.changeCallbacks=[],this.inputViews=[],this.disabled=!1,this.canceled=!1,this.dynamicFieldSets={}}async setValues(t,e=!0){await this.getNode(),this.disableAutoSubmit=!0,this.values=Object.getOwnPropertyNames(t).reduce(((e,s)=>(-1!==this.inputViews.map((t=>t.fieldName)).indexOf(s)&&(e[s]=t[s]),e)),{}),await Promise.all(this.inputViews.map((t=>t.setValue(this.values[t.fieldName],!1)))),await this.evaluateConditions();for(let t of this.inputViews)this.values[t.fieldName]=t.getValue();return this.disableAutoSubmit=!1,this.constructor.autoSubmit&&e&&this.submit(),this}async getInputView(t){return void 0===this.node&&await this.getNode(),this.inputViews.filter((e=>e.fieldName===t)).shift()}async addInput(t,e,s,i,a){let o=new e(this.config,s,a);if(void 0===this.dynamicFieldSets[t]&&(this.dynamicFieldSets[t]={}),this.dynamicFieldSets[t][s]={instance:o,label:i,class:e,config:a},o.onChange((()=>this.inputChanged(s,o))),this.inputViews.push(o),void 0!==this.node){let e=this.node.find(`fieldset.field-set-${kebabCase(t)}`),l=E.label().content(i).for(s),n=E.p().class("error").for(s);null===e&&(e=E.fieldset().content(E.legend().content(t)).class(`field-set-${kebabCase(t)}`),this.node.append(e)),o.fieldSet=e,isEmpty(this.errors[s])||(n.content(this.errors[s]),l.addClass("error")),o.required&&l.addClass("required"),isEmpty(o.tooltip)?isEmpty(a.tooltip)||l.data("tooltip",a.tooltip):l.data("tooltip",o.tooltip),isEmpty(i)&&l.hide(),this.values.hasOwnProperty(s)&&o.setValue(this.values[s],!1),o.onChange((()=>this.inputChanged(s,o))),this.inputViews.push(o);let r=E.div().class("field-container").content(n,await o.getNode(),l);r.addClass(kebabCase(o.constructor.name)).addClass(kebabCase(o.constructor.name)+"-"+kebabCase(s)),e.append(r)}return o}disable(){this.disabled=!0;for(let t of this.inputViews)t.disable();if(!this.constructor.autoSubmit&&!this.constructor.noSubmit&&void 0!==this.node)for(let t of this.node.findAll("input.submit"))t.disabled(!0)}enable(){this.disabled=!1;for(let t of this.inputViews)t.checkEnable();if(!this.constructor.autoSubmit&&!this.constructor.noSubmit&&void 0!==this.node)for(let t of this.node.findAll("input.submit"))t.disabled(!1)}clearError(){this.setError("")}setError(t){if(t instanceof XMLHttpRequest)try{t=JSON.parse(t.responseText)}catch(e){t=t.toString()}"string"!=typeof t&&(void 0!==t.errors&&(t=t.errors[0]),void 0!==t.detail?t=`${t.title}: ${t.detail}`:(console.error(t),t=t.toString())),this.errorMessage=t,void 0!==this.node&&(isEmpty(t)?this.node.find("p.error").empty().hide():this.node.find("p.error").content(t).show())}onChange(t){this.changeCallbacks.push(t)}onSubmit(t){this.submitCallbacks.push(t)}onCancel(t){this.cancelCallbacks.push(t)}async cancel(){for(let t of this.cancelCallbacks)await t();this.disabled=!0,this.canceled=!0}async submit(t=!0){if(this.disabled)throw"Form is disabled.";this.addClass("loading");let e=!1,s={};for(let t of this.inputViews){let i,a;void 0!==this.node&&(i=this.node.find(`p.error[data-for='${t.node.id()}']`),a=this.node.find(`label[data-for='${t.node.id()}']`));try{let e=!0;isEmpty(this.constructor.fieldSetConditions[t.fieldSet])||(isEmpty(s[t.fieldSet])&&(s[t.fieldSet]=this.constructor.fieldSetConditions[t.fieldSet](this.values)),e=s[t.fieldSet]),this.values[t.fieldName]=t.checkGetValue(e),void 0!==this.node&&(isEmpty(i)||i.empty(),isEmpty(a)||a.removeClass("error"))}catch(s){e=!0,this.errors[t.fieldName]=s,void 0!==this.node&&(isEmpty(i)||i.content(s),isEmpty(a)||a.addClass("error"))}}if(e)return this.setError("Error"),void this.removeClass("loading");if(this.constructor.disableOnSubmit&&!this.constructor.autoSubmit&&this.disable(),t){this.submitResults=[];for(let t of this.submitCallbacks)try{this.submitResults.push(await t(this.values))}catch(t){this.setError(t),this.enable();break}}this.removeClass("loading")}async evaluateConditions(){if(void 0!==this.node)for(let t in this.constructor.fieldSetConditions){let e=this.node.find(`fieldset.field-set-${kebabCase(t)}`);if(this.constructor.fieldSetConditions[t](this.values)){isEmpty(e)||e.show();for(let e of this.inputViews)e.required&&e.fieldSet==t&&(await e.getNode()).attr("required",!0)}else{isEmpty(e)||e.hide();for(let e of this.inputViews)e.required&&e.fieldSet==t&&(await e.getNode()).attr("required",!1)}}}async inputChanged(t,e){this.values[t]=e.getValue(),void 0!==this.node&&await this.evaluateConditions();for(let e of this.changeCallbacks)await e(t,this.values);this.constructor.autoSubmit&&!0!==this.disableAutoSubmit&&await this.submit()}async build(){let t=await super.build(),e=this.constructor.fieldSets,s=this.dynamicFieldSets,i=set(Object.getOwnPropertyNames(e).concat(Object.getOwnPropertyNames(s)));t.attr("autocomplete",this.constructor.autoComplete);for(let a of i){let i=E.legend().content(a),o=E.fieldset().content(i).class(`field-set-${kebabCase(a)}`),l=this.constructor.fieldSetConditions[a],n=!1,r=void 0!==s[a],d=r?s[a]:e[a];isEmpty(l)||(n=!l(this.values)),n&&o.hide(),(!0===this.constructor.collapseFieldSets||Array.isArray(this.constructor.collapseFieldSets)&&-1!==this.constructor.collapseFieldSets.indexOf(a))&&(o.addClass("collapsible collapsed"),i.on("click",(t=>{t.stopPropagation(),o.toggleClass("collapsed")})));for(let t in d){let e=E.div().class("field-container"),s=d[t].class,i=d[t].instance,l=d[t].label,c=d[t].config,h=e.elementId;if(isEmpty(s))throw`Field ${t} does not provide a class.`;isEmpty(c)&&(c={});let u,p=E.label().content(l).data("for",h),b=E.p().class("error").data("for",h);if(r?(u=i,e.addClass(kebabCase(i.constructor.name)).addClass(kebabCase(i.constructor.name)+"-"+kebabCase(t)),i.formParent=this):(e.addClass(kebabCase(s.name)).addClass(kebabCase(s.name)+"-"+kebabCase(t)),u=new s(this.config,t,c),u.onChange((()=>this.inputChanged(t,u))),this.inputViews.push(u),u.formParent=this),u.fieldSet=a,u.form=this,isEmpty(this.errors[t])||(b.content(this.errors[t]),p.addClass("error")),u.required&&p.addClass("required"),isEmpty(u.tooltip)||p.data("tooltip",u.tooltip),isEmpty(l)&&p.hide(),this.values.hasOwnProperty(t))u.setValue(this.values[t]);else{let e=u.getValue();e&&(this.values[t]=e)}p.on("click",(()=>u.labelClicked())),o.append(e.content(b,(await u.getNode()).id(h),p)),u.required&&n&&u.node.attr("required",!1)}t.append(o)}let a=E.p().class("error");if(isEmpty(this.errorMessage)?a.hide():a.content(this.errorMessage),t.append(a),!this.constructor.autoSubmit&&!this.constructor.noSubmit){let e=E.input().type("submit").class("submit").value(this.constructor.submitLabel),s=E.div().class("submit-buttons").content(e);if(t.append(s),this.constructor.showCancel){t.addClass("can-cancel");let e=E.input().type("button").class("submit cancel").value(this.constructor.cancelLabel);e.on("click",(()=>{e.hasClass("disabled")||this.cancel()})),s.append(e)}}return t.on("submit",(t=>{t.preventDefault(),t.stopPropagation(),this.submit()})),t}}export{FormView};
