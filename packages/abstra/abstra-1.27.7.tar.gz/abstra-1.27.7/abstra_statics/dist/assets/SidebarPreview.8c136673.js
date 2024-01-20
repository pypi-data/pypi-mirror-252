import{P as b}from"./PlayerNavbar.df3bb374.js";import{W as m}from"./WidgetsFrame.020d847d.js";import{m as y}from"./workspaces.1c1d2e24.js";import{d as k,F as n,b as t,et as o,f as u,w as d,ao as g,u as c,e as f,c as p,ev as h,bo as w,eA as x,eS as v,t as _}from"./outputWidgets.c6b12f47.js";import{a as W}from"./Title.53f8527b.js";(function(){try{var l=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(l._sentryDebugIds=l._sentryDebugIds||{},l._sentryDebugIds[e]="8c6ba633-9960-45d1-9bdc-70da2b5d570d",l._sentryDebugIdIdentifier="sentry-dbid-8c6ba633-9960-45d1-9bdc-70da2b5d570d")}catch{}})();const E=[{type:"text-input",key:null,label:"Insert your text here!",value:"",placeholder:"",required:!0,hint:null,fullWidth:!1,mask:null,disabled:!1,errors:[]},{type:"email-input",key:null,label:"Insert your email",value:"",placeholder:"",required:!0,hint:null,fullWidth:!1,invalidEmailMessage:"i18n_error_invalid_email",disabled:!1,errors:[]},{type:"phone-input",key:null,label:"Insert a phone number.",value:{countryCode:"",nationalNumber:""},placeholder:"",required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[],invalidMessage:"i18n_error_invalid_phone_number"},{type:"number-input",key:null,label:"Number",value:null,placeholder:"",required:!0,hint:null,fullWidth:!1,min:null,max:null,disabled:!1,errors:[]},{type:"date-input",key:null,hint:null,label:"Pick a date of your preference.",value:"",required:!0,fullWidth:!1,disabled:!1,errors:[]},{type:"time-input",key:null,label:"Choose the desired time.",format:"24hs",hint:null,value:{hour:0,minute:0},required:!0,fullWidth:!1,disabled:!1,errors:[]},{type:"cnpj-input",key:null,label:"Insert your CNPJ here!",value:"",placeholder:"00.000.000/0001-00",required:!0,hint:null,fullWidth:!1,disabled:!1,invalidMessage:"i18n_error_invalid_cnpj",errors:[]},{type:"cpf-input",key:null,label:"Insert your CPF here!",value:"",placeholder:"000.000.000-00",required:!0,hint:null,fullWidth:!1,disabled:!1,invalidMessage:"i18n_error_invalid_cpf",errors:[]},{type:"tag-input",key:null,label:"Insert the desired tags.",value:[],placeholder:"",required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"dropdown-input",key:null,label:"",options:[{label:"Option 1",value:1},{label:"Option 2",value:2}],hint:null,multiple:!1,placeholder:"",value:[],required:!0,fullWidth:!1,disabled:!1,errors:[]},{type:"currency-input",key:null,label:"Insert the proper amount.",value:null,placeholder:"",required:!0,hint:null,fullWidth:!1,min:null,max:null,currency:"USD",disabled:!1,errors:[]},{type:"textarea-input",key:null,label:"Insert your text here!",value:"",placeholder:"",required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"rich-text-input",key:null,label:"Insert your rich text here!",value:"",placeholder:"",required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"code-input",key:null,label:"Send your code here!",value:"",language:null,required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"click-input",key:null,label:"Click here!",hint:null,disabled:!1,fullWidth:!1,errors:[]},{type:"progress-output",current:50,total:100,text:"",fullWidth:!1},{type:"file-input",key:null,hint:null,label:"Upload a file.",value:[],required:!0,multiple:!1,fullWidth:!1,disabled:!1,maxFileSize:null,errors:[]},{type:"image-input",key:null,hint:null,label:"Upload",value:[],required:!0,multiple:!1,fullWidth:!1,disabled:!1,maxFileSize:null,errors:[]},{type:"video-input",key:null,hint:null,label:"Upload your video",value:[],required:!0,multiple:!1,fullWidth:!1,disabled:!1,maxFileSize:null,errors:[]},{type:"pandas-row-selection-input",key:null,hint:null,table:{schema:{fields:[{name:"index",type:"integer"},{name:"change the",type:"integer"},{name:"df property",type:"integer"}],primaryKey:["index"],pandas_version:"0.20.0"},data:[{index:0,"change the":1,"df property":4},{index:1,"change the":2,"df property":5},{index:2,"change the":3,"df property":6}]},required:!0,fullWidth:!1,displayIndex:!1,disabled:!1,label:"",multiple:!1,filterable:!1,value:[],errors:[]},{type:"plotly-output",figure:{data:[{coloraxis:"coloraxis",hovertemplate:"total_bill=%{x}<br>tip=%{y}<br>count=%{z}<extra></extra>",name:"",x:[16.99,10.34,21.01,23.68,24.59,25.29,8.77,26.88,15.04,14.78,10.27,35.26,15.42,18.43,14.83,21.58,10.33,16.29,16.97,20.65,17.92,20.29,15.77,39.42,19.82,17.81,13.37,12.69,21.7,19.65,9.55,18.35,15.06,20.69,17.78,24.06,16.31,16.93,18.69,31.27,16.04,17.46,13.94,9.68,30.4,18.29,22.23,32.4,28.55,18.04,12.54,10.29,34.81,9.94,25.56,19.49,38.01,26.41,11.24,48.27,20.29,13.81,11.02,18.29,17.59,20.08,16.45,3.07,20.23,15.01,12.02,17.07,26.86,25.28,14.73,10.51,17.92,27.2,22.76,17.29,19.44,16.66,10.07,32.68,15.98,34.83,13.03,18.28,24.71,21.16,28.97,22.49,5.75,16.32,22.75,40.17,27.28,12.03,21.01,12.46,11.35,15.38,44.3,22.42,20.92,15.36,20.49,25.21,18.24,14.31,14,7.25,38.07,23.95,25.71,17.31,29.93,10.65,12.43,24.08,11.69,13.42,14.26,15.95,12.48,29.8,8.52,14.52,11.38,22.82,19.08,20.27,11.17,12.26,18.26,8.51,10.33,14.15,16,13.16,17.47,34.3,41.19,27.05,16.43,8.35,18.64,11.87,9.78,7.51,14.07,13.13,17.26,24.55,19.77,29.85,48.17,25,13.39,16.49,21.5,12.66,16.21,13.81,17.51,24.52,20.76,31.71,10.59,10.63,50.81,15.81,7.25,31.85,16.82,32.9,17.89,14.48,9.6,34.63,34.65,23.33,45.35,23.17,40.55,20.69,20.9,30.46,18.15,23.1,15.69,19.81,28.44,15.48,16.58,7.56,10.34,43.11,13,13.51,18.71,12.74,13,16.4,20.53,16.47,26.59,38.73,24.27,12.76,30.06,25.89,48.33,13.27,28.17,12.9,28.15,11.59,7.74,30.14,12.16,13.42,8.58,15.98,13.42,16.27,10.09,20.45,13.28,22.12,24.01,15.69,11.61,10.77,15.53,10.07,12.6,32.83,35.83,29.03,27.18,22.67,17.82,18.78],xaxis:"x",xbingroup:"x",y:[1.01,1.66,3.5,3.31,3.61,4.71,2,3.12,1.96,3.23,1.71,5,1.57,3,3.02,3.92,1.67,3.71,3.5,3.35,4.08,2.75,2.23,7.58,3.18,2.34,2,2,4.3,3,1.45,2.5,3,2.45,3.27,3.6,2,3.07,2.31,5,2.24,2.54,3.06,1.32,5.6,3,5,6,2.05,3,2.5,2.6,5.2,1.56,4.34,3.51,3,1.5,1.76,6.73,3.21,2,1.98,3.76,2.64,3.15,2.47,1,2.01,2.09,1.97,3,3.14,5,2.2,1.25,3.08,4,3,2.71,3,3.4,1.83,5,2.03,5.17,2,4,5.85,3,3,3.5,1,4.3,3.25,4.73,4,1.5,3,1.5,2.5,3,2.5,3.48,4.08,1.64,4.06,4.29,3.76,4,3,1,4,2.55,4,3.5,5.07,1.5,1.8,2.92,2.31,1.68,2.5,2,2.52,4.2,1.48,2,2,2.18,1.5,2.83,1.5,2,3.25,1.25,2,2,2,2.75,3.5,6.7,5,5,2.3,1.5,1.36,1.63,1.73,2,2.5,2,2.74,2,2,5.14,5,3.75,2.61,2,3.5,2.5,2,2,3,3.48,2.24,4.5,1.61,2,10,3.16,5.15,3.18,4,3.11,2,2,4,3.55,3.68,5.65,3.5,6.5,3,5,3.5,2,3.5,4,1.5,4.19,2.56,2.02,4,1.44,2,5,2,2,4,2.01,2,2.5,4,3.23,3.41,3,2.03,2.23,2,5.16,9,2.5,6.5,1.1,3,1.5,1.44,3.09,2.2,3.48,1.92,3,1.58,2.5,2,3,2.72,2.88,2,3,3.39,1.47,3,1.25,1,1.17,4.67,5.92,2,2,1.75,3],yaxis:"y",ybingroup:"y",type:"histogram2d"}],layout:{template:{data:{histogram2dcontour:[{type:"histogram2dcontour",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],choropleth:[{type:"choropleth",colorbar:{outlinewidth:0,ticks:""}}],histogram2d:[{type:"histogram2d",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],heatmap:[{type:"heatmap",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],heatmapgl:[{type:"heatmapgl",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],contourcarpet:[{type:"contourcarpet",colorbar:{outlinewidth:0,ticks:""}}],contour:[{type:"contour",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],surface:[{type:"surface",colorbar:{outlinewidth:0,ticks:""},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]}],mesh3d:[{type:"mesh3d",colorbar:{outlinewidth:0,ticks:""}}],scatter:[{fillpattern:{fillmode:"overlay",size:10,solidity:.2},type:"scatter"}],parcoords:[{type:"parcoords",line:{colorbar:{outlinewidth:0,ticks:""}}}],scatterpolargl:[{type:"scatterpolargl",marker:{colorbar:{outlinewidth:0,ticks:""}}}],bar:[{error_x:{color:"#2a3f5f"},error_y:{color:"#2a3f5f"},marker:{line:{color:"#E5ECF6",width:.5},pattern:{fillmode:"overlay",size:10,solidity:.2}},type:"bar"}],scattergeo:[{type:"scattergeo",marker:{colorbar:{outlinewidth:0,ticks:""}}}],scatterpolar:[{type:"scatterpolar",marker:{colorbar:{outlinewidth:0,ticks:""}}}],histogram:[{marker:{pattern:{fillmode:"overlay",size:10,solidity:.2}},type:"histogram"}],scattergl:[{type:"scattergl",marker:{colorbar:{outlinewidth:0,ticks:""}}}],scatter3d:[{type:"scatter3d",line:{colorbar:{outlinewidth:0,ticks:""}},marker:{colorbar:{outlinewidth:0,ticks:""}}}],scattermapbox:[{type:"scattermapbox",marker:{colorbar:{outlinewidth:0,ticks:""}}}],scatterternary:[{type:"scatterternary",marker:{colorbar:{outlinewidth:0,ticks:""}}}],scattercarpet:[{type:"scattercarpet",marker:{colorbar:{outlinewidth:0,ticks:""}}}],carpet:[{aaxis:{endlinecolor:"#2a3f5f",gridcolor:"white",linecolor:"white",minorgridcolor:"white",startlinecolor:"#2a3f5f"},baxis:{endlinecolor:"#2a3f5f",gridcolor:"white",linecolor:"white",minorgridcolor:"white",startlinecolor:"#2a3f5f"},type:"carpet"}],table:[{cells:{fill:{color:"#EBF0F8"},line:{color:"white"}},header:{fill:{color:"#C8D4E3"},line:{color:"white"}},type:"table"}],barpolar:[{marker:{line:{color:"#E5ECF6",width:.5},pattern:{fillmode:"overlay",size:10,solidity:.2}},type:"barpolar"}],pie:[{automargin:!0,type:"pie"}]},layout:{autotypenumbers:"strict",colorway:["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],font:{color:"#2a3f5f"},hovermode:"closest",hoverlabel:{align:"left"},paper_bgcolor:"white",plot_bgcolor:"#E5ECF6",polar:{bgcolor:"#E5ECF6",angularaxis:{gridcolor:"white",linecolor:"white",ticks:""},radialaxis:{gridcolor:"white",linecolor:"white",ticks:""}},ternary:{bgcolor:"#E5ECF6",aaxis:{gridcolor:"white",linecolor:"white",ticks:""},baxis:{gridcolor:"white",linecolor:"white",ticks:""},caxis:{gridcolor:"white",linecolor:"white",ticks:""}},coloraxis:{colorbar:{outlinewidth:0,ticks:""}},colorscale:{sequential:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]],sequentialminus:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]],diverging:[[0,"#8e0152"],[.1,"#c51b7d"],[.2,"#de77ae"],[.3,"#f1b6da"],[.4,"#fde0ef"],[.5,"#f7f7f7"],[.6,"#e6f5d0"],[.7,"#b8e186"],[.8,"#7fbc41"],[.9,"#4d9221"],[1,"#276419"]]},xaxis:{gridcolor:"white",linecolor:"white",ticks:"",title:{standoff:15},zerolinecolor:"white",automargin:!0,zerolinewidth:2},yaxis:{gridcolor:"white",linecolor:"white",ticks:"",title:{standoff:15},zerolinecolor:"white",automargin:!0,zerolinewidth:2},scene:{xaxis:{backgroundcolor:"#E5ECF6",gridcolor:"white",linecolor:"white",showbackground:!0,ticks:"",zerolinecolor:"white",gridwidth:2},yaxis:{backgroundcolor:"#E5ECF6",gridcolor:"white",linecolor:"white",showbackground:!0,ticks:"",zerolinecolor:"white",gridwidth:2},zaxis:{backgroundcolor:"#E5ECF6",gridcolor:"white",linecolor:"white",showbackground:!0,ticks:"",zerolinecolor:"white",gridwidth:2}},shapedefaults:{line:{color:"#2a3f5f"}},annotationdefaults:{arrowcolor:"#2a3f5f",arrowhead:0,arrowwidth:1},geo:{bgcolor:"white",landcolor:"#E5ECF6",subunitcolor:"white",showland:!0,showlakes:!0,lakecolor:"white"},title:{x:.05},mapbox:{style:"light"}}},xaxis:{anchor:"y",domain:[0,1],title:{text:"total_bill"}},yaxis:{anchor:"x",domain:[0,1],title:{text:"tip"}},coloraxis:{colorbar:{title:{text:"count"}},colorscale:[[0,"#0d0887"],[.1111111111111111,"#46039f"],[.2222222222222222,"#7201a8"],[.3333333333333333,"#9c179e"],[.4444444444444444,"#bd3786"],[.5555555555555556,"#d8576b"],[.6666666666666666,"#ed7953"],[.7777777777777778,"#fb9f3a"],[.8888888888888888,"#fdca26"],[1,"#f0f921"]]},legend:{tracegroupgap:0},margin:{t:60}}},fullWidth:!1,label:""},{type:"toggle-input",key:null,label:"Click to confirm the following options",onText:"Yes",offText:"No",value:!1,required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"nps-input",key:null,label:"Rate us!",min:0,max:10,minHint:"Not at all likely",maxHint:"Extremely likely",value:null,required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"checkbox-input",key:null,label:"Choose your option",value:!1,required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"cards-input",key:null,label:"Card Title",hint:null,options:[{title:"Option 1",subtitle:"Subtitle 1",image:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/396px-Mona_Lisa.jpg",description:"option 1 description",topLeftExtra:"Left 1",topRightExtra:"Right 1"}],multiple:!1,searchable:!1,value:[],required:!0,columns:2,fullWidth:!1,layout:"list",disabled:!1,errors:[]},{type:"checklist-input",key:null,options:[{label:"Option 1",value:1},{label:"Option 2",value:2}],label:"Choose your option",value:[],required:!0,hint:null,fullWidth:!1,disabled:!1,errors:[]},{type:"multiple-choice-input",key:null,label:"Select your choices",options:[{label:"Option 1",value:1},{label:"Option 2",value:2}],hint:null,multiple:!1,value:[],required:!0,fullWidth:!1,min:null,max:null,disabled:!1,errors:[]},{type:"rating-input",key:null,label:"Rate us!",value:0,required:!0,hint:null,fullWidth:!1,max:null,char:"\u2B50\uFE0F",disabled:!1,errors:[]},{type:"number-slider-input",key:null,label:"Select a value!",value:0,required:!0,hint:null,fullWidth:!1,min:null,max:null,disabled:!1,errors:[]},{type:"text-output",text:"Your text here!",size:"medium",fullWidth:!1},{type:"latex-output",text:"\\(x^2 + y^2 = z^2\\)",fullWidth:!1},{type:"link-output",linkText:"Click here",linkUrl:"https://www.abstracloud.com",sameTab:!1,fullWidth:!1},{type:"html-output",html:"<div>Hello World</div>",fullWidth:!1},{type:"custom-input",key:null,label:"",value:null,htmlBody:"<h1>Hello World</h1>",htmlHead:"",css:"",js:"",fullWidth:!1},{type:"markdown-output",text:"### Hello World",fullWidth:!1},{type:"image-output",imageUrl:"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mona_Lisa.jpg/396px-Mona_Lisa.jpg",subtitle:"",fullWidth:!1,label:""},{type:"file-output",fileUrl:"https://gist.github.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6/archive/92200bc0a673d5ce2110aaad4544ed6c4010f687.zip",downloadText:"Download",fullWidth:!1},{type:"kanban-board-input",key:null,label:"",value:[],stages:[{key:"To-Do",label:"To-Do"},{key:"Doing",label:"Doing"},{key:"Done",label:"Done"}],disabled:!1,errors:[]}],F={class:"sidebar-preview"},q={class:"sidebar-frame"},C={class:"form"},T={key:0,class:"form-wrapper"},z=k({__name:"SidebarPreview",props:{workspace:{},widgetsVisible:{type:Boolean}},setup(l){const e=l,r=n(()=>e.workspace.makeRunnerData()),s=n(()=>{var a;return e.workspace?{id:"mockId",path:"mockPath",title:"mockTitle",theme:e.workspace.theme,brandName:(a=e.workspace.brandName)!=null?a:null,logoUrl:y("logo",e.workspace.logoUrl,"editor"),mainColor:e.workspace.mainColor,fontFamily:e.workspace.fontFamily,sidebar:e.workspace.sidebar,runtimeType:"form",isLocal:!1,startMessage:"mockStartMessage",endMessage:"mockEndMessage",errorMessage:"mockErrorMessage",timeoutMessage:"mockTimeoutMessage",startButtonText:"mockStartButtonText",allowRestart:!0,autoStart:!0,restartButtonText:"mockRestartButtonText",welcomeTitle:"mockWelcomeTitle"}:null});return(a,I)=>(t(),o("div",F,[u(c(W),{level:4,style:{margin:"0 0 12px 0"}},{default:d(()=>[g("Preview")]),_:1}),f("div",q,[s.value?(t(),p(b,{key:0,runtime:s.value,"user-email":"user@email.com","force-responsivity":"desktop"},null,8,["runtime"])):h("",!0),u(m,{theme:r.value.theme,"main-color":r.value.mainColor,"font-family":r.value.fontFamily,class:"widgets"},{default:d(()=>[f("div",C,[a.widgetsVisible?(t(),o("div",T,[(t(!0),o(w,null,x(c(E),i=>(t(),o("div",{key:i.type,class:"widget"},[(t(),p(v(i.type),{"user-props":i,value:i.value,errors:[]},null,8,["user-props","value"]))]))),128))])):h("",!0)])]),_:1},8,["theme","main-color","font-family"])])]))}});const P=_(z,[["__scopeId","data-v-17fcf615"]]);export{P as S};
//# sourceMappingURL=SidebarPreview.8c136673.js.map
