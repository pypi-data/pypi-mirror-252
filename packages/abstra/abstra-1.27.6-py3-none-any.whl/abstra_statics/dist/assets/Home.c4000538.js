import{d as y,eu as b,F as m,b as d,ev as l,e as c,u as g,ew as r,dp as u,ex as w,ey as h,ez as S,v,r as k,a as C,f,w as I,bq as x}from"./outputWidgets.ed48fa42.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},s=new Error().stack;s&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[s]="e4b41801-5684-464f-a945-e0c06ab8e696",e._sentryDebugIdIdentifier="sentry-dbid-e4b41801-5684-464f-a945-e0c06ab8e696")}catch{}})();const D=y({__name:"Modal",props:{containerStyle:{},headerStyle:{},contentStyle:{}},emits:["open","close"],setup(e,{expose:s,emit:o}){const i=b(),_=()=>{a.isOpened=!0,o("open")},n=()=>{a.isOpened=!1,o("close")};s({open:_,close:n});const a=m({isOpened:!1});return(t,p)=>(d(),l("div",{class:S(["background",a.isOpened&&"visible"]),onClick:n},[c("div",{class:"container",style:r(t.containerStyle),onClick:p[0]||(p[0]=h(()=>{},["stop"]))},[g(i).header?(d(),l("div",{key:0,class:"header",style:r(t.headerStyle)},[u(t.$slots,"header",{},void 0,!0)],4)):w("",!0),c("div",{class:"content",style:r(t.contentStyle)},[u(t.$slots,"content",{},void 0,!0)],4)],4)],2))}});const F=v(D,[["__scopeId","data-v-4d878495"]]),M=["src"],O=y({__name:"Home",setup(e){const s=m({onboardingForm:""}),o=k(null);return(i,_)=>{const n=C("router-view");return d(),l(x,null,[f(n,{class:"router"}),f(F,{ref_key:"modal",ref:o},{content:I(()=>[c("iframe",{class:"form",src:s.onboardingForm},null,8,M)]),_:1},512)],64)}}});const B=v(O,[["__scopeId","data-v-7e290e34"]]);export{B as default};
//# sourceMappingURL=Home.c4000538.js.map
