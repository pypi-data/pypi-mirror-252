var h=Object.defineProperty;var l=(r,t,e)=>t in r?h(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e;var o=(r,t,e)=>(l(r,typeof t!="symbol"?t+"":t,e),e);import{C as n}from"./router.56692652.js";import{A as m}from"./record.c46cf28f.js";import"./outputWidgets.3c34606b.js";(function(){try{var r=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(r._sentryDebugIds=r._sentryDebugIds||{},r._sentryDebugIds[t]="7777a94b-7ea2-498a-9a45-d4f3ff80fea4",r._sentryDebugIdIdentifier="sentry-dbid-7777a94b-7ea2-498a-9a45-d4f3ff80fea4")}catch{}})();class g extends Error{constructor(){super("Subdomain already in use")}}class y{constructor(){o(this,"urlPath","projects")}async create({name:t,organizationId:e}){return n.post(`organizations/${e}/${this.urlPath}`,{name:t})}async delete(t){await n.delete(`/${this.urlPath}/${t}`)}async duplicate(t){return await new Promise(e=>setTimeout(e,5e3)),n.post(`/${this.urlPath}/${t}/duplicate`,{})}async list(t){return n.get(`organizations/${t}/${this.urlPath}`)}async get(t){return n.get(`${this.urlPath}/${t}`)}async update(t,e){const s=await n.patch(`${this.urlPath}/${t}`,e);if("error"in s&&s.error==="subdomain-already-in-use")throw new g;if("error"in s)throw new Error("Unknown error");return s}async checkSubdomain(t,e){return n.get(`${this.urlPath}/${t}/check-subdomain/${e}`)}async getStatus(t){return n.get(`${this.urlPath}/${t}/deploy-status`)}}const a=new y;class i{constructor(t){o(this,"record");this.record=m.create(a,t)}static formatSubdomain(t){const s=t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,""),c=/[a-z0-9]+/g,u=s.matchAll(c);return Array.from(u).map(d=>d[0]).join("-")}static async list(t){return(await a.list(t)).map(s=>new i(s))}static async create(t){const e=await a.create(t);return new i(e)}static async get(t){const e=await a.get(t);return new i(e)}static async getStatus(t){return await a.getStatus(t)}async delete(){await a.delete(this.id)}async duplicate(){const t=await a.duplicate(this.id);return new i(t)}async save(){return this.record.save()}resetChanges(){this.record.resetChanges()}hasChanges(){return this.record.hasChanges()}get id(){return this.record.get("id")}get name(){return this.record.get("name")}set name(t){this.record.set("name",t)}get organizationId(){return this.record.get("organizationId")}get subdomain(){return this.record.get("subdomain")}set subdomain(t){this.record.set("subdomain",t)}get customDomain(){var t;return(t=this.record.get("customDomain"))!=null?t:null}async checkSubdomain(){return await a.checkSubdomain(this.id,this.subdomain)}getUrl(t=""){const e=t.startsWith("/")?t.slice(1):t;return`https://${this.subdomain}.abstra.app/${e}`}getCustomDomainUrl(t=""){const e=t.startsWith("/")?t.slice(1):t;return`https://${this.customDomain}/${e}`}static async rename(t,e){await a.update(t,{name:e})}}export{i as P};
//# sourceMappingURL=project.d605460b.js.map
