import{f as s,eE as I,d as M,ez as H,F,r as G,b as d,c as m,w as u,u as i,ao as y,dm as q,bM as w,e as _,eB as j,et as A,ev as h,cK as J,ci as Q,cA as W,eC as X,eD as Y,t as Z}from"./outputWidgets.c6b12f47.js";import{C as g}from"./router.e92a6711.js";import"./jwt-decode.esm.74bd4619.js";import"./index.bc2c15a2.js";import{a as K}from"./asyncComputed.99914932.js";import{a as ee}from"./ant-design.ee7cb87b.js";import{p as te}from"./popupNotifcation.7f5182e3.js";import{D as ne,a as re}from"./DownloadOutlined.c29e0df6.js";import{a as ae,A as E}from"./Title.53f8527b.js";import{C as oe}from"./Card.9a2b3d3e.js";import"./FormItem.2257bb18.js";import"./hasIn.58982ae4.js";import"./storage.2451d8d4.js";import"./index.cef27eee.js";import"./index.cf4c23b9.js";import"./record.f0b2bfdd.js";import"./pubsub.d22b40f3.js";import"./index.f7c8eeb4.js";import"./Modal.7a04b2f5.js";import"./Text.3372b6bf.js";import"./TabPane.80ecc0b7.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[e]="fc3aa6ee-c672-4dbe-ad9b-ac791988ba72",t._sentryDebugIdIdentifier="sentry-dbid-fc3aa6ee-c672-4dbe-ad9b-ac791988ba72")}catch{}})();var le={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M400 317.7h73.9V656c0 4.4 3.6 8 8 8h60c4.4 0 8-3.6 8-8V317.7H624c6.7 0 10.4-7.7 6.3-12.9L518.3 163a8 8 0 00-12.6 0l-112 141.7c-4.1 5.3-.4 13 6.3 13zM878 626h-60c-4.4 0-8 3.6-8 8v154H214V634c0-4.4-3.6-8-8-8h-60c-4.4 0-8 3.6-8 8v198c0 17.7 14.3 32 32 32h684c17.7 0 32-14.3 32-32V634c0-4.4-3.6-8-8-8z"}}]},name:"upload",theme:"outlined"};const ie=le;function N(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){ce(t,o,n[o])})}return t}function ce(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var C=function(e,n){var a=N({},e,n.attrs);return s(I,N({},a,{icon:ne}),null)};C.displayName="DeleteOutlined";C.inheritAttrs=!1;const se=C;function x(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){ue(t,o,n[o])})}return t}function ue(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var D=function(e,n){var a=x({},e,n.attrs);return s(I,x({},a,{icon:re}),null)};D.displayName="DownloadOutlined";D.inheritAttrs=!1;const de=D;function B(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?Object(arguments[e]):{},a=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(a=a.concat(Object.getOwnPropertySymbols(n).filter(function(o){return Object.getOwnPropertyDescriptor(n,o).enumerable}))),a.forEach(function(o){pe(t,o,n[o])})}return t}function pe(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}var P=function(e,n){var a=B({},e,n.attrs);return s(I,B({},a,{icon:ie}),null)};P.displayName="UploadOutlined";P.inheritAttrs=!1;const fe=P;class ${constructor(e){this.projectId=e}static fromProjectId(e){return new $(e)}async list(){return g.get(`projects/${this.projectId}/files`)}async upload(e){const n={"Content-Type":"multipart/form-data"};return g.post(`projects/${this.projectId}/files/upload?path=${encodeURIComponent(e.name)}`,e,n)}async download(e){return g.getBlob(`projects/${this.projectId}/files/download?path=${encodeURIComponent(e)}`)}async delete(e){return g.delete(`projects/${this.projectId}/files?path=${encodeURIComponent(e)}`)}async move(e,n){return g.patch(`projects/${this.projectId}/files?path=${encodeURIComponent(e)}&newPath=${encodeURIComponent(n)}`,{})}}const R=t=>(X("data-v-e7b42188"),t=t(),Y(),t),me=R(()=>_("br",null,null,-1)),ye=R(()=>_("a",{href:"https://docs.abstra.io/utils/#persistent-dir",target:"_blank"},"Learn more about it",-1)),be={key:0},he={key:0,class:"file-size"},ge=M({__name:"Files",setup(t){const n=H().params.projectId,a=$.fromProjectId(n),{loading:o,result:T,refetch:S}=K(()=>a.list());function k(r){var c,l;return{key:r.path,title:r.name,isLeaf:r.type==="file",file:r,children:r.type==="file"?[]:(l=(c=r.children)==null?void 0:c.map(k))!=null?l:[]}}const p=F(()=>{var r;return(r=T.value)==null?void 0:r.map(k)}),U=r=>{var c,l;return r.isLeaf?1:(l=(c=r.children)==null?void 0:c.reduce((f,b)=>f+U(b),0))!=null?l:0},v=F(()=>p.value?p==null?void 0:p.value.reduce((r,c)=>r+U(c),0):0),O=G(!1);function V(){const r=document.createElement("input");r.type="file",r.onchange=async()=>{var l;const c=(l=r.files)==null?void 0:l[0];if(!!c)try{O.value=!0,await a.upload(c),await S()}catch{te("Failed to upload file","File already exists")}finally{O.value=!1}},r.click()}async function z(r){if(!r)return;const c=await a.download(r.path),l=document.createElement("a");l.href=URL.createObjectURL(c),l.download=r.name,l.click()}async function L(r){!r||await ee("Are you sure you want to delete this file?")&&(await a.delete(r.path),await S())}return(r,c)=>(d(),m(i(W),{direction:"vertical"},{default:u(()=>[s(i(ae),null,{default:u(()=>[y("Files")]),_:1}),s(i(E),null,{default:u(()=>[y(" Here you can upload, download and delete files in your persistent dir."),me,y(" Files can be used in your scripts. "),ye,q(r.$slots,"description",{},void 0,!0)]),_:3}),s(i(w),{type:"primary",loading:O.value,onClick:V},{default:u(()=>[s(i(fe)),y(" Upload ")]),_:1},8,["loading"]),s(i(oe),null,{default:u(()=>[v.value>0?(d(),m(i(E),{key:0},{default:u(()=>[_("b",null,[y(j(v.value)+" file",1),v.value!==1?(d(),A("span",be,"s")):h("",!0)])]),_:1})):h("",!0),p.value&&p.value.length>0?(d(),m(i(J),{key:1,"tree-data":p.value,selectable:!1},{title:u(({title:l,isLeaf:f,file:b})=>[_("span",null,[y(j(l)+" ",1),f?(d(),A("span",he,"("+j(b.size)+")",1)):h("",!0)]),f?(d(),m(i(w),{key:0,type:"text",size:"small",style:{float:"inline-end"},onClick:()=>z(b)},{default:u(()=>[s(i(de))]),_:2},1032,["onClick"])):h("",!0),f?(d(),m(i(w),{key:1,type:"text",size:"small",style:{float:"inline-end"},onClick:()=>L(b)},{default:u(()=>[s(i(se))]),_:2},1032,["onClick"])):h("",!0)]),_:1},8,["tree-data"])):(d(),m(i(Q),{key:2,description:i(o)?"Loading...":"No files"},null,8,["description"]))]),_:1})]),_:3}))}});const Ve=Z(ge,[["__scopeId","data-v-e7b42188"]]);export{Ve as default};
//# sourceMappingURL=Files.25e33987.js.map
