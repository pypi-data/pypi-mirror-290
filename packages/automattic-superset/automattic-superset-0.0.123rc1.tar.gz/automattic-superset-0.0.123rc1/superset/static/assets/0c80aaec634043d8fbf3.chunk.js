"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[790],{50790:(e,t,a)=>{a.r(t),a.d(t,{default:()=>o});var r=a(7349),n=a(32142),l=a(86444),i=a(85867),c=a(71194),s=a(2445);function o({height:e,width:t,echartOptions:a,formData:o,onContextMenu:u,setDataMask:d,filterState:h,emitCrossFilters:f,refs:v,coltypeMapping:p}){const m=e=>{if(null==e||!e.name||null==e||!e.col)return;const{name:t,col:a}=e,r=Object.values((null==h?void 0:h.selectedValues)||{});let n;return n=r.includes(t)?r.filter((e=>e!==t)):[t],{dataMask:{extraFormData:{filters:n.length?[{col:a,op:"IN",val:n}]:[]},filterState:{value:n.length?n:null,selectedValues:n.length?n:null}},isCurrentValueSelected:r.includes(t)}},g={click:e=>{var t;if(!f||!d)return;e.event.stop();const r=a.series[0].data.find((t=>t.id===e.data.id)),n=null==(t=m(r))?void 0:t.dataMask;n&&d(n)},contextmenu:e=>{if(u){e.event.stop();const t=e.event.event,i=a.series[0].data,s="node"===e.dataType?(t=>{const a=t.find((t=>t.id===e.data.id));if(null!=a&&a.name)return[{col:a.col,op:"==",val:a.name,formattedVal:a.name}]})(i):(t=>{var a,r;const n=null==(a=t.find((t=>t.id===e.data.source)))?void 0:a.name,l=null==(r=t.find((t=>t.id===e.data.target)))?void 0:r.name;if(n&&l)return[{col:o.source,op:"==",val:n,formattedVal:n},{col:o.target,op:"==",val:l,formattedVal:l}]})(i),d=i.find((t=>t.id===e.data.id));u(t.clientX,t.clientY,{drillToDetail:s,crossFilter:m(d),drillBy:d&&{filters:[{col:d.col,op:"==",val:d.name,formattedVal:(0,c.Wy)(d.name,{timeFormatter:(0,r.mo)(o.dateFormat),numberFormatter:(0,n.gV)(o.numberFormat),coltype:null==p?void 0:p[(0,l.A)(d.col)]})}],groupbyFieldName:d.col===o.source?"source":"target"}})}}};return(0,s.Y)(i.A,{refs:v,height:e,width:t,echartOptions:a,eventHandlers:g})}},85867:(e,t,a)=>{a.d(t,{A:()=>D});var r=a(96540),n=a(96453),l=a(59936),i=a(53826),c=a(72729),s=a(71422),o=a(52428),u=a(49855),d=a(1385),h=a(82523),f=a(97127),v=a(82843),p=a(86915),m=a(13371),g=a(97624),w=a(37340),b=a(9472),y=a(62245),k=a(39925),V=a(84519),E=a(66108),F=a(68948),O=a(2641),C=a(62404),I=a(26334),M=a(93587),x=a(18953),A=a(13525),R=a(2445);const T=n.I4.div`
  height: ${({height:e})=>e};
  width: ${({width:e})=>e};
`;function j({width:e,height:t,echartOptions:a,eventHandlers:n,zrEventHandlers:l,selectedValues:c={},refs:s},o){const u=(0,r.useRef)(null);s&&(s.divRef=u);const d=(0,r.useRef)(),h=(0,r.useMemo)((()=>Object.keys(c)||[]),[c]),f=(0,r.useRef)([]);(0,r.useImperativeHandle)(o,(()=>({getEchartInstance:()=>d.current}))),(0,r.useEffect)((()=>{u.current&&(d.current||(d.current=(0,i.Ts)(u.current)),Object.entries(n||{}).forEach((([e,t])=>{var a,r;null==(a=d.current)||a.off(e),null==(r=d.current)||r.on(e,t)})),Object.entries(l||{}).forEach((([e,t])=>{var a,r;null==(a=d.current)||a.getZr().off(e),null==(r=d.current)||r.getZr().on(e,t)})),d.current.setOption(a,!0))}),[a,n,l]),(0,r.useEffect)((()=>{d.current&&(d.current.dispatchAction({type:"downplay",dataIndex:f.current.filter((e=>!h.includes(e)))}),h.length&&d.current.dispatchAction({type:"highlight",dataIndex:h}),f.current=h)}),[h]);const v=(0,r.useCallback)((({width:e,height:t})=>{d.current&&d.current.resize({width:e,height:t})}),[]);return(0,r.useEffect)((()=>(v({width:e,height:t}),()=>{var e;return null==(e=d.current)?void 0:e.dispose()})),[]),(0,r.useLayoutEffect)((()=>{v({width:e,height:t})}),[e,t,v]),(0,R.Y)(T,{ref:u,height:t,width:e})}(0,l.Y)([k.a,c.a,s.a,o.a,u.a,d.a,h.a,f.a,v.a,p.a,m.a,g.a,w.a,b.a,y.a,V.a,E.a,F.a,O.a,C.a,I.a,M.a,x.a,A._]);const D=(0,r.forwardRef)(j)}}]);
//# sourceMappingURL=0c80aaec634043d8fbf3.chunk.js.map