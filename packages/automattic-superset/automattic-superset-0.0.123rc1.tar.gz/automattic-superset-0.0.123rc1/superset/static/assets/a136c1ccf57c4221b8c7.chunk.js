"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9074],{6094:(e,t,a)=>{a.d(t,{c:()=>r,l:()=>o});var n=a(78362),l=a(96453);const i=n.A.RangePicker,r=(0,l.I4)(i)`
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,o=n.A},10044:(e,t,a)=>{a.d(t,{A:()=>i});var n=a(16146),l=a(2445);const i=e=>(0,l.Y)(n.A,{...e})},22533:(e,t,a)=>{a.d(t,{A:()=>d,v:()=>r});var n=a(96540),l=a(10044),i=a(2445);const r=()=>{var e;return null==(e=document.getElementById("controlSections"))?void 0:e.lastElementChild},o=e=>{var t,a;const n=null==(t=window)?void 0:t.innerHeight,l=null==e||null==(a=e.getBoundingClientRect())?void 0:a.top;return n&&l?l/n:0},d=({getPopupContainer:e,getVisibilityRatio:t=o,visible:a,destroyTooltipOnHide:d=!1,...c})=>{const s=(0,n.useRef)(),[u,h]=(0,n.useState)(void 0===a?c.defaultVisible:a),[v,m]=n.useState("right"),p=(0,n.useCallback)((()=>{const e=t(s.current);m(e<.35&&"rightTop"!==v?"rightTop":e>.65&&"rightBottom"!==v?"rightBottom":"right")}),[t]),g=(0,n.useCallback)((e=>{const t=r();t&&t.style.setProperty("overflow-y",e?"hidden":"auto","important")}),[p]),f=(0,n.useCallback)((t=>(s.current=t,(null==e?void 0:e(t))||document.body)),[p,e]),b=(0,n.useCallback)((e=>{void 0===e&&g(e),h(!!e),null==c.onVisibleChange||c.onVisibleChange(!!e)}),[c,g]),Y=(0,n.useCallback)((e=>{"Escape"===e.key&&(h(!1),null==c.onVisibleChange||c.onVisibleChange(!1))}),[c]);return(0,n.useEffect)((()=>{void 0!==a&&h(!!a)}),[a]),(0,n.useEffect)((()=>{void 0!==u&&g(u)}),[u,g]),(0,n.useEffect)((()=>(u&&document.addEventListener("keydown",Y),()=>{document.removeEventListener("keydown",Y)})),[Y,u]),(0,n.useEffect)((()=>{u&&p()}),[u,p]),(0,i.Y)(l.A,{...c,visible:u,arrowPointAtCenter:!0,placement:v,onVisibleChange:b,getPopupContainer:f,destroyTooltipOnHide:d})}},45267:(e,t,a)=>{a.d(t,{A:()=>_});var n=a(96540),l=a(96453),i=a(17437),r=a(37827),o=a(96627),d=a(77189),c=a(95579),s=a(46920),u=a(50317),h=a(85861),v=a(15595),m=a(12249),p=a(28990),g=a(19129),f=a(85183),b=a(27023),Y=a(15151),C=a(22533),y=a(39942),w=a(78697),D=a(2445);function A(e){let t="Last week";return y.Be.has(e.value)?t=e.value:e.onChange(t),(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Last...")}),(0,D.Y)(w.s.Group,{value:t,onChange:t=>e.onChange(t.target.value),children:y.z6.map((({value:e,label:t})=>(0,D.Y)(w.s,{value:e,className:"vertical-radio",children:t},e)))})]})}var E=a(7987);function x({onChange:e,value:t}){return(0,n.useEffect)((()=>{y.oo.has(t)||e(E.sw)}),[e,t]),y.oo.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Previous...")}),(0,D.Y)(w.s.Group,{value:t,onChange:t=>e(t.target.value),children:y.cn.map((({value:e,label:t})=>(0,D.Y)(w.s,{value:e,className:"vertical-radio",children:t},e)))})]}):null}function S({onChange:e,value:t}){return(0,n.useEffect)((()=>{y.yI.has(t)||e(E.ke)}),[t]),y.yI.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Current...")}),(0,D.Y)(w.s.Group,{value:t,onChange:t=>{let a=t.target.value;a=a.trim(),""!==a&&e(a)},children:y.ZC.map((({value:e,label:t})=>(0,D.Y)(w.s,{value:e,className:"vertical-radio",children:t},e)))})]}):null}var $=a(64846),F=a.n($),T=a(61225),N=a(13686),k=a(66537),I=a(90868),L=a(6094),V=a(17444);function M(e){const{customRange:t,matchedFlag:a}=(0,N.t)(e.value),[l,i]=(0,n.useState)(null);a||e.onChange((0,y.IS)(t));const{sinceDatetime:r,sinceMode:o,sinceGrain:d,sinceGrainValue:s,untilDatetime:u,untilMode:h,untilGrain:m,untilGrainValue:g,anchorValue:f,anchorMode:b}={...t};function Y(a,n){e.onChange((0,y.IS)({...t,[a]:n}))}function C(a,n){F()(n)&&n>0&&e.onChange((0,y.IS)({...t,[a]:n}))}const A=(0,T.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.locale}));return(0,n.useEffect)((()=>{null===l&&(A&&y.mb[A]?y.mb[A]().then((e=>i(e.default))).catch((()=>i(void 0))):i(void 0))}),[l,A]),null===l?(0,D.Y)(V.A,{position:"inline-centered"}):(0,D.FD)("div",{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure custom time range")}),(0,D.FD)(v.fI,{gutter:24,children:[(0,D.FD)(v.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(k.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(p.A,{ariaLabel:(0,c.t)("START (INCLUSIVE)"),options:y.Wm,value:o,onChange:e=>Y("sinceMode",e)}),"specific"===o&&(0,D.Y)(v.fI,{children:(0,D.Y)(L.l,{showTime:!0,defaultValue:(0,y.d$)(r),onChange:e=>Y("sinceDatetime",e.format(y.zz)),allowClear:!1,locale:l})}),"relative"===o&&(0,D.FD)(v.fI,{gutter:8,children:[(0,D.Y)(v.fv,{span:11,children:(0,D.Y)(I.YI,{placeholder:(0,c.t)("Relative quantity"),value:Math.abs(s),min:1,defaultValue:1,onChange:e=>C("sinceGrainValue",e||1),onStep:e=>C("sinceGrainValue",e||1)})}),(0,D.Y)(v.fv,{span:13,children:(0,D.Y)(p.A,{ariaLabel:(0,c.t)("Relative period"),options:y.IZ,value:d,onChange:e=>Y("sinceGrain",e)})})]})]}),(0,D.FD)(v.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(k.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(p.A,{ariaLabel:(0,c.t)("END (EXCLUSIVE)"),options:y.OP,value:h,onChange:e=>Y("untilMode",e)}),"specific"===h&&(0,D.Y)(v.fI,{children:(0,D.Y)(L.l,{showTime:!0,defaultValue:(0,y.d$)(u),onChange:e=>Y("untilDatetime",e.format(y.zz)),allowClear:!1,locale:l})}),"relative"===h&&(0,D.FD)(v.fI,{gutter:8,children:[(0,D.Y)(v.fv,{span:11,children:(0,D.Y)(I.YI,{placeholder:(0,c.t)("Relative quantity"),value:g,min:1,defaultValue:1,onChange:e=>C("untilGrainValue",e||1),onStep:e=>C("untilGrainValue",e||1)})}),(0,D.Y)(v.fv,{span:13,children:(0,D.Y)(p.A,{ariaLabel:(0,c.t)("Relative period"),options:y.s6,value:m,onChange:e=>Y("untilGrain",e)})})]})]})]}),"relative"===o&&"relative"===h&&(0,D.FD)("div",{className:"control-anchor-to",children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("Anchor to")}),(0,D.FD)(v.fI,{align:"middle",children:[(0,D.Y)(v.fv,{children:(0,D.FD)(w.s.Group,{onChange:function(a){const n=a.target.value;"now"===n?e.onChange((0,y.IS)({...t,anchorValue:"now",anchorMode:n})):e.onChange((0,y.IS)({...t,anchorValue:y.bd,anchorMode:n}))},defaultValue:"now",value:b,children:[(0,D.Y)(w.s,{value:"now",children:(0,c.t)("NOW")},"now"),(0,D.Y)(w.s,{value:"specific",children:(0,c.t)("Date/Time")},"specific")]})}),"now"!==b&&(0,D.Y)(v.fv,{children:(0,D.Y)(L.l,{showTime:!0,defaultValue:(0,y.d$)(f),onChange:e=>Y("anchorValue",e.format(y.zz)),allowClear:!1,className:"control-anchor-to-datetime",locale:l})})]})]})]})}const R=(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETIME"}),(0,D.Y)("p",{children:(0,c.t)("Return to specific datetime.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetime([string])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetime("2020-03-01 12:00:00")\ndatetime("now")\ndatetime("last year")'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATEADD"}),(0,D.Y)("p",{children:(0,c.t)("Moves the given set of dates by a specified interval.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"dateadd([datetime], [integer], [dateunit])\ndateunit = (year | quarter | month | week | day | hour | minute | second)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'dateadd(datetime("today"), -13, day)\ndateadd(datetime("2020-03-01"), 2, day)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETRUNC"}),(0,D.Y)("p",{children:(0,c.t)("Truncates the specified date to the accuracy specified by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetrunc([datetime], [dateunit])\ndateunit = (year | quarter | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetrunc(datetime("2020-03-01"), week)\ndatetrunc(datetime("2020-03-01"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"LASTDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the last date by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"lastday([datetime], [dateunit])\ndateunit = (year | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'lastday(datetime("today"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"HOLIDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the specify date for the holiday")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"holiday([string])\nholiday([holiday string], [datetime])\nholiday([holiday string], [datetime], [country name])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'holiday("new year")\nholiday("christmas", datetime("2019"))\nholiday("christmas", dateadd(datetime("2019"), 1, year))\nholiday("christmas", datetime("2 years ago"))\nholiday("Easter Monday", datetime("2019"), "UK")'})})]})]}),P=e=>{const t=(0,l.DP)();return(0,D.Y)(i.Z2,{children:({css:a})=>(0,D.Y)(g.m,{overlayClassName:a`
            .ant-tooltip-content {
              min-width: ${125*t.gridUnit}px;
              max-height: 410px;
              overflow-y: scroll;

              .ant-tooltip-inner {
                max-width: ${125*t.gridUnit}px;
                h3 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                h4 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                pre {
                  border: none;
                  text-align: left;
                  word-break: break-word;
                  font-size: ${t.typography.sizes.s}px;
                }
              }
            }
          `,...e})})};function G(e){return(0,D.Y)(P,{title:R,...e})}function z(e){return e.includes(d.wv)?e:e.startsWith("Last")?[e,""].join(d.wv):e.startsWith("Next")?["",e].join(d.wv):d.wv}function W(e){const t=z(e.value||""),[a,n]=t.split(d.wv);function l(t,l){"since"===t?e.onChange(`${l}${d.wv}${n}`):e.onChange(`${a}${d.wv}${l}`)}return t!==e.value&&e.onChange(z(e.value||"")),(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{className:"section-title",children:[(0,c.t)("Configure Advanced Time Range "),(0,D.Y)(G,{placement:"rightBottom",children:(0,D.Y)("i",{className:"fa fa-info-circle text-muted"})})]}),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(k.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(I.pd,{value:a,onChange:e=>l("since",e.target.value)},"since"),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(k.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(I.pd,{value:n,onChange:e=>l("until",e.target.value)},"until")]})}const O="#45BED6",U=l.I4.div`
  ${({theme:e,isActive:t,isPlaceholder:a})=>i.AH`
    width: 100%;
    height: ${8*e.gridUnit}px;

    display: flex;
    align-items: center;
    flex-wrap: nowrap;

    padding: 0 ${3*e.gridUnit}px;

    background-color: ${e.colors.grayscale.light5};

    border: 1px solid
      ${t?O:e.colors.grayscale.light2};
    border-radius: ${e.borderRadius}px;

    cursor: pointer;

    transition: border-color 0.3s cubic-bezier(0.65, 0.05, 0.36, 1);
    :hover,
    :focus {
      border-color: ${O};
    }

    .date-label-content {
      color: ${a?e.colors.grayscale.light1:e.colors.grayscale.dark1};
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
      flex-shrink: 1;
      white-space: nowrap;
    }

    span[role='img'] {
      margin-left: auto;
      padding-left: ${e.gridUnit}px;

      & > span[role='img'] {
        line-height: 0;
      }
    }
  `}
`,B=(0,n.forwardRef)(((e,t)=>{const a=(0,l.DP)();return(0,D.FD)(U,{...e,tabIndex:0,children:[(0,D.Y)("span",{className:"date-label-content",ref:t,children:"string"==typeof e.label?(0,c.t)(e.label):e.label}),(0,D.Y)(m.A.CalendarOutlined,{iconSize:"s",iconColor:a.colors.grayscale.base})]})})),H=(0,l.I4)(p.A)`
  width: 272px;
`,q=l.I4.div`
  ${({theme:e})=>i.AH`
    .ant-row {
      margin-top: 8px;
    }

    .ant-input-number {
      width: 100%;
    }

    .ant-picker {
      padding: 4px 17px 4px;
      border-radius: 4px;
      width: 100%;
    }

    .ant-divider-horizontal {
      margin: 16px 0;
    }

    .control-label {
      font-size: 11px;
      font-weight: ${e.typography.weights.medium};
      color: ${e.colors.grayscale.light2};
      line-height: 16px;
      margin: 8px 0;
    }

    .vertical-radio {
      display: block;
      height: 40px;
      line-height: 40px;
    }

    .section-title {
      font-style: normal;
      font-weight: ${e.typography.weights.bold};
      font-size: 15px;
      line-height: 24px;
      margin-bottom: 8px;
    }

    .control-anchor-to {
      margin-top: 16px;
    }

    .control-anchor-to-datetime {
      width: 217px;
    }

    .footer {
      text-align: right;
    }
  `}
`,K=l.I4.span`
  span {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
    vertical-align: middle;
  }
  .text {
    vertical-align: middle;
  }
  .error {
    color: ${({theme:e})=>e.colors.error.base};
  }
`,Z=(e,t,a)=>e?(0,D.FD)("div",{children:[t&&(0,D.Y)("strong",{children:t}),a&&(0,D.Y)("div",{css:e=>i.AH`
            margin-top: ${e.gridUnit}px;
          `,children:a})]}):a||null;function _(e){var t;const{onChange:a,onOpenPopover:i=Y.fZ,onClosePopover:p=Y.fZ,overlayStyle:w="Popover",isOverflowingFilterBar:E=!1}=e,$=(0,y.IM)(),F=null!=(t=e.value)?t:$,[T,N]=(0,n.useState)(F),[k,I]=(0,n.useState)(!1),L=(0,n.useMemo)((()=>(0,y.J5)(F)),[F]),[V,R]=(0,n.useState)(L),[P,G]=(0,n.useState)(F),[z,O]=(0,n.useState)(F),[U,_]=(0,n.useState)(!1),[J,j]=(0,n.useState)(F),[X,Q]=(0,n.useState)(F),ee=(0,l.DP)(),[te,ae]=(0,r.A)();function ne(){O(F),R(L),I(!1),p()}(0,n.useEffect)((()=>{if(F===o.WC)return N(o.WC),Q(null),void _(!0);(0,d.x9)(F).then((({value:e,error:t})=>{t?(j(t||""),_(!1),Q(F||null)):("Common"===L||"Calendar"===L||"Current"===L||"No filter"===L?(N(F),Q(Z(ae,F,e))):(N(e||""),Q(Z(ae,e,F))),_(!0)),G(F),j(e||F)}))}),[L,ae,te,F]),(0,f.sv)((()=>{if(z===o.WC)return j(o.WC),G(o.WC),void _(!0);P!==z&&(0,d.x9)(z).then((({value:e,error:t})=>{t?(j(t||""),_(!1)):(j(e||""),_(!0)),G(z)}))}),b.Qs,[z]);const le=()=>{k?ne():(O(F),R(L),I(!0),i())},ie=(0,D.FD)(q,{children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("RANGE TYPE")}),(0,D.Y)(H,{ariaLabel:(0,c.t)("RANGE TYPE"),options:y.BJ,value:V,onChange:function(e){e===o.WC&&O(o.WC),R(e)}}),"No filter"!==V&&(0,D.Y)(v.cG,{}),"Common"===V&&(0,D.Y)(A,{value:z,onChange:O}),"Calendar"===V&&(0,D.Y)(x,{value:z,onChange:O}),"Current"===V&&(0,D.Y)(S,{value:z,onChange:O}),"Advanced"===V&&(0,D.Y)(W,{value:z,onChange:O}),"Custom"===V&&(0,D.Y)(M,{value:z,onChange:O}),"No filter"===V&&(0,D.Y)("div",{}),(0,D.Y)(v.cG,{}),(0,D.FD)("div",{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Actual time range")}),U&&(0,D.Y)("div",{children:"No filter"===J?(0,c.t)("No filter"):J}),!U&&(0,D.FD)(K,{className:"warning",children:[(0,D.Y)(m.A.ErrorSolidSmall,{iconColor:ee.colors.error.base}),(0,D.Y)("span",{className:"text error",children:J})]})]}),(0,D.Y)(v.cG,{}),(0,D.FD)("div",{className:"footer",children:[(0,D.Y)(s.A,{buttonStyle:"secondary",cta:!0,onClick:ne,children:(0,c.t)("CANCEL")},"cancel"),(0,D.Y)(s.A,{buttonStyle:"primary",cta:!0,disabled:!U,onClick:function(){a(z),I(!1),p()},children:(0,c.t)("APPLY")},"apply")]})]}),re=(0,D.FD)(K,{children:[(0,D.Y)(m.A.EditAlt,{iconColor:ee.colors.grayscale.base}),(0,D.Y)("span",{className:"text",children:(0,c.t)("Edit time range")})]}),oe=(0,D.Y)(C.A,{placement:"right",trigger:"click",content:ie,title:re,defaultVisible:k,visible:k,onVisibleChange:le,overlayStyle:{width:"600px"},getPopupContainer:e=>E?e.parentNode:document.body,destroyTooltipOnHide:!0,children:(0,D.Y)(g.m,{placement:"top",title:X,getPopupContainer:e=>e.parentElement,children:(0,D.Y)(B,{label:T,isActive:k,isPlaceholder:T===o.WC,ref:te})})}),de=(0,D.FD)(D.FK,{children:[(0,D.Y)(g.m,{placement:"top",title:X,getPopupContainer:e=>e.parentElement,children:(0,D.Y)(B,{onClick:le,label:T,isActive:k,isPlaceholder:T===o.WC,ref:te})}),(0,D.Y)(h.A,{title:re,show:k,onHide:le,width:"600px",hideFooter:!0,zIndex:1030,children:ie})]});return(0,D.FD)(D.FK,{children:[(0,D.Y)(u.A,{...e}),"Modal"===w?de:oe]})}},39074:(e,t,a)=>{a.d(t,{Ay:()=>n.A});var n=a(45267);a(39942)},7987:(e,t,a)=>{a.d(t,{RV:()=>c,be:()=>i,cJ:()=>d,ke:()=>o,kw:()=>s,oF:()=>l,sw:()=>n,u_:()=>r});const n="previous calendar week",l="previous calendar month",i="previous calendar year",r="Current day",o="Current week",d="Current month",c="Current year",s="Current quarter"},39942:(e,t,a)=>{a.d(t,{cn:()=>s,oo:()=>C,nS:()=>u,z6:()=>d,Be:()=>Y,OL:()=>c,yI:()=>y,ZC:()=>h,Ex:()=>v,BJ:()=>o,mb:()=>A,bd:()=>D,zz:()=>w,IZ:()=>p,Wm:()=>f,s6:()=>g,OP:()=>b,IS:()=>N,d$:()=>F,J5:()=>V,IM:()=>M});var n=a(95093),l=a.n(n),i=a(95579),r=a(7987);const o=[{value:"Common",label:(0,i.t)("Last")},{value:"Calendar",label:(0,i.t)("Previous")},{value:"Current",label:(0,i.t)("Current")},{value:"Custom",label:(0,i.t)("Custom")},{value:"Advanced",label:(0,i.t)("Advanced")},{value:"No filter",label:(0,i.t)("No filter")}],d=[{value:"Last day",label:(0,i.t)("Last day")},{value:"Last week",label:(0,i.t)("Last week")},{value:"Last month",label:(0,i.t)("Last month")},{value:"Last quarter",label:(0,i.t)("Last quarter")},{value:"Last year",label:(0,i.t)("Last year")}],c=new Set(d.map((({value:e})=>e))),s=[{value:r.sw,label:(0,i.t)("previous calendar week")},{value:r.oF,label:(0,i.t)("previous calendar month")},{value:r.be,label:(0,i.t)("previous calendar year")}],u=new Set(s.map((({value:e})=>e))),h=[{value:r.u_,label:(0,i.t)("Current day")},{value:r.ke,label:(0,i.t)("Current week")},{value:r.cJ,label:(0,i.t)("Current month")},{value:r.kw,label:(0,i.t)("Current quarter")},{value:r.RV,label:(0,i.t)("Current year")}],v=new Set(h.map((({value:e})=>e))),m=[{value:"second",label:e=>(0,i.t)("Seconds %s",e)},{value:"minute",label:e=>(0,i.t)("Minutes %s",e)},{value:"hour",label:e=>(0,i.t)("Hours %s",e)},{value:"day",label:e=>(0,i.t)("Days %s",e)},{value:"week",label:e=>(0,i.t)("Weeks %s",e)},{value:"month",label:e=>(0,i.t)("Months %s",e)},{value:"quarter",label:e=>(0,i.t)("Quarters %s",e)},{value:"year",label:e=>(0,i.t)("Years %s",e)}],p=m.map((e=>({value:e.value,label:e.label((0,i.t)("Before"))}))),g=m.map((e=>({value:e.value,label:e.label((0,i.t)("After"))}))),f=[{value:"specific",label:(0,i.t)("Specific Date/Time")},{value:"relative",label:(0,i.t)("Relative Date/Time")},{value:"now",label:(0,i.t)("Now")},{value:"today",label:(0,i.t)("Midnight")}],b=f.slice(),Y=new Set(["Last day","Last week","Last month","Last quarter","Last year"]),C=new Set([r.sw,r.oF,r.be]),y=new Set([r.u_,r.ke,r.cJ,r.kw,r.RV]),w="YYYY-MM-DD[T]HH:mm:ss",D=(l()().utc().startOf("day").subtract(7,"days").format(w),l()().utc().startOf("day").format(w)),A={en:()=>Promise.resolve().then(a.bind(a,33087)),fr:()=>a.e(4394).then(a.bind(a,64394)),es:()=>a.e(9062).then(a.bind(a,9062)),it:()=>a.e(2936).then(a.bind(a,92936)),zh:()=>a.e(3009).then(a.bind(a,83009)),ja:()=>a.e(7595).then(a.bind(a,97595)),de:()=>a.e(12).then(a.bind(a,50012)),pt:()=>a.e(4998).then(a.bind(a,94998)),pt_BR:()=>a.e(1330).then(a.bind(a,21330)),ru:()=>a.e(5860).then(a.bind(a,95860)),ko:()=>a.e(6461).then(a.bind(a,6461)),sk:()=>a.e(3610).then(a.bind(a,23610)),sl:()=>a.e(8639).then(a.bind(a,78639)),nl:()=>a.e(1982).then(a.bind(a,21982))};var E;!function(e){e.CommonFrame="common-frame",e.ModalOverlay="modal-overlay",e.PopoverOverlay="time-range-trigger",e.NoFilter="no-filter",e.CancelButton="cancel-button",e.ApplyButton="date-filter-control__apply-button"}(E||(E={}));const x=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,S=String.raw`(?:TODAY|NOW)`,$=(RegExp(String.raw`^${x}$|^${S}$`,"i"),["specific","today","now"]),F=e=>"now"===e?l()().utc().startOf("second"):"today"===e?l()().utc().startOf("day"):l()(e),T=e=>F(e).format(w),N=e=>{const{sinceDatetime:t,sinceMode:a,sinceGrain:n,sinceGrainValue:l,untilDatetime:i,untilMode:r,untilGrain:o,untilGrainValue:d,anchorValue:c}={...e};if($.includes(a)&&$.includes(r))return`${"specific"===a?T(t):a} : ${"specific"===r?T(i):r}`;if($.includes(a)&&"relative"===r){const e="specific"===a?T(t):a;return`${e} : DATEADD(DATETIME("${e}"), ${d}, ${o})`}if("relative"===a&&$.includes(r)){const e="specific"===r?T(i):r;return`DATEADD(DATETIME("${e}"), ${-Math.abs(l)}, ${n}) : ${e}`}return`DATEADD(DATETIME("${c}"), ${-Math.abs(l)}, ${n}) : DATEADD(DATETIME("${c}"), ${d}, ${o})`};var k=a(96627),I=a(13686),L=a(61225);const V=e=>c.has(e)?"Common":u.has(e)?"Calendar":v.has(e)?"Current":e===k.WC?"No filter":(0,I.t)(e).matchedFlag?"Custom":"Advanced";function M(){var e;return null!=(e=(0,L.d4)((e=>{var t,a;return null==e||null==(t=e.common)||null==(a=t.conf)?void 0:a.DEFAULT_TIME_FILTER})))?e:k.WC}}}]);
//# sourceMappingURL=a136c1ccf57c4221b8c7.chunk.js.map