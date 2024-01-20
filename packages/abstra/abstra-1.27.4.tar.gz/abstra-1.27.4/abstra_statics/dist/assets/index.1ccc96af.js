import{z as U,B as Y,U as _,Z as q,D as J,be as K,d as ee,L as oe,E as w,G as ne,N as te,f as s,bu as le,ac as ie,ap as ae,b_ as se,bj as re,c1 as ce,Q as R,c0 as de,bv as ue,cV as ge,bt as fe,by as pe,cW as me,cX as ve,cY as $e,cZ as ye,a5 as v}from"./outputWidgets.3c34606b.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},o=new Error().stack;o&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[o]="51bcfbbf-a163-4787-833a-d2d072a6a748",e._sentryDebugIdIdentifier="sentry-dbid-51bcfbbf-a163-4787-833a-d2d072a6a748")}catch{}})();const B=(e,o,n,i,a)=>({backgroundColor:e,border:`${i.lineWidth}px ${i.lineType} ${o}`,[`${a}-icon`]:{color:n}}),be=e=>{const{componentCls:o,motionDurationSlow:n,marginXS:i,marginSM:a,fontSize:u,fontSizeLG:r,lineHeight:g,borderRadiusLG:$,motionEaseInOutCirc:c,alertIconSizeLG:d,colorText:p,paddingContentVerticalSM:m,alertPaddingHorizontal:y,paddingMD:h,paddingContentHorizontalLG:C}=e;return{[o]:_(_({},q(e)),{position:"relative",display:"flex",alignItems:"center",padding:`${m}px ${y}px`,wordWrap:"break-word",borderRadius:$,[`&${o}-rtl`]:{direction:"rtl"},[`${o}-content`]:{flex:1,minWidth:0},[`${o}-icon`]:{marginInlineEnd:i,lineHeight:0},["&-description"]:{display:"none",fontSize:u,lineHeight:g},"&-message":{color:p},[`&${o}-motion-leave`]:{overflow:"hidden",opacity:1,transition:`max-height ${n} ${c}, opacity ${n} ${c},
        padding-top ${n} ${c}, padding-bottom ${n} ${c},
        margin-bottom ${n} ${c}`},[`&${o}-motion-leave-active`]:{maxHeight:0,marginBottom:"0 !important",paddingTop:0,paddingBottom:0,opacity:0}}),[`${o}-with-description`]:{alignItems:"flex-start",paddingInline:C,paddingBlock:h,[`${o}-icon`]:{marginInlineEnd:a,fontSize:d,lineHeight:0},[`${o}-message`]:{display:"block",marginBottom:i,color:p,fontSize:r},[`${o}-description`]:{display:"block"}},[`${o}-banner`]:{marginBottom:0,border:"0 !important",borderRadius:0}}},he=e=>{const{componentCls:o,colorSuccess:n,colorSuccessBorder:i,colorSuccessBg:a,colorWarning:u,colorWarningBorder:r,colorWarningBg:g,colorError:$,colorErrorBorder:c,colorErrorBg:d,colorInfo:p,colorInfoBorder:m,colorInfoBg:y}=e;return{[o]:{"&-success":B(a,i,n,e,o),"&-info":B(y,m,p,e,o),"&-warning":B(g,r,u,e,o),"&-error":_(_({},B(d,c,$,e,o)),{[`${o}-description > pre`]:{margin:0,padding:0}})}}},Ce=e=>{const{componentCls:o,iconCls:n,motionDurationMid:i,marginXS:a,fontSizeIcon:u,colorIcon:r,colorIconHover:g}=e;return{[o]:{["&-action"]:{marginInlineStart:a},[`${o}-close-icon`]:{marginInlineStart:a,padding:0,overflow:"hidden",fontSize:u,lineHeight:`${u}px`,backgroundColor:"transparent",border:"none",outline:"none",cursor:"pointer",[`${n}-close`]:{color:r,transition:`color ${i}`,"&:hover":{color:g}}},"&-close-text":{color:r,transition:`color ${i}`,"&:hover":{color:g}}}}},Ie=e=>[be(e),he(e),Ce(e)],Se=U("Alert",e=>{const{fontSizeHeading3:o}=e,n=Y(e,{alertIconSizeLG:o,alertPaddingHorizontal:12});return[Ie(n)]}),xe={success:ue,info:ge,error:fe,warning:pe},we={success:me,info:ve,error:$e,warning:ye},Be=K("success","info","warning","error"),_e=()=>({type:v.oneOf(Be),closable:{type:Boolean,default:void 0},closeText:v.any,message:v.any,description:v.any,afterClose:Function,showIcon:{type:Boolean,default:void 0},prefixCls:String,banner:{type:Boolean,default:void 0},icon:v.any,closeIcon:v.any,onClose:Function}),He=ee({compatConfig:{MODE:3},name:"AAlert",inheritAttrs:!1,props:_e(),setup(e,o){let{slots:n,emit:i,attrs:a,expose:u}=o;const{prefixCls:r,direction:g}=oe("alert",e),[$,c]=Se(r),d=w(!1),p=w(!1),m=w(),y=l=>{l.preventDefault();const f=m.value;f.style.height=`${f.offsetHeight}px`,f.style.height=`${f.offsetHeight}px`,d.value=!0,i("close",l)},h=()=>{var l;d.value=!1,p.value=!0,(l=e.afterClose)===null||l===void 0||l.call(e)},C=ne(()=>{const{type:l}=e;return l!==void 0?l:e.banner?"warning":"info"});u({animationEnd:h});const V=w({});return()=>{var l,f,H,T,E,z,A,D,L,O;const{banner:W,closeIcon:G=(l=n.closeIcon)===null||l===void 0?void 0:l.call(n)}=e;let{closable:F,showIcon:b}=e;const M=(f=e.closeText)!==null&&f!==void 0?f:(H=n.closeText)===null||H===void 0?void 0:H.call(n),I=(T=e.description)!==null&&T!==void 0?T:(E=n.description)===null||E===void 0?void 0:E.call(n),P=(z=e.message)!==null&&z!==void 0?z:(A=n.message)===null||A===void 0?void 0:A.call(n),S=(D=e.icon)!==null&&D!==void 0?D:(L=n.icon)===null||L===void 0?void 0:L.call(n),N=(O=n.action)===null||O===void 0?void 0:O.call(n);b=W&&b===void 0?!0:b;const j=(I?we:xe)[C.value]||null;M&&(F=!0);const t=r.value,k=te(t,{[`${t}-${C.value}`]:!0,[`${t}-closing`]:d.value,[`${t}-with-description`]:!!I,[`${t}-no-icon`]:!b,[`${t}-banner`]:!!W,[`${t}-closable`]:F,[`${t}-rtl`]:g.value==="rtl",[c.value]:!0}),X=F?s("button",{type:"button",onClick:y,class:`${t}-close-icon`,tabindex:0},[M?s("span",{class:`${t}-close-text`},[M]):G===void 0?s(le,null,null):G]):null,Z=S&&(ie(S)?ae(S,{class:`${t}-icon`}):s("span",{class:`${t}-icon`},[S]))||s(j,{class:`${t}-icon`},null),Q=se(`${t}-motion`,{appear:!1,css:!0,onAfterLeave:h,onBeforeLeave:x=>{x.style.maxHeight=`${x.offsetHeight}px`},onLeave:x=>{x.style.maxHeight="0px"}});return $(p.value?null:s(de,Q,{default:()=>[re(s("div",R(R({role:"alert"},a),{},{style:[a.style,V.value],class:[a.class,k],"data-show":!d.value,ref:m}),[b?Z:null,s("div",{class:`${t}-content`},[P?s("div",{class:`${t}-message`},[P]):null,I?s("div",{class:`${t}-description`},[I]):null]),N?s("div",{class:`${t}-action`},[N]):null,X]),[[ce,!d.value]])]}))}}}),Ee=J(He);export{Ee as A};
//# sourceMappingURL=index.1ccc96af.js.map
