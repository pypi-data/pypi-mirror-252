import{F as I,r as R,g as P,R as q}from"./FormRunner.efecad1d.js";import{d as x,ez as B,ey as D,E,G as p,F as y,u as d,b as s,et as c,f as F,c as S,eC as C,eD as K,e as i,t as L}from"./outputWidgets.c6b12f47.js";import{u as h}from"./uuid.21c758d9.js";import{a as N}from"./asyncComputed.99914932.js";import{L as T}from"./CircularLoading.6d50bc26.js";import"./url.3f6b6909.js";import"./storage.2451d8d4.js";import"./pubsub.d22b40f3.js";import"./jwt-decode.esm.74bd4619.js";import"./index.231c6ebd.js";import"./icons.43aa926b.js";import"./PlayerNavbar.df3bb374.js";import"./ActionButton.f771a894.js";import"./WidgetsFrame.020d847d.js";import"./index.6f3ad0ef.js";import"./Card.9a2b3d3e.js";import"./TabPane.80ecc0b7.js";import"./hasIn.58982ae4.js";import"./index.0869e6f5.js";import"./Text.3372b6bf.js";import"./Link.ed78a9f2.js";import"./Title.53f8527b.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[t]="b701a233-2561-42f4-9d5c-943a8fc0c0f6",o._sentryDebugIdIdentifier="sentry-dbid-b701a233-2561-42f4-9d5c-943a8fc0c0f6")}catch{}})();const u=o=>(C("data-v-485e3719"),o=o(),K(),o),V={key:0,class:"loading"},z={key:1,class:"error"},A=u(()=>i("h1",null,"Oops! Something went wrong",-1)),G=u(()=>i("p",null,"An unknown error ocurred. Please try again or contact support.",-1)),O=[A,G],j={key:2,class:"form"},H={key:3,class:"error not-found",style:{height:"100vh"}},J=u(()=>i("h1",null,"Page not found",-1)),M=u(()=>i("p",null,"The page you requested could not be found.",-1)),Q=[J,M],U=x({__name:"Player",setup(o){const t=B(),l=D(),m=E({playerKey:h()});p(t,()=>w());function v(e,a){R("player",l,e,a)}const g=({path:e})=>{l.push({name:"player",query:t.query,params:{path:e.split("/")}})},_=async()=>{m.playerKey=h()};p([()=>t.path,()=>t.query],()=>_());const{loading:b,result:r,error:k,refetch:w}=N(()=>{var e;return P((e=t.path.slice(1))!=null?e:"")}),f=y(()=>n.value?q.create(n.value.id):null),n=y(()=>{var e,a;return(a=(e=r.value)==null?void 0:e.form)!=null?a:null});return p(r,()=>{var e;!r.value||r.value.form&&(document.title=(e=r.value.form.welcomeTitle)!=null?e:r.value.form.title)}),(e,a)=>d(b)?(s(),c("div",V,[F(T)])):d(k)?(s(),c("div",z,O)):n.value&&f.value?(s(),c("div",j,[(s(),S(I,{key:m.playerKey,class:"player",form:n.value,"is-preview":!1,params:d(t).query,broker:f.value,"enable-auto-focus":!0,onNavigate:g,onLogout:_,onRedirect:v},null,8,["form","params","broker"]))])):(s(),c("div",H,Q))}});const he=L(U,[["__scopeId","data-v-485e3719"]]);export{he as default};
//# sourceMappingURL=Player.3bb318f8.js.map
