"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4644],{5267:(n,i,o)=>{o.d(i,{rJ:()=>t,wk:()=>k,Eg:()=>b,Mk:()=>u,Iy:()=>A,UD:()=>e});const t={CLOCKWISE:1,COUNTER_CLOCKWISE:-1};function e(n,i,o={}){const t=function(n,i={}){return Math.sign(function(n,i={}){const{start:o=0,end:t=n.length}=i,e=i.size||2;let l=0;for(let i=o,c=t-e;i<t;i+=e)l+=(n[i]-n[c])*(n[i+1]+n[c+1]),c=i;return l/2}(n,i))}(n,o);return t!==i&&(function(n,i){const{start:o=0,end:t=n.length,size:e=2}=i,l=(t-o)/e,c=Math.floor(l/2);for(let i=0;i<c;++i){const t=o+i*e,c=o+(l-1-i)*e;for(let i=0;i<e;++i){const o=n[t+i];n[t+i]=n[c+i],n[c+i]=o}}}(n,o),!0)}function l(n,i,o,t,e=[]){let l,c;if(8&o)l=(t[3]-n[1])/(i[1]-n[1]),c=3;else if(4&o)l=(t[1]-n[1])/(i[1]-n[1]),c=1;else if(2&o)l=(t[2]-n[0])/(i[0]-n[0]),c=2;else{if(!(1&o))return null;l=(t[0]-n[0])/(i[0]-n[0]),c=0}for(let o=0;o<n.length;o++)e[o]=(1&c)===o?t[c]:l*(i[o]-n[o])+n[o];return e}function c(n,i){let o=0;return n[0]<i[0]?o|=1:n[0]>i[2]&&(o|=2),n[1]<i[1]?o|=4:n[1]>i[3]&&(o|=8),o}function r(n,i){const o=i.length,t=n.length;if(t>0){let e=!0;for(let l=0;l<o;l++)if(n[t-o+l]!==i[l]){e=!1;break}if(e)return!1}for(let e=0;e<o;e++)n[t+e]=i[e];return!0}function g(n,i){const o=i.length;for(let t=0;t<o;t++)n[t]=i[t]}function s(n,i,o,t,e=[]){const l=t+i*o;for(let i=0;i<o;i++)e[i]=n[l+i];return e}function u(n,i){const{size:o=2,broken:t=!1,gridResolution:e=10,gridOffset:u=[0,0],startIndex:p=0,endIndex:h=n.length}=i||{},f=(h-p)/o;let k=[];const d=[k],v=s(n,0,o,p);let C,A;const b=a(v,e,u,[]),R=[];r(k,v);for(let i=1;i<f;i++){for(C=s(n,i,o,p,C),A=c(C,b);A;){l(v,C,A,b,R);const n=c(R,b);n&&(l(v,R,n,b,R),A=n),r(k,R),g(v,R),_(b,e,A),t&&k.length>o&&(k=[],d.push(k),r(k,v)),A=c(C,b)}r(k,C),g(v,C)}return t?d:d[0]}const p=0,h=1;function f(n,i){for(let o=0;o<i.length;o++)n.push(i[o]);return n}function k(n,i=null,o){if(!n.length)return[];const{size:t=2,gridResolution:e=10,gridOffset:l=[0,0],edgeTypes:r=!1}=o||{},g=[],s=[{pos:n,types:r?new Array(n.length/t).fill(h):null,holes:i||[]}],u=[[],[]];let p=[];for(;s.length;){const{pos:n,types:i,holes:o}=s.shift();v(n,t,o[0]||n.length,u),p=a(u[0],e,l,p);const h=c(u[1],p);if(h){let e=d(n,i,t,0,o[0]||n.length,p,h);const l={pos:e[0].pos,types:e[0].types,holes:[]},c={pos:e[1].pos,types:e[1].types,holes:[]};s.push(l,c);for(let g=0;g<o.length;g++)e=d(n,i,t,o[g],o[g+1]||n.length,p,h),e[0]&&(l.holes.push(l.pos.length),l.pos=f(l.pos,e[0].pos),r&&(l.types=f(l.types,e[0].types))),e[1]&&(c.holes.push(c.pos.length),c.pos=f(c.pos,e[1].pos),r&&(c.types=f(c.types,e[1].types)))}else{const t={positions:n};r&&(t.edgeTypes=i),o.length&&(t.holeIndices=o),g.push(t)}}return g}function d(n,i,o,t,e,c,u){const h=(e-t)/o,f=[],k=[],d=[],a=[],_=[];let v,C,A;const b=s(n,h-1,o,t);let R=Math.sign(8&u?b[1]-c[3]:b[0]-c[2]),y=i&&i[h-1],L=0,m=0;for(let e=0;e<h;e++)v=s(n,e,o,t,v),C=Math.sign(8&u?v[1]-c[3]:v[0]-c[2]),A=i&&i[t/o+e],C&&R&&R!==C&&(l(b,v,u,c,_),r(f,_)&&d.push(y),r(k,_)&&a.push(y)),C<=0?(r(f,v)&&d.push(A),L-=C):d.length&&(d[d.length-1]=p),C>=0?(r(k,v)&&a.push(A),m+=C):a.length&&(a[a.length-1]=p),g(b,v),R=C,y=A;return[L?{pos:f,types:i&&d}:null,m?{pos:k,types:i&&a}:null]}function a(n,i,o,t){const e=Math.floor((n[0]-o[0])/i)*i+o[0],l=Math.floor((n[1]-o[1])/i)*i+o[1];return t[0]=e,t[1]=l,t[2]=e+i,t[3]=l+i,t}function _(n,i,o){8&o?(n[1]+=i,n[3]+=i):4&o?(n[1]-=i,n[3]-=i):2&o?(n[0]+=i,n[2]+=i):1&o&&(n[0]-=i,n[2]-=i)}function v(n,i,o,t){let e=1/0,l=-1/0,c=1/0,r=-1/0;for(let t=0;t<o;t+=i){const i=n[t],o=n[t+1];e=i<e?i:e,l=i>l?i:l,c=o<c?o:c,r=o>r?o:r}return t[0][0]=e,t[0][1]=c,t[1][0]=l,t[1][1]=r,t}const C=85.051129;function A(n,i){const{size:o=2,startIndex:t=0,endIndex:e=n.length,normalize:l=!0}=i||{},c=n.slice(t,e);L(c,o,0,e-t);const r=u(c,{size:o,broken:!0,gridResolution:360,gridOffset:[-180,-180]});if(l)for(const n of r)m(n,o);return r}function b(n,i=null,o){const{size:t=2,normalize:e=!0,edgeTypes:l=!1}=o||{};i=i||[];const c=[],r=[];let g=0,s=0;for(let e=0;e<=i.length;e++){const l=i[e]||n.length,u=s,p=R(n,t,g,l);for(let i=p;i<l;i++)c[s++]=n[i];for(let i=g;i<p;i++)c[s++]=n[i];L(c,t,u,s),y(c,t,u,s,null==o?void 0:o.maxLatitude),g=l,r[e]=s}r.pop();const u=k(c,r,{size:t,gridResolution:360,gridOffset:[-180,-180],edgeTypes:l});if(e)for(const n of u)m(n.positions,t);return u}function R(n,i,o,t){let e=-1,l=-1;for(let c=o+1;c<t;c+=i){const i=Math.abs(n[c]);i>e&&(e=i,l=c-1)}return l}function y(n,i,o,t,e=C){const l=n[o],c=n[t-i];if(Math.abs(l-c)>180){const t=s(n,0,i,o);t[0]+=360*Math.round((c-l)/360),r(n,t),t[1]=Math.sign(t[1])*e,r(n,t),t[0]=l,r(n,t)}}function L(n,i,o,t){let e,l=n[0];for(let c=o;c<t;c+=i){e=n[c];const i=e-l;(i>180||i<-180)&&(e-=360*Math.round(i/360)),n[c]=l=e}}function m(n,i){let o;const t=n.length/i;for(let e=0;e<t&&(o=n[e*i],(o+180)%360==0);e++);const e=360*-Math.round(o/360);if(0!==e)for(let o=0;o<t;o++)n[o*i]+=e}},88514:(n,i,o)=>{o.d(i,{A:()=>e});const t={pickingSelectedColor:null,pickingHighlightColor:new Uint8Array([0,255,255,255]),pickingActive:!1,pickingAttribute:!1},e={inject:{"vs:DECKGL_FILTER_GL_POSITION":"\n    // for picking depth values\n    picking_setPickingAttribute(position.z / position.w);\n  ","vs:DECKGL_FILTER_COLOR":"\n  picking_setPickingColor(geometry.pickingColor);\n  ","fs:#decl":"\nuniform bool picking_uAttribute;\n  ","fs:DECKGL_FILTER_COLOR":{order:99,injection:"\n  // use highlight color if this fragment belongs to the selected object.\n  color = picking_filterHighlightColor(color);\n\n  // use picking color if rendering to picking FBO.\n  color = picking_filterPickingColor(color);\n    "}},name:"picking",vs:"uniform bool picking_uActive;\nuniform bool picking_uAttribute;\nuniform vec3 picking_uSelectedColor;\nuniform bool picking_uSelectedColorValid;\n\nout vec4 picking_vRGBcolor_Avalid;\n\nconst float COLOR_SCALE = 1. / 255.;\n\nbool picking_isColorValid(vec3 color) {\n  return dot(color, vec3(1.0)) > 0.001;\n}\n\nbool isVertexPicked(vec3 vertexColor) {\n  return\n    picking_uSelectedColorValid &&\n    !picking_isColorValid(abs(vertexColor - picking_uSelectedColor));\n}\n\nvoid picking_setPickingColor(vec3 pickingColor) {\n  if (picking_uActive) {\n    picking_vRGBcolor_Avalid.a = float(picking_isColorValid(pickingColor));\n\n    if (!picking_uAttribute) {\n      picking_vRGBcolor_Avalid.rgb = pickingColor * COLOR_SCALE;\n    }\n  } else {\n    picking_vRGBcolor_Avalid.a = float(isVertexPicked(pickingColor));\n  }\n}\n\nvoid picking_setPickingAttribute(float value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.r = value;\n  }\n}\nvoid picking_setPickingAttribute(vec2 value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.rg = value;\n  }\n}\nvoid picking_setPickingAttribute(vec3 value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.rgb = value;\n  }\n}\n",fs:"uniform bool picking_uActive;\nuniform vec3 picking_uSelectedColor;\nuniform vec4 picking_uHighlightColor;\n\nin vec4 picking_vRGBcolor_Avalid;\nvec4 picking_filterHighlightColor(vec4 color) {\n  if (picking_uActive) {\n    return color;\n  }\n  bool selected = bool(picking_vRGBcolor_Avalid.a);\n\n  if (selected) {\n    float highLightAlpha = picking_uHighlightColor.a;\n    float blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);\n    float highLightRatio = highLightAlpha / blendedAlpha;\n\n    vec3 blendedRGB = mix(color.rgb, picking_uHighlightColor.rgb, highLightRatio);\n    return vec4(blendedRGB, blendedAlpha);\n  } else {\n    return color;\n  }\n}\nvec4 picking_filterPickingColor(vec4 color) {\n  if (picking_uActive) {\n    if (picking_vRGBcolor_Avalid.a == 0.0) {\n      discard;\n    }\n    return picking_vRGBcolor_Avalid;\n  }\n  return color;\n}\nvec4 picking_filterColor(vec4 color) {\n  vec4 highightColor = picking_filterHighlightColor(color);\n  return picking_filterPickingColor(highightColor);\n}\n\n",getUniforms:function(){let n=arguments.length>0&&void 0!==arguments[0]?arguments[0]:t;const i={};if(void 0!==n.pickingSelectedColor)if(n.pickingSelectedColor){const o=n.pickingSelectedColor.slice(0,3);i.picking_uSelectedColorValid=1,i.picking_uSelectedColor=o}else i.picking_uSelectedColorValid=0;if(n.pickingHighlightColor){const o=Array.from(n.pickingHighlightColor,(n=>n/255));Number.isFinite(o[3])||(o[3]=1),i.picking_uHighlightColor=o}return void 0!==n.pickingActive&&(i.picking_uActive=Boolean(n.pickingActive),i.picking_uAttribute=Boolean(n.pickingAttribute)),i}}}}]);
//# sourceMappingURL=6e9bc3c4844eadb94431.chunk.js.map