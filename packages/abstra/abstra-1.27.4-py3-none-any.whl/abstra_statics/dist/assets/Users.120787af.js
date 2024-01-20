var B=Object.defineProperty;var V=(l,o,a)=>o in l?B(l,o,{enumerable:!0,configurable:!0,writable:!0,value:a}):l[o]=a;var _=(l,o,a)=>(V(l,typeof o!="symbol"?o+"":o,a),a);import{d as x,F as A,b as h,c as f,w as i,f as r,u as n,bO as b,aq as E,cC as D,bH as I,ad as L,eB as J,r as W,G,ev as Q,ex as H,bq as K}from"./outputWidgets.3c34606b.js";import{u as X,o as Y}from"./icons.e6ec075a.js";import{a as Z}from"./asyncComputed.8707f293.js";import{z as e}from"./index.cf4c23b9.js";import{A as O}from"./FormItem.895a8678.js";import{F as v}from"./Form.d74c49d4.js";import{A as T}from"./index.0cfaf7b7.js";import{C as S}from"./router.56692652.js";import"./index.c3f2d302.js";import{C as ee}from"./CrudView.7c2b0e6f.js";import{p as U}from"./popupNotifcation.11fa3053.js";import"./hasIn.01f4de81.js";import"./isNumeric.75337b1e.js";import"./index.dd5bce3f.js";import"./record.c46cf28f.js";import"./pubsub.28c1e0e3.js";import"./Title.f4855332.js";import"./Text.aa4a1cf1.js";import"./Modal.10b1f4fc.js";import"./DocsButton.vue_vue_type_script_setup_true_lang.36eacc0b.js";import"./url.425cd9cb.js";import"./index.507e77a0.js";(function(){try{var l=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},o=new Error().stack;o&&(l._sentryDebugIds=l._sentryDebugIds||{},l._sentryDebugIds[o]="2f26edc5-ef3a-4c70-9e1a-7b1b7a99bc53",l._sentryDebugIdIdentifier="sentry-dbid-2f26edc5-ef3a-4c70-9e1a-7b1b7a99bc53")}catch{}})();class oe{constructor(){_(this,"urlPath","users")}async create(o,a){return S.post(`projects/${o}/${this.urlPath}`,a)}async delete(o,a){await S.delete(`projects/${o}/${this.urlPath}/${a}`)}async list(o,{limit:a,offset:t}){const s={};a&&(s.limit=a.toString()),t&&(s.offset=t.toString());const m=new URLSearchParams(s);return S.get(`projects/${o}/${this.urlPath}?${m.toString()}`)}async update(o,a,t){return S.patch(`projects/${o}/${this.urlPath}/${a}`,t)}}const R=new oe;class y{constructor(o){this.dto=o}static async list(o,a,t){return(await R.list(o,{limit:a,offset:t})).map(m=>new y(m))}static async create(o,a){const t=await R.create(o,a);return new y(t)}async delete(){await R.delete(this.projectId,this.id)}async change(o){this.roles=o.roles,await R.update(this.projectId,this.id,o)}get id(){return this.dto.id}get email(){return this.dto.email}get projectId(){return this.dto.projectId}get roles(){return this.dto.roles}set roles(o){this.dto.roles=o}}const te=e.boolean().default(!0),ae=e.boolean().default(!0),ne=e.boolean().default(!1),se=e.boolean().default(!0),re=e.boolean().default(!1);e.object({PROJECT_LIVE:te.optional(),ALLOW_RELEASE:ae.optional(),CONNECTORS_CONSOLE:ne.optional(),CONNECTORS_EDITOR:se.optional(),DUPLICATE_PROJECTS:re.optional()});const ie=e.string().default("Free");e.object({plan:ie});const le=e.string(),me=e.string(),ce=e.string(),ue=e.string(),pe=e.null(),de=e.string(),Ce=e.union([pe,de]),ge=e.string().regex(new RegExp("^[0-9]+m$")),he=e.string().regex(new RegExp("^[0-9]+m$")),ye=e.string().regex(new RegExp("^[0-9]+Mi$")),Se=e.string().regex(new RegExp("^[0-9]+Mi$")),Re=e.string().regex(new RegExp("^[0-9]+$")),fe=e.string().regex(new RegExp("^[0-9]+$")),be=e.enum(["shared","clickbus"]),Ee=e.object({requestsCPU:ge.optional(),limitsCPU:he.optional(),requestsMemory:ye.optional(),limitsMemory:Se.optional(),minReplicas:Re.optional(),timeoutSeconds:fe.optional(),workerType:be.optional()});e.object({id:le,name:me,subdomain:ce,organizationId:ue,customDomain:Ce.optional(),deploymentResources:Ee.optional()});const Oe=e.string().regex(new RegExp("^[0-9]+m$")),we=e.string().regex(new RegExp("^[0-9]+m$")),Pe=e.string().regex(new RegExp("^[0-9]+Mi$")),xe=e.string().regex(new RegExp("^[0-9]+Mi$")),je=e.string().regex(new RegExp("^[0-9]+$")),_e=e.string().regex(new RegExp("^[0-9]+$")),Ue=e.enum(["shared","clickbus"]);e.object({requestsCPU:Oe.optional(),limitsCPU:we.optional(),requestsMemory:Pe.optional(),limitsMemory:xe.optional(),minReplicas:je.optional(),timeoutSeconds:_e.optional(),workerType:Ue.optional()});const Ae=e.string(),F=e.string(),De=["workflow_viewer"],Ie=e.literal("workflow_viewer"),j=e.array(Ie),Le=e.string(),ve=e.string(),Te=e.object({id:Ae,email:F,roles:j,projectId:Le,createdAt:ve}),N=e.string(),$=e.string(),Fe=e.boolean().default(!0),Ne=e.boolean().default(!0),$e=e.boolean().default(!1),ke=e.boolean().default(!0),Me=e.boolean().default(!1),k=e.object({PROJECT_LIVE:Fe,ALLOW_RELEASE:Ne,CONNECTORS_CONSOLE:$e,CONNECTORS_EDITOR:ke,DUPLICATE_PROJECTS:Me}),ze=e.string().default("Free"),M=e.object({plan:ze}),qe=e.string().regex(new RegExp("^[0-9]+m$")),Be=e.string().regex(new RegExp("^[0-9]+m$")),Ve=e.string().regex(new RegExp("^[0-9]+Mi$")),Je=e.string().regex(new RegExp("^[0-9]+Mi$")),We=e.string().regex(new RegExp("^[0-9]+$")),Ge=e.string().regex(new RegExp("^[0-9]+$")),Qe=e.enum(["shared","clickbus"]),He=e.object({requestsCPU:qe.optional(),limitsCPU:Be.optional(),requestsMemory:Ve.optional(),limitsMemory:Je.optional(),minReplicas:We.optional(),timeoutSeconds:Ge.optional(),workerType:Qe.optional()});e.object({id:N,name:$,featureFlags:k,billingMetadata:M,deploymentResources:He.optional()});const Ke=N,Xe=$,Ye=k,Ze=M;e.object({id:Ke,name:Xe,featureFlags:Ye,billingMetadata:Ze});const eo=j;e.object({roles:eo});const oo=e.number(),to=e.number();e.object({offset:oo.optional(),limit:to.optional()});const ao=Te;e.array(ao);const no=F,so=j;e.object({email:no,roles:so});const ro=e.boolean();e.object({shouldBeOnboarded:ro.optional()});const io=e.string(),lo=e.string(),mo=e.string(),co=e.string();e.object({name:io.optional(),companyName:lo.optional(),source:mo.optional(),authorEmail:co.optional()});const uo=x({__name:"NewUser",emits:["created","cancel"],setup(l,{emit:o}){const a=De.map(d=>({label:d,value:d})),t=A({email:"",roles:[]});function s(){o("cancel")}function m(){!t.email||o("created",t)}return(d,C)=>(h(),f(n(T),{open:"",title:"New user",width:720,"body-style":{paddingBottom:"80px"},"footer-style":{textAlign:"right"},onClose:s},{extra:i(()=>[r(n(D),null,{default:i(()=>[r(n(b),{onClick:s},{default:i(()=>[E("Cancel")]),_:1}),r(n(b),{type:"primary",onClick:m},{default:i(()=>[E("Submit")]),_:1})]),_:1})]),default:i(()=>[r(n(v),{model:t,layout:"vertical"},{default:i(()=>[r(n(O),{key:"email",label:"Email",required:!0},{default:i(()=>[r(n(I),{value:t.email,"onUpdate:value":C[0]||(C[0]=p=>t.email=p)},null,8,["value"])]),_:1}),r(n(O),{key:"role",label:"Role"},{default:i(()=>[r(n(L),{value:t.roles,"onUpdate:value":C[1]||(C[1]=p=>t.roles=p),mode:"multiple",options:n(a)},null,8,["value","options"])]),_:1})]),_:1},8,["model"])]),_:1}))}}),po=x({__name:"UpdateUser",props:{roles:{},email:{}},emits:["updated","cancel"],setup(l,{emit:o}){const a=l,t=[{value:"workflow_viewer",label:"Workflow viewer"}],s=A({roles:a.roles});function m(){o("cancel")}function d(){o("updated",s)}return(C,p)=>(h(),f(n(T),{open:"",title:"Update user",width:720,"body-style":{paddingBottom:"80px"},"footer-style":{textAlign:"right"},onClose:m},{extra:i(()=>[r(n(D),null,{default:i(()=>[r(n(b),{onClick:m},{default:i(()=>[E("Cancel")]),_:1}),r(n(b),{type:"primary",onClick:d},{default:i(()=>[E("Submit")]),_:1})]),_:1})]),default:i(()=>[r(n(v),{model:s,layout:"vertical"},{default:i(()=>[r(n(O),{key:"email",label:"Email"},{default:i(()=>[r(n(I),{value:a.email,disabled:""},null,8,["value"])]),_:1}),r(n(O),{key:"role",label:"Role"},{default:i(()=>[r(n(L),{value:s.roles,"onUpdate:value":p[0]||(p[0]=w=>s.roles=w),mode:"multiple",options:t},null,8,["value"])]),_:1})]),_:1},8,["model"])]),_:1}))}}),No=x({__name:"Users",setup(l){const a=J().params.projectId,t=W({type:"none"}),s=()=>{t.value.type="none"},m=()=>{t.value.type="new"},d=c=>{t.value={type:"edit",user:c}},C=async c=>{try{await y.create(a,c),s(),P()}catch(u){u instanceof Error&&U("Create Error",u.message)}},p=async c=>{try{if(t.value.type!=="edit")return;t.value.user.roles=c.roles,await t.value.user.change(c),s(),P()}catch(u){u instanceof Error&&U("Update Error",u.message)}},{loading:w,result:z,refetch:P}=Z(()=>y.list(a,100,0)),q=G(()=>{var c,u;return{columns:[{name:"Email"},{name:"Roles"},{name:"",align:"right"}],rows:(u=(c=z.value)==null?void 0:c.map(g=>({key:g.email,cells:[{type:"text",text:g.email},{type:"text",text:g.roles.join(", ")},{type:"actions",actions:[{icon:X,label:"Edit",onClick:()=>d(g)},{icon:Y,label:"Delete",onClick:async()=>{await g.delete(),P()}}]}]})))!=null?u:[]}});return(c,u)=>(h(),Q(K,null,[r(ee,{"entity-name":"users",loading:n(w),title:"Application users",description:"List all application users.","empty-title":"No users yet",table:q.value,"create-button-text":"Add users",onCreate:m},null,8,["loading","table"]),t.value.type==="new"?(h(),f(uo,{key:0,onCancel:s,onCreated:C})):t.value.type==="edit"?(h(),f(po,{key:1,email:t.value.user.email,roles:t.value.user.roles,onUpdated:p,onCancel:s},null,8,["email","roles"])):H("",!0)],64))}});export{No as default};
//# sourceMappingURL=Users.120787af.js.map
