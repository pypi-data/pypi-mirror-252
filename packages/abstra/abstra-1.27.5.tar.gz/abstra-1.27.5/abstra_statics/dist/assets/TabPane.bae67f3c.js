import{dH as Ge,dI as ft,E as H,a0 as De,a$ as ye,d as ee,r as V,G as W,f as p,aC as q,N as ie,av as Te,U as w,aB as L,o as Pe,H as se,bl as pt,dJ as ht,bh as gt,bf as mt,dK as $t,a5 as Ie,ay as j,W as yt,X as xt,aF as St,dL as _t,R as Ke,Q,a2 as xe,dM as $e,ap as Ct,aY as wt,dN as Xe,z as Tt,B as Pt,Y as It,Z as et,d1 as tt,$ as at,af as Rt,O as Et,aw as Ce,b0 as Bt,ax as Lt,ac as At,bU as Ot,a4 as Dt,bo as Oe,L as Mt,aZ as kt,ak as Fe,bu as Nt}from"./outputWidgets.1e038a78.js";import{c as nt,t as Ht,d as Wt,b as zt,h as Gt,f as Kt}from"./hasIn.3b666b8d.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[t]="3acf78bc-9ac9-46ef-8bdb-90441dcbacb5",e._sentryDebugIdIdentifier="sentry-dbid-3acf78bc-9ac9-46ef-8bdb-90441dcbacb5")}catch{}})();function Xt(e,t,a,n){if(!Ge(e))return e;t=nt(t,e);for(var i=-1,l=t.length,o=l-1,c=e;c!=null&&++i<l;){var u=Ht(t[i]),v=a;if(u==="__proto__"||u==="constructor"||u==="prototype")return e;if(i!=o){var b=c[u];v=n?n(b,u,c):void 0,v===void 0&&(v=Ge(b)?b:ft(t[i+1])?[]:{})}Wt(c,u,v),c=c[u]}return e}function Ft(e,t,a){for(var n=-1,i=t.length,l={};++n<i;){var o=t[n],c=zt(e,o);a(c,o)&&Xt(l,nt(o,e),c)}return l}function jt(e,t){return Ft(e,t,function(a,n){return Gt(e,n)})}var Vt=Kt(function(e,t){return e==null?{}:jt(e,t)});const ot=Vt;function Yt(e){const t=H(),a=H(!1);function n(){for(var i=arguments.length,l=new Array(i),o=0;o<i;o++)l[o]=arguments[o];a.value||(ye.cancel(t.value),t.value=ye(()=>{e(...l)}))}return De(()=>{a.value=!0,ye.cancel(t.value)}),n}function Ut(e){const t=H([]),a=H(typeof e=="function"?e():e),n=Yt(()=>{let l=a.value;t.value.forEach(o=>{l=o(l)}),t.value=[],a.value=l});function i(l){t.value.push(l),n()}return[a,i]}const qt=ee({compatConfig:{MODE:3},name:"TabNode",props:{id:{type:String},prefixCls:{type:String},tab:{type:Object},active:{type:Boolean},closable:{type:Boolean},editable:{type:Object},onClick:{type:Function},onResize:{type:Function},renderWrapper:{type:Function},removeAriaLabel:{type:String},onFocus:{type:Function}},emits:["click","resize","remove","focus"],setup(e,t){let{expose:a,attrs:n}=t;const i=V();function l(u){var v;!((v=e.tab)===null||v===void 0)&&v.disabled||e.onClick(u)}a({domRef:i});function o(u){var v;u.preventDefault(),u.stopPropagation(),e.editable.onEdit("remove",{key:(v=e.tab)===null||v===void 0?void 0:v.key,event:u})}const c=W(()=>{var u;return e.editable&&e.closable!==!1&&!(!((u=e.tab)===null||u===void 0)&&u.disabled)});return()=>{var u;const{prefixCls:v,id:b,active:S,tab:{key:h,tab:s,disabled:y,closeIcon:x},renderWrapper:T,removeAriaLabel:_,editable:O,onFocus:G}=e,D=`${v}-tab`,r=p("div",{key:h,ref:i,class:ie(D,{[`${D}-with-remove`]:c.value,[`${D}-active`]:S,[`${D}-disabled`]:y}),style:n.style,onClick:l},[p("div",{role:"tab","aria-selected":S,id:b&&`${b}-tab-${h}`,class:`${D}-btn`,"aria-controls":b&&`${b}-panel-${h}`,"aria-disabled":y,tabindex:y?null:0,onClick:m=>{m.stopPropagation(),l(m)},onKeydown:m=>{[q.SPACE,q.ENTER].includes(m.which)&&(m.preventDefault(),l(m))},onFocus:G},[typeof s=="function"?s():s]),c.value&&p("button",{type:"button","aria-label":_||"remove",tabindex:0,class:`${D}-remove`,onClick:m=>{m.stopPropagation(),o(m)}},[(x==null?void 0:x())||((u=O.removeIcon)===null||u===void 0?void 0:u.call(O))||"\xD7"])]);return T?T(r):r}}}),je={width:0,height:0,left:0,top:0};function Zt(e,t){const a=V(new Map);return Te(()=>{var n,i;const l=new Map,o=e.value,c=t.value.get((n=o[0])===null||n===void 0?void 0:n.key)||je,u=c.left+c.width;for(let v=0;v<o.length;v+=1){const{key:b}=o[v];let S=t.value.get(b);S||(S=t.value.get((i=o[v-1])===null||i===void 0?void 0:i.key)||je);const h=l.get(b)||w({},S);h.right=u-h.left-h.width,l.set(b,h)}a.value=new Map(l)}),a}const it=ee({compatConfig:{MODE:3},name:"AddButton",inheritAttrs:!1,props:{prefixCls:String,editable:{type:Object},locale:{type:Object,default:void 0}},setup(e,t){let{expose:a,attrs:n}=t;const i=V();return a({domRef:i}),()=>{const{prefixCls:l,editable:o,locale:c}=e;return!o||o.showAdd===!1?null:p("button",{ref:i,type:"button",class:`${l}-nav-add`,style:n.style,"aria-label":(c==null?void 0:c.addAriaLabel)||"Add tab",onClick:u=>{o.onEdit("add",{event:u})}},[o.addIcon?o.addIcon():"+"])}}}),Jt={prefixCls:{type:String},id:{type:String},tabs:{type:Object},rtl:{type:Boolean},tabBarGutter:{type:Number},activeKey:{type:[String,Number]},mobile:{type:Boolean},moreIcon:Ie.any,moreTransitionName:{type:String},editable:{type:Object},locale:{type:Object,default:void 0},removeAriaLabel:String,onTabClick:{type:Function},popupClassName:String,getPopupContainer:j()},Qt=ee({compatConfig:{MODE:3},name:"OperationNode",inheritAttrs:!1,props:Jt,emits:["tabClick"],slots:Object,setup(e,t){let{attrs:a,slots:n}=t;const[i,l]=L(!1),[o,c]=L(null),u=s=>{const y=e.tabs.filter(_=>!_.disabled);let x=y.findIndex(_=>_.key===o.value)||0;const T=y.length;for(let _=0;_<T;_+=1){x=(x+s+T)%T;const O=y[x];if(!O.disabled){c(O.key);return}}},v=s=>{const{which:y}=s;if(!i.value){[q.DOWN,q.SPACE,q.ENTER].includes(y)&&(l(!0),s.preventDefault());return}switch(y){case q.UP:u(-1),s.preventDefault();break;case q.DOWN:u(1),s.preventDefault();break;case q.ESC:l(!1);break;case q.SPACE:case q.ENTER:o.value!==null&&e.onTabClick(o.value,s);break}},b=W(()=>`${e.id}-more-popup`),S=W(()=>o.value!==null?`${b.value}-${o.value}`:null),h=(s,y)=>{s.preventDefault(),s.stopPropagation(),e.editable.onEdit("remove",{key:y,event:s})};return Pe(()=>{se(o,()=>{const s=document.getElementById(S.value);s&&s.scrollIntoView&&s.scrollIntoView(!1)},{flush:"post",immediate:!0})}),se(i,()=>{i.value||c(null)}),pt({}),()=>{var s;const{prefixCls:y,id:x,tabs:T,locale:_,mobile:O,moreIcon:G=((s=n.moreIcon)===null||s===void 0?void 0:s.call(n))||p(ht,null,null),moreTransitionName:D,editable:r,tabBarGutter:m,rtl:d,onTabClick:$,popupClassName:E}=e;if(!T.length)return null;const P=`${y}-dropdown`,K=_==null?void 0:_.dropdownAriaLabel,le={[d?"marginRight":"marginLeft"]:m};T.length||(le.visibility="hidden",le.order=1);const de=ie({[`${P}-rtl`]:d,[`${E}`]:!0}),be=O?null:p($t,{prefixCls:P,trigger:["hover"],visible:i.value,transitionName:D,onVisibleChange:l,overlayClassName:de,mouseEnterDelay:.1,mouseLeaveDelay:.1,getPopupContainer:e.getPopupContainer},{overlay:()=>p(gt,{onClick:I=>{let{key:Z,domEvent:M}=I;$(Z,M),l(!1)},id:b.value,tabindex:-1,role:"listbox","aria-activedescendant":S.value,selectedKeys:[o.value],"aria-label":K!==void 0?K:"expanded dropdown"},{default:()=>[T.map(I=>{var Z,M;const Y=r&&I.closable!==!1&&!I.disabled;return p(mt,{key:I.key,id:`${b.value}-${I.key}`,role:"option","aria-controls":x&&`${x}-panel-${I.key}`,disabled:I.disabled},{default:()=>[p("span",null,[typeof I.tab=="function"?I.tab():I.tab]),Y&&p("button",{type:"button","aria-label":e.removeAriaLabel||"remove",tabindex:0,class:`${P}-menu-item-remove`,onClick:U=>{U.stopPropagation(),h(U,I.key)}},[((Z=I.closeIcon)===null||Z===void 0?void 0:Z.call(I))||((M=r.removeIcon)===null||M===void 0?void 0:M.call(r))||"\xD7"])]})})]}),default:()=>p("button",{type:"button",class:`${y}-nav-more`,style:le,tabindex:-1,"aria-hidden":"true","aria-haspopup":"listbox","aria-controls":b.value,id:`${x}-more`,"aria-expanded":i.value,onKeydown:v},[G])});return p("div",{class:ie(`${y}-nav-operations`,a.class),style:a.style},[be,p(it,{prefixCls:y,locale:_,editable:r},null)])}}}),lt=Symbol("tabsContextKey"),rt=e=>{yt(lt,e)},st=()=>xt(lt,{tabs:V([]),prefixCls:V()});ee({compatConfig:{MODE:3},name:"TabsContextProvider",inheritAttrs:!1,props:{tabs:{type:Object,default:void 0},prefixCls:{type:String,default:void 0}},setup(e,t){let{slots:a}=t;return rt(St(e)),()=>{var n;return(n=a.default)===null||n===void 0?void 0:n.call(a)}}});const ea=.1,Ve=.01,we=20,Ye=Math.pow(.995,we);function ta(e,t){const[a,n]=L(),[i,l]=L(0),[o,c]=L(0),[u,v]=L(),b=V();function S(r){const{screenX:m,screenY:d}=r.touches[0];n({x:m,y:d}),clearInterval(b.value)}function h(r){if(!a.value)return;r.preventDefault();const{screenX:m,screenY:d}=r.touches[0],$=m-a.value.x,E=d-a.value.y;t($,E),n({x:m,y:d});const P=Date.now();c(P-i.value),l(P),v({x:$,y:E})}function s(){if(!a.value)return;const r=u.value;if(n(null),v(null),r){const m=r.x/o.value,d=r.y/o.value,$=Math.abs(m),E=Math.abs(d);if(Math.max($,E)<ea)return;let P=m,K=d;b.value=setInterval(()=>{if(Math.abs(P)<Ve&&Math.abs(K)<Ve){clearInterval(b.value);return}P*=Ye,K*=Ye,t(P*we,K*we)},we)}}const y=V();function x(r){const{deltaX:m,deltaY:d}=r;let $=0;const E=Math.abs(m),P=Math.abs(d);E===P?$=y.value==="x"?m:d:E>P?($=m,y.value="x"):($=d,y.value="y"),t(-$,-$)&&r.preventDefault()}const T=V({onTouchStart:S,onTouchMove:h,onTouchEnd:s,onWheel:x});function _(r){T.value.onTouchStart(r)}function O(r){T.value.onTouchMove(r)}function G(r){T.value.onTouchEnd(r)}function D(r){T.value.onWheel(r)}Pe(()=>{var r,m;document.addEventListener("touchmove",O,{passive:!1}),document.addEventListener("touchend",G,{passive:!1}),(r=e.value)===null||r===void 0||r.addEventListener("touchstart",_,{passive:!1}),(m=e.value)===null||m===void 0||m.addEventListener("wheel",D,{passive:!1})}),De(()=>{document.removeEventListener("touchmove",O),document.removeEventListener("touchend",G)})}function Ue(e,t){const a=V(e);function n(i){const l=typeof i=="function"?i(a.value):i;l!==a.value&&t(l,a.value),a.value=l}return[a,n]}const aa=()=>{const e=V(new Map),t=a=>n=>{e.value.set(a,n)};return _t(()=>{e.value=new Map}),[t,e]},na=aa,qe={width:0,height:0,left:0,top:0,right:0},oa=()=>({id:{type:String},tabPosition:{type:String},activeKey:{type:[String,Number]},rtl:{type:Boolean},animated:xe(),editable:xe(),moreIcon:Ie.any,moreTransitionName:{type:String},mobile:{type:Boolean},tabBarGutter:{type:Number},renderTabBar:{type:Function},locale:xe(),popupClassName:String,getPopupContainer:j(),onTabClick:{type:Function},onTabScroll:{type:Function}}),Ze=ee({compatConfig:{MODE:3},name:"TabNavList",inheritAttrs:!1,props:oa(),slots:Object,emits:["tabClick","tabScroll"],setup(e,t){let{attrs:a,slots:n}=t;const{tabs:i,prefixCls:l}=st(),o=H(),c=H(),u=H(),v=H(),[b,S]=na(),h=W(()=>e.tabPosition==="top"||e.tabPosition==="bottom"),[s,y]=Ue(0,(g,f)=>{h.value&&e.onTabScroll&&e.onTabScroll({direction:g>f?"left":"right"})}),[x,T]=Ue(0,(g,f)=>{!h.value&&e.onTabScroll&&e.onTabScroll({direction:g>f?"top":"bottom"})}),[_,O]=L(0),[G,D]=L(0),[r,m]=L(null),[d,$]=L(null),[E,P]=L(0),[K,le]=L(0),[de,be]=Ut(new Map),I=Zt(i,de),Z=W(()=>`${l.value}-nav-operations-hidden`),M=H(0),Y=H(0);Te(()=>{h.value?e.rtl?(M.value=0,Y.value=Math.max(0,_.value-r.value)):(M.value=Math.min(0,r.value-_.value),Y.value=0):(M.value=Math.min(0,d.value-G.value),Y.value=0)});const U=g=>g<M.value?M.value:g>Y.value?Y.value:g,fe=H(),[z,pe]=L(),he=()=>{pe(Date.now())},ge=()=>{clearTimeout(fe.value)},Se=(g,f)=>{g(C=>U(C+f))};ta(o,(g,f)=>{if(h.value){if(r.value>=_.value)return!1;Se(y,g)}else{if(d.value>=G.value)return!1;Se(T,f)}return ge(),he(),!0}),se(z,()=>{ge(),z.value&&(fe.value=setTimeout(()=>{pe(0)},100))});const ce=function(){let g=arguments.length>0&&arguments[0]!==void 0?arguments[0]:e.activeKey;const f=I.value.get(g)||{width:0,height:0,left:0,right:0,top:0};if(h.value){let C=s.value;e.rtl?f.right<s.value?C=f.right:f.right+f.width>s.value+r.value&&(C=f.right+f.width-r.value):f.left<-s.value?C=-f.left:f.left+f.width>-s.value+r.value&&(C=-(f.left+f.width-r.value)),T(0),y(U(C))}else{let C=x.value;f.top<-x.value?C=-f.top:f.top+f.height>-x.value+d.value&&(C=-(f.top+f.height-d.value)),y(0),T(U(C))}},Re=H(0),Ee=H(0);Te(()=>{let g,f,C,R,k,N;const re=I.value;["top","bottom"].includes(e.tabPosition)?(g="width",R=r.value,k=_.value,N=E.value,f=e.rtl?"right":"left",C=Math.abs(s.value)):(g="height",R=d.value,k=_.value,N=K.value,f="top",C=-x.value);let X=R;k+N>R&&k<R&&(X=R-N);const J=i.value;if(!J.length)return[Re.value,Ee.value]=[0,0];const ae=J.length;let ue=ae;for(let A=0;A<ae;A+=1){const F=re.get(J[A].key)||qe;if(F[f]+F[g]>C+X){ue=A-1;break}}let B=0;for(let A=ae-1;A>=0;A-=1)if((re.get(J[A].key)||qe)[f]<C){B=A+1;break}return[Re.value,Ee.value]=[B,ue]});const Be=()=>{var g,f,C,R,k;const N=((g=o.value)===null||g===void 0?void 0:g.offsetWidth)||0,re=((f=o.value)===null||f===void 0?void 0:f.offsetHeight)||0,X=((C=v.value)===null||C===void 0?void 0:C.$el)||{},J=X.offsetWidth||0,ae=X.offsetHeight||0;m(N),$(re),P(J),le(ae);const ue=(((R=c.value)===null||R===void 0?void 0:R.offsetWidth)||0)-J,B=(((k=c.value)===null||k===void 0?void 0:k.offsetHeight)||0)-ae;O(ue),D(B),be(()=>{const A=new Map;return i.value.forEach(F=>{let{key:ve}=F;const ne=S.value.get(ve),oe=(ne==null?void 0:ne.$el)||ne;oe&&A.set(ve,{width:oe.offsetWidth,height:oe.offsetHeight,left:oe.offsetLeft,top:oe.offsetTop})}),A})},ke=W(()=>[...i.value.slice(0,Re.value),...i.value.slice(Ee.value+1)]),[ct,ut]=L(),te=W(()=>I.value.get(e.activeKey)),Ne=H(),He=()=>{ye.cancel(Ne.value)};se([te,h,()=>e.rtl],()=>{const g={};te.value&&(h.value?(e.rtl?g.right=$e(te.value.right):g.left=$e(te.value.left),g.width=$e(te.value.width)):(g.top=$e(te.value.top),g.height=$e(te.value.height))),He(),Ne.value=ye(()=>{ut(g)})}),se([()=>e.activeKey,te,I,h],()=>{ce()},{flush:"post"}),se([()=>e.rtl,()=>e.tabBarGutter,()=>e.activeKey,()=>i.value],()=>{Be()},{flush:"post"});const Le=g=>{let{position:f,prefixCls:C,extra:R}=g;if(!R)return null;const k=R==null?void 0:R({position:f});return k?p("div",{class:`${C}-extra-content`},[k]):null};return De(()=>{ge(),He()}),()=>{const{id:g,animated:f,activeKey:C,rtl:R,editable:k,locale:N,tabPosition:re,tabBarGutter:X,onTabClick:J}=e,{class:ae,style:ue}=a,B=l.value,A=!!ke.value.length,F=`${B}-nav-wrap`;let ve,ne,oe,We;h.value?R?(ne=s.value>0,ve=s.value+r.value<_.value):(ve=s.value<0,ne=-s.value+r.value<_.value):(oe=x.value<0,We=-x.value+d.value<G.value);const _e={};re==="top"||re==="bottom"?_e[R?"marginRight":"marginLeft"]=typeof X=="number"?`${X}px`:X:_e.marginTop=typeof X=="number"?`${X}px`:X;const ze=i.value.map((Ae,vt)=>{const{key:me}=Ae;return p(qt,{id:g,prefixCls:B,key:me,tab:Ae,style:vt===0?void 0:_e,closable:Ae.closable,editable:k,active:me===C,removeAriaLabel:N==null?void 0:N.removeAriaLabel,ref:b(me),onClick:bt=>{J(me,bt)},onFocus:()=>{ce(me),he(),o.value&&(R||(o.value.scrollLeft=0),o.value.scrollTop=0)}},n)});return p("div",{role:"tablist",class:ie(`${B}-nav`,ae),style:ue,onKeydown:()=>{he()}},[p(Le,{position:"left",prefixCls:B,extra:n.leftExtra},null),p(Ke,{onResize:Be},{default:()=>[p("div",{class:ie(F,{[`${F}-ping-left`]:ve,[`${F}-ping-right`]:ne,[`${F}-ping-top`]:oe,[`${F}-ping-bottom`]:We}),ref:o},[p(Ke,{onResize:Be},{default:()=>[p("div",{ref:c,class:`${B}-nav-list`,style:{transform:`translate(${s.value}px, ${x.value}px)`,transition:z.value?"none":void 0}},[ze,p(it,{ref:v,prefixCls:B,locale:N,editable:k,style:w(w({},ze.length===0?void 0:_e),{visibility:A?"hidden":null})},null),p("div",{class:ie(`${B}-ink-bar`,{[`${B}-ink-bar-animated`]:f.inkBar}),style:ct.value},null)])]})])]}),p(Qt,Q(Q({},e),{},{removeAriaLabel:N==null?void 0:N.removeAriaLabel,ref:u,prefixCls:B,tabs:ke.value,class:!A&&Z.value}),ot(n,["moreIcon"])),p(Le,{position:"right",prefixCls:B,extra:n.rightExtra},null),p(Le,{position:"right",prefixCls:B,extra:n.tabBarExtraContent},null)])}}}),ia=ee({compatConfig:{MODE:3},name:"TabPanelList",inheritAttrs:!1,props:{activeKey:{type:[String,Number]},id:{type:String},rtl:{type:Boolean},animated:{type:Object,default:void 0},tabPosition:{type:String},destroyInactiveTabPane:{type:Boolean}},setup(e){const{tabs:t,prefixCls:a}=st();return()=>{const{id:n,activeKey:i,animated:l,tabPosition:o,rtl:c,destroyInactiveTabPane:u}=e,v=l.tabPane,b=a.value,S=t.value.findIndex(h=>h.key===i);return p("div",{class:`${b}-content-holder`},[p("div",{class:[`${b}-content`,`${b}-content-${o}`,{[`${b}-content-animated`]:v}],style:S&&v?{[c?"marginRight":"marginLeft"]:`-${S}00%`}:null},[t.value.map(h=>Ct(h.node,{key:h.key,prefixCls:b,tabKey:h.key,id:n,animated:v,active:h.key===i,destroyInactiveTabPane:u}))])])}}});var la={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"defs",attrs:{},children:[{tag:"style",attrs:{}}]},{tag:"path",attrs:{d:"M482 152h60q8 0 8 8v704q0 8-8 8h-60q-8 0-8-8V160q0-8 8-8z"}},{tag:"path",attrs:{d:"M176 474h672q8 0 8 8v60q0 8-8 8H176q-8 0-8-8v-60q0-8 8-8z"}}]},name:"plus",theme:"outlined"};const ra=la;function Je(e){for(var t=1;t<arguments.length;t++){var a=arguments[t]!=null?Object(arguments[t]):{},n=Object.keys(a);typeof Object.getOwnPropertySymbols=="function"&&(n=n.concat(Object.getOwnPropertySymbols(a).filter(function(i){return Object.getOwnPropertyDescriptor(a,i).enumerable}))),n.forEach(function(i){sa(e,i,a[i])})}return e}function sa(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}var Me=function(t,a){var n=Je({},t,a.attrs);return p(wt,Je({},n,{icon:ra}),null)};Me.displayName="PlusOutlined";Me.inheritAttrs=!1;const da=Me,ca=e=>{const{componentCls:t,motionDurationSlow:a}=e;return[{[t]:{[`${t}-switch`]:{"&-appear, &-enter":{transition:"none","&-start":{opacity:0},"&-active":{opacity:1,transition:`opacity ${a}`}},"&-leave":{position:"absolute",transition:"none",inset:0,"&-start":{opacity:1},"&-active":{opacity:0,transition:`opacity ${a}`}}}}},[Xe(e,"slide-up"),Xe(e,"slide-down")]]},ua=ca,va=e=>{const{componentCls:t,tabsCardHorizontalPadding:a,tabsCardHeadBackground:n,tabsCardGutter:i,colorSplit:l}=e;return{[`${t}-card`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab`]:{margin:0,padding:a,background:n,border:`${e.lineWidth}px ${e.lineType} ${l}`,transition:`all ${e.motionDurationSlow} ${e.motionEaseInOut}`},[`${t}-tab-active`]:{color:e.colorPrimary,background:e.colorBgContainer},[`${t}-ink-bar`]:{visibility:"hidden"}},[`&${t}-top, &${t}-bottom`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab + ${t}-tab`]:{marginLeft:{_skip_check_:!0,value:`${i}px`}}}},[`&${t}-top`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab`]:{borderRadius:`${e.borderRadiusLG}px ${e.borderRadiusLG}px 0 0`},[`${t}-tab-active`]:{borderBottomColor:e.colorBgContainer}}},[`&${t}-bottom`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab`]:{borderRadius:`0 0 ${e.borderRadiusLG}px ${e.borderRadiusLG}px`},[`${t}-tab-active`]:{borderTopColor:e.colorBgContainer}}},[`&${t}-left, &${t}-right`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab + ${t}-tab`]:{marginTop:`${i}px`}}},[`&${t}-left`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab`]:{borderRadius:{_skip_check_:!0,value:`${e.borderRadiusLG}px 0 0 ${e.borderRadiusLG}px`}},[`${t}-tab-active`]:{borderRightColor:{_skip_check_:!0,value:e.colorBgContainer}}}},[`&${t}-right`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab`]:{borderRadius:{_skip_check_:!0,value:`0 ${e.borderRadiusLG}px ${e.borderRadiusLG}px 0`}},[`${t}-tab-active`]:{borderLeftColor:{_skip_check_:!0,value:e.colorBgContainer}}}}}}},ba=e=>{const{componentCls:t,tabsHoverColor:a,dropdownEdgeChildVerticalPadding:n}=e;return{[`${t}-dropdown`]:w(w({},et(e)),{position:"absolute",top:-9999,left:{_skip_check_:!0,value:-9999},zIndex:e.zIndexPopup,display:"block","&-hidden":{display:"none"},[`${t}-dropdown-menu`]:{maxHeight:e.tabsDropdownHeight,margin:0,padding:`${n}px 0`,overflowX:"hidden",overflowY:"auto",textAlign:{_skip_check_:!0,value:"left"},listStyleType:"none",backgroundColor:e.colorBgContainer,backgroundClip:"padding-box",borderRadius:e.borderRadiusLG,outline:"none",boxShadow:e.boxShadowSecondary,"&-item":w(w({},It),{display:"flex",alignItems:"center",minWidth:e.tabsDropdownWidth,margin:0,padding:`${e.paddingXXS}px ${e.paddingSM}px`,color:e.colorText,fontWeight:"normal",fontSize:e.fontSize,lineHeight:e.lineHeight,cursor:"pointer",transition:`all ${e.motionDurationSlow}`,"> span":{flex:1,whiteSpace:"nowrap"},"&-remove":{flex:"none",marginLeft:{_skip_check_:!0,value:e.marginSM},color:e.colorTextDescription,fontSize:e.fontSizeSM,background:"transparent",border:0,cursor:"pointer","&:hover":{color:a}},"&:hover":{background:e.controlItemBgHover},"&-disabled":{"&, &:hover":{color:e.colorTextDisabled,background:"transparent",cursor:"not-allowed"}}})}})}},fa=e=>{const{componentCls:t,margin:a,colorSplit:n}=e;return{[`${t}-top, ${t}-bottom`]:{flexDirection:"column",[`> ${t}-nav, > div > ${t}-nav`]:{margin:`0 0 ${a}px 0`,"&::before":{position:"absolute",right:{_skip_check_:!0,value:0},left:{_skip_check_:!0,value:0},borderBottom:`${e.lineWidth}px ${e.lineType} ${n}`,content:"''"},[`${t}-ink-bar`]:{height:e.lineWidthBold,"&-animated":{transition:`width ${e.motionDurationSlow}, left ${e.motionDurationSlow},
            right ${e.motionDurationSlow}`}},[`${t}-nav-wrap`]:{"&::before, &::after":{top:0,bottom:0,width:e.controlHeight},"&::before":{left:{_skip_check_:!0,value:0},boxShadow:e.boxShadowTabsOverflowLeft},"&::after":{right:{_skip_check_:!0,value:0},boxShadow:e.boxShadowTabsOverflowRight},[`&${t}-nav-wrap-ping-left::before`]:{opacity:1},[`&${t}-nav-wrap-ping-right::after`]:{opacity:1}}}},[`${t}-top`]:{[`> ${t}-nav,
        > div > ${t}-nav`]:{"&::before":{bottom:0},[`${t}-ink-bar`]:{bottom:0}}},[`${t}-bottom`]:{[`> ${t}-nav, > div > ${t}-nav`]:{order:1,marginTop:`${a}px`,marginBottom:0,"&::before":{top:0},[`${t}-ink-bar`]:{top:0}},[`> ${t}-content-holder, > div > ${t}-content-holder`]:{order:0}},[`${t}-left, ${t}-right`]:{[`> ${t}-nav, > div > ${t}-nav`]:{flexDirection:"column",minWidth:e.controlHeight*1.25,[`${t}-tab`]:{padding:`${e.paddingXS}px ${e.paddingLG}px`,textAlign:"center"},[`${t}-tab + ${t}-tab`]:{margin:`${e.margin}px 0 0 0`},[`${t}-nav-wrap`]:{flexDirection:"column","&::before, &::after":{right:{_skip_check_:!0,value:0},left:{_skip_check_:!0,value:0},height:e.controlHeight},"&::before":{top:0,boxShadow:e.boxShadowTabsOverflowTop},"&::after":{bottom:0,boxShadow:e.boxShadowTabsOverflowBottom},[`&${t}-nav-wrap-ping-top::before`]:{opacity:1},[`&${t}-nav-wrap-ping-bottom::after`]:{opacity:1}},[`${t}-ink-bar`]:{width:e.lineWidthBold,"&-animated":{transition:`height ${e.motionDurationSlow}, top ${e.motionDurationSlow}`}},[`${t}-nav-list, ${t}-nav-operations`]:{flex:"1 0 auto",flexDirection:"column"}}},[`${t}-left`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-ink-bar`]:{right:{_skip_check_:!0,value:0}}},[`> ${t}-content-holder, > div > ${t}-content-holder`]:{marginLeft:{_skip_check_:!0,value:`-${e.lineWidth}px`},borderLeft:{_skip_check_:!0,value:`${e.lineWidth}px ${e.lineType} ${e.colorBorder}`},[`> ${t}-content > ${t}-tabpane`]:{paddingLeft:{_skip_check_:!0,value:e.paddingLG}}}},[`${t}-right`]:{[`> ${t}-nav, > div > ${t}-nav`]:{order:1,[`${t}-ink-bar`]:{left:{_skip_check_:!0,value:0}}},[`> ${t}-content-holder, > div > ${t}-content-holder`]:{order:0,marginRight:{_skip_check_:!0,value:-e.lineWidth},borderRight:{_skip_check_:!0,value:`${e.lineWidth}px ${e.lineType} ${e.colorBorder}`},[`> ${t}-content > ${t}-tabpane`]:{paddingRight:{_skip_check_:!0,value:e.paddingLG}}}}}},pa=e=>{const{componentCls:t,padding:a}=e;return{[t]:{"&-small":{[`> ${t}-nav`]:{[`${t}-tab`]:{padding:`${e.paddingXS}px 0`,fontSize:e.fontSize}}},"&-large":{[`> ${t}-nav`]:{[`${t}-tab`]:{padding:`${a}px 0`,fontSize:e.fontSizeLG}}}},[`${t}-card`]:{[`&${t}-small`]:{[`> ${t}-nav`]:{[`${t}-tab`]:{padding:`${e.paddingXXS*1.5}px ${a}px`}},[`&${t}-bottom`]:{[`> ${t}-nav ${t}-tab`]:{borderRadius:`0 0 ${e.borderRadius}px ${e.borderRadius}px`}},[`&${t}-top`]:{[`> ${t}-nav ${t}-tab`]:{borderRadius:`${e.borderRadius}px ${e.borderRadius}px 0 0`}},[`&${t}-right`]:{[`> ${t}-nav ${t}-tab`]:{borderRadius:{_skip_check_:!0,value:`0 ${e.borderRadius}px ${e.borderRadius}px 0`}}},[`&${t}-left`]:{[`> ${t}-nav ${t}-tab`]:{borderRadius:{_skip_check_:!0,value:`${e.borderRadius}px 0 0 ${e.borderRadius}px`}}}},[`&${t}-large`]:{[`> ${t}-nav`]:{[`${t}-tab`]:{padding:`${e.paddingXS}px ${a}px ${e.paddingXXS*1.5}px`}}}}}},ha=e=>{const{componentCls:t,tabsActiveColor:a,tabsHoverColor:n,iconCls:i,tabsHorizontalGutter:l}=e,o=`${t}-tab`;return{[o]:{position:"relative",display:"inline-flex",alignItems:"center",padding:`${e.paddingSM}px 0`,fontSize:`${e.fontSize}px`,background:"transparent",border:0,outline:"none",cursor:"pointer","&-btn, &-remove":w({"&:focus:not(:focus-visible), &:active":{color:a}},tt(e)),"&-btn":{outline:"none",transition:"all 0.3s"},"&-remove":{flex:"none",marginRight:{_skip_check_:!0,value:-e.marginXXS},marginLeft:{_skip_check_:!0,value:e.marginXS},color:e.colorTextDescription,fontSize:e.fontSizeSM,background:"transparent",border:"none",outline:"none",cursor:"pointer",transition:`all ${e.motionDurationSlow}`,"&:hover":{color:e.colorTextHeading}},"&:hover":{color:n},[`&${o}-active ${o}-btn`]:{color:e.colorPrimary,textShadow:e.tabsActiveTextShadow},[`&${o}-disabled`]:{color:e.colorTextDisabled,cursor:"not-allowed"},[`&${o}-disabled ${o}-btn, &${o}-disabled ${t}-remove`]:{"&:focus, &:active":{color:e.colorTextDisabled}},[`& ${o}-remove ${i}`]:{margin:0},[i]:{marginRight:{_skip_check_:!0,value:e.marginSM}}},[`${o} + ${o}`]:{margin:{_skip_check_:!0,value:`0 0 0 ${l}px`}}}},ga=e=>{const{componentCls:t,tabsHorizontalGutter:a,iconCls:n,tabsCardGutter:i}=e;return{[`${t}-rtl`]:{direction:"rtl",[`${t}-nav`]:{[`${t}-tab`]:{margin:{_skip_check_:!0,value:`0 0 0 ${a}px`},[`${t}-tab:last-of-type`]:{marginLeft:{_skip_check_:!0,value:0}},[n]:{marginRight:{_skip_check_:!0,value:0},marginLeft:{_skip_check_:!0,value:`${e.marginSM}px`}},[`${t}-tab-remove`]:{marginRight:{_skip_check_:!0,value:`${e.marginXS}px`},marginLeft:{_skip_check_:!0,value:`-${e.marginXXS}px`},[n]:{margin:0}}}},[`&${t}-left`]:{[`> ${t}-nav`]:{order:1},[`> ${t}-content-holder`]:{order:0}},[`&${t}-right`]:{[`> ${t}-nav`]:{order:0},[`> ${t}-content-holder`]:{order:1}},[`&${t}-card${t}-top, &${t}-card${t}-bottom`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-tab + ${t}-tab`]:{marginRight:{_skip_check_:!0,value:`${i}px`},marginLeft:{_skip_check_:!0,value:0}}}}},[`${t}-dropdown-rtl`]:{direction:"rtl"},[`${t}-menu-item`]:{[`${t}-dropdown-rtl`]:{textAlign:{_skip_check_:!0,value:"right"}}}}},ma=e=>{const{componentCls:t,tabsCardHorizontalPadding:a,tabsCardHeight:n,tabsCardGutter:i,tabsHoverColor:l,tabsActiveColor:o,colorSplit:c}=e;return{[t]:w(w(w(w({},et(e)),{display:"flex",[`> ${t}-nav, > div > ${t}-nav`]:{position:"relative",display:"flex",flex:"none",alignItems:"center",[`${t}-nav-wrap`]:{position:"relative",display:"flex",flex:"auto",alignSelf:"stretch",overflow:"hidden",whiteSpace:"nowrap",transform:"translate(0)","&::before, &::after":{position:"absolute",zIndex:1,opacity:0,transition:`opacity ${e.motionDurationSlow}`,content:"''",pointerEvents:"none"}},[`${t}-nav-list`]:{position:"relative",display:"flex",transition:`opacity ${e.motionDurationSlow}`},[`${t}-nav-operations`]:{display:"flex",alignSelf:"stretch"},[`${t}-nav-operations-hidden`]:{position:"absolute",visibility:"hidden",pointerEvents:"none"},[`${t}-nav-more`]:{position:"relative",padding:a,background:"transparent",border:0,"&::after":{position:"absolute",right:{_skip_check_:!0,value:0},bottom:0,left:{_skip_check_:!0,value:0},height:e.controlHeightLG/8,transform:"translateY(100%)",content:"''"}},[`${t}-nav-add`]:w({minWidth:`${n}px`,marginLeft:{_skip_check_:!0,value:`${i}px`},padding:`0 ${e.paddingXS}px`,background:"transparent",border:`${e.lineWidth}px ${e.lineType} ${c}`,borderRadius:`${e.borderRadiusLG}px ${e.borderRadiusLG}px 0 0`,outline:"none",cursor:"pointer",color:e.colorText,transition:`all ${e.motionDurationSlow} ${e.motionEaseInOut}`,"&:hover":{color:l},"&:active, &:focus:not(:focus-visible)":{color:o}},tt(e))},[`${t}-extra-content`]:{flex:"none"},[`${t}-ink-bar`]:{position:"absolute",background:e.colorPrimary,pointerEvents:"none"}}),ha(e)),{[`${t}-content`]:{position:"relative",display:"flex",width:"100%",["&-animated"]:{transition:"margin 0.3s"}},[`${t}-content-holder`]:{flex:"auto",minWidth:0,minHeight:0},[`${t}-tabpane`]:{outline:"none",flex:"none",width:"100%"}}),[`${t}-centered`]:{[`> ${t}-nav, > div > ${t}-nav`]:{[`${t}-nav-wrap`]:{[`&:not([class*='${t}-nav-wrap-ping'])`]:{justifyContent:"center"}}}}}},$a=Tt("Tabs",e=>{const t=e.controlHeightLG,a=Pt(e,{tabsHoverColor:e.colorPrimaryHover,tabsActiveColor:e.colorPrimaryActive,tabsCardHorizontalPadding:`${(t-Math.round(e.fontSize*e.lineHeight))/2-e.lineWidth}px ${e.padding}px`,tabsCardHeight:t,tabsCardGutter:e.marginXXS/2,tabsHorizontalGutter:32,tabsCardHeadBackground:e.colorFillAlter,dropdownEdgeChildVerticalPadding:e.paddingXXS,tabsActiveTextShadow:"0 0 0.25px currentcolor",tabsDropdownHeight:200,tabsDropdownWidth:120});return[pa(a),ga(a),fa(a),ba(a),va(a),ma(a),ua(a)]},e=>({zIndexPopup:e.zIndexPopupBase+50}));let Qe=0;const dt=()=>({prefixCls:{type:String},id:{type:String},popupClassName:String,getPopupContainer:j(),activeKey:{type:[String,Number]},defaultActiveKey:{type:[String,Number]},direction:Ce(),animated:Bt([Boolean,Object]),renderTabBar:j(),tabBarGutter:{type:Number},tabBarStyle:xe(),tabPosition:Ce(),destroyInactiveTabPane:Lt(),hideAdd:Boolean,type:Ce(),size:Ce(),centered:Boolean,onEdit:j(),onChange:j(),onTabClick:j(),onTabScroll:j(),"onUpdate:activeKey":j(),locale:xe(),onPrevClick:j(),onNextClick:j(),tabBarExtraContent:Ie.any});function ya(e){return e.map(t=>{if(At(t)){const a=w({},t.props||{});for(const[h,s]of Object.entries(a))delete a[h],a[Ot(h)]=s;const n=t.children||{},i=t.key!==void 0?t.key:void 0,{tab:l=n.tab,disabled:o,forceRender:c,closable:u,animated:v,active:b,destroyInactiveTabPane:S}=a;return w(w({key:i},a),{node:t,closeIcon:n.closeIcon,tab:l,disabled:o===""||o,forceRender:c===""||c,closable:u===""||u,animated:v===""||v,active:b===""||b,destroyInactiveTabPane:S===""||S})}return null}).filter(t=>t)}const xa=ee({compatConfig:{MODE:3},name:"InternalTabs",inheritAttrs:!1,props:w(w({},at(dt(),{tabPosition:"top",animated:{inkBar:!0,tabPane:!1}})),{tabs:Dt()}),slots:Object,setup(e,t){let{attrs:a,slots:n}=t;Oe(e.onPrevClick===void 0&&e.onNextClick===void 0,"Tabs","`onPrevClick / @prevClick` and `onNextClick / @nextClick` has been removed. Please use `onTabScroll / @tabScroll` instead."),Oe(e.tabBarExtraContent===void 0,"Tabs","`tabBarExtraContent` prop has been removed. Please use `rightExtra` slot instead."),Oe(n.tabBarExtraContent===void 0,"Tabs","`tabBarExtraContent` slot is deprecated. Please use `rightExtra` slot instead.");const{prefixCls:i,direction:l,size:o,rootPrefixCls:c,getPopupContainer:u}=Mt("tabs",e),[v,b]=$a(i),S=W(()=>l.value==="rtl"),h=W(()=>{const{animated:d,tabPosition:$}=e;return d===!1||["left","right"].includes($)?{inkBar:!1,tabPane:!1}:d===!0?{inkBar:!0,tabPane:!0}:w({inkBar:!0,tabPane:!1},typeof d=="object"?d:{})}),[s,y]=L(!1);Pe(()=>{y(kt())});const[x,T]=Fe(()=>{var d;return(d=e.tabs[0])===null||d===void 0?void 0:d.key},{value:W(()=>e.activeKey),defaultValue:e.defaultActiveKey}),[_,O]=L(()=>e.tabs.findIndex(d=>d.key===x.value));Te(()=>{var d;let $=e.tabs.findIndex(E=>E.key===x.value);$===-1&&($=Math.max(0,Math.min(_.value,e.tabs.length-1)),T((d=e.tabs[$])===null||d===void 0?void 0:d.key)),O($)});const[G,D]=Fe(null,{value:W(()=>e.id)}),r=W(()=>s.value&&!["left","right"].includes(e.tabPosition)?"top":e.tabPosition);Pe(()=>{e.id||(D(`rc-tabs-${Qe}`),Qe+=1)});const m=(d,$)=>{var E,P;(E=e.onTabClick)===null||E===void 0||E.call(e,d,$);const K=d!==x.value;T(d),K&&((P=e.onChange)===null||P===void 0||P.call(e,d))};return rt({tabs:W(()=>e.tabs),prefixCls:i}),()=>{const{id:d,type:$,tabBarGutter:E,tabBarStyle:P,locale:K,destroyInactiveTabPane:le,renderTabBar:de=n.renderTabBar,onTabScroll:be,hideAdd:I,centered:Z}=e,M={id:G.value,activeKey:x.value,animated:h.value,tabPosition:r.value,rtl:S.value,mobile:s.value};let Y;$==="editable-card"&&(Y={onEdit:(pe,he)=>{let{key:ge,event:Se}=he;var ce;(ce=e.onEdit)===null||ce===void 0||ce.call(e,pe==="add"?Se:ge,pe)},removeIcon:()=>p(Nt,null,null),addIcon:n.addIcon?n.addIcon:()=>p(da,null,null),showAdd:I!==!0});let U;const fe=w(w({},M),{moreTransitionName:`${c.value}-slide-up`,editable:Y,locale:K,tabBarGutter:E,onTabClick:m,onTabScroll:be,style:P,getPopupContainer:u.value,popupClassName:ie(e.popupClassName,b.value)});de?U=de(w(w({},fe),{DefaultTabBar:Ze})):U=p(Ze,fe,ot(n,["moreIcon","leftExtra","rightExtra","tabBarExtraContent"]));const z=i.value;return v(p("div",Q(Q({},a),{},{id:d,class:ie(z,`${z}-${r.value}`,{[b.value]:!0,[`${z}-${o.value}`]:o.value,[`${z}-card`]:["card","editable-card"].includes($),[`${z}-editable-card`]:$==="editable-card",[`${z}-centered`]:Z,[`${z}-mobile`]:s.value,[`${z}-editable`]:$==="editable-card",[`${z}-rtl`]:S.value},a.class)}),[U,p(ia,Q(Q({destroyInactiveTabPane:le},M),{},{animated:h.value}),null)]))}}}),wa=ee({compatConfig:{MODE:3},name:"ATabs",inheritAttrs:!1,props:at(dt(),{tabPosition:"top",animated:{inkBar:!0,tabPane:!1}}),slots:Object,setup(e,t){let{attrs:a,slots:n,emit:i}=t;const l=o=>{i("update:activeKey",o),i("change",o)};return()=>{var o;const c=ya(Rt((o=n.default)===null||o===void 0?void 0:o.call(n)));return p(xa,Q(Q(Q({},Et(e,["onUpdate:activeKey"])),a),{},{onChange:l,tabs:c}),n)}}}),Sa=()=>({tab:Ie.any,disabled:{type:Boolean},forceRender:{type:Boolean},closable:{type:Boolean},animated:{type:Boolean},active:{type:Boolean},destroyInactiveTabPane:{type:Boolean},prefixCls:{type:String},tabKey:{type:[String,Number]},id:{type:String}}),Ta=ee({compatConfig:{MODE:3},name:"ATabPane",inheritAttrs:!1,__ANT_TAB_PANE:!0,props:Sa(),slots:Object,setup(e,t){let{attrs:a,slots:n}=t;const i=V(e.forceRender);se([()=>e.active,()=>e.destroyInactiveTabPane],()=>{e.active?i.value=!0:e.destroyInactiveTabPane&&(i.value=!1)},{immediate:!0});const l=W(()=>e.active?{}:e.animated?{visibility:"hidden",height:0,overflowY:"hidden"}:{display:"none"});return()=>{var o;const{prefixCls:c,forceRender:u,id:v,active:b,tabKey:S}=e;return p("div",{id:v&&`${v}-panel-${S}`,role:"tabpanel",tabindex:b?0:-1,"aria-labelledby":v&&`${v}-tab-${S}`,"aria-hidden":!b,style:[l.value,a.style],class:[`${c}-tabpane`,b&&`${c}-tabpane-active`,a.class]},[(b||i.value||u)&&((o=n.default)===null||o===void 0?void 0:o.call(n))])}}});export{Ta as A,wa as T,na as u};
//# sourceMappingURL=TabPane.bae67f3c.js.map
