class MutexLock{constructor(){this.holder=Promise.resolve()}acquire(){let e,s=new Promise((s=>{e=()=>s()})),o=this.holder.then((()=>e));return this.holder=s,o}}class MutexScopeLock{constructor(){this.scopes={}}acquire(e){return this.scopes.hasOwnProperty(e)||(this.scopes[e]=new MutexLock),this.scopes[e].acquire()}}export{MutexLock,MutexScopeLock};
