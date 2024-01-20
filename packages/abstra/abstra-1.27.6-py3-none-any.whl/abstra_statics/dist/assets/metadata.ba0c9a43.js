import{f as i,a as o,j as n,b as s,y as d,z as l}from"./icons.92b5bc38.js";import"./outputWidgets.ed48fa42.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[e]="9b0723aa-f0ce-482e-9e2a-b65635a78673",t._sentryDebugIdIdentifier="sentry-dbid-9b0723aa-f0ce-482e-9e2a-b65635a78673")}catch{}})();const r={stages:[{icon:i,typeName:"forms",description:"Wait for a user input",key:"F",title:"Forms",startingOnly:!1,transitions:[{typeName:"forms:finished",title:"Finished",additionalPayload:[]},{typeName:"forms:failed",title:"Failed",additionalPayload:[]}]},{typeName:"hooks",title:"Hooks",startingOnly:!1,icon:o,description:"Wait for an external API call",key:"H",transitions:[{typeName:"hooks:finished",title:"Finished",additionalPayload:[]},{typeName:"hooks:failed",title:"Failed",additionalPayload:[]}]},{typeName:"jobs",title:"Jobs",startingOnly:!0,icon:n,description:"Scheduled tasks",key:"J",transitions:[{typeName:"jobs:finished",title:"Finished",additionalPayload:[]},{typeName:"jobs:failed",title:"Failed",additionalPayload:[]}]},{typeName:"scripts",title:"Scripts",startingOnly:!1,icon:s,description:"Run a script",key:"S",transitions:[{typeName:"scripts:finished",title:"Finished",additionalPayload:[]},{typeName:"scripts:failed",title:"Failed",additionalPayload:[]}]},{typeName:"conditions",title:"Conditions",startingOnly:!1,icon:d,description:"Make a decision",key:"C",transitions:[{typeName:"conditions:patternMatched",title:"Pattern Matched",additionalPayload:[]},{typeName:"conditions:patternNotMatched",title:"Pattern Not Matched",additionalPayload:[]}]},{typeName:"iterators",title:"Iterators",startingOnly:!1,icon:l,description:"Split thread for each element in a list",key:"I",transitions:[{typeName:"iterators:each",title:"Each",additionalPayload:[{key:"item",type:"typing.Any",title:"Item"}]}]}]};function p(t){const e=r.stages.find(a=>a.typeName===t);if(!e)throw new Error(`No metadata found for stage ${t}`);return e.icon}export{p as s,r as w};
//# sourceMappingURL=metadata.ba0c9a43.js.map
