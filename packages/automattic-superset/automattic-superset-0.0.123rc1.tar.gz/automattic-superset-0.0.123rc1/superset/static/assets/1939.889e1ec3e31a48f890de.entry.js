(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1939],{19593:e=>{const t=[null];e.exports=t.length<=1?t[0]:t},25946:(e,t,n)=>{"use strict";n.d(t,{A:()=>l});var r=n(17437),o=n(94535),a=n(96453),i=n(12249),s=n(2445);function l(e){const{type:t="info",description:n,showIcon:l=!0,closable:d=!0,roomBelow:c=!1,children:u}=e,p=(0,a.DP)(),{colors:h,typography:m,gridUnit:g}=p,{alert:b,error:f,info:v,success:y}=h;let $=v,x=i.A.InfoSolid;return"error"===t?($=f,x=i.A.ErrorSolid):"warning"===t?($=b,x=i.A.AlertSolid):"success"===t&&($=y,x=i.A.CircleCheckSolid),(0,s.Y)(o.default,{role:"alert",showIcon:l,icon:(0,s.Y)(x,{"aria-label":`${t} icon`}),closeText:d&&(0,s.Y)(i.A.XSmall,{"aria-label":"close icon"}),css:(0,r.AH)({marginBottom:c?4*g:0,padding:`${2*g}px ${3*g}px`,alignItems:"flex-start",border:0,backgroundColor:$.light2,"& .ant-alert-icon":{marginRight:2*g},"& .ant-alert-message":{color:$.dark2,fontSize:m.sizes.m,fontWeight:n?m.weights.bold:m.weights.normal},"& .ant-alert-description":{color:$.dark2,fontSize:m.sizes.m}},"",""),...e,children:u})}},24976:(e,t,n)=>{"use strict";n.d(t,{_p:()=>x,rN:()=>y,pw:()=>b,iN:()=>$,nt:()=>f,YU:()=>g,S9:()=>v,jS:()=>p});var r=n(96540),o=n(49262),a=n(86963),i=n(96453),s=n(17437),l=n(2445),d=n(37057),c=n(15595);const u=({title:e,icon:t,body:n,meta:r,footer:o})=>(0,l.FD)("div",{className:"tooltip-detail",children:[(0,l.FD)("div",{className:"tooltip-detail-head",children:[(0,l.FD)("div",{className:"tooltip-detail-title",children:[t,e]}),r&&(0,l.Y)("span",{className:"tooltip-detail-meta",children:(0,l.Y)(c.vw,{color:"default",children:r})})]}),n&&(0,l.Y)("div",{className:"tooltip-detail-body",children:null!=n?n:e}),o&&(0,l.Y)("div",{className:"tooltip-detail-footer",children:o})]}),p=e=>`${(0,d.renderToStaticMarkup)((0,l.Y)(u,{...e}))}`,h={"mode/sql":()=>n.e(2514).then(n.t.bind(n,32514,23)),"mode/markdown":()=>Promise.all([n.e(7472),n.e(9620),n.e(9846),n.e(7613)]).then(n.t.bind(n,7613,23)),"mode/css":()=>Promise.all([n.e(9620),n.e(9994)]).then(n.t.bind(n,29994,23)),"mode/json":()=>n.e(9118).then(n.t.bind(n,59118,23)),"mode/yaml":()=>n.e(7215).then(n.t.bind(n,97215,23)),"mode/html":()=>Promise.all([n.e(7472),n.e(9620),n.e(9846),n.e(6861)]).then(n.t.bind(n,56861,23)),"mode/javascript":()=>Promise.all([n.e(7472),n.e(8263)]).then(n.t.bind(n,8263,23)),"theme/textmate":()=>n.e(2694).then(n.t.bind(n,52694,23)),"theme/github":()=>n.e(3139).then(n.t.bind(n,83139,23)),"ext/language_tools":()=>n.e(6464).then(n.t.bind(n,6464,23)),"ext/searchbox":()=>n.e(8949).then(n.t.bind(n,88949,23))};function m(e,{defaultMode:t,defaultTheme:d,defaultTabSize:c=2,fontFamily:u="Menlo, Consolas, Courier New, Ubuntu Mono, source-code-pro, Lucida Console, monospace",placeholder:p}={}){return(0,o.A)((async()=>{var o,p;const m=Promise.all([n.e(8096),n.e(952),n.e(1541)]).then(n.bind(n,70470)),g=n.e(952).then(n.t.bind(n,80952,23)),b=n.e(61).then(n.t.bind(n,70061,17)),f=n.e(4987).then(n.t.bind(n,34987,23)),[{default:v},{config:y},{default:$},{acequire:x}]=await Promise.all([m,g,b,f]);y.setModuleUrl("ace/mode/css_worker",$),await Promise.all(e.map((e=>h[e]())));const w=t||(null==(o=e.find((e=>e.startsWith("mode/"))))?void 0:o.replace("mode/","")),_=d||(null==(p=e.find((e=>e.startsWith("theme/"))))?void 0:p.replace("theme/",""));return(0,r.forwardRef)((function({keywords:e,mode:t=w,theme:n=_,tabSize:o=c,defaultValue:d="",...p},h){const m=(0,i.DP)(),g=x("ace/ext/language_tools"),b=(0,a.A)((e=>{const n={getCompletions:(n,r,o,a,i)=>{Number.isNaN(parseInt(a,10))&&r.getMode().$id===`ace/mode/${t}`&&i(null,e)}};g.setCompleters([n])}));return(0,r.useEffect)((()=>{e&&b(e)}),[e,b]),(0,l.FD)(l.FK,{children:[(0,l.Y)(s.mL,{styles:s.AH`
                .ace_tooltip {
                  margin-left: ${2*m.gridUnit}px;
                  padding: 0px;
                  border: 1px solid ${m.colors.grayscale.light1};
                }

                & .tooltip-detail {
                  background-color: ${m.colors.grayscale.light5};
                  white-space: pre-wrap;
                  word-break: break-all;
                  min-width: ${50*m.gridUnit}px;
                  max-width: ${100*m.gridUnit}px;
                  & .tooltip-detail-head {
                    background-color: ${m.colors.grayscale.light4};
                    color: ${m.colors.grayscale.dark1};
                    display: flex;
                    column-gap: ${m.gridUnit}px;
                    align-items: baseline;
                    justify-content: space-between;
                  }
                  & .tooltip-detail-title {
                    display: flex;
                    column-gap: ${m.gridUnit}px;
                  }
                  & .tooltip-detail-body {
                    word-break: break-word;
                  }
                  & .tooltip-detail-head,
                  & .tooltip-detail-body {
                    padding: ${m.gridUnit}px
                      ${2*m.gridUnit}px;
                  }
                  & .tooltip-detail-footer {
                    border-top: 1px ${m.colors.grayscale.light2}
                      solid;
                    padding: 0 ${2*m.gridUnit}px;
                    color: ${m.colors.grayscale.dark1};
                    font-size: ${m.typography.sizes.xs}px;
                  }
                  & .tooltip-detail-meta {
                    & > .ant-tag {
                      margin-right: 0px;
                    }
                  }
                }
              `}),(0,l.Y)(v,{ref:h,mode:t,theme:n,tabSize:o,defaultValue:d,setOptions:{fontFamily:u},...p})]})}))}),p)}const g=m(["mode/sql","theme/github","ext/language_tools","ext/searchbox"]),b=m(["mode/sql","theme/github","ext/language_tools","ext/searchbox"],{placeholder:()=>(0,l.FD)("div",{style:{height:"100%"},children:[(0,l.Y)("div",{style:{width:41,height:"100%",background:"#e8e8e8"}}),(0,l.Y)("div",{className:"ace_content"})]})}),f=m(["mode/markdown","theme/textmate"]),v=m(["mode/markdown","mode/sql","mode/json","mode/html","mode/javascript","theme/textmate"]),y=m(["mode/css","theme/github"]),$=m(["mode/json","theme/github"]),x=m(["mode/json","mode/yaml","theme/github"])},49262:(e,t,n)=>{"use strict";n.d(t,{A:()=>s});var r=n(96540),o=n(17444),a=n(2445);function i({width:e,height:t,showLoadingForImport:n=!1,placeholderStyle:r}){return t&&(0,a.Y)("div",{style:{width:e,height:t,...r},children:n&&(0,a.Y)(o.A,{position:"floating"})},"async-asm-placeholder")||null}function s(e,t=i){let n,o;function s(){return n||(n=e instanceof Promise?e:e()),o||n.then((e=>{o=e.default||e})),n}const l=(0,r.forwardRef)((function(e,n){const[i,l]=(0,r.useState)(void 0!==o);(0,r.useEffect)((()=>{let e=!0;return i||s().then((()=>{e&&l(!0)})),()=>{e=!1}}));const d=o||t;return d?(0,a.Y)(d,{ref:d===o?n:null,...e}):null}));return l.preload=s,l}},61693:(e,t,n)=>{"use strict";n.d(t,{A:()=>i});var r=n(96453),o=n(38510),a=n(2445);const i=Object.assign((0,r.I4)((({light:e,bigger:t,bold:n,animateArrows:r,...i})=>(0,a.Y)(o.A,{...i})))`
    .ant-collapse-item {
      .ant-collapse-header {
        font-weight: ${({bold:e,theme:t})=>e?t.typography.weights.bold:t.typography.weights.normal};
        font-size: ${({bigger:e,theme:t})=>e?4*t.gridUnit+"px":"inherit"};

        .ant-collapse-arrow svg {
          transition: ${({animateArrows:e})=>e?"transform 0.24s":"none"};
        }

        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(90deg) !important;\n            }\n          "}

        ${({light:e,theme:t})=>e&&`\n            color: ${t.colors.grayscale.light4};\n            .ant-collapse-arrow svg {\n              color: ${t.colors.grayscale.light4};\n            }\n          `}

        ${({ghost:e,bordered:t,theme:n})=>e&&t&&`\n            border-bottom: 1px solid ${n.colors.grayscale.light3};\n          `}
      }
      .ant-collapse-content {
        .ant-collapse-content-box {
          .loading.inline {
            margin: ${({theme:e})=>12*e.gridUnit}px auto;
            display: block;
          }
        }
      }
    }
    .ant-collapse-item-active {
      .ant-collapse-header {
        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(-90deg) !important;\n            }\n          "}
      }
    }
  `,{Panel:o.A.Panel})},86523:(e,t,n)=>{"use strict";n.d(t,{A:()=>o});var r=n(77925);const o=(0,n(96453).I4)(r.A.Item)`
  ${({theme:e})=>`\n    .ant-form-item-label {\n      padding-bottom: ${e.gridUnit}px;\n      & > label {\n        font-size: ${e.typography.sizes.s}px;\n        color: ${e.colors.grayscale.base};\n\n        &.ant-form-item-required:not(.ant-form-item-required-mark-optional) {\n          &::before {\n            display: none;\n          }\n          &::after {\n            display: inline-block;\n            color: ${e.colors.error.base};\n            font-size: ${e.typography.sizes.s}px;\n            content: '*';\n          }\n        }\n      }\n    }\n  `}
`},40458:(e,t,n)=>{"use strict";n.d(t,{A:()=>s});var r=n(96453),o=n(2445);const a=r.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
`,i=r.I4.label`
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
`;function s({children:e,htmlFor:t,required:n=!1,className:r}){const s=n?i:a;return(0,o.Y)(s,{htmlFor:t,className:r,children:e})}},97987:(e,t,n)=>{"use strict";n.d(t,{A:()=>k});var r,o=n(36255),a=n(27236),i=n(96453),s=n(17437),l=n(95579),d=n(31641),c=n(12249),u=n(46920),p=n(96540);function h(){return h=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)({}).hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},h.apply(null,arguments)}const m=({title:e,titleId:t,...n},o)=>p.createElement("svg",h({xmlns:"http://www.w3.org/2000/svg",width:24,height:24,fill:"none",ref:o,"aria-labelledby":t},n),e?p.createElement("title",{id:t},e):null,r||(r=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M12 7a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V8a1 1 0 0 0-1-1m0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9.71-7.44-5.27-5.27a1.05 1.05 0 0 0-.71-.29H8.27a1.05 1.05 0 0 0-.71.29L2.29 7.56a1.05 1.05 0 0 0-.29.71v7.46c.004.265.107.518.29.71l5.27 5.27c.192.183.445.286.71.29h7.46a1.05 1.05 0 0 0 .71-.29l5.27-5.27a1.05 1.05 0 0 0 .29-.71V8.27a1.05 1.05 0 0 0-.29-.71M20 15.31 15.31 20H8.69L4 15.31V8.69L8.69 4h6.62L20 8.69z",clipRule:"evenodd"}))),g=(0,p.forwardRef)(m);var b=n(86523),f=n(40458),v=n(2445);const y=(0,i.I4)(o.A)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,$=(0,i.I4)(o.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,x=(0,i.I4)("div")`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`,w=i.I4.div`
  display: flex;
  align-items: center;
`,_=(0,i.I4)(f.A)`
  margin-bottom: 0;
`,A=s.AH`
  &.anticon > * {
    line-height: 0;
  }
`,k=({label:e,validationMethods:t,errorMessage:n,helpText:r,required:o=!1,hasTooltip:i=!1,tooltipText:p,id:h,className:m,visibilityToggle:f,get_url:k,description:S,...C})=>(0,v.FD)(x,{className:m,children:[(0,v.FD)(w,{children:[(0,v.Y)(_,{htmlFor:h,required:o,children:e}),i&&(0,v.Y)(d.A,{tooltip:`${p}`})]}),(0,v.FD)(b.A,{css:e=>((e,t)=>s.AH`
  .ant-form-item-children-icon {
    display: none;
  }
  ${t&&`.ant-form-item-control-input-content {\n      position: relative;\n      &:after {\n        content: ' ';\n        display: inline-block;\n        background: ${e.colors.error.base};\n        mask: url(${g});\n        mask-size: cover;\n        width: ${4*e.gridUnit}px;\n        height: ${4*e.gridUnit}px;\n        position: absolute;\n        right: ${1.25*e.gridUnit}px;\n        top: ${2.75*e.gridUnit}px;\n      }\n    }`}
`)(e,!!n),validateTrigger:Object.keys(t),validateStatus:n?"error":"success",help:n||r,hasFeedback:!!n,children:[f||"password"===C.name?(0,v.Y)($,{...C,...t,iconRender:e=>e?(0,v.Y)(a.A,{title:(0,l.t)("Hide password."),children:(0,v.Y)(c.A.EyeInvisibleOutlined,{iconSize:"m",css:A})}):(0,v.Y)(a.A,{title:(0,l.t)("Show password."),children:(0,v.Y)(c.A.EyeOutlined,{iconSize:"m",css:A})}),role:"textbox"}):(0,v.Y)(y,{...C,...t}),k&&S?(0,v.FD)(u.A,{type:"link",htmlType:"button",buttonStyle:"default",onClick:()=>(window.open(k),!0),children:["Get ",S]}):(0,v.Y)("br",{})]})]})},40563:(e,t,n)=>{"use strict";n.d(t,{lV:()=>s,eI:()=>l.A,lR:()=>d.A,MA:()=>c.A});var r=n(77925),o=n(96453),a=n(2445);const i=(0,o.I4)(r.A)`
  &.ant-form label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }
`;function s(e){return(0,a.Y)(i,{...e})}var l=n(86523),d=n(40458),c=n(97987)},78532:(e,t,n)=>{"use strict";n.d(t,{K:()=>i});var r=n(71519),o=n(32132),a=n(2445);const i=({to:e,component:t,replace:n,innerRef:i,children:s,...l})=>"string"==typeof e&&(0,o.JE)(e)?(0,a.Y)("a",{href:(0,o.Dl)(e),...l,children:s}):(0,a.Y)(r.N_,{to:e,component:t,replace:n,innerRef:i,...l,children:s})},31641:(e,t,n)=>{"use strict";n.d(t,{A:()=>u});var r=n(96453),o=n(19129),a=n(12249),i=n(2445);const s=(0,r.I4)(o.m)`
  cursor: pointer;
`,l=r.I4.span`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,d={fontSize:"12px",lineHeight:"16px"},c="rgba(0,0,0,0.9)";function u({tooltip:e,iconStyle:t={},placement:n="right",trigger:o="hover",overlayStyle:u=d,bgColor:p=c,viewBox:h="0 -1 24 24"}){const m=(0,r.DP)(),g={...t,color:t.color||m.colors.grayscale.base};return(0,i.Y)(s,{title:(0,i.Y)(l,{children:e}),placement:n,trigger:o,overlayStyle:u,color:p,children:(0,i.Y)(a.A.InfoSolidSmall,{style:g,viewBox:h})})}},90868:(e,t,n)=>{"use strict";n.d(t,{YI:()=>s,fs:()=>l,pd:()=>i});var r=n(96453),o=n(36255),a=n(89542);const i=(0,r.I4)(o.A)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,s=(0,r.I4)(a.A)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`,l=(0,r.I4)(o.A.TextArea)`
  border: 1px solid ${({theme:e})=>e.colors.secondary.light3};
  border-radius: ${({theme:e})=>e.borderRadius}px;
`},2738:(e,t,n)=>{"use strict";n.d(t,{A:()=>s});var r=n(17437),o=n(15595),a=n(96453),i=n(2445);function s(e){const t=(0,a.DP)(),{colors:n,transitionTiming:s}=t,{type:l="default",onClick:d,children:c,...u}=e,{alert:p,primary:h,secondary:m,grayscale:g,success:b,warning:f,error:v,info:y}=n;let $=g.light3,x=d?h.light2:g.light3,w=d?g.light2:"transparent",_=d?h.light1:"transparent",A=g.dark1;if("default"!==l){let e;A=g.light4,"alert"===l?(A=g.dark1,e=p):e="success"===l?b:"warning"===l?f:"danger"===l?v:"info"===l?y:"secondary"===l?m:h,$=e.base,x=d?e.dark1:e.base,w=d?e.dark1:"transparent",_=d?e.dark2:"transparent"}return(0,i.Y)(o.vw,{onClick:d,role:d?"button":void 0,...u,css:(0,r.AH)({transition:`background-color ${s}s`,whiteSpace:"nowrap",cursor:d?"pointer":"default",overflow:"hidden",textOverflow:"ellipsis",backgroundColor:$,borderColor:w,borderRadius:21,padding:"0.35em 0.8em",lineHeight:1,color:A,maxWidth:"100%","&:hover":{backgroundColor:x,borderColor:_,opacity:1}},"",""),children:c})}},6749:(e,t,n)=>{"use strict";n.d(t,{DJ:()=>r,NG:()=>m,Np:()=>i,W1:()=>h,YX:()=>d,eJ:()=>s,ez:()=>l});var r,o=n(96453),a=n(6570);!function(e){e.MenuItem="menu-item",e.SubMenu="submenu",e.SubMenuItem="submenu-item"}(r||(r={}));const i=e=>{var t,n;return void 0!==(null==e||null==(t=e.current)||null==(n=t.props)?void 0:n.parentMenu)},s=e=>{var t;return"Styled(MenuItem)"===(null==e||null==(t=e.type)?void 0:t.displayName)},l=e=>{var t;return 1===(null==e||null==(t=e.type)?void 0:t.isSubMenu)},d=e=>e===r.SubMenu||e===r.SubMenuItem,c=(0,o.I4)(a.A.Item)`
  > a {
    text-decoration: none;
  }

  &.ant-menu-item {
    height: ${({theme:e})=>8*e.gridUnit}px;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
    a {
      border-bottom: none;
      transition: background-color ${({theme:e})=>e.transitionTiming}s;
      &:after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 50%;
        width: 0;
        height: 3px;
        opacity: 0;
        transform: translateX(-50%);
        transition: all ${({theme:e})=>e.transitionTiming}s;
        background-color: ${({theme:e})=>e.colors.primary.base};
      }
      &:focus {
        border-bottom: none;
        background-color: transparent;
        @media (max-width: 767px) {
          background-color: ${({theme:e})=>e.colors.primary.light5};
        }
      }
    }
  }

  &.ant-menu-item,
  &.ant-dropdown-menu-item {
    span[role='button'] {
      display: inline-block;
      width: 100%;
    }
    transition-duration: 0s;
  }
