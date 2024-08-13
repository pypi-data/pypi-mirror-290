"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[7976],{86523:(e,t,r)=>{r.d(t,{A:()=>n});var i=r(77925);const n=(0,r(96453).I4)(i.A.Item)`
  ${({theme:e})=>`\n    .ant-form-item-label {\n      padding-bottom: ${e.gridUnit}px;\n      & > label {\n        font-size: ${e.typography.sizes.s}px;\n        color: ${e.colors.grayscale.base};\n\n        &.ant-form-item-required:not(.ant-form-item-required-mark-optional) {\n          &::before {\n            display: none;\n          }\n          &::after {\n            display: inline-block;\n            color: ${e.colors.error.base};\n            font-size: ${e.typography.sizes.s}px;\n            content: '*';\n          }\n        }\n      }\n    }\n  `}
`},40458:(e,t,r)=>{r.d(t,{A:()=>a});var i=r(96453),n=r(2445);const o=i.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
`,l=i.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
  &::after {
    display: inline-block;
    margin-left: ${({theme:e})=>e.gridUnit}px;
    color: ${({theme:e})=>e.colors.error.base};
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
    content: '*';
  }
`;function a({children:e,htmlFor:t,required:r=!1,className:i}){const a=r?l:o;return(0,n.Y)(a,{htmlFor:t,className:i,children:e})}},97987:(e,t,r)=>{r.d(t,{A:()=>k});var i,n=r(36255),o=r(27236),l=r(96453),a=r(17437),s=r(95579),d=r(31641),c=r(12249),h=r(46920),p=r(96540);function m(){return m=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var i in r)({}).hasOwnProperty.call(r,i)&&(e[i]=r[i])}return e},m.apply(null,arguments)}const g=({title:e,titleId:t,...r},n)=>p.createElement("svg",m({xmlns:"http://www.w3.org/2000/svg",width:24,height:24,fill:"none",ref:n,"aria-labelledby":t},r),e?p.createElement("title",{id:t},e):null,i||(i=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M12 7a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V8a1 1 0 0 0-1-1m0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9.71-7.44-5.27-5.27a1.05 1.05 0 0 0-.71-.29H8.27a1.05 1.05 0 0 0-.71.29L2.29 7.56a1.05 1.05 0 0 0-.29.71v7.46c.004.265.107.518.29.71l5.27 5.27c.192.183.445.286.71.29h7.46a1.05 1.05 0 0 0 .71-.29l5.27-5.27a1.05 1.05 0 0 0 .29-.71V8.27a1.05 1.05 0 0 0-.29-.71M20 15.31 15.31 20H8.69L4 15.31V8.69L8.69 4h6.62L20 8.69z",clipRule:"evenodd"}))),u=(0,p.forwardRef)(g);var b=r(86523),v=r(40458),f=r(2445);const x=(0,l.I4)(n.A)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,$=(0,l.I4)(n.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,y=(0,l.I4)("div")`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`,w=l.I4.div`
  display: flex;
  align-items: center;
`,A=(0,l.I4)(v.A)`
  margin-bottom: 0;
`,Y=a.AH`
  &.anticon > * {
    line-height: 0;
  }
`,k=({label:e,validationMethods:t,errorMessage:r,helpText:i,required:n=!1,hasTooltip:l=!1,tooltipText:p,id:m,className:g,visibilityToggle:v,get_url:k,description:I,...F})=>(0,f.FD)(y,{className:g,children:[(0,f.FD)(w,{children:[(0,f.Y)(A,{htmlFor:m,required:n,children:e}),l&&(0,f.Y)(d.A,{tooltip:`${p}`})]}),(0,f.FD)(b.A,{css:e=>((e,t)=>a.AH`
  .ant-form-item-children-icon {
    display: none;
  }
  ${t&&`.ant-form-item-control-input-content {\n      position: relative;\n      &:after {\n        content: ' ';\n        display: inline-block;\n        background: ${e.colors.error.base};\n        mask: url(${u});\n        mask-size: cover;\n        width: ${4*e.gridUnit}px;\n        height: ${4*e.gridUnit}px;\n        position: absolute;\n        right: ${1.25*e.gridUnit}px;\n        top: ${2.75*e.gridUnit}px;\n      }\n    }`}
