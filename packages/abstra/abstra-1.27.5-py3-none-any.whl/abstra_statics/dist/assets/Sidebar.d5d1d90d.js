import{d as T,r as h,G as $,b as o,ev as g,dp as A,e as m,eD as w,ew as M,v as N,eA as V,eB as q,c,w as l,eC as k,u as i,cu as z,aq as y,bq as I,bf as E,ez as B,f as S,I as D,ex as x,bh as O}from"./outputWidgets.1e038a78.js";import{J as R}from"./icons.d1aae4c7.js";import{A as C}from"./index.912bd131.js";(function(){try{var s=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(s._sentryDebugIds=s._sentryDebugIds||{},s._sentryDebugIds[t]="ebf8ef71-7fcb-4282-b3a3-a16af13e2b09",s._sentryDebugIdIdentifier="sentry-dbid-ebf8ef71-7fcb-4282-b3a3-a16af13e2b09")}catch{}})();const G={class:"text"},F=T({__name:"Tooltip",props:{text:{type:String,required:!0},left:{type:Number},top:{type:Number},fixed:{type:Boolean,default:!1}},setup(s){const t=s,d=h(Date.now()),f=()=>{d.value=Date.now()},u=h(null),_=()=>{var r,e,v;const a=(r=u.value)==null?void 0:r.getBoundingClientRect();if(!a)return{};const{x:n,y:p}=a;return d.value,{position:"fixed",top:`${p+((e=t.top)!=null?e:0)}px`,left:`${n+((v=t.left)!=null?v:0)}px`}},b=$(()=>{var a;return t.fixed?_():{left:`${(a=t.left)!=null?a:-14}px`,...t.top?{top:`${t.top}px`}:{}}});return(a,n)=>(o(),g("div",{ref_key:"tooltipBox",ref:u,class:"tooltip-box",onMouseenter:f},[A(a.$slots,"default",{},void 0,!0),m("div",{class:"tooltip",style:M(b.value)},[m("span",G,w(s.text),1)],4)],544))}});const J=N(F,[["__scopeId","data-v-c3a6ca5e"]]),L={style:{"margin-right":"5px"}},P=T({__name:"Sidebar",props:{sections:{}},setup(s){var a;const t=s,d=V(),f=q(),u=h((a=f.name)!=null?a:"forms"),_=$(()=>t.sections.map(n=>({...n,items:n.items.filter(p=>!p.unavailable)}))),b=n=>{n.unavailable||(d.push(n.path),u.value=n.path)};return(n,p)=>(o(),c(i(O),null,{default:l(()=>[(o(!0),g(I,null,k(_.value,r=>(o(),c(i(z),{key:r.name},{title:l(()=>[y(w(r.name),1)]),default:l(()=>[(o(!0),g(I,null,k(r.items,e=>(o(),c(i(E),{key:e.name,role:"button",class:B({"menu-item":!0,active:u.value===e.path,disabled:e.unavailable||r.cloud}),tabindex:"0",onClick:v=>b(e)},{icon:l(()=>[S(D,{class:B({disabled:e.unavailable,active:u.value===e.path}),path:e.icon,width:"20",height:"20"},null,8,["class","path"])]),default:l(()=>[m("span",L,w(e.name),1),e.unavailable?(o(),c(i(C),{key:0},{default:l(()=>[y("SOON")]),_:1})):x("",!0),e.beta?(o(),c(i(C),{key:1},{default:l(()=>[y("BETA")]),_:1})):x("",!0),e.warning?(o(),c(J,{key:2,text:e.warning,fixed:!0,top:18,left:18},{default:l(()=>[S(D,{path:i(R),fill:"#D35249",width:"20",height:"20"},null,8,["path"])]),_:2},1032,["text"])):x("",!0)]),_:2},1032,["class","onClick"]))),128))]),_:2},1024))),128))]),_:1}))}});const Q=N(P,[["__scopeId","data-v-38667610"]]);export{Q as S};
//# sourceMappingURL=Sidebar.d5d1d90d.js.map
