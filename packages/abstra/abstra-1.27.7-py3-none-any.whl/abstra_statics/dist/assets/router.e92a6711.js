var b=Object.defineProperty;var R=(o,t,e)=>t in o?b(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e;var h=(o,t,e)=>(R(o,typeof t!="symbol"?t+"":t,e),e);import{C as T,R as v}from"./FormItem.2257bb18.js";import{B as y,cO as f,g as I,h as O,_ as n}from"./outputWidgets.c6b12f47.js";import{o as A}from"./jwt-decode.esm.74bd4619.js";import{S as l}from"./storage.2451d8d4.js";import{u as P}from"./index.cef27eee.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[t]="e52e60ae-de36-48f7-81b0-763bace73a1f",o._sentryDebugIdIdentifier="sentry-dbid-e52e60ae-de36-48f7-81b0-763bace73a1f")}catch{}})();const B=y(T),x=y(v);class g{static async trackSession(t){const e=Object.fromEntries(document.cookie.split("; ").map(r=>r.split(/=(.*)/s).map(decodeURIComponent))),a=new URLSearchParams(window.location.search).get("session")||e.abstra_session;await fetch("https://usage-api.abstra.cloud/api/rest/session",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({referrer:document.referrer,href:location.href,queryParams:Object.fromEntries(new URLSearchParams(location.search)),previousSessionId:a,email:t})})}static async trackPageView(t){const e=Object.fromEntries(document.cookie.split("; ").map(r=>r.split(/=(.*)/s).map(decodeURIComponent))),a=new URLSearchParams(window.location.search).get("session")||e.abstra_session;await fetch("https://usage-api.abstra.cloud/api/rest/hackerforms/browser",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({previousSessionId:a,author_email:t,type:"PageView",payload:{referrer:document.referrer,href:location.href,queryParams:Object.fromEntries(new URLSearchParams(location.search))}})})}}const L=()=>window.location.host.includes(".abstra.io"),D={"cloud-api":"/api/cloud-api"},V={"cloud-api":"https://cloud-api.abstra.cloud"},j=o=>{const t="VITE_"+f.toUpper(f.snakeCase(o)),e={VITE_SENTRY_RELEASE:"52e4b1be678a6bf172214a9661c67c25581a2e12",BASE_URL:"/",MODE:"production",DEV:!1,PROD:!0}[t];return e||(L()?D[o]:V[o])},p={cloudApi:j("cloud-api")};class m extends Error{constructor(t,e){super(t),this.status=e}static async fromResponse(t){const e=await t.text();return new m(e,t.status)}}class E{static async get(t,e){const a=Object.fromEntries(Object.entries(e!=null?e:{}).filter(([,u])=>u!=null)),r=`?${new URLSearchParams(a).toString()}`,s=await fetch(`${p.cloudApi}/console/${t}${r}`,{headers:{...i.headers}});s.status===403&&(window.location.href="/login");const c=await s.text();return c?JSON.parse(c):null}static async getBlob(t){return await(await fetch(`${p.cloudApi}/console/${t}`,{headers:{...i.headers}})).blob()}static async post(t,e,a){const r=!!(a!=null&&a["Content-Type"])&&a["Content-Type"]!=="application/json",s=await fetch(`${p.cloudApi}/console/${t}`,{method:"POST",headers:{"Content-Type":"application/json",...i.headers,...a},body:r?e:JSON.stringify(e)});if(!s.ok)throw await m.fromResponse(s);const c=await s.text();return c?JSON.parse(c):null}static async patch(t,e){const a=await fetch(`${p.cloudApi}/console/${t}`,{method:"PATCH",headers:{"Content-Type":"application/json",...i.headers},body:JSON.stringify(e)});if(!a.ok)throw await m.fromResponse(a);const r=await a.text();return r?JSON.parse(r):null}static async delete(t){const e=await fetch(`${p.cloudApi}/console/${t}`,{method:"DELETE",headers:{"Content-Type":"application/json",...i.headers}});if(!e.ok)throw await m.fromResponse(e)}}const _=class{async authenticate(t){try{return await E.post("authn/authenticate",{email:t}),null}catch(e){return e.message}}async verify(t,e){const a=await E.post("authn/verify",{email:t,token:e});if(!(a&&"jwt"in a))throw new Error("Invalid token");return this.saveJWT(a.jwt),g.trackSession(t),this.getAuthor()}saveJWT(t){l.set(_.key,t)}getJWT(){return l.get(_.key)}getAuthor(){const t=this.getJWT();if(t)try{const e=A(t);if(e.exp&&e.exp>Date.now()/1e3)return{jwt:t,claims:e}}catch{console.warn("Invalid JWT")}return null}removeAuthor(){l.remove(_.key)}get headers(){const t=this.getJWT();return t?{"Author-Authorization":`Bearer ${t}`}:{}}};let d=_;h(d,"key","abstracloud:auth:jwt");const i=new d,w=I({history:O("/"),routes:[{path:"/widget-preview",name:"widget-preview",meta:{allowUnauthenticated:!0},component:()=>n(()=>import("./WidgetPreview.baa67577.js"),["assets/WidgetPreview.baa67577.js","assets/ActionButton.f771a894.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/ActionButton.f74e60ec.css","assets/WidgetsFrame.020d847d.js","assets/WidgetsFrame.97ae601d.css","assets/WidgetPreview.2be4ed12.css"])},{path:"/login",name:"login",meta:{allowUnauthenticated:!0},component:()=>n(()=>import("./Login.aa8ed483.js"),["assets/Login.aa8ed483.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/CircularLoading.6d50bc26.js","assets/CircularLoading.f81b57b4.css","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/member.5b862810.js","assets/WidgetsFrame.020d847d.js","assets/WidgetsFrame.97ae601d.css","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/jwt-decode.esm.74bd4619.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js","assets/Login.6f9ffede.css"])},{path:"/api-key",name:"api-key",component:()=>n(()=>import("./ReturnApiKey.f6c83967.js"),["assets/ReturnApiKey.f6c83967.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/apiKey.a75be50e.js","assets/project.6182e90d.js","assets/organization.be70a7ac.js","assets/asyncComputed.99914932.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/index.36688629.js","assets/Modal.7a04b2f5.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js","assets/ReturnApiKey.909cd622.css"])},{path:"/",name:"home",redirect:{name:"organizations"}},{path:"/organizations",name:"organizations",component:()=>n(()=>import("./Organizations.3d4e2b80.js"),["assets/Organizations.3d4e2b80.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/organization.be70a7ac.js","assets/Navbar.vue_vue_type_script_setup_true_lang.3897cd7f.js","assets/logo.084e5d7c.js","assets/Text.3372b6bf.js","assets/index.cd9ab856.js","assets/Navbar.f4a98ea3.css","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/BaseLayout.b0f5c7c3.js","assets/BaseLayout.881bfa61.css","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"/organizations/:organizationId",name:"organization",component:()=>n(()=>import("./Organization.cb422ba6.js"),["assets/Organization.cb422ba6.js","assets/Sidebar.6705fcda.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/index.c1b6adb2.js","assets/Sidebar.055402cc.css","assets/Navbar.vue_vue_type_script_setup_true_lang.3897cd7f.js","assets/logo.084e5d7c.js","assets/asyncComputed.99914932.js","assets/Text.3372b6bf.js","assets/index.cd9ab856.js","assets/Navbar.f4a98ea3.css","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/organization.be70a7ac.js","assets/BaseLayout.b0f5c7c3.js","assets/BaseLayout.881bfa61.css","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"]),redirect:{name:"projects"},children:[{path:"projects",name:"projects",component:()=>n(()=>import("./Projects.dae1f840.js"),["assets/Projects.dae1f840.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/project.6182e90d.js","assets/organization.be70a7ac.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"settings",name:"organization-settings",component:()=>n(()=>import("./OrganizationSettings.70b961fe.js"),["assets/OrganizationSettings.70b961fe.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css"])},{path:"members",name:"members",component:()=>n(()=>import("./Members.8986fd38.js"),["assets/Members.8986fd38.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/asyncComputed.99914932.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/member.5b862810.js","assets/CrudView.f289f315.js","assets/icons.43aa926b.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/jwt-decode.esm.74bd4619.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"billing",name:"billing",component:()=>n(()=>import("./Billing.99727a2f.js"),["assets/Billing.99727a2f.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/organization.be70a7ac.js","assets/asyncComputed.99914932.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/index.5bfbc989.js","assets/index.ef082e10.js","assets/Card.9a2b3d3e.js","assets/TabPane.80ecc0b7.js","assets/hasIn.58982ae4.js","assets/FormItem.2257bb18.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])}]},{path:"/projects/:projectId",name:"project",component:()=>n(()=>import("./Project.f82207cc.js"),["assets/Project.f82207cc.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/BaseLayout.b0f5c7c3.js","assets/BaseLayout.881bfa61.css","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/project.6182e90d.js","assets/organization.be70a7ac.js","assets/Navbar.vue_vue_type_script_setup_true_lang.3897cd7f.js","assets/logo.084e5d7c.js","assets/Text.3372b6bf.js","assets/index.cd9ab856.js","assets/Navbar.f4a98ea3.css","assets/Sidebar.6705fcda.js","assets/icons.43aa926b.js","assets/index.c1b6adb2.js","assets/Sidebar.055402cc.css","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"]),redirect:{name:"live"},children:[{path:"live",name:"live",component:()=>n(()=>import("./Live.5729a49c.js"),["assets/Live.5729a49c.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/build.de7237d5.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/project.6182e90d.js","assets/CrudView.f289f315.js","assets/icons.43aa926b.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/ExecutionStatusIcon.vue_vue_type_script_setup_true_lang.e23663a3.js","assets/CheckCircleFilled.7eee08f1.js","assets/index.36688629.js","assets/Link.ed78a9f2.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js","assets/Live.8870c9e7.css"])},{path:"builds",name:"builds",component:()=>n(()=>import("./Builds.ddc24b53.js"),["assets/Builds.ddc24b53.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/build.de7237d5.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/project.6182e90d.js","assets/CrudView.f289f315.js","assets/icons.43aa926b.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/index.f5cf641c.js","assets/datetime.74210d1c.js","assets/index.cef27eee.js","assets/storage.2451d8d4.js","assets/Builds.eeb5cc41.css"])},{path:"connectors",name:"connectors",component:()=>n(()=>import("./Connectors.f8c8410f.js"),["assets/Connectors.f8c8410f.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/jwt-decode.esm.74bd4619.js","assets/connector.2bb7d592.js","assets/asyncComputed.99914932.js","assets/icons.43aa926b.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"tables",name:"tables",component:()=>n(()=>import("./Tables.85903e7d.js"),["assets/Tables.85903e7d.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/tables.4e918c51.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/string.0f0ba6dc.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"api-keys",name:"api-keys",component:()=>n(()=>import("./ApiKeys.091b42c2.js"),["assets/ApiKeys.091b42c2.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/index.cef27eee.js","assets/icons.43aa926b.js","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/member.5b862810.js","assets/apiKey.a75be50e.js","assets/project.6182e90d.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/storage.2451d8d4.js"])},{path:"logs",name:"logs",component:()=>n(()=>import("./Logs.fd55054c.js"),["assets/Logs.fd55054c.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/jwt-decode.esm.74bd4619.js","assets/build.de7237d5.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/ExecutionStatusIcon.vue_vue_type_script_setup_true_lang.e23663a3.js","assets/CheckCircleFilled.7eee08f1.js","assets/datetime.74210d1c.js","assets/dayjs.42afc0b6.js","assets/index.af14be85.js","assets/index.c1b6adb2.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/index.36688629.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/CollapsePanel.6cefc28a.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"legacy-logs",name:"legacy-logs",component:()=>n(()=>import("./LegacyLogs.0c44e12b.js"),["assets/LegacyLogs.0c44e12b.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/Modal.7a04b2f5.js","assets/StarFilled.fad29e50.js","assets/Timeline.ba10013e.js","assets/CheckCircleFilled.7eee08f1.js","assets/index.cef27eee.js","assets/jwt-decode.esm.74bd4619.js","assets/build.de7237d5.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/asyncComputed.99914932.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/index.36688629.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/dayjs.42afc0b6.js","assets/index.af14be85.js","assets/index.c1b6adb2.js","assets/Form.4b59ec63.js","assets/storage.2451d8d4.js","assets/LegacyLogs.752e315d.css"])},{path:"settings",name:"project-settings",component:()=>n(()=>import("./ProjectSettings.0f4191cb.js"),["assets/ProjectSettings.0f4191cb.js","assets/asyncComputed.99914932.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/project.6182e90d.js","assets/SaveButton.vue_vue_type_script_setup_true_lang.a7eaebe6.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"env-vars",name:"env-vars",component:()=>n(()=>import("./EnvVars.41fb28a2.js"),["assets/EnvVars.41fb28a2.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/asyncComputed.99914932.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/icons.43aa926b.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])},{path:"files",name:"files",component:()=>n(()=>import("./Files.25e33987.js"),["assets/Files.25e33987.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/asyncComputed.99914932.js","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/Modal.7a04b2f5.js","assets/popupNotifcation.7f5182e3.js","assets/DownloadOutlined.c29e0df6.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/Card.9a2b3d3e.js","assets/TabPane.80ecc0b7.js","assets/hasIn.58982ae4.js","assets/FormItem.2257bb18.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js","assets/Files.fefbf3f0.css"])},{path:"users",name:"users",component:()=>n(()=>import("./Users.bb6b799a.js"),["assets/Users.bb6b799a.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/icons.43aa926b.js","assets/asyncComputed.99914932.js","assets/index.cf4c23b9.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/Form.4b59ec63.js","assets/index.d300c7ea.js","assets/isNumeric.75337b1e.js","assets/jwt-decode.esm.74bd4619.js","assets/index.bc2c15a2.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/CrudView.f289f315.js","assets/Title.53f8527b.js","assets/Text.3372b6bf.js","assets/Modal.7a04b2f5.js","assets/DocsButton.vue_vue_type_script_setup_true_lang.5349014a.js","assets/url.3f6b6909.js","assets/index.c1b6adb2.js","assets/CrudView.4c069239.css","assets/popupNotifcation.7f5182e3.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js"])}]},{path:"/projects/:projectId/tables/:tableId",name:"tableEditor",component:()=>n(()=>import("./TableEditor.554fde91.js"),["assets/TableEditor.554fde91.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/tables.4e918c51.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/string.0f0ba6dc.js","assets/BaseLayout.b0f5c7c3.js","assets/BaseLayout.881bfa61.css","assets/asyncComputed.99914932.js","assets/popupNotifcation.7f5182e3.js","assets/index.ef082e10.js","assets/Form.4b59ec63.js","assets/FormItem.2257bb18.js","assets/hasIn.58982ae4.js","assets/index.d300c7ea.js","assets/isNumeric.75337b1e.js","assets/jwt-decode.esm.74bd4619.js","assets/project.6182e90d.js","assets/organization.be70a7ac.js","assets/icons.43aa926b.js","assets/index.d69f3ec4.js","assets/CircularLoading.6d50bc26.js","assets/CircularLoading.f81b57b4.css","assets/TabPane.80ecc0b7.js","assets/index.cd9ab856.js","assets/Text.3372b6bf.js","assets/storage.2451d8d4.js","assets/index.cef27eee.js","assets/TableEditor.00c1ec33.css"])},{path:"/connectors/:connectorId",name:"connectorEditor",component:()=>n(()=>import("./ConnectorEditor.54ee327f.js"),["assets/ConnectorEditor.54ee327f.js","assets/outputWidgets.c6b12f47.js","assets/outputWidgets.3c848cd5.css","assets/BaseLayout.b0f5c7c3.js","assets/BaseLayout.881bfa61.css","assets/asyncComputed.99914932.js","assets/index.bc2c15a2.js","assets/index.cf4c23b9.js","assets/record.f0b2bfdd.js","assets/pubsub.d22b40f3.js","assets/SaveButton.vue_vue_type_script_setup_true_lang.0f709681.js","assets/ant-design.ee7cb87b.js","assets/index.f7c8eeb4.js","assets/Modal.7a04b2f5.js","assets/storage.2451d8d4.js","assets/Link.ed78a9f2.js","assets/Text.3372b6bf.js","assets/index.0869e6f5.js","assets/Title.53f8527b.js","assets/SaveButton.13ece1cb.css","assets/jwt-decode.esm.74bd4619.js","assets/project.6182e90d.js","assets/connector.2bb7d592.js","assets/organization.be70a7ac.js","assets/TabPane.80ecc0b7.js","assets/hasIn.58982ae4.js","assets/index.cd9ab856.js","assets/Form.4b59ec63.js","assets/FormItem.2257bb18.js","assets/index.ef082e10.js","assets/index.cef27eee.js","assets/ConnectorEditor.77a62f6e.css"])}],scrollBehavior(o){if(o.hash)return{el:o.hash}}});w.beforeEach(async(o,t)=>{P(o,t);const e=i.getAuthor();if(g.trackPageView(e==null?void 0:e.claims.email),!o.meta.allowUnauthenticated&&!e){await w.push({name:"login",query:{...o.query,redirect:o.path,"prev-redirect":o.query.redirect}});return}});export{B as A,E as C,x as a,i as b,w as r};
//# sourceMappingURL=router.e92a6711.js.map
