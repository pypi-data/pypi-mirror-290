"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4478],{54478:(e,t,r)=>{r.r(t),r.d(t,{default:()=>c});var n=r(85867),a=r(2445);function c(e){const{height:t,width:r,echartOptions:c,refs:u}=e;return(0,a.Y)(n.A,{refs:u,height:t,width:r,echartOptions:c})}},85867:(e,t,r)=>{r.d(t,{A:()=>Z});var n=r(96540),a=r(96453),c=r(59936),u=r(53826),h=r(72729),s=r(71422),i=r(52428),d=r(49855),l=r(1385),f=r(82523),o=r(97127),g=r(82843),p=r(86915),w=r(13371),v=r(97624),b=r(37340),E=r(9472),O=r(62245),k=r(39925),y=r(84519),I=r(66108),R=r(68948),A=r(2641),j=r(62404),C=r(26334),H=r(93587),T=r(18953),Y=r(13525),m=r(2445);const x=a.I4.div`
  height: ${({height:e})=>e};
  width: ${({width:e})=>e};
`;function z({width:e,height:t,echartOptions:r,eventHandlers:a,zrEventHandlers:c,selectedValues:h={},refs:s},i){const d=(0,n.useRef)(null);s&&(s.divRef=d);const l=(0,n.useRef)(),f=(0,n.useMemo)((()=>Object.keys(h)||[]),[h]),o=(0,n.useRef)([]);(0,n.useImperativeHandle)(i,(()=>({getEchartInstance:()=>l.current}))),(0,n.useEffect)((()=>{d.current&&(l.current||(l.current=(0,u.Ts)(d.current)),Object.entries(a||{}).forEach((([e,t])=>{var r,n;null==(r=l.current)||r.off(e),null==(n=l.current)||n.on(e,t)})),Object.entries(c||{}).forEach((([e,t])=>{var r,n;null==(r=l.current)||r.getZr().off(e),null==(n=l.current)||n.getZr().on(e,t)})),l.current.setOption(r,!0))}),[r,a,c]),(0,n.useEffect)((()=>{l.current&&(l.current.dispatchAction({type:"downplay",dataIndex:o.current.filter((e=>!f.includes(e)))}),f.length&&l.current.dispatchAction({type:"highlight",dataIndex:f}),o.current=f)}),[f]);const g=(0,n.useCallback)((({width:e,height:t})=>{l.current&&l.current.resize({width:e,height:t})}),[]);return(0,n.useEffect)((()=>(g({width:e,height:t}),()=>{var e;return null==(e=l.current)?void 0:e.dispose()})),[]),(0,n.useLayoutEffect)((()=>{g({width:e,height:t})}),[e,t,g]),(0,m.Y)(x,{ref:d,height:t,width:e})}(0,c.Y)([k.a,h.a,s.a,i.a,d.a,l.a,f.a,o.a,g.a,p.a,w.a,v.a,b.a,E.a,O.a,y.a,I.a,R.a,A.a,j.a,C.a,H.a,T.a,Y._]);const Z=(0,n.forwardRef)(z)}}]);
//# sourceMappingURL=e4e992a5c68825831439.chunk.js.map