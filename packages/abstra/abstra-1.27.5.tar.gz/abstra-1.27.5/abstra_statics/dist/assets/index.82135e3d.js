import{M as C}from"./Modal.57f7ea40.js";import{d as j,an as Y,f as u,by as ve,bt as xe,bv as ye,cV as ge,N as W,dh as K,aV as G,U as i,O as be,di as J,Q as w,A as ke,dj as he,dk as Te,$ as we,G as E,dl as Fe,bJ as Pe,E as b,H as q,u as Ae,dm as $e}from"./outputWidgets.1e038a78.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},n=new Error().stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="333e6f0b-3cd6-44c2-bef1-ddd809a89b2f",e._sentryDebugIdIdentifier="sentry-dbid-333e6f0b-3cd6-44c2-bef1-ddd809a89b2f")}catch{}})();function T(e){return typeof e=="function"?e():e}const Z=j({name:"ConfirmDialog",inheritAttrs:!1,props:["icon","onCancel","onOk","close","closable","zIndex","afterClose","visible","open","keyboard","centered","getContainer","maskStyle","okButtonProps","cancelButtonProps","okType","prefixCls","okCancel","width","mask","maskClosable","okText","cancelText","autoFocusButton","transitionName","maskTransitionName","type","title","content","direction","rootPrefixCls","bodyStyle","closeIcon","modalRender","focusTriggerAfterClose","wrapClassName","confirmPrefixCls","footer"],setup(e,n){let{attrs:t}=n;const[s]=Y("Modal");return()=>{const{icon:v,onCancel:r,onOk:p,close:m,okText:y,closable:c=!1,zIndex:a,afterClose:l,keyboard:x,centered:o,getContainer:f,maskStyle:g,okButtonProps:F,cancelButtonProps:H,okCancel:N,width:d=416,mask:P=!0,maskClosable:h=!1,type:M,open:B,title:L,content:le,direction:ae,closeIcon:se,modalRender:re,focusTriggerAfterClose:ce,rootPrefixCls:S,bodyStyle:ie,wrapClassName:ue,footer:z}=e;let A=v;if(!v&&v!==null)switch(M){case"info":A=u(ge,null,null);break;case"success":A=u(ye,null,null);break;case"error":A=u(xe,null,null);break;default:A=u(ve,null,null)}const fe=e.okType||"primary",R=e.prefixCls||"ant-modal",$=`${R}-confirm`,de=t.style||{},Q=N!=null?N:M==="confirm",V=e.autoFocusButton===null?!1:e.autoFocusButton||"ok",D=`${R}-confirm`,me=W(D,`${D}-${e.type}`,{[`${D}-rtl`]:ae==="rtl"},t.class),O=s.value,Ce=Q&&u(K,{actionFn:r,close:m,autofocus:V==="cancel",buttonProps:H,prefixCls:`${S}-btn`},{default:()=>[T(e.cancelText)||O.cancelText]});return u(C,{prefixCls:R,class:me,wrapClassName:W({[`${D}-centered`]:!!o},ue),onCancel:pe=>m==null?void 0:m({triggerCancel:!0},pe),open:B,title:"",footer:"",transitionName:G(S,"zoom",e.transitionName),maskTransitionName:G(S,"fade",e.maskTransitionName),mask:P,maskClosable:h,maskStyle:g,style:de,bodyStyle:ie,width:d,zIndex:a,afterClose:l,keyboard:x,centered:o,getContainer:f,closable:c,closeIcon:se,modalRender:re,focusTriggerAfterClose:ce},{default:()=>[u("div",{class:`${$}-body-wrapper`},[u("div",{class:`${$}-body`},[T(A),L===void 0?null:u("span",{class:`${$}-title`},[T(L)]),u("div",{class:`${$}-content`},[T(le)])]),z!==void 0?T(z):u("div",{class:`${$}-btns`},[Ce,u(K,{type:fe,actionFn:p,close:m,autofocus:V==="ok",buttonProps:F,prefixCls:`${S}-btn`},{default:()=>[T(y)||(Q?O.okText:O.justOkText)]})])])]})}}}),Ie=[],k=Ie,Ne=e=>{const n=document.createDocumentFragment();let t=i(i({},be(e,["parentContext","appContext"])),{close:r,open:!0}),s=null;function v(){s&&(J(null,n),s.component.update(),s=null);for(var c=arguments.length,a=new Array(c),l=0;l<c;l++)a[l]=arguments[l];const x=a.some(o=>o&&o.triggerCancel);e.onCancel&&x&&e.onCancel(()=>{},...a.slice(1));for(let o=0;o<k.length;o++)if(k[o]===r){k.splice(o,1);break}}function r(){for(var c=arguments.length,a=new Array(c),l=0;l<c;l++)a[l]=arguments[l];t=i(i({},t),{open:!1,afterClose:()=>{typeof e.afterClose=="function"&&e.afterClose(),v.apply(this,a)}}),t.visible&&delete t.visible,p(t)}function p(c){typeof c=="function"?t=c(t):t=i(i({},t),c),s&&(i(s.component.props,t),s.component.update())}const m=c=>{const a=he,l=a.prefixCls,x=c.prefixCls||`${l}-modal`,o=a.iconPrefixCls,f=Te();return u(ke,w(w({},a),{},{prefixCls:l}),{default:()=>[u(Z,w(w({},c),{},{rootPrefixCls:l,prefixCls:x,iconPrefixCls:o,locale:f,cancelText:c.cancelText||f.cancelText}),null)]})};function y(c){const a=u(m,i({},c));return a.appContext=e.parentContext||e.appContext||a.appContext,J(a,n),a}return s=y(t),k.push(r),{destroy:r,update:p}},I=Ne;function U(e){return i(i({},e),{type:"warning"})}function _(e){return i(i({},e),{type:"info"})}function ee(e){return i(i({},e),{type:"success"})}function ne(e){return i(i({},e),{type:"error"})}function oe(e){return i(i({},e),{type:"confirm"})}const Me=()=>({config:Object,afterClose:Function,destroyAction:Function,open:Boolean}),Be=j({name:"HookModal",inheritAttrs:!1,props:we(Me(),{config:{width:520,okType:"primary"}}),setup(e,n){let{expose:t}=n;var s;const v=E(()=>e.open),r=E(()=>e.config),{direction:p,getPrefixCls:m}=Fe(),y=m("modal"),c=m(),a=()=>{var f,g;e==null||e.afterClose(),(g=(f=r.value).afterClose)===null||g===void 0||g.call(f)},l=function(){e.destroyAction(...arguments)};t({destroy:l});const x=(s=r.value.okCancel)!==null&&s!==void 0?s:r.value.type==="confirm",[o]=Y("Modal",Pe.Modal);return()=>u(Z,w(w({prefixCls:y,rootPrefixCls:c},r.value),{},{close:l,open:v.value,afterClose:a,okText:r.value.okText||(x?o==null?void 0:o.value.okText:o==null?void 0:o.value.justOkText),direction:r.value.direction||p.value,cancelText:r.value.cancelText||(o==null?void 0:o.value.cancelText)}),null)}});let X=0;const Se=j({name:"ElementsHolder",inheritAttrs:!1,setup(e,n){let{expose:t}=n;const s=b([]);return t({addModal:r=>(s.value.push(r),s.value=s.value.slice(),()=>{s.value=s.value.filter(p=>p!==r)})}),()=>s.value.map(r=>r())}});function De(){const e=b(null),n=b([]);q(n,()=>{n.value.length&&([...n.value].forEach(p=>{p()}),n.value=[])},{immediate:!0});const t=r=>function(m){var y;X+=1;const c=b(!0),a=b(null),l=b(Ae(m)),x=b({});q(()=>m,d=>{F(i(i({},$e(d)?d.value:d),x.value))});const o=function(){c.value=!1;for(var d=arguments.length,P=new Array(d),h=0;h<d;h++)P[h]=arguments[h];const M=P.some(B=>B&&B.triggerCancel);l.value.onCancel&&M&&l.value.onCancel(()=>{},...P.slice(1))};let f;const g=()=>u(Be,{key:`modal-${X}`,config:r(l.value),ref:a,open:c.value,destroyAction:o,afterClose:()=>{f==null||f()}},null);f=(y=e.value)===null||y===void 0?void 0:y.addModal(g),f&&k.push(f);const F=d=>{l.value=i(i({},l.value),d)};return{destroy:()=>{a.value?o():n.value=[...n.value,o]},update:d=>{x.value=d,a.value?F(d):n.value=[...n.value,()=>F(d)]}}},s=E(()=>({info:t(_),success:t(ee),error:t(ne),warning:t(U),confirm:t(oe)})),v=Symbol("modalHolderKey");return[s.value,()=>u(Se,{key:v,ref:e},null)]}function te(e){return I(U(e))}C.useModal=De;C.info=function(n){return I(_(n))};C.success=function(n){return I(ee(n))};C.error=function(n){return I(ne(n))};C.warning=te;C.warn=te;C.confirm=function(n){return I(oe(n))};C.destroyAll=function(){for(;k.length;){const n=k.pop();n&&n()}};C.install=function(e){return e.component(C.name,C),e};export{De as u};
//# sourceMappingURL=index.82135e3d.js.map