`,u=(0,o.I4)(a.A)`
  line-height: 51px;
  border: none;

  & > .ant-menu-item,
  & > .ant-menu-submenu {
    vertical-align: inherit;
    &:hover {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    &:hover {
      border-bottom: none;
    }
  }

  &:not(.ant-menu-dark) > .ant-menu-submenu,
  &:not(.ant-menu-dark) > .ant-menu-item {
    margin: 0px;
  }

  & > .ant-menu-item > a {
    padding: ${({theme:e})=>4*e.gridUnit}px;
  }
`,p=(0,o.I4)(a.A.SubMenu)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  border-bottom: none;
  .ant-menu-submenu-open,
  .ant-menu-submenu-active {
    background-color: ${({theme:e})=>e.colors.primary.light5};
    .ant-menu-submenu-title {
      color: ${({theme:e})=>e.colors.grayscale.dark1};
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: none;
      margin: 0;
      &:after {
        opacity: 1;
        width: calc(100% - 1);
      }
    }
  }
  .ant-menu-submenu-title {
    position: relative;
    top: ${({theme:e})=>-e.gridUnit-3}px;
    &:after {
      content: '';
      position: absolute;
      bottom: -3px;
      left: 50%;
      width: 0;
      height: 3px;
      opacity: 0;
      transform: translateX(-50%);
      transition: all ${({theme:e})=>e.transitionTiming}s;
      background-color: ${({theme:e})=>e.colors.primary.base};
    }
  }
  .ant-menu-submenu-arrow {
    top: 67%;
  }
  & > .ant-menu-submenu-title {
    padding: 0 ${({theme:e})=>6*e.gridUnit}px 0
      ${({theme:e})=>3*e.gridUnit}px !important;
    span[role='img'] {
      position: absolute;
      right: ${({theme:e})=>-e.gridUnit-2}px;
      top: ${({theme:e})=>5.25*e.gridUnit}px;
      svg {
        font-size: ${({theme:e})=>6*e.gridUnit}px;
        color: ${({theme:e})=>e.colors.grayscale.base};
      }
    }
    & > span {
      position: relative;
      top: 7px;
    }
    &:hover {
      color: ${({theme:e})=>e.colors.primary.base};
    }
  }
`,h=Object.assign(a.A,{Item:c}),m=Object.assign(u,{Item:c,SubMenu:p,Divider:a.A.Divider,ItemGroup:a.A.ItemGroup})},78697:(e,t,n)=>{"use strict";n.d(t,{s:()=>s});var r=n(96453),o=n(1612);const a=(0,r.I4)(o.Ay)`
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
`,i=(0,r.I4)(o.Ay.Group)`
  font-size: inherit;
`,s=Object.assign(a,{Group:i,Button:o.Ay.Button})},53107:(e,t,n)=>{"use strict";n.d(t,{d:()=>s});var r=n(96453),o=n(1035),a=n(2445);const i=(0,r.I4)(o.A)`
  .ant-switch-checked {
    background-color: ${({theme:e})=>e.colors.primary.base};
  }
`,s=e=>(0,a.Y)(i,{...e})},48327:(e,t,n)=>{"use strict";n.d(t,{fn:()=>h,pX:()=>g,Ay:()=>b});var r=n(17437),o=n(96453),a=n(80899),i=n(12249),s=n(2445);const l=({animated:e=!1,fullWidth:t=!0,allowOverflow:n=!0,...o})=>(0,s.Y)(a.A,{animated:e,...o,css:e=>r.AH`
      overflow: ${n?"visible":"hidden"};

      .ant-tabs-content-holder {
        overflow: ${n?"visible":"auto"};
      }
      .ant-tabs-tab {
        flex: 1 1 auto;
        &.ant-tabs-tab-active .ant-tabs-tab-btn {
          color: inherit;
        }
        &:hover {
          .anchor-link-container {
            cursor: pointer;
            .fa.fa-link {
              visibility: visible;
            }
          }
        }
        .short-link-trigger.btn {
          padding: 0 ${e.gridUnit}px;
          & > .fa.fa-link {
            top: 0;
          }
        }
      }
      ${t&&r.AH`
        .ant-tabs-nav-list {
          width: 100%;
        }
      `};

      .ant-tabs-tab-btn {
        display: flex;
        flex: 1 1 auto;
        align-items: center;
        justify-content: center;
        font-size: ${e.typography.sizes.s}px;
        text-align: center;
        user-select: none;
        .required {
          margin-left: ${e.gridUnit/2}px;
          color: ${e.colors.error.base};
        }
      }
      .ant-tabs-ink-bar {
        background: ${e.colors.secondary.base};
      }
    `}),d=(0,o.I4)(a.A.TabPane)``,c=Object.assign(l,{TabPane:d}),u=(0,o.I4)(l)`
  ${({theme:e,fullWidth:t})=>`\n    .ant-tabs-content-holder {\n      background: ${e.colors.grayscale.light5};\n    }\n\n    & > .ant-tabs-nav {\n      margin-bottom: 0;\n    }\n\n    .ant-tabs-tab-remove {\n      padding-top: 0;\n      padding-bottom: 0;\n      height: ${6*e.gridUnit}px;\n    }\n\n    ${t?r.AH`
            .ant-tabs-nav-list {
              width: 100%;
            }
          `:""}\n  `}
`,p=(0,o.I4)(i.A.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,h=Object.assign(u,{TabPane:d});h.defaultProps={type:"editable-card",fullWidth:!1,animated:{inkBar:!0,tabPane:!1}},h.TabPane.defaultProps={closeIcon:(0,s.Y)(p,{role:"button",tabIndex:0})};const m=(0,o.I4)(h)`
  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-tab {
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;
    padding: ${({theme:e})=>`${3*e.gridUnit}px ${e.gridUnit}px`};
    background: transparent;
    border: none;
  }

  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-ink-bar {
    visibility: visible;
  }

  .ant-tabs-tab-btn {
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
  }

  .ant-tabs-tab-remove {
    margin-left: 0;
    padding-right: 0;
  }

  .ant-tabs-nav-add {
    min-width: unset !important;
    background: transparent !important;
    border: none !important;
  }
`,g=Object.assign(m,{TabPane:d}),b=c},28292:(e,t,n)=>{"use strict";n.d(t,{B:()=>o});var r=n(61225);function o(){return(0,r.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.conf}))}},3139:(e,t,n)=>{"use strict";var r,o;n.d(t,{$:()=>o,N:()=>r}),function(e){e.Charts="CHARTS",e.Dashboards="DASHBOARDS",e.Recents="RECENTS",e.SavedQueries="SAVED_QUERIES"}(r||(r={})),function(e){e.GoogleSheets="gsheets",e.DbConnection="dbconnection",e.DatasetCreation="datasetCreation",e.CSVUpload="csvUpload",e.ExcelUpload="excelUpload",e.ColumnarUpload="columnarUpload"}(o||(o={}))},27588:(e,t,n)=>{"use strict";n.d(t,{A:()=>r});const r=(()=>{try{return n(19593)||{}}catch(e){return{}}})()},50500:(e,t,n)=>{"use strict";n.d(t,{Fp:()=>w,RU:()=>m,Y8:()=>C,bN:()=>b,bR:()=>y,d5:()=>k,fn:()=>g,g9:()=>x,oG:()=>v,oi:()=>I,q4:()=>$,xK:()=>_,ym:()=>A});var r=n(58561),o=n.n(r),a=n(96540),i=n(35742),s=n(95579),l=n(51436),d=n(93505),c=n(30703),u=n(73135),p=n(27588);const h=e=>"string"==typeof e?e:Object.entries(e).map((([e,t])=>Array.isArray(t)?`(${e}) ${t.join(", ")}`:`(${e}) ${t}`)).join("\n");function m(e,t,n,r=!0,l=[],d,u=!0,p){const[h,m]=(0,a.useState)({count:0,collection:l,loading:u,lastFetchDataConfig:null,permissions:[],bulkSelectEnabled:!1});function g(e){m((t=>({...t,...e})))}(0,a.useEffect)((()=>{r&&i.A.get({endpoint:`/api/v1/${e}/_info?q=${o().encode({keys:["permissions"]})}`}).then((({json:e={}})=>{g({permissions:e.permissions})}),(0,c.JF)((e=>n((0,s.t)("An error occurred while fetching %s info: %s",t,e)))))}),[]);const b=(0,a.useCallback)((({pageIndex:r,pageSize:a,sortBy:l,filters:u})=>{g({lastFetchDataConfig:{filters:u,pageIndex:r,pageSize:a,sortBy:l},loading:!0});const h=(d||[]).concat(u).map((({id:e,operator:t,value:n})=>({col:e,opr:t,value:n&&"object"==typeof n&&"value"in n?n.value:n}))),m=o().encode_uri({order_column:l[0].id,order_direction:l[0].desc?"desc":"asc",page:r,page_size:a,...h.length?{filters:h}:{},...null!=p&&p.length?{select_columns:p}:{}});return i.A.get({endpoint:`/api/v1/${e}/?q=${m}`}).then((({json:e={}})=>{g({collection:e.result,count:e.count,lastFetched:(new Date).toISOString()})}),(0,c.JF)((e=>n((0,s.t)("An error occurred while fetching %ss: %s",t,e))))).finally((()=>{g({loading:!1})}))}),[d]);return{state:{loading:h.loading,resourceCount:h.count,resourceCollection:h.collection,bulkSelectEnabled:h.bulkSelectEnabled,lastFetched:h.lastFetched},setResourceCollection:e=>g({collection:e}),hasPerm:function(e){return!!h.permissions.length&&Boolean(h.permissions.find((t=>t===e)))},fetchData:b,toggleBulkSelect:function(){g({bulkSelectEnabled:!h.bulkSelectEnabled})},refreshData:e=>h.lastFetchDataConfig?b(h.lastFetchDataConfig):e?b(e):null}}function g(e,t,n,r=""){const[o,l]=(0,a.useState)({loading:!1,resource:null,error:null});function d(e){l((t=>({...t,...e})))}return{state:o,setResource:e=>d({resource:e}),fetchResource:(0,a.useCallback)((o=>{d({loading:!0});const a=`/api/v1/${e}/${o}`,l=""!==r?`${a}/${r}`:a;return i.A.get({endpoint:l}).then((({json:e={}})=>(d({resource:e.result,error:null}),e.result)),(0,c.JF)((e=>{n((0,s.t)("An error occurred while fetching %ss: %s",t,h(e))),d({error:e})}))).finally((()=>{d({loading:!1})}))}),[n,e,t]),createResource:(0,a.useCallback)(((r,o=!1)=>(d({loading:!0}),i.A.post({endpoint:`/api/v1/${e}/`,body:JSON.stringify(r),headers:{"Content-Type":"application/json"}}).then((({json:e={}})=>(d({resource:{id:e.id,...e.result},error:null}),e.id)),(0,c.JF)((e=>{o||n((0,s.t)("An error occurred while creating %ss: %s",t,h(e))),d({error:e})}))).finally((()=>{d({loading:!1})})))),[n,e,t]),updateResource:(0,a.useCallback)(((r,o,a=!1,l=!0)=>(l&&d({loading:!0}),i.A.put({endpoint:`/api/v1/${e}/${r}`,body:JSON.stringify(o),headers:{"Content-Type":"application/json"}}).then((({json:e={}})=>(d({resource:{...e.result,id:e.id},error:null}),e.result)),(0,c.JF)((e=>(a||n((0,s.t)("An error occurred while fetching %ss: %s",t,JSON.stringify(e))),d({error:e}),e)))).finally((()=>{l&&d({loading:!1})})))),[n,e,t]),clearError:()=>d({error:null})}}function b(e,t,n){const[r,o]=(0,a.useState)({loading:!1,passwordsNeeded:[],alreadyExists:[],sshPasswordNeeded:[],sshPrivateKeyNeeded:[],sshPrivateKeyPasswordNeeded:[],failed:!1});function d(e){o((t=>({...t,...e})))}return{state:r,importResource:(0,a.useCallback)(((r,o={},a={},u={},p={},h=!1)=>{d({loading:!0,failed:!1});const m=new FormData;m.append("formData",r);const g=(0,s.t)("Please re-export your file and try importing again");return o&&m.append("passwords",JSON.stringify(o)),h&&m.append("overwrite","true"),a&&m.append("ssh_tunnel_passwords",JSON.stringify(a)),u&&m.append("ssh_tunnel_private_keys",JSON.stringify(u)),p&&m.append("ssh_tunnel_private_key_passwords",JSON.stringify(p)),i.A.post({endpoint:`/api/v1/${e}/import/`,body:m,headers:{Accept:"application/json"}}).then((()=>(d({passwordsNeeded:[],alreadyExists:[],sshPasswordNeeded:[],sshPrivateKeyNeeded:[],sshPrivateKeyPasswordNeeded:[],failed:!1}),!0))).catch((e=>(0,l.h4)(e).then((e=>(d({failed:!0}),e.errors?((0,c.ec)(e.errors)?n((0,s.t)("An error occurred while importing %s: %s",t,[...e.errors.map((e=>e.message)),g].join(".\n"))):d({passwordsNeeded:(0,c.uN)(e.errors),sshPasswordNeeded:(0,c.Um)(e.errors),sshPrivateKeyNeeded:(0,c.dl)(e.errors),sshPrivateKeyPasswordNeeded:(0,c.I7)(e.errors),alreadyExists:(0,c.Xh)(e.errors)}),!1):(n((0,s.t)("An error occurred while importing %s: %s",t,e.message||e.error)),!1)))))).finally((()=>{d({loading:!1})}))}),[])}}const f={chart:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/chart/favorite_status/"}),dashboard:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/dashboard/favorite_status/"}),tag:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/tag/favorite_status/"})};function v(e,t,n){const[r,o]=(0,a.useState)({}),l=e=>o((t=>({...t,...e})));return(0,a.useEffect)((()=>{t.length&&f[e](t).then((({result:e})=>{const t=e.reduce(((e,t)=>(e[t.id]=t.value,e)),{});l(t)}),(0,c.JF)((e=>n((0,s.t)("There was an error fetching the favorite status: %s",e)))))}),[t,e,n]),[(0,a.useCallback)(((t,r)=>{const o=`/api/v1/${e}/${t}/favorites/`;(r?i.A.delete({endpoint:o}):i.A.post({endpoint:o})).then((()=>{l({[t]:!r})}),(0,c.JF)((e=>n((0,s.t)("There was an error saving the favorite status: %s",e)))))}),[e]),r]}const y=(e,t)=>{const[n,r]=(0,a.useState)(null);return{sliceCurrentlyEditing:n,handleChartUpdated:function(n){const r=t.map((e=>e.id===n.id?{...e,...n}:e));e(r)},openChartEditModal:function(e){r({slice_id:e.id,slice_name:e.slice_name,description:e.description,cache_timeout:e.cache_timeout,certified_by:e.certified_by,certification_details:e.certification_details,is_managed_externally:e.is_managed_externally})},closeChartEditModal:function(){r(null)}}},$=(e,t,n)=>{(0,u.A)((()=>Promise.resolve(`${window.location.origin}/sqllab?savedQueryId=${e}`))).then((()=>{n((0,s.t)("Link Copied!"))})).catch((()=>{t((0,s.t)("Sorry, your browser does not support copying."))}))},x=()=>p.A.DB_IMAGES,w=()=>p.A.DB_CONNECTION_ALERTS,_=()=>p.A.DB_CONNECTION_DOC_LINKS,A=(e,t,n)=>{i.A.post({endpoint:"api/v1/database/test_connection/",body:JSON.stringify(e),headers:{"Content-Type":"application/json"}}).then((()=>{n((0,s.t)("Connection looks good!"))}),(0,c.JF)((e=>{t((0,s.t)("ERROR: %s",h(e)))})))};function k(){const[e,t]=(0,a.useState)(null);return[e,(0,a.useCallback)((()=>{i.A.get({endpoint:"/api/v1/database/available/"}).then((({json:e})=>{t(e)}))}),[t])]}const S=e=>e&&Array.isArray(null==e?void 0:e.catalog)?{...e,catalog:Object.assign({},...e.catalog.map((e=>({[e.name]:e.value}))))}:e;function C(){const[e,t]=(0,a.useState)(null);return[e,(0,a.useCallback)(((e,n=!1)=>{var r;return null!=e&&null!=(r=e.parameters)&&r.ssh?(t(null),[]):i.A.post({endpoint:"/api/v1/database/validate_parameters/",body:JSON.stringify(S(e)),headers:{"Content-Type":"application/json"}}).then((()=>{t(null)})).catch((e=>{if("function"==typeof e.json)return e.json().then((({errors:e=[]})=>{const r=e.filter((e=>!["CONNECTION_MISSING_PARAMETERS_ERROR","CONNECTION_ACCESS_DENIED_ERROR"].includes(e.error_type)||n)).reduce(((e,{error_type:t,extra:n,message:r})=>{var o,a;return n.catalog?n.catalog.name?{...e,error_type:t,[n.catalog.idx]:{name:r}}:n.catalog.url?{...e,error_type:t,[n.catalog.idx]:{url:r}}:{...e,error_type:t,[n.catalog.idx]:{name:r,url:r}}:n.invalid?{...e,[n.invalid[0]]:r,error_type:t}:n.missing?{...e,error_type:t,...Object.assign({},...n.missing.map((e=>({[e]:"This is a required field"}))))}:null!=(o=n.issue_codes)&&o.length?{...e,error_type:t,description:r||(null==(a=n.issue_codes[0])?void 0:a.message)}:e}),{});return t(r),r}));console.error(e)}))}),[t]),t]}const I=(e,t,n)=>{var r;return n?null==(r=e.reports[t])?void 0:r[n]:null}},23193:(e,t,n)=>{"use strict";var r,o;n.d(t,{G:()=>r,H:()=>o}),function(e){e.Favorite="Favorite",e.Mine="Mine",e.Other="Other",e.Viewed="Viewed",e.Created="Created",e.Edited="Edited"}(r||(r={})),function(e){e.Id="id",e.ChangedOn="changed_on",e.ChangedBy="changed_by",e.Database="database",e.DatabaseName="database.database_name",e.Schema="schema",e.Sql="sql",e.ExecutedSql="executed_sql",e.SqlTables="sql_tables",e.Status="status",e.TabName="tab_name",e.User="user",e.UserFirstName="user.first_name",e.StartTime="start_time",e.EndTime="end_time",e.Rows="rows",e.TmpTableName="tmp_table_name",e.TrackingUrl="tracking_url"}(o||(o={}))},30703:(e,t,n)=>{"use strict";n.d(t,{$C:()=>k,Af:()=>U,En:()=>f,GP:()=>C,I7:()=>J,J7:()=>_,JF:()=>S,ND:()=>V,Q_:()=>j,Um:()=>M,VY:()=>O,Xh:()=>G,c8:()=>L,dl:()=>q,ec:()=>B,lH:()=>w,md:()=>y,mq:()=>E,oE:()=>x,s4:()=>N,u1:()=>A,uN:()=>F,vE:()=>T,yT:()=>I});var r=n(5287),o=n.n(r),a=n(96453),i=n(35742),s=n(95579),l=n(51436),d=n(5362),c=n(17437),u=n(58561),p=n.n(u),h=n(27588),m=n(84666),g=n(3139),b=n(23193);(()=>{const e=p(),t=[];for(let e=0;e<16;e+=1)for(let n=0;n<16;n+=1){if(e+n===0)continue;const r=String.fromCharCode(16*e+n);/\w|[-_./~]/.test(r)||t.push(`\\u00${e.toString(16)}${n.toString(16)}`)}e.not_idchar=t.join(""),e.not_idstart="-0123456789";const n=`[^${e.not_idstart}${e.not_idchar}][^${e.not_idchar}]*`;e.id_ok=new RegExp(`^${n}$`),e.next_id=new RegExp(n,"g")})();const f=a.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,v=e=>(t,n,r,o)=>async(r="",a,s)=>{var l;const d=`/api/v1/${t}/${e}/${n}`,c=p().encode_uri({filter:r,page:a,page_size:s}),{json:u={}}=await i.A.get({endpoint:`${d}?q=${c}`});let h=!1;const m=o?{label:`${o.firstName} ${o.lastName}`,value:o.userId}:void 0,g=[];return null==u||null==(l=u.result)||l.filter((({text:e})=>e.trim().length>0)).forEach((({text:e,value:t})=>{m&&t===m.value&&e===m.label?h=!0:g.push({label:e,value:t})})),!m||r&&!h||g.unshift(m),{data:g,totalCount:null==u?void 0:u.count}},y=5,$=(e,t)=>{const n={order_column:"changed_on_delta_humanized",order_direction:"desc",page:0,page_size:y,filters:e,select_columns:t};return e||delete n.filters,t||delete n.select_columns,p().encode(n)},x=e=>{const t={edited:[{col:"changed_by",opr:"rel_o_m",value:`${e}`}]},n=[i.A.get({endpoint:`/api/v1/dashboard/?q=${$(t.edited)}`}),i.A.get({endpoint:`/api/v1/chart/?q=${$(t.edited)}`})];return Promise.all(n).then((([e,t])=>{var n,r;return{editedDash:null==(n=t.json)?void 0:n.result.slice(0,3),editedChart:null==(r=e.json)?void 0:r.result.slice(0,3)}})).catch((e=>e))},w=(e,t,n=[{col:"owners",opr:"rel_m_m",value:`${e}`}],r)=>i.A.get({endpoint:`/api/v1/${t}/?q=${$(n,r)}`}).then((e=>{var t;return null==(t=e.json)?void 0:t.result})),_=(e,t,n,r)=>i.A.get({endpoint:t}).then((e=>{const t={};return((e,t,n,r)=>{const o=[i.A.get({endpoint:`/api/v1/chart/?q=${$(t,void 0)}`}),i.A.get({endpoint:`/api/v1/dashboard/?q=${$(t,void 0)}`})];return Promise.all(o).then((([e,t])=>({other:[...e.json.result,...t.json.result]}))).catch((t=>(e((0,s.t)("There was an error fetching the filtered charts and dashboards:"),t),{other:[]})))})(n,r).then((({other:n})=>(t.other=n,t.viewed=e.json.result,t)))})),A=v("related"),k=v("distinct");function S(e){return async t=>{const n=await(0,l.h4)(t),r=null==n?void 0:n.errors,o=await h.A;null!=r&&r.length&&null!=o&&o.ERRORS&&r[0].error_type in o.ERRORS&&(n.message=o.ERRORS[r[0].error_type]),d.A.error(t),e(n.message||n.error)}}function C({id:e,slice_name:t},n,r,o,a,l){const d={pageIndex:0,pageSize:y,sortBy:[{id:"changed_on_delta_humanized",desc:!0}],filters:[{id:"created_by",operator:"rel_o_m",value:`${l}`}]};i.A.delete({endpoint:`/api/v1/chart/${e}`}).then((()=>{"Mine"===a?o(d):o(),n((0,s.t)("Deleted: %s",t))}),(()=>{r((0,s.t)("There was an issue deleting: %s",t))}))}function I({id:e,dashboard_title:t},n,r,o,a,l){return i.A.delete({endpoint:`/api/v1/dashboard/${e}`}).then((()=>{"Mine"===a?n({pageIndex:0,pageSize:y,sortBy:[{id:"changed_on_delta_humanized",desc:!0}],filters:[{id:"owners",operator:"rel_m_m",value:`${l}`}]}):n(),r((0,s.t)("Deleted: %s",t))}),S((e=>o((0,s.t)("There was an issue deleting %s: %s",t,e)))))}function N(e,t){let n=e.split("\n");return n.length>=t&&(n=n.slice(0,t),n.push("...")),n.join("\n")}const U=5,E=[576,768,992,1200].map((e=>`@media (max-width: ${e}px)`)),j=a.I4.div`
  ${({showThumbnails:e,theme:t})=>`\n    overflow: hidden;\n    display: grid;\n    grid-gap: ${12*t.gridUnit}px ${4*t.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    max-height: ${e?"314":"148"}px;\n    margin-top: ${-6*t.gridUnit}px;\n    padding: ${e?`${8*t.gridUnit+3}px ${9*t.gridUnit}px`:`${8*t.gridUnit+1}px ${9*t.gridUnit}px`};\n  `}
