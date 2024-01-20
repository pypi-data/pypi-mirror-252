import{F as I,r as R,g as B,R as P}from"./FormRunner.fed0fdae.js";import{d as q,eB as x,eA as F,F as D,H as d,G as y,u as p,b as s,ev as u,f as E,c as S,eE as K,eF as L,e as i,v as N}from"./outputWidgets.1e038a78.js";import{u as h}from"./uuid.85c49363.js";import{a as A}from"./asyncComputed.499f8882.js";import{L as C}from"./CircularLoading.e568b47f.js";import"./url.a1386e61.js";import"./index.c49825a0.js";import"./pubsub.3f35ef3d.js";import"./icons.d1aae4c7.js";import"./PlayerNavbar.6e2cc034.js";import"./ActionButton.3307e2f3.js";import"./WidgetsFrame.d39e04d2.js";import"./index.a37ecea0.js";import"./Card.7ef17651.js";import"./TabPane.bae67f3c.js";import"./hasIn.3b666b8d.js";import"./index.91e038e7.js";import"./Text.44f96dcb.js";import"./Link.8515b130.js";import"./Title.0b1584ed.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[t]="aef47045-535a-48d8-ab5d-31a7370c6025",o._sentryDebugIdIdentifier="sentry-dbid-aef47045-535a-48d8-ab5d-31a7370c6025")}catch{}})();const c=o=>(K("data-v-485e3719"),o=o(),L(),o),T={key:0,class:"loading"},V={key:1,class:"error"},G=c(()=>i("h1",null,"Oops! Something went wrong",-1)),H=c(()=>i("p",null,"An unknown error ocurred. Please try again or contact support.",-1)),O=[G,H],j={key:2,class:"form"},z={key:3,class:"error not-found",style:{height:"100vh"}},J=c(()=>i("h1",null,"Page not found",-1)),M=c(()=>i("p",null,"The page you requested could not be found.",-1)),Q=[J,M],U=q({__name:"Player",setup(o){const t=x(),l=F(),m=D({playerKey:h()});d(t,()=>w());function v(e,a){R("player",l,e,a)}const g=({path:e})=>{l.push({name:"player",query:t.query,params:{path:e.split("/")}})},_=async()=>{m.playerKey=h()};d([()=>t.path,()=>t.query],()=>_());const{loading:b,result:r,error:k,refetch:w}=A(()=>{var e;return B((e=t.path.slice(1))!=null?e:"")}),f=y(()=>n.value?P.create(n.value.id):null),n=y(()=>{var e,a;return(a=(e=r.value)==null?void 0:e.form)!=null?a:null});return d(r,()=>{var e;!r.value||r.value.form&&(document.title=(e=r.value.form.welcomeTitle)!=null?e:r.value.form.title)}),(e,a)=>p(b)?(s(),u("div",T,[E(C)])):p(k)?(s(),u("div",V,O)):n.value&&f.value?(s(),u("div",j,[(s(),S(I,{key:m.playerKey,class:"player",form:n.value,"is-preview":!1,params:p(t).query,broker:f.value,"enable-auto-focus":!0,onNavigate:g,onLogout:_,onRedirect:v},null,8,["form","params","broker"]))])):(s(),u("div",z,Q))}});const fe=N(U,[["__scopeId","data-v-485e3719"]]);export{fe as default};
//# sourceMappingURL=Player.00aa3ac4.js.map
