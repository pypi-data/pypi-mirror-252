var g=Object.defineProperty;var f=(r,t,e)=>t in r?g(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e;var d=(r,t,e)=>(f(r,typeof t!="symbol"?t+"":t,e),e);import{A as p}from"./record.f0b2bfdd.js";import"./outputWidgets.c6b12f47.js";(function(){try{var r=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(r._sentryDebugIds=r._sentryDebugIds||{},r._sentryDebugIds[t]="8984ce6c-cd49-420e-98e8-8f0e4a5bdf89",r._sentryDebugIdIdentifier="sentry-dbid-8984ce6c-cd49-420e-98e8-8f0e4a5bdf89")}catch{}})();class b{async list(){return await(await fetch("/_editor/api/hooks")).json()}async create(t,e,s){return await(await fetch("/_editor/api/hooks",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title:t,file:e,position:s})})).json()}async get(t){return await(await fetch(`/_editor/api/hooks/${t}`)).json()}async update(t,e){return await(await fetch(`/_editor/api/hooks/${t}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json()}async delete(t,e){const s=e?"?remove_file=true":"",a=`/_editor/api/hooks/${t}`+s;await fetch(a,{method:"DELETE",headers:{"Content-Type":"application/json"}})}async test(t,e){const s=new URLSearchParams(e.query),a=await fetch(`/_editor/api/hooks/${t}/test?${s.toString()}`,{method:e.method,headers:{"Content-Type":"application/json",...e.headers},body:e.method==="GET"?void 0:e.body}),{status:h,headers:u,body:l,stderr:y,stdout:w}=await a.json();return{status:h,headers:u,body:l,stderr:y,stdout:w}}}const i=new b;class o{constructor(t){d(this,"record");this.record=p.create(i,t)}static async list(){return(await i.list()).map(e=>new o(e))}static async create(t,e,s){const a=await i.create(t,e,s);return new o(a)}static async get(t){const e=await i.get(t);return new o(e)}async delete(t){await i.delete(this.id,t)}async duplicate(){return this}async save(t){await this.record.save(t)}onUpdate(t){this.record.pubsub.subscribe("update",t)}hasChanges(t){return this.record.hasChanges(t)}getInitialState(t){return this.record.getInitialState(t)}updateInitialState(t,e){this.record.updateInitialState(t,e)}get id(){return this.record.get("id")}get path(){return this.record.get("path")}set path(t){this.record.set("path",t)}get title(){return this.record.get("title")}set title(t){this.record.set("title",t)}get codeContent(){return this.record.get("code_content")}set codeContent(t){this.record.set("code_content",t)}get file(){return this.record.get("file")}set file(t){this.record.set("file",t)}async test(t){return i.test(this.id,t)}get position(){const[t,e]=this.record.get("workflow_position");return{x:t,y:e,referential:"world"}}get isInitial(){return this.record.get("is_initial")}static from(t){return new o(t)}}class j{async list(){return await(await fetch("/_editor/api/jobs")).json()}async create(t,e,s){return await(await fetch("/_editor/api/jobs",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title:t,file:e,position:s})})).json()}async get(t){return await(await fetch(`/_editor/api/jobs/${t}`)).json()}async update(t,e){return await(await fetch(`/_editor/api/jobs/${t}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json()}async delete(t,e){const s=e?"?remove_file=true":"",a=`/_editor/api/jobs/${t}`+s;await fetch(a,{method:"DELETE",headers:{"Content-Type":"application/json"}})}async test(t){return(await fetch(`/_editor/api/jobs/${t}/test`,{method:"POST",headers:{"Content-Type":"application/json"}})).json()}}const n=new j;class c{constructor(t){d(this,"record");d(this,"isInitial",!0);this.record=p.create(n,t)}static async list(){return(await n.list()).map(e=>new c(e))}static async create(t,e,s){const a=await n.create(t,e,s);return new c(a)}static async get(t){const e=await n.get(t);return new c(e)}async delete(t){await n.delete(this.id,t)}async duplicate(){return this}async save(t){await this.record.save(t)}onUpdate(t){this.record.pubsub.subscribe("update",t)}hasChanges(t){return this.record.hasChanges(t)}getInitialState(t){return this.record.getInitialState(t)}updateInitialState(t,e){this.record.updateInitialState(t,e)}get schedule(){return this.record.get("schedule")}set schedule(t){this.record.set("schedule",t)}get title(){return this.record.get("title")}set title(t){this.record.set("title",t)}get codeContent(){return this.record.get("code_content")}set codeContent(t){this.record.set("code_content",t)}get file(){return this.record.get("file")}set file(t){this.record.set("file",t)}get id(){return this.record.get("id")}async test(){return n.test(this.id)}get position(){const[t,e]=this.record.get("workflow_position");return{x:t,y:e,referential:"world"}}static from(t){return new c(t)}}export{o as H,c as J};
//# sourceMappingURL=jobs.c3c8bf0c.js.map
