"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[5721],{55721:(e,t,r)=>{r.r(t),r.d(t,{default:()=>w});var o=r(62193),n=r.n(o),i=r(96540),s=r(96453),l=r(49277),a=r(62952),c=r(77189),d=r(17437),u=r(95579),f=r(97689),h=r(45186),m=r(38221),p=r.n(m);const g=e=>{const t=(0,i.useRef)(null),r=(0,i.useRef)(null),[o,n]=(0,i.useState)(!1);return(0,i.useEffect)((()=>{let o;const i=t.current,s=r.current;if(i&&s){const t=Array.from(i.children);o=new ResizeObserver(p()((()=>{t.reduce(((e,t)=>{var r,o;return e+(null!=(r=null==(o=t.firstElementChild)?void 0:o.scrollWidth)?r:0)}),0)+e*Math.max(t.length-1,0)>s.clientWidth?n(!0):n(!1)}),500)),o.observe(document.body),t.forEach((e=>{o.observe(e)}))}return()=>{var e;return null==(e=o)?void 0:e.disconnect()}}),[e]),{isOverflowing:o,symbolContainerRef:t,wrapperRef:r}};var b=r(2445);const x=s.I4.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  width: 100%;
  overflow: auto;
`,v=s.I4.div`
  ${({theme:e,subheaderFontSize:t})=>`\n    font-weight: ${e.typography.weights.light};\n    display: flex;\n    justify-content: center;\n    font-size: ${t||20}px;\n    flex: 1 1 0px;\n  `}
`,y=s.I4.span`
  ${({theme:e,backgroundColor:t,textColor:r})=>`\n    background-color: ${t};\n    color: ${r};\n    padding: ${e.gridUnit}px ${2*e.gridUnit}px;\n    border-radius: ${2*e.gridUnit}px;\n    margin-right: ${e.gridUnit}px;\n  `}
`;function w(e){const{height:t,width:r,bigNumber:o,prevNumber:m,valueDifference:p,percentDifferenceFormattedString:w,headerFontSize:$,subheaderFontSize:C,comparisonColorEnabled:R,comparisonColorScheme:k,percentDifferenceNumber:A,currentTimeRangeFilter:D,startDateOffset:F,shift:S,dashboardTimeRange:T}=e,[z,H]=(0,i.useState)("");(0,i.useEffect)((()=>{if(D&&(S||F)){if(!n()(S)||F){const e=(0,l.TX)({timeRangeFilter:{...D,comparator:null!=T?T:D.comparator},shifts:(0,a.A)(S),startDate:F||""}),t=(0,c.x9)(null!=T?T:D.comparator,D.subject,e||[]);Promise.resolve(t).then((e=>{const t=(0,a.A)(e.value).flat()[0].split("vs\n");H(t.length>1?t[1].trim():t[0])}))}}else H("")}),[D,S,F,T]);const U=(0,s.DP)(),j=5*U.gridUnit,E=d.AH`
    font-family: ${U.typography.families.sansSerif};
    display: flex;
    justify-content: center;
    align-items: center;
    height: ${t}px;
    width: ${r}px;
    overflow: auto;
  `,Y=d.AH`
    font-size: ${$||60}px;
    font-weight: ${U.typography.weights.normal};
    text-align: center;
    margin-bottom: ${4*U.gridUnit}px;
  `,O=d.AH`
    color: ${R&&0!==A?A>0?k===h.m.Green?U.colors.success.base:U.colors.error.base:k===h.m.Red?U.colors.success.base:U.colors.error.base:U.colors.grayscale.base};
    margin-left: ${U.gridUnit}px;
  `,I=U.colors.grayscale.light4,M=U.colors.grayscale.base,{backgroundColor:N,textColor:P}=(0,i.useMemo)((()=>{let e=I,t=M;if(R&&0!==A){const r=A>0&&k===h.m.Green||A<0&&k===h.m.Red;e=r?U.colors.success.light2:U.colors.error.light2,t=r?U.colors.success.base:U.colors.error.base}return{backgroundColor:e,textColor:t}}),[U,k,R,A]),G=(0,i.useMemo)((()=>[{symbol:"#",value:m,tooltipText:(0,u.t)("Data for %s",z||"previous range")},{symbol:"△",value:p,tooltipText:(0,u.t)("Value difference between the time periods")},{symbol:"%",value:w,tooltipText:(0,u.t)("Percentage difference between the time periods")}]),[z,m,p,w]),{isOverflowing:W,symbolContainerRef:V,wrapperRef:X}=g(j);return(0,b.Y)("div",{css:E,ref:X,children:(0,b.FD)(x,{css:W&&d.AH`
            width: fit-content;
            margin: auto;
            align-items: flex-start;
          `,children:[(0,b.FD)("div",{css:Y,children:[o,0!==A&&(0,b.Y)("span",{css:O,children:A>0?"↑":"↓"})]}),(0,b.Y)("div",{css:[d.AH`
              display: flex;
              justify-content: space-around;
              gap: ${j}px;
              min-width: 0;
              flex-shrink: 1;
            `,W?d.AH`
                  flex-direction: column;
                  align-items: flex-start;
                  width: fit-content;
                `:d.AH`
                  align-items: center;
                  width: 100%;
                `,"",""],ref:V,children:G.map(((e,t)=>(0,b.Y)(v,{subheaderFontSize:C,children:(0,b.FD)(f.m,{id:"tooltip",placement:"top",title:e.tooltipText,children:[(0,b.Y)(y,{backgroundColor:t>0?N:I,textColor:t>0?P:M,children:e.symbol}),e.value]})},`comparison-symbol-${e.symbol}`)))})]})})}}}]);
//# sourceMappingURL=b5c87816b0adbd109537.chunk.js.map