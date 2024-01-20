import{d as G,E as Ue,o as re,U as f,f as p,Q as k,aC as W,aY as ae,d3 as Oe,dO as Fe,aj as We,z as Ke,aF as Ve,F as Ee,H as oe,r as ie,N as we,cp as Xe,i as qe,L as Te,dP as $e,G as q,a0 as Ge,a$ as Z,a3 as ge,av as Qe,ab as le,ak as Ye,bx as ee,O as se,bq as me,bP as Je,R as Ze,br as te,bK as et,bw as tt}from"./outputWidgets.3c34606b.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[t]="7966af21-82fd-4a98-9e8d-3d54afcdb220",e._sentryDebugIdIdentifier="sentry-dbid-7966af21-82fd-4a98-9e8d-3d54afcdb220")}catch{}})();var nt=globalThis&&globalThis.__rest||function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var i=0,o=Object.getOwnPropertySymbols(e);i<o.length;i++)t.indexOf(o[i])<0&&Object.prototype.propertyIsEnumerable.call(e,o[i])&&(n[o[i]]=e[o[i]]);return n};const ot={border:0,background:"transparent",padding:0,lineHeight:"inherit",display:"inline-block"},it=G({compatConfig:{MODE:3},name:"TransButton",inheritAttrs:!1,props:{noStyle:{type:Boolean,default:void 0},onClick:Function,disabled:{type:Boolean,default:void 0},autofocus:{type:Boolean,default:void 0}},setup(e,t){let{slots:n,emit:o,attrs:i,expose:c}=t;const a=Ue(),l=h=>{const{keyCode:S}=h;S===W.ENTER&&h.preventDefault()},m=h=>{const{keyCode:S}=h;S===W.ENTER&&o("click",h)},x=h=>{o("click",h)},y=()=>{a.value&&a.value.focus()},$=()=>{a.value&&a.value.blur()};return re(()=>{e.autofocus&&y()}),c({focus:y,blur:$}),()=>{var h;const{noStyle:S,disabled:I}=e,D=nt(e,["noStyle","disabled"]);let B={};return S||(B=f({},ot)),I&&(B.pointerEvents="none"),p("div",k(k(k({role:"button",tabindex:0,ref:a},D),i),{},{onClick:x,onKeydown:l,onKeyup:m,style:f(f({},B),i.style||{})}),[(h=n.default)===null||h===void 0?void 0:h.call(n)])}}}),be=it;var lt={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M864 170h-60c-4.4 0-8 3.6-8 8v518H310v-73c0-6.7-7.8-10.5-13-6.3l-141.9 112a8 8 0 000 12.6l141.9 112c5.3 4.2 13 .4 13-6.3v-75h498c35.3 0 64-28.7 64-64V178c0-4.4-3.6-8-8-8z"}}]},name:"enter",theme:"outlined"};const rt=lt;function ve(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]!=null?Object(arguments[t]):{},o=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(i){return Object.getOwnPropertyDescriptor(n,i).enumerable}))),o.forEach(function(i){at(e,i,n[i])})}return e}function at(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var ce=function(t,n){var o=ve({},t,n.attrs);return p(ae,ve({},o,{icon:rt}),null)};ce.displayName="EnterOutlined";ce.inheritAttrs=!1;const st=ce,ct=(e,t,n,o)=>{const{sizeMarginHeadingVerticalEnd:i,fontWeightStrong:c}=o;return{marginBottom:i,color:n,fontWeight:c,fontSize:e,lineHeight:t}},dt=e=>{const t=[1,2,3,4,5],n={};return t.forEach(o=>{n[`
      h${o}&,
      div&-h${o},
      div&-h${o} > textarea,
      h${o}
    `]=ct(e[`fontSizeHeading${o}`],e[`lineHeightHeading${o}`],e.colorTextHeading,e)}),n},ut=e=>{const{componentCls:t}=e;return{"a&, a":f(f({},Oe(e)),{textDecoration:e.linkDecoration,"&:active, &:hover":{textDecoration:e.linkHoverDecoration},[`&[disabled], &${t}-disabled`]:{color:e.colorTextDisabled,cursor:"not-allowed","&:active, &:hover":{color:e.colorTextDisabled},"&:active":{pointerEvents:"none"}}})}},pt=()=>({code:{margin:"0 0.2em",paddingInline:"0.4em",paddingBlock:"0.2em 0.1em",fontSize:"85%",background:"rgba(150, 150, 150, 0.1)",border:"1px solid rgba(100, 100, 100, 0.2)",borderRadius:3},kbd:{margin:"0 0.2em",paddingInline:"0.4em",paddingBlock:"0.15em 0.1em",fontSize:"90%",background:"rgba(150, 150, 150, 0.06)",border:"1px solid rgba(100, 100, 100, 0.2)",borderBottomWidth:2,borderRadius:3},mark:{padding:0,backgroundColor:Fe[2]},"u, ins":{textDecoration:"underline",textDecorationSkipInk:"auto"},"s, del":{textDecoration:"line-through"},strong:{fontWeight:600},"ul, ol":{marginInline:0,marginBlock:"0 1em",padding:0,li:{marginInline:"20px 0",marginBlock:0,paddingInline:"4px 0",paddingBlock:0}},ul:{listStyleType:"circle",ul:{listStyleType:"disc"}},ol:{listStyleType:"decimal"},"pre, blockquote":{margin:"1em 0"},pre:{padding:"0.4em 0.6em",whiteSpace:"pre-wrap",wordWrap:"break-word",background:"rgba(150, 150, 150, 0.1)",border:"1px solid rgba(100, 100, 100, 0.2)",borderRadius:3,code:{display:"inline",margin:0,padding:0,fontSize:"inherit",fontFamily:"inherit",background:"transparent",border:0}},blockquote:{paddingInline:"0.6em 0",paddingBlock:0,borderInlineStart:"4px solid rgba(100, 100, 100, 0.2)",opacity:.85}}),ft=e=>{const{componentCls:t}=e,o=We(e).inputPaddingVertical+1;return{"&-edit-content":{position:"relative","div&":{insetInlineStart:-e.paddingSM,marginTop:-o,marginBottom:`calc(1em - ${o}px)`},[`${t}-edit-content-confirm`]:{position:"absolute",insetInlineEnd:e.marginXS+2,insetBlockEnd:e.marginXS,color:e.colorTextDescription,fontWeight:"normal",fontSize:e.fontSize,fontStyle:"normal",pointerEvents:"none"},textarea:{margin:"0!important",MozTransition:"none",height:"1em"}}}},yt=e=>({"&-copy-success":{[`
    &,
    &:hover,
    &:focus`]:{color:e.colorSuccess}}}),gt=()=>({[`
  a&-ellipsis,
  span&-ellipsis
  `]:{display:"inline-block",maxWidth:"100%"},"&-single-line":{whiteSpace:"nowrap"},"&-ellipsis-single-line":{overflow:"hidden",textOverflow:"ellipsis","a&, span&":{verticalAlign:"bottom"}},"&-ellipsis-multiple-line":{display:"-webkit-box",overflow:"hidden",WebkitLineClamp:3,WebkitBoxOrient:"vertical"}}),mt=e=>{const{componentCls:t,sizeMarginHeadingVerticalStart:n}=e;return{[t]:f(f(f(f(f(f(f(f(f({color:e.colorText,wordBreak:"break-word",lineHeight:e.lineHeight,[`&${t}-secondary`]:{color:e.colorTextDescription},[`&${t}-success`]:{color:e.colorSuccess},[`&${t}-warning`]:{color:e.colorWarning},[`&${t}-danger`]:{color:e.colorError,"a&:active, a&:focus":{color:e.colorErrorActive},"a&:hover":{color:e.colorErrorHover}},[`&${t}-disabled`]:{color:e.colorTextDisabled,cursor:"not-allowed",userSelect:"none"},[`
        div&,
        p
      `]:{marginBottom:"1em"}},dt(e)),{[`
      & + h1${t},
      & + h2${t},
      & + h3${t},
      & + h4${t},
      & + h5${t}
      `]:{marginTop:n},[`
      div,
      ul,
      li,
      p,
      h1,
      h2,
      h3,
      h4,
      h5`]:{[`
        + h1,
        + h2,
        + h3,
        + h4,
        + h5
        `]:{marginTop:n}}}),pt()),ut(e)),{[`
        ${t}-expand,
        ${t}-edit,
        ${t}-copy
      `]:f(f({},Oe(e)),{marginInlineStart:e.marginXXS})}),ft(e)),yt(e)),gt()),{"&-rtl":{direction:"rtl"}})}},De=Ke("Typography",e=>[mt(e)],{sizeMarginHeadingVerticalStart:"1.2em",sizeMarginHeadingVerticalEnd:"0.5em"}),bt=()=>({prefixCls:String,value:String,maxlength:Number,autoSize:{type:[Boolean,Object]},onSave:Function,onCancel:Function,onEnd:Function,onChange:Function,originContent:String,direction:String,component:String}),vt=G({compatConfig:{MODE:3},name:"Editable",inheritAttrs:!1,props:bt(),setup(e,t){let{emit:n,slots:o,attrs:i}=t;const{prefixCls:c}=Ve(e),a=Ee({current:e.value||"",lastKeyCode:void 0,inComposition:!1,cancelFlag:!1});oe(()=>e.value,g=>{a.current=g});const l=ie();re(()=>{var g;if(l.value){const d=(g=l.value)===null||g===void 0?void 0:g.resizableTextArea,v=d==null?void 0:d.textArea;v.focus();const{length:b}=v.value;v.setSelectionRange(b,b)}});function m(g){l.value=g}function x(g){let{target:{value:d}}=g;a.current=d.replace(/[\r\n]/g,""),n("change",a.current)}function y(){a.inComposition=!0}function $(){a.inComposition=!1}function h(g){const{keyCode:d}=g;d===W.ENTER&&g.preventDefault(),!a.inComposition&&(a.lastKeyCode=d)}function S(g){const{keyCode:d,ctrlKey:v,altKey:b,metaKey:w,shiftKey:A}=g;a.lastKeyCode===d&&!a.inComposition&&!v&&!b&&!w&&!A&&(d===W.ENTER?(D(),n("end")):d===W.ESC&&(a.current=e.originContent,n("cancel")))}function I(){D()}function D(){n("save",a.current.trim())}const[B,_]=De(c);return()=>{const g=we({[`${c.value}`]:!0,[`${c.value}-edit-content`]:!0,[`${c.value}-rtl`]:e.direction==="rtl",[e.component?`${c.value}-${e.component}`:""]:!0},i.class,_.value);return B(p("div",k(k({},i),{},{class:g}),[p(Xe,{ref:m,maxlength:e.maxlength,value:a.current,onChange:x,onKeydown:h,onKeyup:S,onCompositionstart:y,onCompositionend:$,onBlur:I,rows:1,autoSize:e.autoSize===void 0||e.autoSize},null),o.enterIcon?o.enterIcon({className:`${e.prefixCls}-edit-content-confirm`}):p(st,{class:`${e.prefixCls}-edit-content-confirm`},null)]))}}}),ht=vt,Ct=3,xt=8;let E;const ne={padding:0,margin:0,display:"inline",lineHeight:"inherit"};function St(e){return Array.prototype.slice.apply(e).map(n=>`${n}: ${e.getPropertyValue(n)};`).join("")}function Ie(e,t){e.setAttribute("aria-hidden","true");const n=window.getComputedStyle(t),o=St(n);e.setAttribute("style",o),e.style.position="fixed",e.style.left="0",e.style.height="auto",e.style.minHeight="auto",e.style.maxHeight="auto",e.style.paddingTop="0",e.style.paddingBottom="0",e.style.borderTopWidth="0",e.style.borderBottomWidth="0",e.style.top="-999999px",e.style.zIndex="-1000",e.style.textOverflow="clip",e.style.whiteSpace="normal",e.style.webkitLineClamp="none"}function Ot(e){const t=document.createElement("div");Ie(t,e),t.appendChild(document.createTextNode("text")),document.body.appendChild(t);const n=t.getBoundingClientRect().height;return document.body.removeChild(t),n}const Et=(e,t,n,o,i)=>{E||(E=document.createElement("div"),E.setAttribute("aria-hidden","true"),document.body.appendChild(E));const{rows:c,suffix:a=""}=t,l=Ot(e),m=Math.round(l*c*100)/100;Ie(E,e);const x=qe({render(){return p("div",{style:ne},[p("span",{style:ne},[n,a]),p("span",{style:ne},[o])])}});x.mount(E);function y(){return Math.round(E.getBoundingClientRect().height*100)/100-.1<=m}if(y())return x.unmount(),{content:n,text:E.innerHTML,ellipsis:!1};const $=Array.prototype.slice.apply(E.childNodes[0].childNodes[0].cloneNode(!0).childNodes).filter(d=>{let{nodeType:v,data:b}=d;return v!==xt&&b!==""}),h=Array.prototype.slice.apply(E.childNodes[0].childNodes[1].cloneNode(!0).childNodes);x.unmount();const S=[];E.innerHTML="";const I=document.createElement("span");E.appendChild(I);const D=document.createTextNode(i+a);I.appendChild(D),h.forEach(d=>{E.appendChild(d)});function B(d){I.insertBefore(d,D)}function _(d,v){let b=arguments.length>2&&arguments[2]!==void 0?arguments[2]:0,w=arguments.length>3&&arguments[3]!==void 0?arguments[3]:v.length,A=arguments.length>4&&arguments[4]!==void 0?arguments[4]:0;const j=Math.floor((b+w)/2),Y=v.slice(0,j);if(d.textContent=Y,b>=w-1)for(let H=w;H>=b;H-=1){const U=v.slice(0,H);if(d.textContent=U,y()||!U)return H===v.length?{finished:!1,vNode:v}:{finished:!0,vNode:U}}return y()?_(d,v,j,w,j):_(d,v,b,j,A)}function g(d){if(d.nodeType===Ct){const b=d.textContent||"",w=document.createTextNode(b);return B(w),_(w,b)}return{finished:!1,vNode:null}}return $.some(d=>{const{finished:v,vNode:b}=g(d);return b&&S.push(b),v}),{content:S,text:E.innerHTML,ellipsis:!0}};var wt=globalThis&&globalThis.__rest||function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var i=0,o=Object.getOwnPropertySymbols(e);i<o.length;i++)t.indexOf(o[i])<0&&Object.prototype.propertyIsEnumerable.call(e,o[i])&&(n[o[i]]=e[o[i]]);return n};const Tt=()=>({prefixCls:String,direction:String,component:String}),$t=G({name:"ATypography",inheritAttrs:!1,props:Tt(),setup(e,t){let{slots:n,attrs:o}=t;const{prefixCls:i,direction:c}=Te("typography",e),[a,l]=De(i);return()=>{var m;const x=f(f({},e),o),{prefixCls:y,direction:$,component:h="article"}=x,S=wt(x,["prefixCls","direction","component"]);return a(p(h,k(k({},S),{},{class:we(i.value,{[`${i.value}-rtl`]:c.value==="rtl"},o.class,l.value)}),{default:()=>[(m=n.default)===null||m===void 0?void 0:m.call(n)]}))}}}),Dt=$t,It=()=>{const e=document.getSelection();if(!e.rangeCount)return function(){};let t=document.activeElement;const n=[];for(let o=0;o<e.rangeCount;o++)n.push(e.getRangeAt(o));switch(t.tagName.toUpperCase()){case"INPUT":case"TEXTAREA":t.blur();break;default:t=null;break}return e.removeAllRanges(),function(){e.type==="Caret"&&e.removeAllRanges(),e.rangeCount||n.forEach(function(o){e.addRange(o)}),t&&t.focus()}},Bt=It,he={"text/plain":"Text","text/html":"Url",default:"Text"},Nt="Copy to clipboard: #{key}, Enter";function Pt(e){const t=(/mac os x/i.test(navigator.userAgent)?"\u2318":"Ctrl")+"+C";return e.replace(/#{\s*key\s*}/g,t)}function kt(e,t){let n,o,i,c,a,l=!1;t||(t={});const m=t.debug||!1;try{if(o=Bt(),i=document.createRange(),c=document.getSelection(),a=document.createElement("span"),a.textContent=e,a.style.all="unset",a.style.position="fixed",a.style.top=0,a.style.clip="rect(0, 0, 0, 0)",a.style.whiteSpace="pre",a.style.webkitUserSelect="text",a.style.MozUserSelect="text",a.style.msUserSelect="text",a.style.userSelect="text",a.addEventListener("copy",function(y){if(y.stopPropagation(),t.format)if(y.preventDefault(),typeof y.clipboardData>"u"){m&&console.warn("unable to use e.clipboardData"),m&&console.warn("trying IE specific stuff"),window.clipboardData.clearData();const $=he[t.format]||he.default;window.clipboardData.setData($,e)}else y.clipboardData.clearData(),y.clipboardData.setData(t.format,e);t.onCopy&&(y.preventDefault(),t.onCopy(y.clipboardData))}),document.body.appendChild(a),i.selectNodeContents(a),c.addRange(i),!document.execCommand("copy"))throw new Error("copy command was unsuccessful");l=!0}catch(x){m&&console.error("unable to copy using execCommand: ",x),m&&console.warn("trying IE specific stuff");try{window.clipboardData.setData(t.format||"text",e),t.onCopy&&t.onCopy(window.clipboardData),l=!0}catch(y){m&&console.error("unable to copy using clipboardData: ",y),m&&console.error("falling back to prompt"),n=Pt("message"in t?t.message:Nt),window.prompt(n,e)}}finally{c&&(typeof c.removeRange=="function"?c.removeRange(i):c.removeAllRanges()),a&&document.body.removeChild(a),o()}return l}var _t={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M832 64H296c-4.4 0-8 3.6-8 8v56c0 4.4 3.6 8 8 8h496v688c0 4.4 3.6 8 8 8h56c4.4 0 8-3.6 8-8V96c0-17.7-14.3-32-32-32zM704 192H192c-17.7 0-32 14.3-32 32v530.7c0 8.5 3.4 16.6 9.4 22.6l173.3 173.3c2.2 2.2 4.7 4 7.4 5.5v1.9h4.2c3.5 1.3 7.2 2 11 2H704c17.7 0 32-14.3 32-32V224c0-17.7-14.3-32-32-32zM350 856.2L263.9 770H350v86.2zM664 888H414V746c0-22.1-17.9-40-40-40H232V264h432v624z"}}]},name:"copy",theme:"outlined"};const Rt=_t;function Ce(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]!=null?Object(arguments[t]):{},o=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(i){return Object.getOwnPropertyDescriptor(n,i).enumerable}))),o.forEach(function(i){At(e,i,n[i])})}return e}function At(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var de=function(t,n){var o=Ce({},t,n.attrs);return p(ae,Ce({},o,{icon:Rt}),null)};de.displayName="CopyOutlined";de.inheritAttrs=!1;const jt=de;var Ht={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M257.7 752c2 0 4-.2 6-.5L431.9 722c2-.4 3.9-1.3 5.3-2.8l423.9-423.9a9.96 9.96 0 000-14.1L694.9 114.9c-1.9-1.9-4.4-2.9-7.1-2.9s-5.2 1-7.1 2.9L256.8 538.8c-1.5 1.5-2.4 3.3-2.8 5.3l-29.5 168.2a33.5 33.5 0 009.4 29.8c6.6 6.4 14.9 9.9 23.8 9.9zm67.4-174.4L687.8 215l73.3 73.3-362.7 362.6-88.9 15.7 15.6-89zM880 836H144c-17.7 0-32 14.3-32 32v36c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-36c0-17.7-14.3-32-32-32z"}}]},name:"edit",theme:"outlined"};const zt=Ht;function xe(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]!=null?Object(arguments[t]):{},o=Object.keys(n);typeof Object.getOwnPropertySymbols=="function"&&(o=o.concat(Object.getOwnPropertySymbols(n).filter(function(i){return Object.getOwnPropertyDescriptor(n,i).enumerable}))),o.forEach(function(i){Mt(e,i,n[i])})}return e}function Mt(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var ue=function(t,n){var o=xe({},t,n.attrs);return p(ae,xe({},o,{icon:zt}),null)};ue.displayName="EditOutlined";ue.inheritAttrs=!1;const Lt=ue;var Ut=globalThis&&globalThis.__rest||function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var i=0,o=Object.getOwnPropertySymbols(e);i<o.length;i++)t.indexOf(o[i])<0&&Object.prototype.propertyIsEnumerable.call(e,o[i])&&(n[o[i]]=e[o[i]]);return n};const Ft=$e("webkitLineClamp"),Wt=$e("textOverflow"),Se="...",Be=()=>({editable:{type:[Boolean,Object],default:void 0},copyable:{type:[Boolean,Object],default:void 0},prefixCls:String,component:String,type:String,disabled:{type:Boolean,default:void 0},ellipsis:{type:[Boolean,Object],default:void 0},code:{type:Boolean,default:void 0},mark:{type:Boolean,default:void 0},underline:{type:Boolean,default:void 0},delete:{type:Boolean,default:void 0},strong:{type:Boolean,default:void 0},keyboard:{type:Boolean,default:void 0},content:String,"onUpdate:content":Function}),Kt=G({compatConfig:{MODE:3},name:"TypographyBase",inheritAttrs:!1,props:Be(),setup(e,t){let{slots:n,attrs:o,emit:i}=t;const{prefixCls:c,direction:a}=Te("typography",e),l=Ee({copied:!1,ellipsisText:"",ellipsisContent:null,isEllipsis:!1,expanded:!1,clientRendered:!1,expandStr:"",copyStr:"",copiedStr:"",editStr:"",copyId:void 0,rafId:void 0,prevProps:void 0,originContent:""}),m=ie(),x=ie(),y=q(()=>{const r=e.ellipsis;return r?f({rows:1,expandable:!1},typeof r=="object"?r:null):{}});re(()=>{l.clientRendered=!0}),Ge(()=>{clearTimeout(l.copyId),Z.cancel(l.rafId)}),oe([()=>y.value.rows,()=>e.content],()=>{ge(()=>{w()})},{flush:"post",deep:!0,immediate:!0}),Qe(()=>{e.content===void 0&&(le(!e.editable),le(!e.ellipsis))});function $(){var r;return e.ellipsis||e.editable?e.content:(r=ee(m.value))===null||r===void 0?void 0:r.innerText}function h(r){const{onExpand:s}=y.value;l.expanded=!0,s==null||s(r)}function S(r){r.preventDefault(),l.originContent=e.content,b(!0)}function I(r){D(r),b(!1)}function D(r){const{onChange:s}=g.value;r!==e.content&&(i("update:content",r),s==null||s(r))}function B(){var r,s;(s=(r=g.value).onCancel)===null||s===void 0||s.call(r),b(!1)}function _(r){r.preventDefault(),r.stopPropagation();const{copyable:s}=e,u=f({},typeof s=="object"?s:null);u.text===void 0&&(u.text=$()),kt(u.text||""),l.copied=!0,ge(()=>{u.onCopy&&u.onCopy(r),l.copyId=setTimeout(()=>{l.copied=!1},3e3)})}const g=q(()=>{const r=e.editable;return r?f({},typeof r=="object"?r:null):{editing:!1}}),[d,v]=Ye(!1,{value:q(()=>g.value.editing)});function b(r){const{onStart:s}=g.value;r&&s&&s(),v(r)}oe(d,r=>{var s;r||(s=x.value)===null||s===void 0||s.focus()},{flush:"post"});function w(){Z.cancel(l.rafId),l.rafId=Z(()=>{j()})}const A=q(()=>{const{rows:r,expandable:s,suffix:u,onEllipsis:C,tooltip:O}=y.value;return u||O||e.editable||e.copyable||s||C?!1:r===1?Wt:Ft}),j=()=>{const{ellipsisText:r,isEllipsis:s}=l,{rows:u,suffix:C,onEllipsis:O}=y.value;if(!u||u<0||!ee(m.value)||l.expanded||e.content===void 0||A.value)return;const{content:N,text:z,ellipsis:R}=Et(ee(m.value),{rows:u,suffix:C},e.content,pe(!0),Se);(r!==z||l.isEllipsis!==R)&&(l.ellipsisText=z,l.ellipsisContent=N,l.isEllipsis=R,s!==R&&O&&O(R))};function Y(r,s){let{mark:u,code:C,underline:O,delete:N,strong:z,keyboard:R}=r,F=s;function P(K,T){if(!K)return;const V=function(){return F}();F=p(T,null,{default:()=>[V]})}return P(z,"strong"),P(O,"u"),P(N,"del"),P(C,"code"),P(u,"mark"),P(R,"kbd"),F}function H(r){const{expandable:s,symbol:u}=y.value;if(!s||!r&&(l.expanded||!l.isEllipsis))return null;const C=(n.ellipsisSymbol?n.ellipsisSymbol():u)||l.expandStr;return p("a",{key:"expand",class:`${c.value}-expand`,onClick:h,"aria-label":l.expandStr},[C])}function U(){if(!e.editable)return;const{tooltip:r,triggerType:s=["icon"]}=e.editable,u=n.editableIcon?n.editableIcon():p(Lt,{role:"button"},null),C=n.editableTooltip?n.editableTooltip():l.editStr,O=typeof C=="string"?C:"";return s.indexOf("icon")!==-1?p(te,{key:"edit",title:r===!1?"":C},{default:()=>[p(be,{ref:x,class:`${c.value}-edit`,onClick:S,"aria-label":O},{default:()=>[u]})]}):null}function Ne(){if(!e.copyable)return;const{tooltip:r}=e.copyable,s=l.copied?l.copiedStr:l.copyStr,u=n.copyableTooltip?n.copyableTooltip({copied:l.copied}):s,C=typeof u=="string"?u:"",O=l.copied?p(tt,null,null):p(jt,null,null),N=n.copyableIcon?n.copyableIcon({copied:!!l.copied}):O;return p(te,{key:"copy",title:r===!1?"":u},{default:()=>[p(be,{class:[`${c.value}-copy`,{[`${c.value}-copy-success`]:l.copied}],onClick:_,"aria-label":C},{default:()=>[N]})]})}function Pe(){const{class:r,style:s}=o,{maxlength:u,autoSize:C,onEnd:O}=g.value;return p(ht,{class:r,style:s,prefixCls:c.value,value:e.content,originContent:l.originContent,maxlength:u,autoSize:C,onSave:I,onChange:D,onCancel:B,onEnd:O,direction:a.value,component:e.component},{enterIcon:n.editableEnterIcon})}function pe(r){return[H(r),U(),Ne()].filter(s=>s)}return()=>{var r;const{triggerType:s=["icon"]}=g.value,u=e.ellipsis||e.editable?e.content!==void 0?e.content:(r=n.default)===null||r===void 0?void 0:r.call(n):n.default?n.default():e.content;return d.value?Pe():p(et,{componentName:"Text",children:C=>{const O=f(f({},e),o),{type:N,disabled:z,content:R,class:F,style:P}=O,K=Ut(O,["type","disabled","content","class","style"]),{rows:T,suffix:V,tooltip:J}=y.value,{edit:ke,copy:_e,copied:Re,expand:Ae}=C;l.editStr=ke,l.copyStr=_e,l.copiedStr=Re,l.expandStr=Ae;const je=se(K,["prefixCls","editable","copyable","ellipsis","mark","code","delete","underline","strong","keyboard","onUpdate:content"]),X=A.value,He=T===1&&X,fe=T&&T>1&&X;let M=u,ze;if(T&&l.isEllipsis&&!l.expanded&&!X){const{title:ye}=K;let L=ye||"";!ye&&(typeof u=="string"||typeof u=="number")&&(L=String(u)),L=L==null?void 0:L.slice(String(l.ellipsisContent||"").length),M=p(me,null,[Je(l.ellipsisContent),p("span",{title:L,"aria-hidden":"true"},[Se]),V])}else M=p(me,null,[u,V]);M=Y(e,M);const Me=J&&T&&l.isEllipsis&&!l.expanded&&!X,Le=n.ellipsisTooltip?n.ellipsisTooltip():J;return p(Ze,{onResize:w,disabled:!T},{default:()=>[p(Dt,k({ref:m,class:[{[`${c.value}-${N}`]:N,[`${c.value}-disabled`]:z,[`${c.value}-ellipsis`]:T,[`${c.value}-single-line`]:T===1&&!l.isEllipsis,[`${c.value}-ellipsis-single-line`]:He,[`${c.value}-ellipsis-multiple-line`]:fe},F],style:f(f({},P),{WebkitLineClamp:fe?T:void 0}),"aria-label":ze,direction:a.value,onClick:s.indexOf("text")!==-1?S:()=>{}},je),{default:()=>[Me?p(te,{title:J===!0?u:Le},{default:()=>[p("span",null,[M])]}):M,pe()]})]})}},null)}}}),Vt=Kt,Xt=()=>f(f({},se(Be(),["component"])),{ellipsis:{type:[Boolean,Object],default:void 0}}),Q=(e,t)=>{let{slots:n,attrs:o}=t;const{ellipsis:i}=e;le();const c=f(f(f({},e),{ellipsis:i&&typeof i=="object"?se(i,["expandable","rows"]):i,component:"span"}),o);return p(Vt,c,n)};Q.displayName="ATypographyText";Q.inheritAttrs=!1;Q.props=Xt();const Gt=Q;export{Gt as A,Vt as B,be as T,Dt as a,Be as b};
//# sourceMappingURL=Text.aa4a1cf1.js.map
