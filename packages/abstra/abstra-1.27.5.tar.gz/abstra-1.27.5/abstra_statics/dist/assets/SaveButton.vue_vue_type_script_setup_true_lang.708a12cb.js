import{a as D}from"./ant-design.0362b5ba.js";import{f as d,eG as V,d as S,eJ as B,H as E,o as L,K as A,b as C,ev as O,v as P,r as y,S as _,w as i,e as U,u,aq as h,bO as k,ez as z,eD as H,cy as I,bq as $,cw as j}from"./outputWidgets.1e038a78.js";import{A as M}from"./Link.8515b130.js";import"./index.91e038e7.js";import{a as N}from"./Text.44f96dcb.js";(function(){try{var a=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(a._sentryDebugIds=a._sentryDebugIds||{},a._sentryDebugIds[e]="e572b115-7201-425a-a9d8-0aefbfbe8b0d",a._sentryDebugIdIdentifier="sentry-dbid-e572b115-7201-425a-a9d8-0aefbfbe8b0d")}catch{}})();var q={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M893.3 293.3L730.7 130.7c-7.5-7.5-16.7-13-26.7-16V112H144c-17.7 0-32 14.3-32 32v736c0 17.7 14.3 32 32 32h736c17.7 0 32-14.3 32-32V338.5c0-17-6.7-33.2-18.7-45.2zM384 184h256v104H384V184zm456 656H184V184h136v136c0 17.7 14.3 32 32 32h320c17.7 0 32-14.3 32-32V205.8l136 136V840zM512 442c-79.5 0-144 64.5-144 144s64.5 144 144 144 144-64.5 144-144-64.5-144-144-144zm0 224c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z"}}]},name:"save",theme:"outlined"};const x=q;function w(a){for(var e=1;e<arguments.length;e++){var t=arguments[e]!=null?Object(arguments[e]):{},r=Object.keys(t);typeof Object.getOwnPropertySymbols=="function"&&(r=r.concat(Object.getOwnPropertySymbols(t).filter(function(s){return Object.getOwnPropertyDescriptor(t,s).enumerable}))),r.forEach(function(s){F(a,s,t[s])})}return a}function F(a,e,t){return e in a?Object.defineProperty(a,e,{value:t,enumerable:!0,configurable:!0,writable:!0}):a[e]=t,a}var p=function(e,t){var r=w({},e,t.attrs);return d(V,w({},r,{icon:x}),null)};p.displayName="SaveOutlined";p.inheritAttrs=!1;const T=p,Y={class:"unsaved-changes-handler"},g="You have unsaved changes. Are you sure you want to leave?",G=S({__name:"UnsavedChangesHandler",props:{hasChanges:{type:Boolean}},setup(a){const e=a,t=o=>(o=o||window.event,o&&(o.returnValue=g),g),r=()=>{window.addEventListener("beforeunload",t)};B(async(o,n,l)=>{if(!e.hasChanges)return l();await D(g)?l():l(!1)});const s=()=>window.removeEventListener("beforeunload",t),c=o=>o?r():s();return E(()=>e.hasChanges,c),L(()=>c(e.hasChanges)),A(s),(o,n)=>(C(),O("div",Y))}});const J=P(G,[["__scopeId","data-v-fa94acdd"]]),K={style:{padding:"0px 4px"}},ee=S({__name:"SaveButton",props:{model:{},neverShowPopover:{type:Boolean}},setup(a){var o;const e=a,t=y((o=_.get("dontShowUnsavedChanges"))!=null?o:!1),r=()=>{_.set("dontShowUnsavedChanges",!0),t.value=!0},s=y(!1);async function c(){s.value=!0;try{await e.model.save()}catch{j.error({message:"Error saving"})}finally{s.value=!1}}return addEventListener("keydown",n=>{(n.metaKey||n.ctrlKey)&&n.key==="s"&&(n.preventDefault(),c())}),addEventListener("beforeunload",n=>{e.model.hasChanges()&&(n.preventDefault(),n.returnValue="")}),(n,l)=>{var f;return C(),O($,null,[d(u(I),{placement:"left",visible:n.model.hasChanges()&&!t.value&&!n.neverShowPopover},{content:i(()=>[U("div",K,[d(u(N),null,{default:i(()=>[h("You have unsaved changes")]),_:1}),d(u(M),{onClick:r},{default:i(()=>[h("Don't show this again")]),_:1})])]),default:i(()=>{var m,b;return[d(u(k),{class:z(["save-button",{changes:(m=n.model)==null?void 0:m.hasChanges()}]),loading:s.value,disabled:!((b=n.model)!=null&&b.hasChanges()),onClick:l[0]||(l[0]=v=>c())},{icon:i(()=>[d(u(T))]),default:i(()=>{var v;return[h(H((v=n.model)!=null&&v.hasChanges()?"Save":"Saved")+" ",1)]}),_:1},8,["class","loading","disabled"])]}),_:1},8,["visible"]),d(J,{"has-changes":(f=n.model)==null?void 0:f.hasChanges()},null,8,["has-changes"])],64)}}});export{ee as _};
//# sourceMappingURL=SaveButton.vue_vue_type_script_setup_true_lang.708a12cb.js.map
