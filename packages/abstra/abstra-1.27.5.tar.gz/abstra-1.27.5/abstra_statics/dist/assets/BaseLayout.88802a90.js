import{d as c,b as t,ev as n,dp as s,e as o,ez as d,ex as r,v as i}from"./outputWidgets.1e038a78.js";(function(){try{var a=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(a._sentryDebugIds=a._sentryDebugIds||{},a._sentryDebugIds[e]="30dca349-acc2-42a1-8122-adc31d528e0d",a._sentryDebugIdIdentifier="sentry-dbid-30dca349-acc2-42a1-8122-adc31d528e0d")}catch{}})();const u={key:0,class:"canvas-container"},v={class:"canvas-content"},_={class:"canvas-absolute"},f={class:"canvas-footer"},y={key:1,class:"content-container"},p={class:"content-layout"},b={key:0,class:"content-footer"},m=c({__name:"BaseLayout",props:{fullCanvas:{type:Boolean}},setup(a){return(e,l)=>(t(),n("div",{class:d(["base-layout",{"full-canvas":e.fullCanvas}])},[s(e.$slots,"navbar",{},void 0,!0),o("div",{class:d(["middle-layout",{"full-canvas":e.fullCanvas}])},[s(e.$slots,"sidebar",{},void 0,!0),e.fullCanvas?(t(),n("div",u,[o("div",v,[o("div",_,[s(e.$slots,"content",{},void 0,!0)])]),o("div",f,[s(e.$slots,"footer",{},void 0,!0)])])):(t(),n("div",y,[o("div",p,[s(e.$slots,"content",{},void 0,!0)])]))],2),e.fullCanvas?r("",!0):(t(),n("div",b,[s(e.$slots,"footer",{},void 0,!0)]))],2))}});const B=i(m,[["__scopeId","data-v-f51eb3de"]]);export{B};
//# sourceMappingURL=BaseLayout.88802a90.js.map