`,O=a.I4.div`
  cursor: pointer;
  a {
    text-decoration: none;
  }
  .ant-card-cover > div {
    /* Height is calculated based on 300px width, to keep the same aspect ratio as the 800*450 thumbnails */
    height: 168px;
  }
`,T=e=>c.AH`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,R=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a password for the database"===e)))},D=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a password for the ssh tunnel"===e)))},P=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a private key for the ssh tunnel"===e)))},z=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a private key password for the ssh tunnel"===e)))},Y=e=>"string"==typeof e&&e.includes("already exists and `overwrite=true` was not passed"),F=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>R(e))).map((([e])=>e)))).flat(),M=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>D(e))).map((([e])=>e)))).flat(),q=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>P(e))).map((([e])=>e)))).flat(),J=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>z(e))).map((([e])=>e)))).flat(),G=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>Y(e))).map((([e])=>e)))).flat(),B=e=>e.some((e=>{const t=Object.entries(e.extra).filter((([e])=>"issue_codes"!==e));return 0===t.length||!t.every((([,e])=>R(e)||Y(e)||D(e)||P(e)||z(e)))})),H=(e,t)=>void 0!==e&&o()(e,t).length>0,L=(e,t,n,r,o)=>{const a=(0,m.L)("can_csv_upload","Database",e)&&H(t,o),i=H(n,o)&&(0,m.L)("can_columnar_upload","Database",e),s=H(r,o)&&(0,m.L)("can_excel_upload","Database",e);return{canUploadCSV:a,canUploadColumnar:i,canUploadExcel:s,canUploadData:a||i||s}};function V(e,t,n,r){return e===b.G.Created||t===g.N.SavedQueries&&e===b.G.Mine?[{id:"created_by",operator:"rel_o_m",value:`${null==n?void 0:n.userId}`}]:t===g.N.SavedQueries&&e===b.G.Favorite?[{id:"id",operator:"saved_query_is_fav",value:!0}]:e===b.G.Mine&&n?[{id:"owners",operator:"rel_m_m",value:`${n.userId}`}]:e===b.G.Favorite&&[g.N.Dashboards,g.N.Charts].includes(t)?[{id:"id",operator:t===g.N.Dashboards?"dashboard_is_favorite":"chart_is_favorite",value:!0}]:e===b.G.Other?(r||[]).map((e=>({id:e.col,operator:e.opr,value:e.value}))):[]}}}]);
//# sourceMappingURL=1939.889e1ec3e31a48f890de.entry.js.map