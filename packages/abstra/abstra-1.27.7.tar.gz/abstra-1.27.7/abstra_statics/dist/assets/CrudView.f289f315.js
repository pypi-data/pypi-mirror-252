import{E}from"./icons.43aa926b.js";import{d as U,E as O,r as M,b as o,c as p,w as l,u as n,f as i,ao as c,eB as y,et as w,eA as $,bF as z,ab as R,bo as V,cz as j,ev as b,F as L,a as Y,dm as N,bM as q,cC as x,eu as G,bK as H,bf as J,bd as Q,e as W,I as F,cw as X,be as Z,cA as K,t as ee}from"./outputWidgets.c6b12f47.js";import{A as D,a as te}from"./Title.53f8527b.js";import{A as ae}from"./FormItem.2257bb18.js";import{F as le}from"./Form.4b59ec63.js";import{M as ne}from"./Modal.7a04b2f5.js";import{_ as se}from"./DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js";import{A as P,a as oe,r as ue}from"./router.e92a6711.js";import{i as re}from"./url.3f6b6909.js";import{A as S}from"./Text.3372b6bf.js";import{A as pe}from"./index.c1b6adb2.js";(function(){try{var m=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},v=new Error().stack;v&&(m._sentryDebugIds=m._sentryDebugIds||{},m._sentryDebugIds[v]="0e1af2a8-7c6f-4856-bfcb-a1696e83c7db",m._sentryDebugIdIdentifier="sentry-dbid-0e1af2a8-7c6f-4856-bfcb-a1696e83c7db")}catch{}})();const ie=U({__name:"CreationModal",props:{entityName:{},fields:{}},emits:["create"],setup(m,{expose:v,emit:k}){const _=m,B=`Create a new ${_.entityName}`,r=O({inputValue:{}}),g=M(!1),I=()=>g.value=!0,C=()=>g.value=!1,t=()=>{k("create",r.inputValue),C()},A=(d,a)=>{const e=d.target.value,s=_.fields.find(f=>f.key===a);s!=null&&s.format?r.inputValue[a]=s.format(e):r.inputValue[a]=e},h=(d,a)=>{const e=d.target.value,s=_.fields.find(f=>f.key===a);s!=null&&s.blur?r.inputValue[a]=s.blur(e):r.inputValue[a]=e};return v({open:I,close:C}),(d,a)=>(o(),p(n(ne),{open:g.value,title:B,onCancel:C,onOk:t},{default:l(()=>[i(n(D),null,{default:l(()=>[c(" You may edit the "+y(d.entityName)+" name afterwards at Settings. ",1)]),_:1}),i(n(le),{layout:"vertical"},{default:l(()=>[(o(!0),w(V,null,$(d.fields,e=>{var s;return o(),p(n(ae),{key:e.key,label:e.label,help:(s=e.hint)==null?void 0:s.call(e,r.inputValue[e.key])},{default:l(()=>{var f,T;return[!e.type||typeof e.type=="string"?(o(),p(n(z),{key:0,value:r.inputValue[e.key],"onUpdate:value":u=>r.inputValue[e.key]=u,placeholder:(f=e.placeholder)!=null?f:"",type:(T=e.type)!=null?T:"text",onInput:u=>A(u,e.key),onBlur:u=>h(u,e.key)},null,8,["value","onUpdate:value","placeholder","type","onInput","onBlur"])):Array.isArray(e.type)?(o(),p(n(R),{key:1,value:r.inputValue[e.key],"onUpdate:value":u=>r.inputValue[e.key]=u},{default:l(()=>[(o(!0),w(V,null,$(e.type,u=>(o(),p(n(j),{key:typeof u=="string"?u:u.value,value:typeof u=="string"?u:u.value},{default:l(()=>[c(y(typeof u=="string"?u:u.label),1)]),_:2},1032,["value"]))),128))]),_:2},1032,["value","onUpdate:value"])):b("",!0)]}),_:2},1032,["label","help"])}),128))]),_:1})]),_:1},8,["open"]))}}),ce={class:"action-item"},ye=U({__name:"CrudView",props:{table:{},loading:{type:Boolean},title:{},emptyTitle:{},entityName:{},description:{},createButtonText:{},docsPath:{},live:{type:Boolean},fields:{}},emits:["create"],setup(m,{emit:v}){const k=m,_=M(null),B=()=>{var t;k.fields?(t=_.value)==null||t.open():v("create",{})},r=M(!1);async function g(t,A){var h;if(!r.value){r.value=!0;try{"onClick"in t?await((h=t.onClick)==null?void 0:h.call(t,{key:A.key})):"link"in t&&(typeof t.link=="string"&&re(t.link)?open(t.link,"_blank"):ue.push(t.link))}finally{r.value=!1}}}async function I(t){v("create",t)}const C=L(()=>({"--columnCount":`${k.table.columns.length}`}));return(t,A)=>{const h=Y("router-link");return o(),w(V,null,[i(n(K),{direction:"vertical"},{default:l(()=>{var d;return[i(n(te),null,{default:l(()=>[c(y(t.title),1)]),_:1}),i(n(D),null,{default:l(()=>[c(y(t.description)+" ",1),N(t.$slots,"description",{},void 0,!0),t.docsPath?(o(),p(se,{key:0,path:t.docsPath},null,8,["path"])):b("",!0)]),_:3}),t.createButtonText?(o(),p(n(q),{key:0,type:"primary",onClick:B},{default:l(()=>[c(y(t.createButtonText),1)]),_:1})):b("",!0),N(t.$slots,"extra",{},void 0,!0),i(n(x),{style:G(C.value),"data-source":t.table.rows,loading:r.value||t.loading&&!t.live,columns:(d=t.table.columns)==null?void 0:d.map(({name:a,align:e},s,f)=>({title:a,key:s,align:e!=null?e:"center"}))},{emptyText:l(()=>[c(y(t.emptyTitle),1)]),headerCell:l(a=>[c(y(a.title),1)]),bodyCell:l(({column:{key:a},record:e})=>[e.cells[a].type==="slot"?N(t.$slots,e.cells[a].key,{key:0,payload:e.cells[a].payload},void 0,!0):(o(),p(n(X),{key:1,open:e.cells[a].hover?void 0:!1},{content:l(()=>[i(n(D),{style:{width:"300px",overflow:"auto","font-family":"monospace"},copyable:"",content:e.cells[a].hover},null,8,["content"])]),default:l(()=>[e.cells[a].type==="text"?(o(),p(n(S),{key:0,secondary:e.cells[a].secondary,code:e.cells[a].code},{default:l(()=>[c(y(e.cells[a].text),1)]),_:2},1032,["secondary","code"])):e.cells[a].type==="tag"?(o(),p(n(pe),{key:1,color:e.cells[a].tagColor},{default:l(()=>[c(y(e.cells[a].text),1)]),_:2},1032,["color"])):e.cells[a].type==="link"?(o(),p(h,{key:2,to:e.cells[a].to},{default:l(()=>[c(y(e.cells[a].text),1)]),_:2},1032,["to"])):e.cells[a].type==="actions"?(o(),p(n(H),{key:3},{overlay:l(()=>[i(n(J),{disabled:r.value},{default:l(()=>[(o(!0),w(V,null,$(e.cells[a].actions.filter(s=>!s.hide),(s,f)=>(o(),p(n(Q),{key:f,danger:s.dangerous,onClick:T=>g(s,e)},{default:l(()=>[W("div",ce,[s.icon?(o(),p(F,{key:0,path:s.icon},null,8,["path"])):b("",!0),i(n(S),null,{default:l(()=>[c(y(s.label),1)]),_:2},1024)])]),_:2},1032,["danger","onClick"]))),128))]),_:2},1032,["disabled"])]),default:l(()=>[i(F,{path:n(E),style:{cursor:"pointer"}},null,8,["path"])]),_:2},1024)):b("",!0)]),_:2},1032,["open"]))]),footer:l(()=>[t.live?(o(),p(n(oe),{key:0,justify:"end",gutter:10},{default:l(()=>[i(n(P),null,{default:l(()=>[i(n(Z),{size:"small"})]),_:1}),i(n(P),null,{default:l(()=>[i(n(S),null,{default:l(()=>[c(" auto updating ")]),_:1})]),_:1})]),_:1})):b("",!0)]),_:3},8,["style","data-source","loading","columns"])]}),_:3}),t.fields?(o(),p(ie,{key:0,ref_key:"modalRef",ref:_,fields:t.fields,"entity-name":t.entityName,onCreate:I},null,8,["fields","entity-name"])):b("",!0)],64)}}});const we=ee(ye,[["__scopeId","data-v-128e2f5b"]]);export{we as C};
//# sourceMappingURL=CrudView.f289f315.js.map
