import{f as c,eG as I,d as M,eB as H,G as F,r as G,b as d,c as m,w as u,u as i,aq as y,dp as q,bO as w,e as _,eD as j,ev as A,ex as h,cM as J,ck as Q,cC as W,eE as X,eF as Y,v as Z}from"./outputWidgets.3c34606b.js";import{C as g}from"./router.56692652.js";import"./index.c3f2d302.js";import{a as K}from"./asyncComputed.8707f293.js";import{a as ee}from"./ant-design.8f4f3ad4.js";import{p as te}from"./popupNotifcation.11fa3053.js";import{D as ne,a as re}from"./DownloadOutlined.c29e0df6.js";import{a as ae,A as E}from"./Title.f4855332.js";import{C as oe}from"./Card.b797d31c.js";import"./FormItem.895a8678.js";import"./hasIn.01f4de81.js";import"./index.dd5bce3f.js";import"./index.cf4c23b9.js";import"./record.c46cf28f.js";import"./pubsub.28c1e0e3.js";import"./index.5cd5e321.js";import"./Modal.10b1f4fc.js";import"./Text.aa4a1cf1.js";import"./TabPane.71fe903b.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[e]="7fabb60e-1bca-4975-a8f8-9d58456b0e03",t._sentryDebugIdIdentifier="sentry-dbid-7fabb60e-1bca-4975-a8f8-9d58456b0e03")}catch{}})();var le={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M400 317.7h73.9V656c0 4.4 3.6 8 8 8h60c4.4 0 8-3.6 8-8V317.7H624c6.7 0 10.4-7.7 6.3-12.9L518.3 163a8 8 0 00-12.6 0l-112 141.7c-4.1 5.3-.4 13 6.3 13zM878 626h-60c-4.4 0-8 3.6-8 8v154H214V634c0-4.4-3.6-8-8-8h-60c-4.4 0-8 3.6-8 8v198c0 17.7 14.3 32 32 32h684c17.7 0 32-14.3 32-32V634c0-4.4-3.6-8-8-8z"}}]},name:"upload",theme:"outlined"};const ie=le;function x(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){se(t,o,n[o])})}return t}function se(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var C=function(e,n){var a=x({},e,n.attrs);return c(I,x({},a,{icon:ne}),null)};C.displayName="DeleteOutlined";C.inheritAttrs=!1;const ce=C;function N(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){ue(t,o,n[o])})}return t}function ue(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var D=function(e,n){var a=N({},e,n.attrs);return c(I,N({},a,{icon:re}),null)};D.displayName="DownloadOutlined";D.inheritAttrs=!1;const de=D;function B(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){pe(t,o,n[o])})}return t}function pe(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var P=function(e,n){var a=B({},e,n.attrs);return c(I,B({},a,{icon:ie}),null)};P.displayName="UploadOutlined";P.inheritAttrs=!1;const fe=P;class ${constructor(e){this.projectId=e}static fromProjectId(e){return new $(e)}async list(){return g.get(`projects/${this.projectId}/files`)}async upload(e){const n={"Content-Type":"multipart/form-data"};return g.post(`projects/${this.projectId}/files/upload?path=${encodeURIComponent(e.name)}`,e,n)}async download(e){return g.getBlob(`projects/${this.projectId}/files/download?path=${encodeURIComponent(e)}`)}async delete(e){return g.delete(`projects/${this.projectId}/files?path=${encodeURIComponent(e)}`)}async move(e,n){return g.patch(`projects/${this.projectId}/files?path=${encodeURIComponent(e)}&newPath=${encodeURIComponent(n)}`,{})}}const R=t=>(X("data-v-e7b42188"),t=t(),Y(),t),me=R(()=>_("br",null,null,-1)),ye=R(()=>_("a",{href:"https://docs.abstra.io/utils/#persistent-dir",target:"_blank"},"Learn more about it",-1)),be={key:0},he={key:0,class:"file-size"},ge=M({__name:"Files",setup(t){const n=H().params.projectId,a=$.fromProjectId(n),{loading:o,result:T,refetch:S}=K(()=>a.list());function k(r){var s,l;return{key:r.path,title:r.name,isLeaf:r.type==="file",file:r,children:r.type==="file"?[]:(l=(s=r.children)==null?void 0:s.map(k))!=null?l:[]}}const p=F(()=>{var r;return(r=T.value)==null?void 0:r.map(k)}),U=r=>{var s,l;return r.isLeaf?1:(l=(s=r.children)==null?void 0:s.reduce((f,b)=>f+U(b),0))!=null?l:0},v=F(()=>p.value?p==null?void 0:p.value.reduce((r,s)=>r+U(s),0):0),O=G(!1);function V(){const r=document.createElement("input");r.type="file",r.onchange=async()=>{var l;const s=(l=r.files)==null?void 0:l[0];if(!!s)try{O.value=!0,await a.upload(s),await S()}catch{te("Failed to upload file","File already exists")}finally{O.value=!1}},r.click()}async function z(r){if(!r)return;const s=await a.download(r.path),l=document.createElement("a");l.href=URL.createObjectURL(s),l.download=r.name,l.click()}async function L(r){!r||await ee("Are you sure you want to delete this file?")&&(await a.delete(r.path),await S())}return(r,s)=>(d(),m(i(W),{direction:"vertical"},{default:u(()=>[c(i(ae),null,{default:u(()=>[y("Files")]),_:1}),c(i(E),null,{default:u(()=>[y(" Here you can upload, download and delete files in your persistent dir."),me,y(" Files can be used in your scripts. "),ye,q(r.$slots,"description",{},void 0,!0)]),_:3}),c(i(w),{type:"primary",loading:O.value,onClick:V},{default:u(()=>[c(i(fe)),y(" Upload ")]),_:1},8,["loading"]),c(i(oe),null,{default:u(()=>[v.value>0?(d(),m(i(E),{key:0},{default:u(()=>[_("b",null,[y(j(v.value)+" file",1),v.value!==1?(d(),A("span",be,"s")):h("",!0)])]),_:1})):h("",!0),p.value&&p.value.length>0?(d(),m(i(J),{key:1,"tree-data":p.value,selectable:!1},{title:u(({title:l,isLeaf:f,file:b})=>[_("span",null,[y(j(l)+" ",1),f?(d(),A("span",he,"("+j(b.size)+")",1)):h("",!0)]),f?(d(),m(i(w),{key:0,type:"text",size:"small",style:{float:"inline-end"},onClick:()=>z(b)},{default:u(()=>[c(i(de))]),_:2},1032,["onClick"])):h("",!0),f?(d(),m(i(w),{key:1,type:"text",size:"small",style:{float:"inline-end"},onClick:()=>L(b)},{default:u(()=>[c(i(ce))]),_:2},1032,["onClick"])):h("",!0)]),_:1},8,["tree-data"])):(d(),m(i(Q),{key:2,description:i(o)?"Loading...":"No files"},null,8,["description"]))]),_:1})]),_:3}))}});const Re=Z(ge,[["__scopeId","data-v-e7b42188"]]);export{Re as default};
//# sourceMappingURL=Files.b3e375a2.js.map