`)(e,!!r),validateTrigger:Object.keys(t),validateStatus:r?"error":"success",help:r||i,hasFeedback:!!r,children:[v||"password"===F.name?(0,f.Y)($,{...F,...t,iconRender:e=>e?(0,f.Y)(o.A,{title:(0,s.t)("Hide password."),children:(0,f.Y)(c.A.EyeInvisibleOutlined,{iconSize:"m",css:Y})}):(0,f.Y)(o.A,{title:(0,s.t)("Show password."),children:(0,f.Y)(c.A.EyeOutlined,{iconSize:"m",css:Y})}),role:"textbox"}):(0,f.Y)(x,{...F,...t}),k&&I?(0,f.FD)(h.A,{type:"link",htmlType:"button",buttonStyle:"default",onClick:()=>(window.open(k),!0),children:["Get ",I]}):(0,f.Y)("br",{})]})]})},40563:(e,t,r)=>{r.d(t,{lV:()=>a,eI:()=>s.A,lR:()=>d.A,MA:()=>c.A});var i=r(77925),n=r(96453),o=r(2445);const l=(0,n.I4)(i.A)`
  &.ant-form label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }
`;function a(e){return(0,o.Y)(l,{...e})}var s=r(86523),d=r(40458),c=r(97987)},31641:(e,t,r)=>{r.d(t,{A:()=>h});var i=r(96453),n=r(19129),o=r(12249),l=r(2445);const a=(0,i.I4)(n.m)`
  cursor: pointer;
