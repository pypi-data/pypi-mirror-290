"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7889],{80270:(e,t,r)=>{r.r(t),r.d(t,{default:()=>s});var n=r(85867),a=r(28166),l=r(2445);function s(e){const{height:t,width:r,echartOptions:s,selectedValues:c,refs:u}=e,i=(0,a.j7)(e);return(0,l.Y)(n.A,{refs:u,height:t,width:r,echartOptions:s,eventHandlers:i,selectedValues:c})}},85867:(e,t,r)=>{r.d(t,{A:()=>H});var n=r(96540),a=r(96453),l=r(59936),s=r(53826),c=r(72729),u=r(71422),i=r(52428),o=r(49855),h=r(1385),d=r(82523),f=r(97127),p=r(82843),g=r(86915),v=r(13371),m=r(97624),b=r(37340),w=r(9472),y=r(62245),k=r(39925),E=r(84519),F=r(66108),O=r(68948),V=r(2641),I=r(62404),M=r(26334),j=r(93587),C=r(18953),x=r(13525),A=r(2445);const R=a.I4.div`
  height: ${({height:e})=>e};
  width: ${({width:e})=>e};
`;function D({width:e,height:t,echartOptions:r,eventHandlers:a,zrEventHandlers:l,selectedValues:c={},refs:u},i){const o=(0,n.useRef)(null);u&&(u.divRef=o);const h=(0,n.useRef)(),d=(0,n.useMemo)((()=>Object.keys(c)||[]),[c]),f=(0,n.useRef)([]);(0,n.useImperativeHandle)(i,(()=>({getEchartInstance:()=>h.current}))),(0,n.useEffect)((()=>{o.current&&(h.current||(h.current=(0,s.Ts)(o.current)),Object.entries(a||{}).forEach((([e,t])=>{var r,n;null==(r=h.current)||r.off(e),null==(n=h.current)||n.on(e,t)})),Object.entries(l||{}).forEach((([e,t])=>{var r,n;null==(r=h.current)||r.getZr().off(e),null==(n=h.current)||n.getZr().on(e,t)})),h.current.setOption(r,!0))}),[r,a,l]),(0,n.useEffect)((()=>{h.current&&(h.current.dispatchAction({type:"downplay",dataIndex:f.current.filter((e=>!d.includes(e)))}),d.length&&h.current.dispatchAction({type:"highlight",dataIndex:d}),f.current=d)}),[d]);const p=(0,n.useCallback)((({width:e,height:t})=>{h.current&&h.current.resize({width:e,height:t})}),[]);return(0,n.useEffect)((()=>(p({width:e,height:t}),()=>{var e;return null==(e=h.current)?void 0:e.dispose()})),[]),(0,n.useLayoutEffect)((()=>{p({width:e,height:t})}),[e,t,p]),(0,A.Y)(R,{ref:o,height:t,width:e})}(0,l.Y)([k.a,c.a,u.a,i.a,o.a,h.a,d.a,f.a,p.a,g.a,v.a,m.a,b.a,w.a,y.a,E.a,F.a,O.a,V.a,I.a,M.a,j.a,C.a,x._]);const H=(0,n.forwardRef)(D)},28166:(e,t,r)=>{r.d(t,{j7:()=>o});var n=r(7349),a=r(32142),l=r(86444),s=r(71194);const c=(e,t,r)=>n=>{const a=Object.values(e);let l;l=a.includes(n)?a.filter((e=>e!==n)):[n];const s=l.map((e=>r[e]));return{dataMask:{extraFormData:{filters:0===l.length?[]:t.map(((e,t)=>{const r=s.map((e=>e[t]));return null==r?{col:e,op:"IS NULL"}:{col:e,op:"IN",val:r}}))},filterState:{value:s.length?s:null,selectedValues:l.length?l:null}},isCurrentValueSelected:a.includes(n)}},u=(e,t,r)=>({name:n})=>{var a;if(!r)return;const l=null==(a=e(n))?void 0:a.dataMask;l&&t(l)},i=(e,t,r,c,u,i)=>o=>{if(t){o.event.stop();const h=o.event.event,d=[];if(e.length>0){const t=r[o.name];e.forEach(((e,r)=>{d.push({col:e,op:"==",val:t[r],formattedVal:(0,s.Wy)(t[r],{timeFormatter:(0,n.mo)(u.dateFormat),numberFormatter:(0,a.gV)(u.numberFormat),coltype:null==i?void 0:i[(0,l.A)(e)]})})}))}t(h.clientX,h.clientY,{drillToDetail:d,crossFilter:c(o.name),drillBy:{filters:d,groupbyFieldName:"groupby"}})}},o=e=>{const{groupby:t,onContextMenu:r,setDataMask:n,labelMap:a,emitCrossFilters:l,selectedValues:s,coltypeMapping:o,formData:h}=e;return{click:u(c(s,t,a),n,l),contextmenu:i(t,r,a,c(s,t,a),h,o)}}}}]);
//# sourceMappingURL=fa35cf4191c9db3c1036.chunk.js.map