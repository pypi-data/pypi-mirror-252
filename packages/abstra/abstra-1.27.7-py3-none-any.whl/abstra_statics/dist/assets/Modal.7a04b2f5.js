import{d as L,Y as A,al as M,K as R,cP as $,a9 as z,L as P,f as r,Q as w,bs as U,O as d,aT as B,cQ as Q,cR as W,v as Y,a3 as c,a0 as f,bM as N,cS as K,bo as V}from"./outputWidgets.c6b12f47.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},l=new Error().stack;l&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[l]="8b00759f-3747-421d-9339-b898e8a4fbe0",e._sentryDebugIdIdentifier="sentry-dbid-8b00759f-3747-421d-9339-b898e8a4fbe0")}catch{}})();var X=globalThis&&globalThis.__rest||function(e,l){var t={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&l.indexOf(n)<0&&(t[n]=e[n]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var a=0,n=Object.getOwnPropertySymbols(e);a<n.length;a++)l.indexOf(n[a])<0&&Object.prototype.propertyIsEnumerable.call(e,n[a])&&(t[n[a]]=e[n[a]]);return t};let g;const q=e=>{g={x:e.pageX,y:e.pageY},setTimeout(()=>g=null,100)};W()&&Y(document.documentElement,"click",q,!0);const G=()=>({prefixCls:String,visible:{type:Boolean,default:void 0},open:{type:Boolean,default:void 0},confirmLoading:{type:Boolean,default:void 0},title:c.any,closable:{type:Boolean,default:void 0},closeIcon:c.any,onOk:Function,onCancel:Function,"onUpdate:visible":Function,"onUpdate:open":Function,onChange:Function,afterClose:Function,centered:{type:Boolean,default:void 0},width:[String,Number],footer:c.any,okText:c.any,okType:String,cancelText:c.any,icon:c.any,maskClosable:{type:Boolean,default:void 0},forceRender:{type:Boolean,default:void 0},okButtonProps:f(),cancelButtonProps:f(),destroyOnClose:{type:Boolean,default:void 0},wrapClassName:String,maskTransitionName:String,transitionName:String,getContainer:{type:[String,Function,Boolean,Object],default:void 0},zIndex:Number,bodyStyle:f(),maskStyle:f(),mask:{type:Boolean,default:void 0},keyboard:{type:Boolean,default:void 0},wrapProps:Object,focusTriggerAfterClose:{type:Boolean,default:void 0},modalRender:Function,mousePosition:f()}),J=L({compatConfig:{MODE:3},name:"AModal",inheritAttrs:!1,props:A(G(),{width:520,confirmLoading:!1,okType:"primary"}),setup(e,l){let{emit:t,slots:n,attrs:a}=l;const[b]=M("Modal"),{prefixCls:i,rootPrefixCls:v,direction:O,getPopupContainer:p}=R("modal",e),[S,C]=$(i);z(e.visible===void 0);const T=o=>{t("update:visible",!1),t("update:open",!1),t("cancel",o),t("change",!1)},h=o=>{t("ok",o)},I=()=>{var o,s;const{okText:k=(o=n.okText)===null||o===void 0?void 0:o.call(n),okType:m,cancelText:u=(s=n.cancelText)===null||s===void 0?void 0:s.call(n),confirmLoading:y}=e;return r(V,null,[r(N,d({onClick:T},e.cancelButtonProps),{default:()=>[u||b.value.cancelText]}),r(N,d(d({},K(m)),{},{loading:y,onClick:h},e.okButtonProps),{default:()=>[k||b.value.okText]})])};return()=>{var o,s;const{prefixCls:k,visible:m,open:u,wrapClassName:y,centered:_,getContainer:F,closeIcon:j=(o=n.closeIcon)===null||o===void 0?void 0:o.call(n),focusTriggerAfterClose:D=!0}=e,x=X(e,["prefixCls","visible","open","wrapClassName","centered","getContainer","closeIcon","focusTriggerAfterClose"]),E=P(y,{[`${i.value}-centered`]:!!_,[`${i.value}-wrap-rtl`]:O.value==="rtl"});return S(r(Q,d(d(d({},x),a),{},{rootClassName:C.value,class:P(C.value,a.class),getContainer:F||(p==null?void 0:p.value),prefixCls:i.value,wrapClassName:E,visible:u!=null?u:m,onClose:T,focusTriggerAfterClose:D,transitionName:B(v.value,"zoom",e.transitionName),maskTransitionName:B(v.value,"fade",e.maskTransitionName),mousePosition:(s=x.mousePosition)!==null&&s!==void 0?s:g}),w(w({},n),{footer:n.footer||I,closeIcon:()=>r("span",{class:`${i.value}-close-x`},[j||r(U,{class:`${i.value}-close-icon`},null)])})))}}});export{J as M};
//# sourceMappingURL=Modal.7a04b2f5.js.map
