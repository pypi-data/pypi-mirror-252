import{a$ as Q,f as c,aY as tt,a5 as Y,aw as z,ay as C,a2 as vt,U as h,ax as bt,d as R,bE as ht,bq as et,Q as b,W as mt,X as yt,r as E,z as $t,B as Bt,dc as St,bs as Z,dd as xt,Z as ot,$ as L,L as V,G as I,N as H,br as wt,ak as Ot,H as nt,a0 as at,b_ as rt,c0 as it,bj as lt,c1 as st,bu as Ct,bx as Tt,c9 as It,F as Et,o as Pt,a3 as A,bC as zt,de as Rt,a7 as Ft,a6 as Mt}from"./outputWidgets.1e038a78.js";import{B as Dt}from"./index.fb5ebdb4.js";import{T as P,A as _}from"./Timeline.7229683c.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},n=new Error().stack;n&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[n]="90ac7a23-2946-4e05-b120-fc99c841c012",t._sentryDebugIdIdentifier="sentry-dbid-90ac7a23-2946-4e05-b120-fc99c841c012")}catch{}})();function At(t){let n;const e=a=>()=>{n=null,t(...a)},o=function(){if(n==null){for(var a=arguments.length,r=new Array(a),d=0;d<a;d++)r[d]=arguments[d];n=Q(e(r))}};return o.cancel=()=>{Q.cancel(n),n=null},o}var Ht={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M854.6 288.6L639.4 73.4c-6-6-14.1-9.4-22.6-9.4H192c-17.7 0-32 14.3-32 32v832c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V311.3c0-8.5-3.4-16.7-9.4-22.7zM790.2 326H602V137.8L790.2 326zm1.8 562H232V136h302v216a42 42 0 0042 42h216v494zM504 618H320c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h184c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8zM312 490v48c0 4.4 3.6 8 8 8h384c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8H320c-4.4 0-8 3.6-8 8z"}}]},name:"file-text",theme:"outlined"};const _t=Ht;function J(t){for(var n=1;n<arguments.length;n++){var e=arguments[n]!=null?Object(arguments[n]):{},o=Object.keys(e);typeof Object.getOwnPropertySymbols=="function"&&(o=o.concat(Object.getOwnPropertySymbols(e).filter(function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),o.forEach(function(a){jt(t,a,e[a])})}return t}function jt(t,n,e){return n in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}var q=function(n,e){var o=J({},n,e.attrs);return c(tt,J({},o,{icon:_t}),null)};q.displayName="FileTextOutlined";q.inheritAttrs=!1;const ct=q,N=()=>({prefixCls:String,description:Y.any,type:z("default"),shape:z("circle"),tooltip:Y.any,href:String,target:C(),badge:vt(),onClick:C()}),Gt=()=>({prefixCls:z()}),Lt=()=>h(h({},N()),{trigger:z(),open:bt(),onOpenChange:C(),"onUpdate:open":C()}),Vt=()=>h(h({},N()),{prefixCls:String,duration:Number,target:C(),visibilityHeight:Number,onClick:C()}),qt=R({compatConfig:{MODE:3},name:"AFloatButtonContent",inheritAttrs:!1,props:Gt(),setup(t,n){let{attrs:e,slots:o}=n;return()=>{var a;const{prefixCls:r}=t,d=ht((a=o.description)===null||a===void 0?void 0:a.call(o));return c("div",b(b({},e),{},{class:[e.class,`${r}-content`]}),[o.icon||d.length?c(et,null,[o.icon&&c("div",{class:`${r}-icon`},[o.icon()]),d.length?c("div",{class:`${r}-description`},[d]):null]):c("div",{class:`${r}-icon`},[c(ct,null,null)])])}}}),Nt=qt,dt=Symbol("floatButtonGroupContext"),Xt=t=>(mt(dt,t),t),ut=()=>yt(dt,{shape:E()}),Ut=t=>t===0?0:t-Math.sqrt(Math.pow(t,2)/2),K=Ut,Wt=t=>{const{componentCls:n,floatButtonSize:e,motionDurationSlow:o,motionEaseInOutCirc:a}=t,r=`${n}-group`,d=new Z("antFloatButtonMoveDownIn",{"0%":{transform:`translate3d(0, ${e}px, 0)`,transformOrigin:"0 0",opacity:0},"100%":{transform:"translate3d(0, 0, 0)",transformOrigin:"0 0",opacity:1}}),p=new Z("antFloatButtonMoveDownOut",{"0%":{transform:"translate3d(0, 0, 0)",transformOrigin:"0 0",opacity:1},"100%":{transform:`translate3d(0, ${e}px, 0)`,transformOrigin:"0 0",opacity:0}});return[{[`${r}-wrap`]:h({},xt(`${r}-wrap`,d,p,o,!0))},{[`${r}-wrap`]:{[`
          &${r}-wrap-enter,
          &${r}-wrap-appear
        `]:{opacity:0,animationTimingFunction:a},[`&${r}-wrap-leave`]:{animationTimingFunction:a}}}]},Qt=t=>{const{antCls:n,componentCls:e,floatButtonSize:o,margin:a,borderRadiusLG:r,borderRadiusSM:d,badgeOffset:p,floatButtonBodyPadding:u}=t,s=`${e}-group`;return{[s]:h(h({},ot(t)),{zIndex:99,display:"block",border:"none",position:"fixed",width:o,height:"auto",boxShadow:"none",minHeight:o,insetInlineEnd:t.floatButtonInsetInlineEnd,insetBlockEnd:t.floatButtonInsetBlockEnd,borderRadius:r,[`${s}-wrap`]:{zIndex:-1,display:"block",position:"relative",marginBottom:a},[`&${s}-rtl`]:{direction:"rtl"},[e]:{position:"static"}}),[`${s}-circle`]:{[`${e}-circle:not(:last-child)`]:{marginBottom:t.margin,[`${e}-body`]:{width:o,height:o,borderRadius:"50%"}}},[`${s}-square`]:{[`${e}-square`]:{borderRadius:0,padding:0,"&:first-child":{borderStartStartRadius:r,borderStartEndRadius:r},"&:last-child":{borderEndStartRadius:r,borderEndEndRadius:r},"&:not(:last-child)":{borderBottom:`${t.lineWidth}px ${t.lineType} ${t.colorSplit}`},[`${n}-badge`]:{[`${n}-badge-count`]:{top:-(u+p),insetInlineEnd:-(u+p)}}},[`${s}-wrap`]:{display:"block",borderRadius:r,boxShadow:t.boxShadowSecondary,[`${e}-square`]:{boxShadow:"none",marginTop:0,borderRadius:0,padding:u,"&:first-child":{borderStartStartRadius:r,borderStartEndRadius:r},"&:last-child":{borderEndStartRadius:r,borderEndEndRadius:r},"&:not(:last-child)":{borderBottom:`${t.lineWidth}px ${t.lineType} ${t.colorSplit}`},[`${e}-body`]:{width:t.floatButtonBodySize,height:t.floatButtonBodySize}}}},[`${s}-circle-shadow`]:{boxShadow:"none"},[`${s}-square-shadow`]:{boxShadow:t.boxShadowSecondary,[`${e}-square`]:{boxShadow:"none",padding:u,[`${e}-body`]:{width:t.floatButtonBodySize,height:t.floatButtonBodySize,borderRadius:d}}}}},Yt=t=>{const{antCls:n,componentCls:e,floatButtonBodyPadding:o,floatButtonIconSize:a,floatButtonSize:r,borderRadiusLG:d,badgeOffset:p,dotOffsetInSquare:u,dotOffsetInCircle:s}=t;return{[e]:h(h({},ot(t)),{border:"none",position:"fixed",cursor:"pointer",zIndex:99,display:"block",justifyContent:"center",alignItems:"center",width:r,height:r,insetInlineEnd:t.floatButtonInsetInlineEnd,insetBlockEnd:t.floatButtonInsetBlockEnd,boxShadow:t.boxShadowSecondary,"&-pure":{position:"relative",inset:"auto"},"&:empty":{display:"none"},[`${n}-badge`]:{width:"100%",height:"100%",[`${n}-badge-count`]:{transform:"translate(0, 0)",transformOrigin:"center",top:-p,insetInlineEnd:-p}},[`${e}-body`]:{width:"100%",height:"100%",display:"flex",justifyContent:"center",alignItems:"center",transition:`all ${t.motionDurationMid}`,[`${e}-content`]:{overflow:"hidden",textAlign:"center",minHeight:r,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center",padding:`${o/2}px ${o}px`,[`${e}-icon`]:{textAlign:"center",margin:"auto",width:a,fontSize:a,lineHeight:1}}}}),[`${e}-rtl`]:{direction:"rtl"},[`${e}-circle`]:{height:r,borderRadius:"50%",[`${n}-badge`]:{[`${n}-badge-dot`]:{top:s,insetInlineEnd:s}},[`${e}-body`]:{borderRadius:"50%"}},[`${e}-square`]:{height:"auto",minHeight:r,borderRadius:d,[`${n}-badge`]:{[`${n}-badge-dot`]:{top:u,insetInlineEnd:u}},[`${e}-body`]:{height:"auto",borderRadius:d}},[`${e}-default`]:{backgroundColor:t.floatButtonBackgroundColor,transition:`background-color ${t.motionDurationMid}`,[`${e}-body`]:{backgroundColor:t.floatButtonBackgroundColor,transition:`background-color ${t.motionDurationMid}`,"&:hover":{backgroundColor:t.colorFillContent},[`${e}-content`]:{[`${e}-icon`]:{color:t.colorText},[`${e}-description`]:{display:"flex",alignItems:"center",lineHeight:`${t.fontSizeLG}px`,color:t.colorText,fontSize:t.fontSizeSM}}}},[`${e}-primary`]:{backgroundColor:t.colorPrimary,[`${e}-body`]:{backgroundColor:t.colorPrimary,transition:`background-color ${t.motionDurationMid}`,"&:hover":{backgroundColor:t.colorPrimaryHover},[`${e}-content`]:{[`${e}-icon`]:{color:t.colorTextLightSolid},[`${e}-description`]:{display:"flex",alignItems:"center",lineHeight:`${t.fontSizeLG}px`,color:t.colorTextLightSolid,fontSize:t.fontSizeSM}}}}}},X=$t("FloatButton",t=>{const{colorTextLightSolid:n,colorBgElevated:e,controlHeightLG:o,marginXXL:a,marginLG:r,fontSize:d,fontSizeIcon:p,controlItemBgHover:u,paddingXXS:s,borderRadiusLG:g}=t,v=Bt(t,{floatButtonBackgroundColor:e,floatButtonColor:n,floatButtonHoverBackgroundColor:u,floatButtonFontSize:d,floatButtonIconSize:p*1.5,floatButtonSize:o,floatButtonInsetBlockEnd:a,floatButtonInsetInlineEnd:r,floatButtonBodySize:o-s*2,floatButtonBodyPadding:s,badgeOffset:s*1.5,dotOffsetInCircle:K(o/2),dotOffsetInSquare:K(g)});return[Qt(v),Yt(v),St(t),Wt(v)]});var Zt=globalThis&&globalThis.__rest||function(t,n){var e={};for(var o in t)Object.prototype.hasOwnProperty.call(t,o)&&n.indexOf(o)<0&&(e[o]=t[o]);if(t!=null&&typeof Object.getOwnPropertySymbols=="function")for(var a=0,o=Object.getOwnPropertySymbols(t);a<o.length;a++)n.indexOf(o[a])<0&&Object.prototype.propertyIsEnumerable.call(t,o[a])&&(e[o[a]]=t[o[a]]);return e};const U="float-btn",Jt=R({compatConfig:{MODE:3},name:"AFloatButton",inheritAttrs:!1,props:L(N(),{type:"default",shape:"circle"}),setup(t,n){let{attrs:e,slots:o}=n;const{prefixCls:a,direction:r}=V(U,t),[d,p]=X(a),{shape:u}=ut(),s=E(null),g=I(()=>(u==null?void 0:u.value)||t.shape);return()=>{var v;const{prefixCls:B,type:S="default",shape:O="circle",description:x=(v=o.description)===null||v===void 0?void 0:v.call(o),tooltip:f,badge:i={}}=t,l=Zt(t,["prefixCls","type","shape","description","tooltip","badge"]),m=H(a.value,`${a.value}-${S}`,`${a.value}-${g.value}`,{[`${a.value}-rtl`]:r.value==="rtl"},e.class,p.value),y=c(wt,{placement:"left"},{title:o.tooltip||f?()=>o.tooltip&&o.tooltip()||f:void 0,default:()=>c(Dt,i,{default:()=>[c("div",{class:`${a.value}-body`},[c(Nt,{prefixCls:a.value},{icon:o.icon,description:()=>x})])]})});return d(t.href?c("a",b(b(b({ref:s},e),l),{},{class:m}),[y]):c("button",b(b(b({ref:s},e),l),{},{class:m,type:"button"}),[y]))}}}),w=Jt,Kt=R({compatConfig:{MODE:3},name:"AFloatButtonGroup",inheritAttrs:!1,props:L(Lt(),{type:"default",shape:"circle"}),setup(t,n){let{attrs:e,slots:o,emit:a}=n;const{prefixCls:r,direction:d}=V(U,t),[p,u]=X(r),[s,g]=Ot(!1,{value:I(()=>t.open)}),v=E(null),B=E(null);Xt({shape:I(()=>t.shape)});const S={onMouseenter(){var i;g(!0),a("update:open",!0),(i=t.onOpenChange)===null||i===void 0||i.call(t,!0)},onMouseleave(){var i;g(!1),a("update:open",!1),(i=t.onOpenChange)===null||i===void 0||i.call(t,!1)}},O=I(()=>t.trigger==="hover"?S:{}),x=()=>{var i;const l=!s.value;a("update:open",l),(i=t.onOpenChange)===null||i===void 0||i.call(t,l),g(l)},f=i=>{var l,m,y;if(!((l=v.value)===null||l===void 0)&&l.contains(i.target)){!((m=Tt(B.value))===null||m===void 0)&&m.contains(i.target)&&x();return}g(!1),a("update:open",!1),(y=t.onOpenChange)===null||y===void 0||y.call(t,!1)};return nt(I(()=>t.trigger),i=>{!It()||(document.removeEventListener("click",f),i==="click"&&document.addEventListener("click",f))},{immediate:!0}),at(()=>{document.removeEventListener("click",f)}),()=>{var i;const{shape:l="circle",type:m="default",tooltip:y,description:F,trigger:T}=t,$=`${r.value}-group`,ft=H($,u.value,e.class,{[`${$}-rtl`]:d.value==="rtl",[`${$}-${l}`]:l,[`${$}-${l}-shadow`]:!T}),pt=H(u.value,`${$}-wrap`),gt=rt(`${$}-wrap`);return p(c("div",b(b({ref:v},e),{},{class:ft},O.value),[T&&["click","hover"].includes(T)?c(et,null,[c(it,gt,{default:()=>[lt(c("div",{class:pt},[o.default&&o.default()]),[[st,s.value]])]}),c(w,{ref:B,type:m,shape:l,tooltip:y,description:F},{icon:()=>{var M,D;return s.value?((M=o.closeIcon)===null||M===void 0?void 0:M.call(o))||c(Ct,null,null):((D=o.icon)===null||D===void 0?void 0:D.call(o))||c(ct,null,null)},tooltip:o.tooltip,description:o.description})]):(i=o.default)===null||i===void 0?void 0:i.call(o)]))}}}),j=Kt;var kt={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M859.9 168H164.1c-4.5 0-8.1 3.6-8.1 8v60c0 4.4 3.6 8 8.1 8h695.8c4.5 0 8.1-3.6 8.1-8v-60c0-4.4-3.6-8-8.1-8zM518.3 355a8 8 0 00-12.6 0l-112 141.7a7.98 7.98 0 006.3 12.9h73.9V848c0 4.4 3.6 8 8 8h60c4.4 0 8-3.6 8-8V509.7H624c6.7 0 10.4-7.7 6.3-12.9L518.3 355z"}}]},name:"vertical-align-top",theme:"outlined"};const te=kt;function k(t){for(var n=1;n<arguments.length;n++){var e=arguments[n]!=null?Object(arguments[n]):{},o=Object.keys(e);typeof Object.getOwnPropertySymbols=="function"&&(o=o.concat(Object.getOwnPropertySymbols(e).filter(function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),o.forEach(function(a){ee(t,a,e[a])})}return t}function ee(t,n,e){return n in t?Object.defineProperty(t,n,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[n]=e,t}var W=function(n,e){var o=k({},n,e.attrs);return c(tt,k({},o,{icon:te}),null)};W.displayName="VerticalAlignTopOutlined";W.inheritAttrs=!1;const oe=W,ne=R({compatConfig:{MODE:3},name:"ABackTop",inheritAttrs:!1,props:L(Vt(),{visibilityHeight:400,target:()=>window,duration:450,type:"default",shape:"circle"}),setup(t,n){let{slots:e,attrs:o,emit:a}=n;const{prefixCls:r,direction:d}=V(U,t),[p]=X(r),u=E(),s=Et({visible:t.visibilityHeight===0,scrollEvent:null}),g=()=>u.value&&u.value.ownerDocument?u.value.ownerDocument:window,v=f=>{const{target:i=g,duration:l}=t;Ft(0,{getContainer:i,duration:l}),a("click",f)},B=At(f=>{const{visibilityHeight:i}=t,l=Mt(f.target,!0);s.visible=l>=i}),S=()=>{const{target:f}=t,l=(f||g)();B({target:l}),l==null||l.addEventListener("scroll",B)},O=()=>{const{target:f}=t,l=(f||g)();B.cancel(),l==null||l.removeEventListener("scroll",B)};nt(()=>t.target,()=>{O(),A(()=>{S()})}),Pt(()=>{A(()=>{S()})}),zt(()=>{A(()=>{S()})}),Rt(()=>{O()}),at(()=>{O()});const x=ut();return()=>{const{description:f,type:i,shape:l,tooltip:m,badge:y}=t,F=h(h({},o),{shape:(x==null?void 0:x.shape.value)||l,onClick:v,class:{[`${r.value}`]:!0,[`${o.class}`]:o.class,[`${r.value}-rtl`]:d.value==="rtl"},description:f,type:i,tooltip:m,badge:y}),T=rt("fade");return p(c(it,T,{default:()=>[lt(c(w,b(b({},F),{},{ref:u}),{icon:()=>{var $;return(($=e.icon)===null||$===void 0?void 0:$.call(e))||c(oe,null,null)}}),[[st,s.visible]])]}))}}}),G=ne;w.Group=j;w.BackTop=G;w.install=function(t){return t.component(w.name,w),t.component(j.name,j),t.component(G.name,G),t};P.Item=_;P.install=function(t){return t.component(P.name,P),t.component(_.name,_),t};export{G as B,w as F,j as a,At as t};
//# sourceMappingURL=index.5073a4b2.js.map
