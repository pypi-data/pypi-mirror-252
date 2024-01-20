import{d as J,r as q,G as L,F as se,b as s,ev as T,f as t,w as a,bq as F,aq as S,eD as K,ex as D,e as w,u as e,cx as re,bO as O,cE as ie,cC as W,eC as Y,c as C,bH as V,eL as X,a as Z,ad as te,cB as de,bg as ce,v as ae,H as he,eA as pe,eE as me,eF as fe,eB as _e,eK as ke}from"./outputWidgets.ed48fa42.js";import{p as ve,T as Ce}from"./tables.289ddc57.js";import{B as we}from"./BaseLayout.d9525cfc.js";import{a as le}from"./asyncComputed.bb2b1403.js";import{p as H}from"./popupNotifcation.e339c81d.js";import{A as ye}from"./index.23112e9a.js";import{F as ne}from"./Form.471d6bcc.js";import{A as N}from"./FormItem.c1c36356.js";import{A as oe}from"./index.65c4e78e.js";import"./router.1b12d634.js";import{P as De}from"./project.74c1366e.js";import"./index.5e38be4e.js";import{O as $e}from"./organization.96c70a51.js";import{T as Se,U as Ie,V as Ue,W as Te,X as xe,J as Ee,Y as Ne}from"./icons.92b5bc38.js";import{A as Q}from"./index.214fcc89.js";import{L as Ae}from"./CircularLoading.96c0f42c.js";import{T as Be,A as ee}from"./TabPane.9d812117.js";import{B as qe,a as Le,c as ze}from"./index.ce22d79e.js";import"./record.2ea2ab4d.js";import"./pubsub.90864e85.js";import"./string.2456334b.js";import"./hasIn.a220eabf.js";import"./isNumeric.75337b1e.js";import"./index.60984836.js";import"./index.cf4c23b9.js";import"./Text.b5b9d884.js";(function(){try{var h=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},b=new Error().stack;b&&(h._sentryDebugIds=h._sentryDebugIds||{},h._sentryDebugIds[b]="0a7e061f-d832-4945-8557-138661b48d76",h._sentryDebugIdIdentifier="sentry-dbid-0a7e061f-d832-4945-8557-138661b48d76")}catch{}})();const Re={class:"table-data",style:{width:"calc(100% - 80px)"}},Oe={key:1},Pe=["onClick"],je=w("a",null,"Delete",-1),Ve=J({__name:"TableData",props:{table:{}},setup(h){var i,p;const b=h,l=q(1),f=q(10),x=L(()=>{var c,n;return{total:(n=(c=r.value)==null?void 0:c.total)!=null?n:0,current:l.value,pageSize:f.value,totalBoundaryShowSizeChanger:10,showSizeChanger:!0,pageSizeOptions:["10","25","50","100"],onChange:async(U,j)=>{l.value=U,f.value=j,await v()}}}),m=L(()=>{var c;return((c=r.value)==null?void 0:c.rows.length)===1}),{result:r,loading:I,refetch:v}=le(()=>b.table.select({},(l.value-1)*f.value,f.value)),g=(c,n)=>U=>{if(c==="json"&&U==""){o.value[n]="null";return}o.value[n]=U},A=(i=b.table)==null?void 0:i.getColumns().map(c=>({title:c.name,dataIndex:c.name,resizable:!0,minWidth:100,ellipsis:!1})),_=q([...A,{title:"",key:"action",fixed:"right",width:150,align:"center"}]);function u(c,n){n.width=c}const y=L(()=>{var c;return((c=r.value)==null?void 0:c.rows.map(n=>({key:n.id,...n})))||[]}),$=q(!1),o=q({}),d=()=>{$.value=!0},k=()=>{o.value={},$.value=!1};let E=se((p=b.table)==null?void 0:p.getUnprotectedColumns().reduce((c,n)=>({...c,[n.name]:""}),{}));async function z(){if(!(!b.table||!E))try{o.value.id?await b.table.updateRow(o.value.id,o.value):await b.table.insertRow(o.value),o.value={},v(),k()}catch(c){c instanceof Error&&H("Database error",c.message)}}const B=async c=>{if(!(!r.value||!r.value.rows.find(n=>n.id===c)))try{await b.table.deleteRow(c),m.value&&(l.value=Math.max(1,l.value-1)),v()}catch(n){n instanceof Error&&H("Database error",n.message)}},P=c=>{var M;const n=(M=y.value)==null?void 0:M.filter(R=>c===R.key)[0],U=b.table.getColumns(),j=U.map(R=>R.name),G=U.filter(R=>R.type==="json").map(R=>R.name);o.value=X.exports.pick(X.exports.cloneDeep(n),j),G.forEach(R=>{o.value[R]&&(o.value[R]=JSON.stringify(o.value[R]))}),d()};return(c,n)=>(s(),T("div",Re,[t(e(ie),{columns:_.value,"data-source":y.value,pagination:x.value,bordered:"",loading:e(I),scroll:{x:2e3,y:720},size:"small",onResizeColumn:u},{bodyCell:a(({column:U,text:j,record:G})=>[_.value.map(M=>M.title).includes(U.dataIndex)?(s(),T(F,{key:0},[S(K(j),1)],64)):D("",!0),U.key==="action"?(s(),T("div",Oe,[w("span",null,[w("a",{onClick:M=>P(G.id)},"Edit",8,Pe)]),t(e(ye),{type:"vertical"}),t(e(re),{title:"Sure to delete?",onConfirm:M=>B(G.id)},{default:a(()=>[je]),_:2},1032,["onConfirm"])])):D("",!0)]),footer:a(()=>[t(e(O),{type:"primary",onClick:d},{default:a(()=>[S("+ Add New Data")]),_:1})]),_:1},8,["columns","data-source","pagination","loading"]),t(e(oe),{title:"Data",width:720,open:$.value,"body-style":{paddingBottom:"80px"},"footer-style":{textAlign:"right"},onClose:k},{extra:a(()=>[t(e(W),null,{default:a(()=>[t(e(O),{onClick:k},{default:a(()=>[S("Cancel")]),_:1}),t(e(O),{type:"primary",onClick:z},{default:a(()=>[S("Submit")]),_:1})]),_:1})]),default:a(()=>[t(e(ne),{model:o.value,layout:"vertical"},{default:a(()=>[(s(!0),T(F,null,Y(c.table.getUnprotectedColumns(),U=>(s(),C(e(N),{key:U.id,label:U.name},{default:a(()=>[o.value?(s(),C(e(V),{key:0,value:o.value[U.name],"onUpdate:value":j=>g(U.type,U.name)(j)},null,8,["value","onUpdate:value"])):D("",!0)]),_:2},1032,["label"]))),128))]),_:1},8,["model"])]),_:1},8,["open"])]))}});const ge=(h,b)=>b.includes(h)?{status:"error",help:"There already is a column with this name in the table"}:{status:""},Fe=J({__name:"NewColumn",props:{open:{type:Boolean},table:{}},emits:["created","cancel"],setup(h,{emit:b}){const l=h,f=L(()=>{var u;return((u=l.table)==null?void 0:u.getColumns().map(y=>y.name))||[]}),x=L(()=>ge(m.value.name,f.value)),m=q({name:"",type:"varchar",default:"''",nullable:!0,unique:!1}),r=q({error:"success",message:"",fakeLoading:!1}),I=()=>{r.value.fakeLoading=!0,v()},v=X.exports.debounce(async()=>{var y;const u=`select (${m.value.default})::${m.value.type} `;(y=l.table)==null||y.executeQuery(u,[]).then($=>{r.value.error=$.errors.length>0?"error":"success",r.value.message=$.errors[0]||"",r.value.fakeLoading=!1})},500),g=()=>{m.value={name:"",type:"varchar",default:"''",nullable:!0,unique:!1}};function A(){b("cancel")}async function _(){if(!!l.table&&!(!m.value.name||!m.value.type))try{await l.table.addColumn(m.value),g(),b("created")}catch(u){u instanceof Error&&H("Database error",u.message)}}return(u,y)=>{const $=Z("icon");return s(),C(e(oe),{title:"New column",width:720,open:l.open,"body-style":{paddingBottom:"80px"},"footer-style":{textAlign:"right"},onClose:A},{extra:a(()=>[t(e(W),null,{default:a(()=>[t(e(O),{onClick:A},{default:a(()=>[S("Cancel")]),_:1}),t(e(O),{type:"primary",onClick:_},{default:a(()=>[S("Submit")]),_:1})]),_:1})]),default:a(()=>[t(e(ne),{model:m.value,layout:"vertical"},{default:a(()=>[t(e(N),{key:"name",label:"Name",required:!0,"validate-status":x.value.status,help:x.value.help},{default:a(()=>[t(e(V),{value:m.value.name,"onUpdate:value":y[0]||(y[0]=o=>m.value.name=o)},null,8,["value"])]),_:1},8,["validate-status","help"]),t(e(N),{key:"type",label:"Type",required:!0},{default:a(()=>[t(e(te),{value:m.value.type,"onUpdate:value":y[1]||(y[1]=o=>m.value.type=o),"default-active-first-option":"",onChange:I},{default:a(()=>[(s(!0),T(F,null,Y(e(ve),o=>(s(),C(e(de),{key:o,value:o},{default:a(()=>[S(K(o),1)]),_:2},1032,["value"]))),128))]),_:1},8,["value"])]),_:1}),t(e(N),{key:"default-value",label:"Default value","validate-status":r.value.error,help:r.value.message},{default:a(()=>[t(e(V),{value:m.value.default,"onUpdate:value":y[2]||(y[2]=o=>m.value.default=o),onInput:I},{suffix:a(()=>[r.value.fakeLoading?(s(),C(e(ce),{key:0})):D("",!0),!r.value.fakeLoading&&r.value.error==="success"?(s(),C($,{key:1,path:e(Se)},null,8,["path"])):D("",!0),!r.value.fakeLoading&&r.value.error==="error"?(s(),C($,{key:2,path:e(Ie)},null,8,["path"])):D("",!0)]),_:1},8,["value"])]),_:1},8,["validate-status","help"]),t(e(N),{key:"nullable",label:"Nullable"},{default:a(()=>[t(e(Q),{checked:m.value.nullable,"onUpdate:checked":y[3]||(y[3]=o=>m.value.nullable=o)},null,8,["checked"])]),_:1}),t(e(N),{key:"unique",label:"Unique"},{default:a(()=>[t(e(Q),{checked:m.value.unique,"onUpdate:checked":y[4]||(y[4]=o=>m.value.unique=o)},null,8,["checked"])]),_:1})]),_:1},8,["model"])]),_:1},8,["open"])}}}),Ke={class:"types-container"},Me={class:"fullwidth-input"},He={class:"fullwidth-input"},Je={class:"using-container"},Qe={class:"fullwidth-input"},We=J({__name:"UpdateColumn",props:{open:{type:Boolean},table:{},column:{}},emits:["updated","cancel"],setup(h,{emit:b}){const l=h,f=L(()=>{var i;return((i=l.table)==null?void 0:i.getColumns().map(p=>p.record.initialState.name))||[]}),x=L(()=>l.column.name===l.column.record.initialState.name?{status:"",help:""}:ge(l.column.name,f.value)),{result:m,loading:r}=le(async()=>l.table.select({},10,0).then(({total:i})=>i));function I(){l.column.record.resetChanges(),b("cancel")}const v=q({error:"success",message:"",fakeLoading:!1}),g=()=>{v.value.fakeLoading=!0,A()},A=X.exports.debounce(async()=>{var c;if(!l.column.default){v.value.fakeLoading=!1;return}const i=`select (${l.column.default})::${l.column.type} `,p=await((c=l.table)==null?void 0:c.executeQuery(i,[]));v.value.error=p.errors.length>0?"error":"success",v.value.message=p.errors[0]||"",v.value.fakeLoading=!1},500),_=()=>m.value===0||r.value?!1:l.column.record.hasChangesDeep("type"),u=q({type:"default"});function y(i,p){return p==="varchar"||i==="int"&&p==="boolean"||i==="boolean"&&p==="int"}const $=()=>{g(),o.value||(u.value={type:"user-defined",using:B.value,mandatory:!0})},o=L(()=>u.value.type==="default"&&y(l.column.record.initialState.type,l.column.type)),d=L(()=>!y(l.column.record.initialState.type,l.column.type));function k(i){i?u.value={type:"default"}:u.value={type:"user-defined",using:B.value,mandatory:!1}}function E(i){if(u.value.type==="default")throw new Error("Can't change using when using default casting");u.value.using=i!=null?i:""}const z=()=>d.value?!0:_()&&u.value.type==="user-defined",B=L(()=>`${l.column.record.initialState.name}::${l.column.type}`);async function P(){if(!l.column)return;let i=u.value.type==="default"?B.value:u.value.using;m.value===0&&(i=`${l.column.name}::text::${l.column.type}`);try{await l.column.update(i),b("updated")}catch(p){p instanceof Error&&H("Database error",p.message)}}return(i,p)=>{const c=Z("icon");return s(),C(e(oe),{title:"Edit column",width:720,open:i.open,"body-style":{paddingBottom:"80px"},"footer-style":{textAlign:"right"},onClose:I},{extra:a(()=>[t(e(W),null,{default:a(()=>[t(e(O),{onClick:I},{default:a(()=>[S("Cancel")]),_:1}),t(e(O),{type:"primary",onClick:P},{default:a(()=>[S("Submit")]),_:1})]),_:1})]),default:a(()=>[t(e(ne),{model:i.column,layout:"vertical"},{default:a(()=>[t(e(N),{key:"name",label:"Name","validate-status":x.value.status,help:x.value.help},{default:a(()=>[t(e(V),{value:i.column.name,"onUpdate:value":p[0]||(p[0]=n=>i.column.name=n)},null,8,["value"])]),_:1},8,["validate-status","help"]),w("div",Ke,[w("span",Me,[t(e(N),{key:"type",label:"Current Type"},{default:a(()=>[t(e(te),{value:i.column.record.initialState.type,"onUpdate:value":p[1]||(p[1]=n=>i.column.record.initialState.type=n),"default-active-first-option":"",disabled:""},null,8,["value"])]),_:1})]),t(c,{class:"right-arrow",path:e(Ue)},null,8,["path"]),w("span",He,[t(e(N),{key:"new-type",label:"New Type"},{default:a(()=>[t(e(te),{value:i.column.type,"onUpdate:value":p[2]||(p[2]=n=>i.column.type=n),"default-active-first-option":"",onChange:p[3]||(p[3]=n=>$())},{default:a(()=>[(s(!0),T(F,null,Y(e(ve),n=>(s(),C(e(de),{key:n,value:n},{default:a(()=>[S(K(n),1)]),_:2},1032,["value"]))),128))]),_:1},8,["value"])]),_:1})])]),t(e(N),{key:"default-value",label:"Default value","validate-status":v.value.error,help:v.value.message},{default:a(()=>[t(e(V),{value:i.column.default,"onUpdate:value":p[4]||(p[4]=n=>i.column.default=n),onInput:g},{suffix:a(()=>[v.value.fakeLoading?(s(),C(e(ce),{key:0,size:"small"})):D("",!0),!v.value.fakeLoading&&v.value.error==="success"?(s(),C(c,{key:1,path:e(Te),width:"18",height:"18"},null,8,["path"])):D("",!0),!v.value.fakeLoading&&v.value.error==="error"?(s(),C(c,{key:2,path:e(xe),width:"18",height:"18"},null,8,["path"])):D("",!0)]),_:1},8,["value"])]),_:1},8,["validate-status","help"]),w("div",Je,[_()?(s(),C(e(N),{key:"default-casting",label:"Use default casting"},{default:a(()=>[t(e(Q),{checked:o.value,disabled:d.value,"onUpdate:checked":p[5]||(p[5]=n=>k(!!n))},null,8,["checked","disabled"])]),_:1})):D("",!0),w("span",Qe,[_()?(s(),C(e(N),{key:"using",label:"Using"},{default:a(()=>[t(e(V),{value:u.value.type==="user-defined"?u.value.using:B.value,disabled:!z(),onInput:p[6]||(p[6]=n=>E(n.target.value))},null,8,["value","disabled"])]),_:1})):D("",!0)])]),t(e(N),{key:"nullable",label:"Nullable"},{default:a(()=>[t(e(Q),{checked:i.column.nullable,"onUpdate:checked":p[7]||(p[7]=n=>i.column.nullable=n)},null,8,["checked"])]),_:1}),t(e(N),{key:"unique",label:"Unique"},{default:a(()=>[t(e(Q),{checked:i.column.unique,"onUpdate:checked":p[8]||(p[8]=n=>i.column.unique=n)},null,8,["checked"])]),_:1})]),_:1},8,["model"])]),_:1},8,["open"])}}});const Ge=ae(We,[["__scopeId","data-v-2dd03764"]]),be=h=>(me("data-v-dc242058"),h=h(),fe(),h),Xe={class:"table-settings"},Ye={key:0},Ze=be(()=>w("span",null," protected ",-1)),et=[Ze],tt={key:1},at=["onClick"],lt=be(()=>w("a",null,"Delete",-1)),nt=J({__name:"TableColumns",props:{table:{},loading:{type:Boolean}},emits:["refresh"],setup(h,{emit:b}){var o;const l=h,f=q(l.loading);he(()=>l.loading,()=>{f.value=l.loading});const x=pe();(o=l.table)==null||o.onUpdate(()=>{var d;x.replace({name:"tableEditor",params:{tableName:(d=l.table)==null?void 0:d.name}})});const r=[...[{title:"Name",dataIndex:"name",sorter:(d,k)=>d.name.localeCompare(k.name)},{title:"Type",dataIndex:"type",sorter:(d,k)=>d.type.localeCompare(k.type)},{title:"Default Value",dataIndex:"default",sorter:(d,k)=>{var E,z,B,P;return(P=(B=d.default)==null?void 0:B.localeCompare((z=(E=k.default)==null?void 0:E.toString())!=null?z:""))!=null?P:0}},{title:"Nullable",dataIndex:"nullable",sorter:(d,k)=>d.nullable||!k.nullable?1:-1},{title:"Unique",dataIndex:"unique",sorter:(d,k)=>d.unique||!k.unique?1:-1},{title:"Primary Key",dataIndex:"primaryKey",sorter:(d,k)=>d.primaryKey||!k.primaryKey?1:-1}],{title:"",key:"action"}],I=L(()=>{var d;return(d=l.table)==null?void 0:d.getColumns()});function v(){_.value={type:"idle"}}function g(){v(),f.value=!0,setTimeout(()=>{b("refresh")},500)}function A(){_.value={type:"creating"}}const _=q({type:"idle"});function u(d){var k,E;(E=(k=l.table)==null?void 0:k.getColumn(d))==null||E.delete(),f.value=!0,setTimeout(()=>{b("refresh")},500)}const y=d=>{var k,E,z;return(z=(E=(k=l.table)==null?void 0:k.getColumn(d))==null?void 0:E.protected)!=null?z:!1},$=d=>{if(!l.table)throw new Error("Table not found");_.value={type:"editing",column:l.table.getColumn(d)}};return(d,k)=>(s(),T("div",Xe,[t(e(ie),{columns:r,"data-source":I.value,bordered:"",loading:f.value,pagination:!1},{bodyCell:a(({column:E,text:z,record:B})=>[E.key!=="action"?(s(),T(F,{key:0},[S(K(z),1)],64)):(s(),T(F,{key:1},[y(B.id)?(s(),T("div",Ye,et)):(s(),T("div",tt,[w("span",null,[w("a",{onClick:()=>$(B.id)},"Edit",8,at)]),t(e(ye),{type:"vertical"}),t(e(re),{title:"Sure to delete?",onConfirm:P=>u(B.id)},{default:a(()=>[lt]),_:2},1032,["onConfirm"])]))],64))]),footer:a(()=>[t(e(O),{type:"primary",onClick:A},{default:a(()=>[S("+ Add New Column")]),_:1})]),_:1},8,["data-source","loading"]),d.table&&_.value.type==="creating"?(s(),C(Fe,{key:0,open:"",table:l.table,onClose:v,onCancel:v,onCreated:g},null,8,["table"])):D("",!0),d.table&&_.value.type==="editing"?(s(),C(Ge,{key:1,column:_.value.column,open:"",table:d.table,onUpdated:g,onClose:v,onCancel:v},null,8,["column","table"])):D("",!0)]))}});const ot=ae(nt,[["__scopeId","data-v-dc242058"]]),ue=h=>(me("data-v-06f57b7a"),h=h(),fe(),h),ut={class:"table-settings"},st=ue(()=>w("h2",{class:"title"},"Table settings",-1)),rt=ue(()=>w("div",{class:"subtitle"},"Edit table metadata",-1)),it={key:0,class:"table-presenter"},dt={class:"table-property-item"},ct={class:"property-item"},pt={key:1},mt={class:"change-warning"},ft={class:"section-title"},vt=ue(()=>w("div",{class:"section-body"}," Changing the table's name can possibly result in the break of running applications. ",-1)),yt={class:"table-name-value-input"},gt={key:0,class:"error"},bt=J({__name:"TableSettings",props:{table:{}},emits:["refresh"],setup(h,{emit:b}){const l=h,f=se({error:"",editing:!1,loading:!1}),x=()=>f.editing=!0,m=()=>{l.table.resetChanges(),f.editing=!1,f.error=""},r=async()=>{f.error="",f.loading=!0;try{await I()}catch(g){g instanceof Error&&(H("Database error",g.message),f.error=g.message)}f.error||(f.editing=!1),f.loading=!1},I=async()=>{if(!l.table.name){f.error="Table name cannot be empty";return}try{await l.table.save(),b("refresh")}catch(g){g instanceof Error&&(H("Database error",g.message),f.error=g.message)}},v=g=>{l.table.name=g.target.value};return(g,A)=>{var u;const _=Z("icon");return s(),T("div",ut,[st,rt,f.editing?(s(),T("div",pt,[w("div",mt,[w("div",ft,[t(_,{path:e(Ee),width:"12",height:"12",fill:"#D35249"},null,8,["path"]),S(" Be careful ")]),vt]),t(e(W),{direction:"vertical"},{default:a(()=>[w("div",yt,[t(e(V),{value:g.table.name,type:"text",onInput:v,onBlur:A[0]||(A[0]=y=>g.table.fixTraillingName())},null,8,["value"])]),f.error?(s(),T("div",gt,[t(_,{path:e(Ne),fill:"#D35249",width:"12",height:"12"},null,8,["path"]),S(" "+K(f.error),1)])):D("",!0),t(e(W),null,{default:a(()=>[t(e(O),{onClick:m},{default:a(()=>[S("Cancel")]),_:1}),t(e(O),{type:"primary",disabled:!g.table.hasChangesDeep("name"),onClick:r},{default:a(()=>[S(" Save Changes "),f.loading?(s(),C(Ae,{key:0,size:"16"})):D("",!0)]),_:1},8,["disabled"])]),_:1})]),_:1})])):(s(),T("div",it,[w("div",dt,[w("div",ct,"Name: "+K((u=g.table)==null?void 0:u.name),1)]),t(e(O),{onClick:x},{default:a(()=>[S("Edit Name")]),_:1})]))])}}});const ht=ae(bt,[["__scopeId","data-v-06f57b7a"]]),Ht=J({__name:"TableEditor",setup(h){const b=pe(),l=_e(),f=l.params.tableId,x=l.params.projectId,m=q("data"),{result:r,loading:I,refetch:v}=le(()=>Promise.all([De.get(x).then(async _=>{const u=await $e.get(_.organizationId);return{project:_,organization:u}}),Ce.get(x,f)]).then(([{project:_,organization:u},y])=>ke({project:_,organization:u,table:y}))),g=L(()=>!I.value&&r.value?[{label:"My organizations",path:"/organizations"},{label:r.value.organization.name,path:`/organizations/${r.value.organization.id}`},{label:r.value.project.name,path:`/projects/${r.value.project.id}/tables`}]:void 0);function A(){b.push({name:"tables",params:{projectId:x}})}return(_,u)=>{const y=Z("router-link");return s(),C(we,null,{navbar:a(()=>{var $;return[t(e(ze),{title:($=e(r))==null?void 0:$.table.name,style:{padding:"5px 25px"},onBack:A},{footer:a(()=>[t(e(Be),{"active-key":m.value,"onUpdate:activeKey":u[0]||(u[0]=o=>m.value=o)},{default:a(()=>[t(e(ee),{key:"data",tab:"Data"}),t(e(ee),{key:"columns",tab:"Columns"}),t(e(ee),{key:"settings",tab:"Settings"})]),_:1},8,["active-key"])]),breadcrumb:a(()=>[g.value?(s(),C(e(qe),{key:0},{default:a(()=>[(s(!0),T(F,null,Y(g.value,(o,d)=>(s(),C(e(Le),{key:d},{default:a(()=>[t(y,{to:o.path},{default:a(()=>[S(K(o.label),1)]),_:2},1032,["to"])]),_:2},1024))),128))]),_:1})):D("",!0)]),_:1},8,["title"])]}),content:a(()=>[e(r)&&m.value==="data"?(s(),C(Ve,{key:0,loading:e(I),table:e(r).table},null,8,["loading","table"])):D("",!0),e(r)&&m.value==="columns"?(s(),C(ot,{key:1,table:e(r).table,loading:e(I),onRefresh:u[1]||(u[1]=$=>e(v)())},null,8,["table","loading"])):D("",!0),e(r)&&m.value==="settings"?(s(),C(ht,{key:2,table:e(r).table,loading:e(I),onRefresh:u[2]||(u[2]=$=>e(v)())},null,8,["table","loading"])):D("",!0)]),_:1})}}});export{Ht as default};
//# sourceMappingURL=TableEditor.223b1af5.js.map
