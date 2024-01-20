import{a as I}from"./asyncComputed.bb2b1403.js";import{a as p}from"./router.1b12d634.js";import{d as j,r as T,eL as P,G as g,b as m,c as B,w as a,u as e,f as t,aq as r,e as i,eD as d,bH as F,ev as y,ex as k,cC as H,eB as E}from"./outputWidgets.ed48fa42.js";import"./index.5e38be4e.js";import{P as A}from"./project.74c1366e.js";import{_ as U}from"./SaveButton.vue_vue_type_script_setup_true_lang.bf6c2051.js";import{a as f,A as h}from"./Title.89d211e5.js";import{A as s}from"./Text.b5b9d884.js";import{A as N}from"./FormItem.c1c36356.js";import{F as V}from"./Form.471d6bcc.js";import"./index.60984836.js";import"./index.cf4c23b9.js";import"./record.2ea2ab4d.js";import"./pubsub.90864e85.js";import"./hasIn.a220eabf.js";(function(){try{var u=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},n=new Error().stack;n&&(u._sentryDebugIds=u._sentryDebugIds||{},u._sentryDebugIds[n]="1e820789-9e3f-49ac-9e34-ed5c531aa5e9",u._sentryDebugIdIdentifier="sentry-dbid-1e820789-9e3f-49ac-9e34-ed5c531aa5e9")}catch{}})();const R={key:0},$=j({__name:"SubdomainEditor",props:{project:{}},setup(u){const n=u,o=T(void 0),c=P.exports.debounce(async()=>{try{const{available:l}=await n.project.checkSubdomain();o.value=l?"available":"unavailable"}catch{o.value=void 0}},500);function v(){n.project.subdomain?(o.value="loading",c()):o.value="invalid"}const b=g(()=>{switch(o.value){case"invalid":return"error";case"loading":return"validating";case"available":return"success";case"unavailable":return"error";default:return}}),w=g(()=>{switch(o.value){case"loading":return"Checking availability...";case"available":return"Available";case"unavailable":return"Unavailable";case"invalid":return"Invalid subdomain";default:return}}),S=()=>{n.project.subdomain=A.formatSubdomain(n.project.subdomain),v()};function C(){n.project.resetChanges(),o.value=void 0}return(l,_)=>(m(),B(e(H),{direction:"vertical"},{default:a(()=>[t(e(f),{level:2},{default:a(()=>[r("Subdomain")]),_:1}),t(e(h),null,{default:a(()=>[r(" Every project in Abstra Cloud comes with a default subdomain, which will appear on all shared project links. ")]),_:1}),t(e(p),null,{default:a(()=>[t(e(s),null,{default:a(()=>[r("Forms available at:")]),_:1}),t(e(s),{code:""},{default:a(()=>[i("span",null,d(l.project.getUrl("[PATH]")),1)]),_:1})]),_:1}),t(e(p),null,{default:a(()=>[t(e(s),null,{default:a(()=>[r("Hooks available at:")]),_:1}),t(e(s),{code:""},{default:a(()=>[i("span",null,d(l.project.getUrl("_hooks/[PATH]")),1)]),_:1})]),_:1}),t(e(V),null,{default:a(()=>[t(e(N),{"validate-status":b.value,help:w.value,"has-feedback":""},{default:a(()=>[t(e(F),{value:l.project.subdomain,"onUpdate:value":_[0]||(_[0]=D=>l.project.subdomain=D),type:"text",loading:o.value==="loading",onBlur:S},{addonBefore:a(()=>[r("https://")]),addonAfter:a(()=>[r(".abstra.app")]),_:1},8,["value","loading"])]),_:1},8,["validate-status","help"]),t(U,{model:l.project,disabled:o.value!=="available",onError:C},null,8,["model","disabled"])]),_:1}),l.project.customDomain?(m(),y("div",R,[t(e(f),{level:2},{default:a(()=>[r("Custom Domain")]),_:1}),t(e(h),null,{default:a(()=>[r(" Your project also has a custom domain: "),t(e(s),{code:""},{default:a(()=>[i("span",null,d(l.project.customDomain),1)]),_:1})]),_:1}),t(e(p),null,{default:a(()=>[t(e(s),null,{default:a(()=>[r("Forms available at:")]),_:1}),t(e(s),{code:""},{default:a(()=>[i("span",null,d(l.project.getCustomDomainUrl("[PATH]")),1)]),_:1})]),_:1}),t(e(p),null,{default:a(()=>[t(e(s),null,{default:a(()=>[r("Hooks available at:")]),_:1}),t(e(s),{code:""},{default:a(()=>[i("span",null,d(l.project.getCustomDomainUrl("_hooks/[PATH]")),1)]),_:1})]),_:1})])):k("",!0)]),_:1}))}}),q={key:0,class:"project-settings"},te=j({__name:"ProjectSettings",setup(u){const o=E().params.projectId,{result:c}=I(()=>A.get(o));return(v,b)=>e(c)?(m(),y("div",q,[t(e(f),null,{default:a(()=>[r("Project Settings")]),_:1}),t($,{project:e(c)},null,8,["project"])])):k("",!0)}});export{te as default};
//# sourceMappingURL=ProjectSettings.c70c409c.js.map
