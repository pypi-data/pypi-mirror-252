/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.34.1(547870b6881302c5b4ff32173c16d06009e3588f)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[t]="71a20a88-7a00-4afc-9fdb-d15e53142c50",e._sentryDebugIdIdentifier="sentry-dbid-71a20a88-7a00-4afc-9fdb-d15e53142c50")}catch{}})();var s={wordPattern:/(-?\d*\.\d\w*)|([^\`\~\!\#\$\%\^\&\*\(\)\-\=\+\[\{\]\}\\\|\;\:\'\"\,\.\<\>\/\?\s]+)/g,comments:{lineComment:"//",blockComment:["/*","*/"]},brackets:[["{","}"],["[","]"],["(",")"]],autoClosingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:"'",close:"'",notIn:["string","comment"]},{open:'"',close:'"',notIn:["string","comment"]}],surroundingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:"<",close:">"},{open:"'",close:"'"},{open:'"',close:'"'}],folding:{markers:{start:new RegExp("^\\s*#region\\b"),end:new RegExp("^\\s*#endregion\\b")}}},o={defaultToken:"",tokenPostfix:".cs",brackets:[{open:"{",close:"}",token:"delimiter.curly"},{open:"[",close:"]",token:"delimiter.square"},{open:"(",close:")",token:"delimiter.parenthesis"},{open:"<",close:">",token:"delimiter.angle"}],keywords:["extern","alias","using","bool","decimal","sbyte","byte","short","ushort","int","uint","long","ulong","char","float","double","object","dynamic","string","assembly","is","as","ref","out","this","base","new","typeof","void","checked","unchecked","default","delegate","var","const","if","else","switch","case","while","do","for","foreach","in","break","continue","goto","return","throw","try","catch","finally","lock","yield","from","let","where","join","on","equals","into","orderby","ascending","descending","select","group","by","namespace","partial","class","field","event","method","param","public","protected","internal","private","abstract","sealed","static","struct","readonly","volatile","virtual","override","params","get","set","add","remove","operator","true","false","implicit","explicit","interface","enum","null","async","await","fixed","sizeof","stackalloc","unsafe","nameof","when"],namespaceFollows:["namespace","using"],parenFollows:["if","for","while","switch","foreach","using","catch","when"],operators:["=","??","||","&&","|","^","&","==","!=","<=",">=","<<","+","-","*","/","%","!","~","++","--","+=","-=","*=","/=","%=","&=","|=","^=","<<=",">>=",">>","=>"],symbols:/[=><!~?:&|+\-*\/\^%]+/,escapes:/\\(?:[abfnrtv\\"']|x[0-9A-Fa-f]{1,4}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})/,tokenizer:{root:[[/\@?[a-zA-Z_]\w*/,{cases:{"@namespaceFollows":{token:"keyword.$0",next:"@namespace"},"@keywords":{token:"keyword.$0",next:"@qualified"},"@default":{token:"identifier",next:"@qualified"}}}],{include:"@whitespace"},[/}/,{cases:{"$S2==interpolatedstring":{token:"string.quote",next:"@pop"},"$S2==litinterpstring":{token:"string.quote",next:"@pop"},"@default":"@brackets"}}],[/[{}()\[\]]/,"@brackets"],[/[<>](?!@symbols)/,"@brackets"],[/@symbols/,{cases:{"@operators":"delimiter","@default":""}}],[/[0-9_]*\.[0-9_]+([eE][\-+]?\d+)?[fFdD]?/,"number.float"],[/0[xX][0-9a-fA-F_]+/,"number.hex"],[/0[bB][01_]+/,"number.hex"],[/[0-9_]+/,"number"],[/[;,.]/,"delimiter"],[/"([^"\\]|\\.)*$/,"string.invalid"],[/"/,{token:"string.quote",next:"@string"}],[/\$\@"/,{token:"string.quote",next:"@litinterpstring"}],[/\@"/,{token:"string.quote",next:"@litstring"}],[/\$"/,{token:"string.quote",next:"@interpolatedstring"}],[/'[^\\']'/,"string"],[/(')(@escapes)(')/,["string","string.escape","string"]],[/'/,"string.invalid"]],qualified:[[/[a-zA-Z_][\w]*/,{cases:{"@keywords":{token:"keyword.$0"},"@default":"identifier"}}],[/\./,"delimiter"],["","","@pop"]],namespace:[{include:"@whitespace"},[/[A-Z]\w*/,"namespace"],[/[\.=]/,"delimiter"],["","","@pop"]],comment:[[/[^\/*]+/,"comment"],["\\*/","comment","@pop"],[/[\/*]/,"comment"]],string:[[/[^\\"]+/,"string"],[/@escapes/,"string.escape"],[/\\./,"string.escape.invalid"],[/"/,{token:"string.quote",next:"@pop"}]],litstring:[[/[^"]+/,"string"],[/""/,"string.escape"],[/"/,{token:"string.quote",next:"@pop"}]],litinterpstring:[[/[^"{]+/,"string"],[/""/,"string.escape"],[/{{/,"string.escape"],[/}}/,"string.escape"],[/{/,{token:"string.quote",next:"root.litinterpstring"}],[/"/,{token:"string.quote",next:"@pop"}]],interpolatedstring:[[/[^\\"{]+/,"string"],[/@escapes/,"string.escape"],[/\\./,"string.escape.invalid"],[/{{/,"string.escape"],[/}}/,"string.escape"],[/{/,{token:"string.quote",next:"root.interpolatedstring"}],[/"/,{token:"string.quote",next:"@pop"}]],whitespace:[[/^[ \t\v\f]*#((r)|(load))(?=\s)/,"directive.csx"],[/^[ \t\v\f]*#\w.*$/,"namespace.cpp"],[/[ \t\v\f\r\n]+/,""],[/\/\*/,"comment","@comment"],[/\/\/.*$/,"comment"]]}};export{s as conf,o as language};
//# sourceMappingURL=csharp.711e6ef5.js.map