`,s=i.I4.span`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,d={fontSize:"12px",lineHeight:"16px"},c="rgba(0,0,0,0.9)";function h({tooltip:e,iconStyle:t={},placement:r="right",trigger:n="hover",overlayStyle:h=d,bgColor:p=c,viewBox:m="0 -1 24 24"}){const g=(0,i.DP)(),u={...t,color:t.color||g.colors.grayscale.base};return(0,l.Y)(a,{title:(0,l.Y)(s,{children:e}),placement:r,trigger:n,overlayStyle:h,color:p,children:(0,l.Y)(o.A.InfoSolidSmall,{style:u,viewBox:m})})}},90868:(e,t,r)=>{r.d(t,{YI:()=>a,fs:()=>s,pd:()=>l});var i=r(96453),n=r(36255),o=r(89542);const l=(0,i.I4)(n.A)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,a=(0,i.I4)(o.A)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,s=(0,i.I4)(n.A.TextArea)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`},78697:(e,t,r)=>{r.d(t,{s:()=>a});var i=r(96453),n=r(1612);const o=(0,i.I4)(n.Ay)`
  .ant-radio-inner {
    top: -1px;
    left: 2px;
    width: ${({theme:e})=>4*e.gridUnit}px;
    height: ${({theme:e})=>4*e.gridUnit}px;
    border-width: 2px;
    border-color: ${({theme:e})=>e.colors.grayscale.light2};
  }

  .ant-radio.ant-radio-checked {
    .ant-radio-inner {
      border-width: ${({theme:e})=>e.gridUnit+1}px;
      border-color: ${({theme:e})=>e.colors.primary.base};
    }

    .ant-radio-inner::after {
      background-color: ${({theme:e})=>e.colors.grayscale.light5};
      top: 0;
      left: 0;
      width: ${({theme:e})=>e.gridUnit+2}px;
      height: ${({theme:e})=>e.gridUnit+2}px;
    }
  }

  .ant-radio:hover,
  .ant-radio:focus {
    .ant-radio-inner {
      border-color: ${({theme:e})=>e.colors.primary.dark1};
    }
  }
`,l=(0,i.I4)(n.Ay.Group)`
  font-size: inherit;
`,a=Object.assign(o,{Group:l,Button:n.Ay.Button})},50317:(e,t,r)=>{r.d(t,{A:()=>m});var i=r(96540),n=r(17437),o=r(96453),l=r(95579),a=r(66537),s=r(19129),d=r(40563),c=r(12249),h=r(2445);const p=n.AH`
  &.anticon {
    font-size: unset;
    .anticon {
      line-height: unset;
      vertical-align: unset;
    }
  }
`,m=({name:e,label:t,description:r,validationErrors:m=[],renderTrigger:g=!1,rightNode:u,leftNode:b,onClick:v,hovered:f=!1,tooltipOnClick:x=(()=>{}),warning:$,danger:y})=>{const{gridUnit:w,colors:A}=(0,o.DP)(),Y=(0,i.useRef)(!1),k=(0,i.useMemo)((()=>(m.length||(Y.current=!0),Y.current?m.length?A.error.base:"unset":A.alert.base)),[A.error.base,A.alert.base,m.length]);return t?(0,h.FD)("div",{className:"ControlHeader",children:[(0,h.Y)("div",{className:"pull-left",children:(0,h.FD)(d.lR,{css:e=>n.AH`
            margin-bottom: ${.5*e.gridUnit}px;
            position: relative;
          `,children:[b&&(0,h.Y)("span",{children:b}),(0,h.Y)("span",{role:"button",tabIndex:0,onClick:v,style:{cursor:v?"pointer":""},children:t})," ",$&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:$,children:(0,h.Y)(c.A.AlertSolid,{iconColor:A.alert.base,iconSize:"s"})})," "]}),y&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:y,children:(0,h.Y)(c.A.ErrorSolid,{iconColor:A.error.base,iconSize:"s"})})," "]}),(null==m?void 0:m.length)>0&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:null==m?void 0:m.join(" "),children:(0,h.Y)(c.A.ExclamationCircleOutlined,{css:n.AH`
                    ${p};
                    color: ${k};
                  `})})," "]}),f?(0,h.FD)("span",{css:()=>n.AH`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${w}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `,children:[r&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"description-tooltip",title:r,placement:"top",children:(0,h.Y)(c.A.InfoCircleOutlined,{css:p,onClick:x})})," "]}),g&&(0,h.FD)("span",{children:[(0,h.Y)(a.W,{label:(0,l.t)("bolt"),tooltip:(0,l.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," "]})]}):null]})}),u&&(0,h.Y)("div",{className:"pull-right",children:u}),(0,h.Y)("div",{className:"clearfix"})]}):null}},87615:(e,t,r)=>{r.r(t),r.d(t,{default:()=>h});var i=r(96453),n=r(96627),o=r(96540),l=r(39074),a=r(67874),s=r(2445);const d=(0,i.I4)(a.j3)`
  display: flex;
  align-items: center;
  overflow-x: auto;

  & .ant-tag {
    margin-right: 0;
  }
`,c=i.I4.div`
  display: flex;
  height: 100%;
  max-width: 100%;
  width: 100%;
  & > div,
  & > div:hover {
    ${({validateStatus:e,theme:t})=>{var r;return e&&`border-color: ${null==(r=t.colors[e])?void 0:r.base}`}}
  }
`;function h(e){var t;const{setDataMask:r,setHoveredFilter:i,unsetHoveredFilter:a,setFocusedFilter:h,unsetFocusedFilter:p,setFilterActive:m,width:g,height:u,filterState:b,inputRef:v,isOverflowingFilterBar:f=!1}=e,x=(0,o.useCallback)((e=>{const t=e&&e!==n.WC;r({extraFormData:t?{time_range:e}:{},filterState:{value:t?e:void 0}})}),[r]);return(0,o.useEffect)((()=>{x(b.value)}),[b.value]),null!=(t=e.formData)&&t.inView?(0,s.Y)(d,{width:g,height:u,children:(0,s.Y)(c,{ref:v,validateStatus:b.validateStatus,onFocus:h,onBlur:p,onMouseEnter:i,onMouseLeave:a,children:(0,s.Y)(l.Ay,{value:b.value||n.WC,name:"time_range",onChange:x,onOpenPopover:()=>m(!0),onClosePopover:()=>{m(!1),a(),p()},isOverflowingFilterBar:f})})}):null}},67874:(e,t,r)=>{r.d(t,{JF:()=>a,Mo:()=>s,YH:()=>o,j3:()=>l});var i=r(96453),n=r(86523);const o=0,l=i.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===o?"100%":`${e}px`};
`,a=(0,i.I4)(n.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,s=i.I4.div`
  color: ${({theme:e,status:t="error"})=>{var r;return null==(r=e.colors[t])?void 0:r.base}};
`}}]);
//# sourceMappingURL=b9ef43208c0a3f533a49.chunk.js.map