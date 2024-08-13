"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2741],{31383:(e,a,t)=>{t.d(a,{A:()=>c});var n=t(95579),l=t(50500),i=t(25946),r=t(17437),o=t(2445);const s=(0,l.xK)(),d=s?s.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c=({errorMessage:e,showDbInstallInstructions:a})=>(0,o.Y)(i.A,{closable:!1,css:e=>(e=>r.AH`
  border: 1px solid ${e.colors.warning.light1};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;
  color: ${e.colors.warning.dark2};

  .ant-alert-message {
    margin: 0;
  }

  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),type:"error",showIcon:!0,message:e,description:a?(0,o.FD)(o.FK,{children:[(0,o.Y)("br",{}),(0,n.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: "),(0,o.Y)("a",{href:d,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,n.t)("here")}),"."]}):""})},85994:(e,a,t)=>{t.d(a,{A:()=>u});var n=t(96540),l=t(96453),i=t(12249),r=t(2445);const o=l.I4.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,l.I4)(i.A.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,l.I4)(i.A.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,l.I4)(i.A.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,h=l.I4.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,p=l.I4.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,u=(0,n.forwardRef)((({indeterminate:e,id:a,checked:t,onChange:l,title:i="",labelText:u=""},m)=>{const g=(0,n.useRef)(),b=m||g;return(0,n.useEffect)((()=>{b.current.indeterminate=e}),[b,e]),(0,r.FD)(r.FK,{children:[(0,r.FD)(p,{children:[e&&(0,r.Y)(s,{}),!e&&t&&(0,r.Y)(c,{}),!e&&!t&&(0,r.Y)(d,{}),(0,r.Y)(h,{name:a,id:a,type:"checkbox",ref:b,checked:t,onChange:l})]}),(0,r.Y)(o,{title:i,htmlFor:a,children:u})]})}))},46740:(e,a,t)=>{t.d(a,{A:()=>s});var n=t(96540),l=t(96453),i=t(16707),r=t(2445);const o=l.I4.div`
  max-width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
`,s=({tags:e,editable:a=!1,onDelete:t,maxTags:l})=>{const[s,d]=(0,n.useState)(l),c=e=>{null==t||t(e)},h=(0,n.useMemo)((()=>s?e.length>s:null),[e.length,s]),p=(0,n.useMemo)((()=>"number"==typeof s?e.length-s+1:null),[h,e.length,s]);return(0,r.Y)(o,{className:"tag-list",children:h&&"number"==typeof s?(0,r.FD)(r.FK,{children:[e.slice(0,s-1).map(((e,t)=>(0,r.Y)(i.A,{id:e.id,name:e.name,index:t,onDelete:c,editable:a},e.id))),e.length>s?(0,r.Y)(i.A,{name:`+${p}...`,onClick:()=>d(void 0),toolTipTitle:e.map((e=>e.name)).join(", ")}):null]}):(0,r.FD)(r.FK,{children:[e.map(((e,t)=>(0,r.Y)(i.A,{id:e.id,name:e.name,index:t,onDelete:c,editable:a},e.id))),l&&e.length>l?(0,r.Y)(i.A,{name:"...",onClick:()=>d(l)}):null]})})}},16817:(e,a,t)=>{t.d(a,{hT:()=>sa,Ay:()=>ha});var n=t(44383),l=t.n(n),i=t(62193),r=t.n(i),o=t(72391),s=t(96453),d=t(95579),c=t(96540),h=t(61574),p=t(62221),u=t(48327),m=t(15595),g=t(25946),b=t(85861),v=t(46920),f=t(12249);function y(){return y=Object.assign?Object.assign.bind():function(e){for(var a=1;a<arguments.length;a++){var t=arguments[a];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},y.apply(this,arguments)}const _={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},x=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"],Y=["component","ellipsis","trimRight","className"];function w(e,a){for(;e&&a--;)e=e.previousElementSibling;return e}const C={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},S=Object.keys(C);class A extends c.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas&&(this.canvas.parentNode.removeChild(this.canvas),this.canvas=null)}setState(e,a){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,a)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(_).forEach((a=>{e.style[a]=_[a]})),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);x.forEach((a=>{this.canvas.style[a]=e[a]}))}reflow(e){const a=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(a){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${a}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map((e=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("");const t=this.putEllipsis(this.calcIndexes()),n=t>-1,l={clamped:n,text:n?this.units.slice(0,t).join(""):e.text};this.setState(l,e.onReflow.bind(this,l))}calcIndexes(){const e=[0];let a=this.canvas.firstElementChild;if(!a)return e;let t=0,n=1,l=a.offsetTop;for(;(a=a.nextElementSibling)&&(a.offsetTop>l&&(n++,e.push(t),l=a.offsetTop),t++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const a=e[this.maxLine],t=this.units.slice(0,a),n=this.canvas.children[a].offsetTop;this.canvas.innerHTML=t.map(((e,a)=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const l=this.canvas.lastElementChild;let i=w(l,2);for(;i&&(l.offsetTop>n||l.offsetHeight>i.offsetHeight||l.offsetTop>i.offsetTop);)this.canvas.removeChild(i),i=w(l,2),t.pop();return t.length}isClamped(){return this.clamped}render(){const{text:e,clamped:a}=this.state,t=this.props,{component:n,ellipsis:l,trimRight:i,className:r}=t,o=function(e,a){if(null==e)return{};var t,n,l={},i=Object.keys(e);for(n=0;n<i.length;n++)t=i[n],a.indexOf(t)>=0||(l[t]=e[t]);return l}(t,Y);return c.createElement(n,y({className:`LinesEllipsis ${a?"LinesEllipsis--clamped":""} ${r}`,ref:e=>this.target=e},function(e,a){if(!e||"object"!=typeof e)return e;const t={};return Object.keys(e).forEach((n=>{a.indexOf(n)>-1||(t[n]=e[n])})),t}(o,S)),a&&i?e.replace(/[\s\uFEFF\xA0]+$/,""):e,c.createElement("wbr",null),a&&c.createElement("span",{className:"LinesEllipsis-ellipsis"},l))}}A.defaultProps=C;var $=t(2445);const D=(0,s.I4)(v.A)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,N=s.I4.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,F=s.I4.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,k=s.I4.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`,E=(0,s.I4)((({icon:e,altText:a,buttonText:t,...n})=>(0,$.FD)(D,{...n,children:[(0,$.FD)(N,{children:[e&&(0,$.Y)("img",{src:e,alt:a}),!e&&(0,$.Y)(f.A.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})]}),(0,$.Y)(k,{children:(0,$.Y)(F,{children:(0,$.Y)(A,{text:t,maxLine:"2",basedOn:"words",trimRight:!0})})})]})))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`;var T,U,I=t(31641),P=t(5261),q=t(97987),L=t(79427),M=t(31383),O=t(50500),H=t(28292),R=t(17444);!function(e){e.SqlalchemyUri="sqlalchemy_form",e.DynamicForm="dynamic_form"}(T||(T={})),function(e){e.GSheet="gsheets",e.Snowflake="snowflake"}(U||(U={}));var z=t(17437),j=t(46942),B=t.n(j),V=t(27366),G=t(85994),K=t(61693),Q=t(24976);const J=z.AH`
  margin-bottom: 0;
`,W=s.I4.header`
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  .subheader-text {
    line-height: ${({theme:e})=>4.25*e.gridUnit}px;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,X=z.AH`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,Z=z.AH`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,ee=e=>z.AH`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,ae=e=>z.AH`
  padding-left: ${2*e.gridUnit}px;
`,te=e=>z.AH`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,ne=e=>z.AH`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,le=e=>z.AH`
  border: 1px solid ${e.colors.info.base};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;

  .ant-alert-message {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.m}px;
    font-weight: ${e.typography.weights.bold};
  }

  .ant-alert-description {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.m}px;
    line-height: ${5*e.gridUnit}px;

    a {
      text-decoration: underline;
    }

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,ie=s.I4.div`
  ${({theme:e})=>z.AH`
    margin: 0 ${4*e.gridUnit}px -${4*e.gridUnit}px;
  `}
`,re=e=>z.AH`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    text-align: left;
  }
`,oe=e=>z.AH`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 480px;
  }
`,se=e=>z.AH`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
    margin-bottom: 0;
  }
`,de=s.I4.div`
  ${({theme:e})=>z.AH`
    margin-bottom: ${6*e.gridUnit}px;
    &.mb-0 {
      margin-bottom: 0;
    }
    &.mb-8 {
      margin-bottom: ${2*e.gridUnit}px;
    }

    .control-label {
      color: ${e.colors.grayscale.dark1};
      font-size: ${e.typography.sizes.s}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    &.extra-container {
      padding-top: ${2*e.gridUnit}px;
    }

    .input-container {
      display: flex;
      align-items: top;

      label {
        display: flex;
        margin-left: ${2*e.gridUnit}px;
        margin-top: ${.75*e.gridUnit}px;
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
      }

      i {
        margin: 0 ${e.gridUnit}px;
      }
    }

    input,
    textarea {
      flex: 1 1 auto;
    }

    textarea {
      height: 160px;
      resize: none;
    }

    input::placeholder,
    textarea::placeholder {
      color: ${e.colors.grayscale.light1};
    }

    textarea,
    input[type='text'],
    input[type='number'] {
      padding: ${1.5*e.gridUnit}px ${2*e.gridUnit}px;
      border-style: none;
      border: 1px solid ${e.colors.grayscale.light2};
      border-radius: ${e.gridUnit}px;

      &[name='name'] {
        flex: 0 1 auto;
        width: 40%;
      }
    }
    &.expandable {
      height: 0;
      overflow: hidden;
      transition: height 0.25s;
      margin-left: ${8*e.gridUnit}px;
      margin-bottom: 0;
      padding: 0;
      .control-label {
        margin-bottom: 0;
      }
      &.open {
        height: ${108}px;
        padding-right: ${5*e.gridUnit}px;
      }
    }
  `}
`,ce=(0,s.I4)(Q.iN)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,he=s.I4.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${261}px;
      &.ctas-open {
        height: ${363}px;
      }
    }
  }
`,pe=s.I4.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ue=e=>z.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,me=e=>z.AH`
  font-size: ${3.5*e.gridUnit}px;
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,ge=s.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0px;
  }
`,be=(s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`),ve=s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,fe=s.I4.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none !important;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,ye=s.I4.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>e.typography.sizes.l}px;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,_e=(0,s.I4)(v.A)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,xe=s.I4.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
  height: auto;
`,Ye=s.I4.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,we=s.I4.div`
  .ant-progress-inner {
    display: none;
  }

  .ant-upload-list-item-card-actions {
    display: none;
  }
`,Ce=({db:e,onInputChange:a,onTextChange:t,onEditorChange:n,onExtraInputChange:l,onExtraEditorChange:i,extraExtension:r})=>{var o,c,h,p,u;const m=!(null==e||!e.expose_in_sqllab),g=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas),b=null==e||null==(o=e.engine_information)?void 0:o.supports_file_upload,v=null==e||null==(c=e.engine_information)?void 0:c.supports_dynamic_catalog,f=JSON.parse((null==e?void 0:e.extra)||"{}",((e,a)=>"engine_params"===e&&"object"==typeof a?JSON.stringify(a):a)),y=(0,s.DP)(),_=null==r?void 0:r.component,x=null==r?void 0:r.logo,Y=null==r?void 0:r.description,w=!!(0,V.G7)(V.TO.ForceSqlLabRunAsync)||!(null==e||!e.allow_run_async),C=(0,V.G7)(V.TO.ForceSqlLabRunAsync);return(0,$.FD)(K.A,{expandIconPosition:"right",accordion:!0,css:e=>(e=>z.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,$.Y)(K.A.Panel,{header:(0,$.FD)("div",{children:[(0,$.Y)("h4",{children:(0,d.t)("SQL Lab")}),(0,$.Y)("p",{className:"helper",children:(0,d.t)("Adjust how this database will interact with SQL Lab.")})]}),children:(0,$.FD)(de,{css:J,children:[(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:a,labelText:(0,d.t)("Expose database in SQL Lab")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Allow this database to be queried in SQL Lab")})]}),(0,$.FD)(he,{className:B()("expandable",{open:m,"ctas-open":g}),children:[(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:a,labelText:(0,d.t)("Allow CREATE TABLE AS")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Allow creation of new tables based on queries")})]})}),(0,$.FD)(de,{css:J,children:[(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:a,labelText:(0,d.t)("Allow CREATE VIEW AS")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Allow creation of new views based on queries")})]}),(0,$.FD)(de,{className:B()("expandable",{open:g}),children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("CTAS & CVAS SCHEMA")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"text",name:"force_ctas_schema",placeholder:(0,d.t)("Create or select schema..."),onChange:a,value:(null==e?void 0:e.force_ctas_schema)||""})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")})]})]}),(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:a,labelText:(0,d.t)("Allow DML")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")})]})}),(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==f||!f.cost_estimate_enabled),onChange:l,labelText:(0,d.t)("Enable query cost estimation")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("For Bigquery, Presto and Postgres, shows a button to compute cost before running a query.")})]})}),(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!1!==(null==f?void 0:f.allows_virtual_table_explore),onChange:l,labelText:(0,d.t)("Allow this database to be explored")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})]})}),(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"disable_data_preview",indeterminate:!1,checked:!(null==f||!f.disable_data_preview),onChange:l,labelText:(0,d.t)("Disable SQL Lab data preview queries")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Disable data preview when fetching table metadata in SQL Lab.  Useful to avoid browser performance issues when using  databases with very wide tables.")})]})}),(0,$.Y)(de,{children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"expand_rows",indeterminate:!1,checked:!(null==f||null==(h=f.schema_options)||!h.expand_rows),onChange:l,labelText:(0,d.t)("Enable row expansion in schemas")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("For Trino, describe full schemas of nested ROW types, expanding them with dotted paths")})]})})]})]})},"1"),(0,$.FD)(K.A.Panel,{header:(0,$.FD)("div",{children:[(0,$.Y)("h4",{children:(0,d.t)("Performance")}),(0,$.Y)("p",{className:"helper",children:(0,d.t)("Adjust performance settings of this database.")})]}),children:[(0,$.FD)(de,{className:"mb-8",children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Chart cache timeout")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:a})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires, and -1 bypasses the cache. Note this defaults to the global timeout if undefined.")})]}),(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Schema cache timeout")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"number",name:"schema_cache_timeout",value:(null==f||null==(p=f.metadata_cache_timeout)?void 0:p.schema_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires.")})]}),(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Table cache timeout")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"number",name:"table_cache_timeout",value:(null==f||null==(u=f.metadata_cache_timeout)?void 0:u.table_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. ")})]}),(0,$.Y)(de,{css:(0,z.AH)({no_margin_bottom:J},"",""),children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allow_run_async",indeterminate:!1,checked:w,onChange:a,labelText:(0,d.t)("Asynchronous query execution")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}),C&&(0,$.Y)(I.A,{iconStyle:{color:y.colors.error.base},tooltip:(0,d.t)("This option has been disabled by the administrator.")})]})}),(0,$.Y)(de,{css:(0,z.AH)({no_margin_bottom:J},"",""),children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==f||!f.cancel_query_on_windows_unload),onChange:l,labelText:(0,d.t)("Cancel query on window unload event")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})]})})]},"2"),(0,$.FD)(K.A.Panel,{header:(0,$.FD)("div",{children:[(0,$.Y)("h4",{children:(0,d.t)("Security")}),(0,$.Y)("p",{className:"helper",children:(0,d.t)("Add extra connection information.")})]}),children:[(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Secure extra")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)(ce,{name:"masked_encrypted_extra",value:(null==e?void 0:e.masked_encrypted_extra)||"",placeholder:(0,d.t)("Secure extra"),onChange:e=>n({json:e,name:"masked_encrypted_extra"}),width:"100%",height:"160px"})}),(0,$.Y)("div",{className:"helper",children:(0,$.Y)("div",{children:(0,d.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")})})]}),(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Root certificate")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,d.t)("Enter CA_BUNDLE"),onChange:t})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines.")})]}),(0,$.Y)(de,{css:b?{}:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:a,labelText:(0,d.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")})]})}),b&&(0,$.Y)(de,{css:null!=e&&e.allow_file_upload?{}:J,children:(0,$.Y)("div",{className:"input-container",children:(0,$.Y)(G.A,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:a,labelText:(0,d.t)("Allow file uploads to database")})})}),b&&!(null==e||!e.allow_file_upload)&&(0,$.FD)(de,{css:J,children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Schemas allowed for File upload")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==f?void 0:f.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("A comma-separated list of schemas that files are allowed to upload to.")})]})]},"3"),r&&_&&Y&&(0,$.Y)(K.A.Panel,{header:(0,$.FD)("div",{children:[x&&(0,$.Y)(x,{}),(0,$.Y)("span",{css:e=>({fontSize:e.typography.sizes.l,fontWeight:e.typography.weights.bold}),children:null==r?void 0:r.title}),(0,$.Y)("p",{className:"helper",children:(0,$.Y)(Y,{})})]}),collapsible:null!=r.enabled&&r.enabled()?"icon":"disabled",children:(0,$.Y)(de,{css:J,children:(0,$.Y)(_,{db:e,onEdit:r.onEdit})})},null==r?void 0:r.title),(0,$.FD)(K.A.Panel,{header:(0,$.FD)("div",{children:[(0,$.Y)("h4",{children:(0,d.t)("Other")}),(0,$.Y)("p",{className:"helper",children:(0,d.t)("Additional settings.")})]}),children:[(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Metadata Parameters")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)(ce,{name:"metadata_params",placeholder:(0,d.t)("Metadata Parameters"),onChange:e=>i({json:e,name:"metadata_params"}),width:"100%",height:"160px",value:Object.keys((null==f?void 0:f.metadata_params)||{}).length?null==f?void 0:f.metadata_params:""})}),(0,$.Y)("div",{className:"helper",children:(0,$.Y)("div",{children:(0,d.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")})})]}),(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Engine Parameters")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)(ce,{name:"engine_params",placeholder:(0,d.t)("Engine Parameters"),onChange:e=>i({json:e,name:"engine_params"}),width:"100%",height:"160px",value:Object.keys((null==f?void 0:f.engine_params)||{}).length?null==f?void 0:f.engine_params:""})}),(0,$.Y)("div",{className:"helper",children:(0,$.Y)("div",{children:(0,d.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")})})]}),(0,$.FD)(de,{children:[(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Version")}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"text",name:"version",placeholder:(0,d.t)("Version number"),onChange:l,value:(null==f?void 0:f.version)||""})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Specify the database version. This is used with Presto for query cost estimation, and Dremio for syntax changes, among others.")})]}),(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"disable_drill_to_detail",indeterminate:!1,checked:!(null==f||!f.disable_drill_to_detail),onChange:l,labelText:(0,d.t)("Disable drill to detail")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Disables the drill to detail feature for this database.")})]})}),v&&(0,$.Y)(de,{css:J,children:(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(G.A,{id:"allow_multi_catalog",indeterminate:!1,checked:!(null==f||!f.allow_multi_catalog),onChange:l,labelText:(0,d.t)("Allow changing catalogs")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Give access to multiple catalogs in a single database connection.")})]})})]},"4")]})};var Se=t(27588);const Ae=({db:e,onInputChange:a,testConnection:t,conf:n,testInProgress:l=!1,children:i})=>{var r,o;const s=(null==Se.A||null==(r=Se.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:r.SQLALCHEMY_DOCS_URL)||"https://docs.sqlalchemy.org/en/13/core/engines.html",c=(null==Se.A||null==(o=Se.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:o.SQLALCHEMY_DISPLAY_TEXT)||"SQLAlchemy docs";return(0,$.FD)($.FK,{children:[(0,$.FD)(de,{children:[(0,$.FD)("div",{className:"control-label",children:[(0,d.t)("Display Name"),(0,$.Y)("span",{className:"required",children:"*"})]}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:(0,d.t)("Name your database"),onChange:a})}),(0,$.Y)("div",{className:"helper",children:(0,d.t)("Pick a name to help you identify this database.")})]}),(0,$.FD)(de,{children:[(0,$.FD)("div",{className:"control-label",children:[(0,d.t)("SQLAlchemy URI"),(0,$.Y)("span",{className:"required",children:"*"})]}),(0,$.Y)("div",{className:"input-container",children:(0,$.Y)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(null==e?void 0:e.sqlalchemy_uri_placeholder)||(0,d.t)("dialect+driver://username:password@host:port/database"),onChange:a})}),(0,$.FD)("div",{className:"helper",children:[(0,d.t)("Refer to the")," ",(0,$.Y)("a",{href:s||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer",children:c||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||""})," ",(0,d.t)("for more information on how to structure your URI.")]})]}),i,(0,$.Y)(v.A,{onClick:t,loading:l,cta:!0,buttonStyle:"link",css:e=>(e=>z.AH`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e),children:(0,d.t)("Test connection")})]})};var $e=t(40563);const De={account:{helpText:(0,d.t)("Copy the identifier of the account you are trying to connect to."),placeholder:(0,d.t)("e.g. xy12345.us-east-2.aws")},warehouse:{placeholder:(0,d.t)("e.g. compute_wh"),className:"form-group-w-50"},role:{placeholder:(0,d.t)("e.g. AccountAdmin"),className:"form-group-w-50"}},Ne=({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,field:i})=>{var r;return(0,$.Y)(q.A,{id:i,name:i,required:e,value:null==l||null==(r=l.parameters)?void 0:r[i],validationMethods:{onBlur:t},errorMessage:null==n?void 0:n[i],placeholder:De[i].placeholder,helpText:De[i].helpText,label:i,onChange:a.onParametersChange,className:De[i].className||i})};var Fe,ke=t(40458);!function(e){e[e.JsonUpload=0]="JsonUpload",e[e.CopyPaste=1]="CopyPaste"}(Fe||(Fe={}));const Ee={gsheets:"service_account_info",bigquery:"credentials_info"};var Te={name:"s5xdrg",styles:"display:flex;align-items:center"};const Ue=({changeMethods:e,isEditMode:a,db:t,editNewDb:n})=>{var l,i,r;const[o,s]=(0,c.useState)(Fe.JsonUpload.valueOf()),[h,p]=(0,c.useState)(null),[u,g]=(0,c.useState)(!0),b="gsheets"===(null==t?void 0:t.engine)?!a&&!u:!a,v=a&&"{}"!==(null==t?void 0:t.masked_encrypted_extra),y=(null==t?void 0:t.engine)&&Ee[t.engine],_="object"==typeof(null==t||null==(l=t.parameters)?void 0:l[y])?JSON.stringify(null==t||null==(i=t.parameters)?void 0:i[y]):null==t||null==(r=t.parameters)?void 0:r[y];return(0,$.FD)(fe,{children:["gsheets"===(null==t?void 0:t.engine)&&(0,$.FD)("div",{className:"catalog-type-select",children:[(0,$.Y)(ke.A,{css:e=>(e=>z.AH`
  margin-bottom: ${2*e.gridUnit}px;
`)(e),required:!0,children:(0,d.t)("Type of Google Sheets allowed")}),(0,$.FD)(m._P,{style:{width:"100%"},defaultValue:v?"false":"true",onChange:e=>g("true"===e),children:[(0,$.Y)(m._P.Option,{value:"true",children:(0,d.t)("Publicly shared sheets only")},1),(0,$.Y)(m._P.Option,{value:"false",children:(0,d.t)("Public and privately shared sheets")},2)]})]}),b&&(0,$.FD)($.FK,{children:[(0,$.Y)(ke.A,{required:!0,children:(0,d.t)("How do you want to enter service account credentials?")}),(0,$.FD)(m._P,{defaultValue:o,style:{width:"100%"},onChange:e=>s(e),children:[(0,$.Y)(m._P.Option,{value:Fe.JsonUpload,children:(0,d.t)("Upload JSON file")}),(0,$.Y)(m._P.Option,{value:Fe.CopyPaste,children:(0,d.t)("Copy and Paste JSON credentials")})]})]}),o===Fe.CopyPaste||a||n?(0,$.FD)("div",{className:"input-container",children:[(0,$.Y)(ke.A,{required:!0,children:(0,d.t)("Service Account")}),(0,$.Y)("textarea",{className:"input-form",name:y,value:_,onChange:e.onParametersChange,placeholder:(0,d.t)("Paste content of service credentials JSON file here")}),(0,$.Y)("span",{className:"label-paste",children:(0,d.t)("Copy and paste the entire service account .json file here")})]}):b&&(0,$.FD)("div",{className:"input-container",css:e=>ee(e),children:[(0,$.FD)("div",{css:Te,children:[(0,$.Y)(ke.A,{required:!0,children:(0,d.t)("Upload Credentials")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Use the JSON file you automatically downloaded when creating your service account."),viewBox:"0 0 24 24"})]}),!h&&(0,$.Y)(m.QC,{className:"input-upload-btn",onClick:()=>{var e,a;return null==(e=document)||null==(a=e.getElementById("selectedFile"))?void 0:a.click()},children:(0,d.t)("Choose File")}),h&&(0,$.FD)("div",{className:"input-upload-current",children:[h,(0,$.Y)(f.A.DeleteFilled,{iconSize:"m",onClick:()=>{p(null),e.onParametersChange({target:{name:y,value:""}})}})]}),(0,$.Y)("input",{id:"selectedFile",accept:".json",className:"input-upload",type:"file",onChange:async a=>{var t,n;let l;a.target.files&&(l=a.target.files[0]),p(null==(t=l)?void 0:t.name),e.onParametersChange({target:{type:null,name:y,value:await(null==(n=l)?void 0:n.text()),checked:!1}}),document.getElementById("selectedFile").value=null}})]})]})},Ie=({clearValidationErrors:e,changeMethods:a,db:t,dbModel:n})=>{var l,i,o;const[s,h]=(0,c.useState)(!1),p=(0,V.G7)(V.TO.SshTunneling),u=(null==n||null==(l=n.engine_information)?void 0:l.disable_ssh_tunneling)||!1,g=p&&!u;return(0,c.useEffect)((()=>{var e;g&&void 0!==(null==t||null==(e=t.parameters)?void 0:e.ssh)&&h(t.parameters.ssh)}),[null==t||null==(i=t.parameters)?void 0:i.ssh,g]),(0,c.useEffect)((()=>{var e;g&&void 0===(null==t||null==(e=t.parameters)?void 0:e.ssh)&&!r()(null==t?void 0:t.ssh_tunnel)&&a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:!0}})}),[a,null==t||null==(o=t.parameters)?void 0:o.ssh,null==t?void 0:t.ssh_tunnel,g]),g?(0,$.FD)("div",{css:e=>ee(e),children:[(0,$.Y)(m._b,{checked:s,onChange:t=>{h(t),a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:t}}),e()}}),(0,$.Y)("span",{css:ae,children:(0,d.t)("SSH Tunnel")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"})]}):null};var Pe;const qe=["host","port","database","default_catalog","default_schema","username","password","access_token","http_path","http_path_field","database_name","credentials_info","service_account_info","catalog","query","encryption","account","warehouse","role","ssh"],Le={host:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return(0,$.Y)(q.A,{id:"host",name:"host",value:null==l||null==(i=l.parameters)?void 0:i.host,required:e,hasTooltip:!0,tooltipText:(0,d.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.host,placeholder:(0,d.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,d.t)("Host"),onChange:a.onParametersChange})},http_path:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i,r;const o=JSON.parse((null==l?void 0:l.extra)||"{}");return(0,$.Y)(q.A,{id:"http_path",name:"http_path",required:e,value:null==(i=o.engine_params)||null==(r=i.connect_args)?void 0:r.http_path,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onExtraInputChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},http_path_field:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return console.error(l),(0,$.Y)(q.A,{id:"http_path_field",name:"http_path_field",required:e,value:null==l||null==(i=l.parameters)?void 0:i.http_path_field,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},port:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return(0,$.Y)($.FK,{children:(0,$.Y)(q.A,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(i=l.parameters)?void 0:i.port,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.port,placeholder:(0,d.t)("e.g. 5432"),className:"form-group-w-50",label:(0,d.t)("Port"),onChange:a.onParametersChange})})},database:({required:e,changeMethods:a,getValidation:t,validationErrors:n,placeholder:l,db:i})=>{var r;return(0,$.Y)(q.A,{id:"database",name:"database",required:e,value:null==i||null==(r=i.parameters)?void 0:r.database,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.database,placeholder:null!=l?l:(0,d.t)("e.g. world_population"),label:(0,d.t)("Database name"),onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the database you are trying to connect to.")})},default_catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return(0,$.Y)(q.A,{id:"default_catalog",name:"default_catalog",required:e,value:null==l||null==(i=l.parameters)?void 0:i.default_catalog,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_catalog,placeholder:(0,d.t)("e.g. hive_metastore"),label:(0,d.t)("Default Catalog"),onChange:a.onParametersChange,helpText:(0,d.t)("The default catalog that should be used for the connection.")})},default_schema:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return(0,$.Y)(q.A,{id:"default_schema",name:"default_schema",required:e,value:null==l||null==(i=l.parameters)?void 0:i.default_schema,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_schema,placeholder:(0,d.t)("e.g. default"),label:(0,d.t)("Default Schema"),onChange:a.onParametersChange,helpText:(0,d.t)("The default schema that should be used for the connection.")})},username:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var i;return(0,$.Y)(q.A,{id:"username",name:"username",required:e,value:null==l||null==(i=l.parameters)?void 0:i.username,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.username,placeholder:(0,d.t)("e.g. Analytics"),label:(0,d.t)("Username"),onChange:a.onParametersChange})},password:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:i})=>{var r;return(0,$.Y)(q.A,{id:"password",name:"password",required:e,visibilityToggle:!i,value:null==l||null==(r=l.parameters)?void 0:r.password,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.password,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Password"),onChange:a.onParametersChange})},access_token:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:i,default_value:r,description:o})=>{var s;return(0,$.Y)(q.A,{id:"access_token",name:"access_token",required:e,visibilityToggle:!i,value:null==l||null==(s=l.parameters)?void 0:s.access_token,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.access_token,placeholder:(0,d.t)("Paste your access token here"),get_url:"string"==typeof r&&r.includes("https://")?r:null,description:o,label:(0,d.t)("Access token"),onChange:a.onParametersChange})},database_name:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>(0,$.Y)($.FK,{children:(0,$.Y)(q.A,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.database_name,placeholder:"",label:(0,d.t)("Display Name"),onChange:e.onChange,helpText:(0,d.t)("Pick a nickname for how the database will display in Superset.")})}),query:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>(0,$.Y)(q.A,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.query,placeholder:(0,d.t)("e.g. param1=value1&param2=value2"),label:(0,d.t)("Additional Parameters"),onChange:a.onQueryChange,helpText:(0,d.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:a,db:t,sslForced:n})=>{var l;return(0,$.FD)("div",{css:e=>ee(e),children:[(0,$.Y)(m._b,{disabled:n&&!e,checked:(null==t||null==(l=t.parameters)?void 0:l.encryption)||n,onChange:e=>{a.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,$.Y)("span",{css:ae,children:"SSL"}),(0,$.Y)(I.A,{tooltip:(0,d.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"})]})},credentials_info:Ue,service_account_info:Ue,catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{const i=(null==l?void 0:l.catalog)||[],r=n||{};return(0,$.FD)(Ye,{children:[(0,$.Y)("h4",{className:"gsheet-title",children:(0,d.t)("Connect Google Sheets as tables to this database")}),(0,$.FD)("div",{children:[null==i?void 0:i.map(((n,l)=>{var o,s;return(0,$.FD)($.FK,{children:[(0,$.Y)(ke.A,{className:"catalog-label",required:!0,children:(0,d.t)("Google Sheet Name and URL")}),(0,$.FD)("div",{className:"catalog-name",children:[(0,$.Y)(q.A,{className:"catalog-name-input",required:e,validationMethods:{onBlur:t},errorMessage:null==(o=r[l])?void 0:o.name,placeholder:(0,d.t)("Enter a name for this sheet"),onChange:e=>{a.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:n.name}),(null==i?void 0:i.length)>1&&(0,$.Y)(f.A.CloseOutlined,{css:e=>z.AH`
                    align-self: center;
                    background: ${e.colors.grayscale.light4};
                    margin: 5px 5px 8px 5px;

                    &.anticon > * {
                      line-height: 0;
                    }
                  `,iconSize:"m",onClick:()=>a.onRemoveTableCatalog(l)})]}),(0,$.Y)(q.A,{className:"catalog-name-url",required:e,validationMethods:{onBlur:t},errorMessage:null==(s=r[l])?void 0:s.url,placeholder:(0,d.t)("Paste the shareable Google Sheet URL here"),onChange:e=>a.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:n.value})]})})),(0,$.FD)(_e,{className:"catalog-add-btn",onClick:()=>{a.onAddTableCatalog()},children:["+ ",(0,d.t)("Add sheet")]})]})]})},warehouse:Ne,role:Ne,account:Ne,ssh:null!=(Pe=(0,o.a)().get("ssh_tunnel.form.switch"))?Pe:Ie},Me=({dbModel:e,db:a,editNewDb:t,getPlaceholder:n,getValidation:l,isEditMode:i=!1,onAddTableCatalog:r,onChange:o,onExtraInputChange:s,onParametersChange:d,onParametersUploadFileChange:c,onQueryChange:h,onRemoveTableCatalog:p,sslForced:u,validationErrors:m,clearValidationErrors:g})=>{const b=null==e?void 0:e.parameters;return(0,$.Y)($e.lV,{children:(0,$.Y)("div",{css:e=>[te,se(e)],children:b&&qe.filter((e=>Object.keys(b.properties).includes(e)||"database_name"===e)).map((e=>{var v,f,y;return Le[e]({required:null==(v=b.required)?void 0:v.includes(e),changeMethods:{onParametersChange:d,onChange:o,onQueryChange:h,onParametersUploadFileChange:c,onAddTableCatalog:r,onRemoveTableCatalog:p,onExtraInputChange:s},validationErrors:m,getValidation:l,clearValidationErrors:g,db:a,key:e,field:e,default_value:null==(f=b.properties[e])?void 0:f.default,description:null==(y=b.properties[e])?void 0:y.description,isEditMode:i,sslForced:u,editNewDb:t,placeholder:n?n(e):void 0})}))})})},Oe=(0,O.xK)(),He=Oe?Oe.support:"https://superset.apache.org/docs/configuration/databases#installing-database-drivers",Re={postgresql:"https://superset.apache.org",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},ze=({isLoading:e,isEditMode:a,useSqlAlchemyForm:t,hasConnectedDb:n,db:l,dbName:i,dbModel:r,editNewDb:o,fileList:s})=>{const c=s&&(null==s?void 0:s.length)>0,h=(0,$.FD)(W,{children:[(0,$.Y)(be,{children:null==l?void 0:l.backend}),(0,$.Y)(ve,{children:i})]}),p=(0,$.FD)(W,{children:[(0,$.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,$.Y)("h4",{children:(0,d.t)("Enter Primary Credentials")}),(0,$.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn how to connect your database")," ",(0,$.Y)("a",{href:(null==Oe?void 0:Oe.default)||He,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})]}),u=(0,$.Y)(xe,{children:(0,$.FD)(W,{children:[(0,$.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:3,stepLast:3})}),(0,$.Y)("h4",{className:"step-3-text",children:(0,d.t)("Database connected")}),(0,$.Y)("p",{className:"subheader-text",children:(0,d.t)("Create a dataset to begin visualizing your data as a chart or go to\n          SQL Lab to query your data.")})]})}),m=(0,$.Y)(xe,{children:(0,$.FD)(W,{children:[(0,$.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:3})}),(0,$.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:r.name})}),(0,$.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn more about")," ",(0,$.FD)("a",{href:(g=null==l?void 0:l.engine,g?Oe?Oe[g]||Oe.default:Re[g]?Re[g]:`https://superset.apache.org/docs/databases/${g}`:null),target:"_blank",rel:"noopener noreferrer",children:[(0,d.t)("connecting to %(dbModelName)s",{dbModelName:r.name}),"."]})]})]})});var g;const b=(0,$.Y)(W,{children:(0,$.FD)("div",{className:"select-db",children:[(0,$.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:1,stepLast:3})}),(0,$.Y)("h4",{children:(0,d.t)("Select a database to connect")})]})}),v=(0,$.Y)(xe,{children:(0,$.FD)(W,{children:[(0,$.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,$.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:r.name})}),(0,$.Y)("p",{className:"helper-bottom",children:c?s[0].name:""})]})});return c?v:e?(0,$.Y)($.FK,{}):a?h:t?p:n&&!o?u:l||o?m:b};var je=t(78697),Be=t(90868),Ve=t(36255),Ge=t(27236),Ke=t(94904),Qe=t(11387);const Je=s.I4.div`
  padding-top: ${({theme:e})=>2*e.gridUnit}px;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,We=(0,s.I4)(m.fI)`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,Xe=(0,s.I4)(m.Wq.Item)`
  margin-bottom: 0 !important;
`,Ze=(0,s.I4)(Ve.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,ea=({db:e,onSSHTunnelParametersChange:a,setSSHTunnelLoginMethod:t})=>{var n,l,i,r,o,s;const[h,p]=(0,c.useState)(sa.Password);return(0,$.FD)($e.lV,{children:[(0,$.FD)(We,{gutter:16,children:[(0,$.Y)(m.fv,{xs:24,md:12,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"server_address",required:!0,children:(0,d.t)("SSH Host")}),(0,$.Y)(Be.pd,{name:"server_address",type:"text",placeholder:(0,d.t)("e.g. 127.0.0.1"),value:(null==e||null==(n=e.ssh_tunnel)?void 0:n.server_address)||"",onChange:a})]})}),(0,$.Y)(m.fv,{xs:24,md:12,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"server_port",required:!0,children:(0,d.t)("SSH Port")}),(0,$.Y)(Be.pd,{name:"server_port",placeholder:(0,d.t)("22"),type:"number",value:null==e||null==(l=e.ssh_tunnel)?void 0:l.server_port,onChange:a})]})})]}),(0,$.Y)(We,{gutter:16,children:(0,$.Y)(m.fv,{xs:24,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"username",required:!0,children:(0,d.t)("Username")}),(0,$.Y)(Be.pd,{name:"username",type:"text",placeholder:(0,d.t)("e.g. Analytics"),value:(null==e||null==(i=e.ssh_tunnel)?void 0:i.username)||"",onChange:a})]})})}),(0,$.Y)(We,{gutter:16,children:(0,$.Y)(m.fv,{xs:24,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"use_password",required:!0,children:(0,d.t)("Login with")}),(0,$.Y)(Xe,{name:"use_password",initialValue:h,children:(0,$.FD)(je.s.Group,{onChange:({target:{value:e}})=>{p(e),t(e)},children:[(0,$.Y)(je.s,{value:sa.Password,children:(0,d.t)("Password")}),(0,$.Y)(je.s,{value:sa.PrivateKey,children:(0,d.t)("Private Key & Password")})]})})]})})}),h===sa.Password&&(0,$.Y)(We,{gutter:16,children:(0,$.Y)(m.fv,{xs:24,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"password",required:!0,children:(0,d.t)("SSH Password")}),(0,$.Y)(Ze,{name:"password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(r=e.ssh_tunnel)?void 0:r.password)||"",onChange:a,iconRender:e=>e?(0,$.Y)(Ge.A,{title:"Hide password.",children:(0,$.Y)(Ke.A,{})}):(0,$.Y)(Ge.A,{title:"Show password.",children:(0,$.Y)(Qe.A,{})}),role:"textbox"})]})})}),h===sa.PrivateKey&&(0,$.FD)($.FK,{children:[(0,$.Y)(We,{gutter:16,children:(0,$.Y)(m.fv,{xs:24,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"private_key",required:!0,children:(0,d.t)("Private Key")}),(0,$.Y)(Be.fs,{name:"private_key",placeholder:(0,d.t)("Paste Private Key here"),value:(null==e||null==(o=e.ssh_tunnel)?void 0:o.private_key)||"",onChange:a,rows:4})]})})}),(0,$.Y)(We,{gutter:16,children:(0,$.Y)(m.fv,{xs:24,children:(0,$.FD)(Je,{children:[(0,$.Y)($e.lR,{htmlFor:"private_key_password",required:!0,children:(0,d.t)("Private Key Password")}),(0,$.Y)(Ze,{name:"private_key_password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(s=e.ssh_tunnel)?void 0:s.private_key_password)||"",onChange:a,iconRender:e=>e?(0,$.Y)(Ge.A,{title:"Hide password.",children:(0,$.Y)(Ke.A,{})}):(0,$.Y)(Ge.A,{title:"Show password.",children:(0,$.Y)(Qe.A,{})}),role:"textbox"})]})})})]})]})},aa=(0,o.a)(),ta=JSON.stringify({allows_virtual_table_explore:!0}),na={[U.GSheet]:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},la=(0,s.I4)(u.Ay)`
  .ant-tabs-content {
    display: flex;
    width: 100%;
    overflow: inherit;

    & > .ant-tabs-tabpane {
      position: relative;
    }
  }
`,ia=s.I4.div`
  ${({theme:e})=>`\n    margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;\n  `};
`,ra=s.I4.div`
  ${({theme:e})=>`\n    padding: 0px ${4*e.gridUnit}px;\n  `};
`;var oa,sa;!function(e){e[e.AddTableCatalogSheet=0]="AddTableCatalogSheet",e[e.ConfigMethodChange=1]="ConfigMethodChange",e[e.DbSelected=2]="DbSelected",e[e.EditorChange=3]="EditorChange",e[e.ExtraEditorChange=4]="ExtraEditorChange",e[e.ExtraInputChange=5]="ExtraInputChange",e[e.Fetched=6]="Fetched",e[e.InputChange=7]="InputChange",e[e.ParametersChange=8]="ParametersChange",e[e.QueryChange=9]="QueryChange",e[e.RemoveTableCatalogSheet=10]="RemoveTableCatalogSheet",e[e.Reset=11]="Reset",e[e.TextChange=12]="TextChange",e[e.ParametersSSHTunnelChange=13]="ParametersSSHTunnelChange",e[e.SetSSHTunnelLoginMethod=14]="SetSSHTunnelLoginMethod",e[e.RemoveSSHTunnelConfig=15]="RemoveSSHTunnelConfig"}(oa||(oa={})),function(e){e[e.Password=0]="Password",e[e.PrivateKey=1]="PrivateKey"}(sa||(sa={}));const da=s.I4.div`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  margin-left: ${({theme:e})=>3*e.gridUnit}px;
`;function ca(e,a){var t,n,i,r;const o={...e||{}};let s,d,c={},h="";const p=JSON.parse(o.extra||"{}");switch(a.type){case oa.ExtraEditorChange:try{d=JSON.parse(a.payload.json||"{}")}catch(e){d=a.payload.json}return{...o,extra:JSON.stringify({...p,[a.payload.name]:d})};case oa.ExtraInputChange:return"schema_cache_timeout"===a.payload.name||"table_cache_timeout"===a.payload.name?{...o,extra:JSON.stringify({...p,metadata_cache_timeout:{...null==p?void 0:p.metadata_cache_timeout,[a.payload.name]:a.payload.value}})}:"schemas_allowed_for_file_upload"===a.payload.name?{...o,extra:JSON.stringify({...p,schemas_allowed_for_file_upload:(a.payload.value||"").split(",").filter((e=>""!==e))})}:"http_path"===a.payload.name?{...o,extra:JSON.stringify({...p,engine_params:{connect_args:{[a.payload.name]:null==(u=a.payload.value)?void 0:u.trim()}}})}:"expand_rows"===a.payload.name?{...o,extra:JSON.stringify({...p,schema_options:{...null==p?void 0:p.schema_options,[a.payload.name]:!!a.payload.value}})}:{...o,extra:JSON.stringify({...p,[a.payload.name]:"checkbox"===a.payload.type?a.payload.checked:a.payload.value})};var u;case oa.InputChange:return"checkbox"===a.payload.type?{...o,[a.payload.name]:a.payload.checked}:{...o,[a.payload.name]:a.payload.value};case oa.ParametersChange:if(null!=(t=a.payload.type)&&t.startsWith("catalog")&&void 0!==o.catalog){var m;const e=[...o.catalog],t=null==(m=a.payload.type)?void 0:m.split("-")[1],n=e[t]||{};return n[a.payload.name]=a.payload.value,e.splice(parseInt(t,10),1,n),s=e.reduce(((e,a)=>{const t={...e};return t[a.name]=a.value,t}),{}),{...o,catalog:e,parameters:{...o.parameters,catalog:s}}}return{...o,parameters:{...o.parameters,[a.payload.name]:a.payload.value}};case oa.ParametersSSHTunnelChange:return{...o,ssh_tunnel:{...o.ssh_tunnel,[a.payload.name]:a.payload.value}};case oa.SetSSHTunnelLoginMethod:{let e={};var g,b,v;return null!=o&&o.ssh_tunnel&&(e=l()(o.ssh_tunnel,["id","server_address","server_port","username"])),a.payload.login_method===sa.PrivateKey?{...o,ssh_tunnel:{private_key:null==o||null==(g=o.ssh_tunnel)?void 0:g.private_key,private_key_password:null==o||null==(b=o.ssh_tunnel)?void 0:b.private_key_password,...e}}:a.payload.login_method===sa.Password?{...o,ssh_tunnel:{password:null==o||null==(v=o.ssh_tunnel)?void 0:v.password,...e}}:{...o}}case oa.RemoveSSHTunnelConfig:return{...o,ssh_tunnel:void 0};case oa.AddTableCatalogSheet:return void 0!==o.catalog?{...o,catalog:[...o.catalog,{name:"",value:""}]}:{...o,catalog:[{name:"",value:""}]};case oa.RemoveTableCatalogSheet:return null==(n=o.catalog)||n.splice(a.payload.indexToDelete,1),{...o};case oa.EditorChange:return{...o,[a.payload.name]:a.payload.json};case oa.QueryChange:return{...o,parameters:{...o.parameters,query:Object.fromEntries(new URLSearchParams(a.payload.value))},query_input:a.payload.value};case oa.TextChange:return{...o,[a.payload.name]:a.payload.value};case oa.Fetched:if(c=(null==(i=a.payload)||null==(r=i.parameters)?void 0:r.query)||{},h=Object.entries(c).map((([e,a])=>`${e}=${a}`)).join("&"),a.payload.masked_encrypted_extra&&a.payload.configuration_method===T.DynamicForm){var f;const e=null==(f={...JSON.parse(a.payload.extra||"{}")}.engine_params)?void 0:f.catalog,t=Object.entries(e||{}).map((([e,a])=>({name:e,value:a})));return{...a.payload,engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,catalog:t,parameters:{...a.payload.parameters||o.parameters,catalog:e},query_input:h}}return{...a.payload,masked_encrypted_extra:a.payload.masked_encrypted_extra||"",engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,parameters:a.payload.parameters||o.parameters,ssh_tunnel:a.payload.ssh_tunnel||o.ssh_tunnel,query_input:h};case oa.DbSelected:return{...a.payload,extra:ta,expose_in_sqllab:!0};case oa.ConfigMethodChange:return{...a.payload};case oa.Reset:default:return null}}const ha=(0,P.Ay)((({addDangerToast:e,addSuccessToast:a,onDatabaseAdd:t,onHide:n,show:l,databaseId:i,dbEngine:o})=>{var s,f,y,_;const[x,Y]=(0,c.useReducer)(ca,null),{state:{loading:w,resource:C,error:S},fetchResource:A,createResource:D,updateResource:N,clearError:F}=(0,O.fn)("database",(0,d.t)("database"),e,"connection"),[k,P]=(0,c.useState)("1"),[j,B]=(0,O.d5)(),[V,G,K]=(0,O.Y8)(),[Q,J]=(0,c.useState)(!1),[W,ae]=(0,c.useState)(!1),[se,de]=(0,c.useState)(""),[ce,he]=(0,c.useState)(!1),[be,ve]=(0,c.useState)(!1),[fe,Ye]=(0,c.useState)(!1),[Se,$e]=(0,c.useState)({}),[De,Ne]=(0,c.useState)({}),[Fe,ke]=(0,c.useState)({}),[Ee,Te]=(0,c.useState)({}),[Ue,Pe]=(0,c.useState)(!1),[qe,Le]=(0,c.useState)([]),[Oe,Re]=(0,c.useState)(!1),[je,Be]=(0,c.useState)(),[Ve,Ge]=(0,c.useState)([]),[Ke,Qe]=(0,c.useState)([]),[Je,We]=(0,c.useState)([]),[Xe,Ze]=(0,c.useState)([]),[ta,sa]=(0,c.useState)({}),ha=null!=(s=aa.get("ssh_tunnel.form.switch"))?s:Ie,[pa,ua]=(0,c.useState)(void 0);let ma=aa.get("databaseconnection.extraOption");ma&&(ma={...ma,onEdit:e=>{sa({...ta,...e})}});const ga=(0,H.B)(),ba=(0,O.g9)(),va=(0,O.Fp)(),fa=!!i,ya=va||!(null==x||!x.engine||!na[x.engine]),_a=(null==x?void 0:x.configuration_method)===T.SqlalchemyUri,xa=fa||_a,Ya=V||S,wa=(0,h.W6)(),Ca=(null==j||null==(f=j.databases)?void 0:f.find((e=>e.engine===(fa?null==x?void 0:x.backend:null==x?void 0:x.engine)&&e.default_driver===(null==x?void 0:x.driver))))||(null==j||null==(y=j.databases)?void 0:y.find((e=>e.engine===(fa?null==x?void 0:x.backend:null==x?void 0:x.engine))))||{},Sa=e=>{if("database"===e)return(0,d.t)("e.g. world_population")},Aa=(0,c.useCallback)(((e,a)=>{Y({type:e,payload:a})}),[]),$a=(0,c.useCallback)((()=>{K(null)}),[K]),Da=(0,c.useCallback)((({target:e})=>{Aa(oa.ParametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})}),[Aa]),Na=()=>{Y({type:oa.Reset}),J(!1),$a(),F(),he(!1),Le([]),Re(!1),Be(""),Ge([]),Qe([]),We([]),Ze([]),$e({}),Ne({}),ke({}),Te({}),Pe(!1),ua(void 0),n()},Fa=e=>{wa.push(e)},{state:{alreadyExists:ka,passwordsNeeded:Ea,sshPasswordNeeded:Ta,sshPrivateKeyNeeded:Ua,sshPrivateKeyPasswordNeeded:Ia,loading:Pa,failed:qa},importResource:La}=(0,O.bN)("database",(0,d.t)("database"),(e=>{Be(e)})),Ma=async()=>{var n,l;let i;if(ve(!0),null==(n=ma)||n.onSave(ta,x).then((({error:a})=>{a&&(i=a,e(a))})),i)return void ve(!1);const o={...x||{}};if(o.configuration_method===T.DynamicForm){var s,c;null!=o&&null!=(s=o.parameters)&&s.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}}));const a=await G(o,!0);if(!r()(V)||null!=a&&a.length)return e((0,d.t)("Connection failed, please check your connection settings.")),void ve(!1);const t=fa?null==(c=o.parameters_schema)?void 0:c.properties:null==Ca?void 0:Ca.parameters.properties,n=JSON.parse(o.masked_encrypted_extra||"{}");Object.keys(t||{}).forEach((e=>{var a,l,i,r;t[e]["x-encrypted-extra"]&&null!=(a=o.parameters)&&a[e]&&("object"==typeof(null==(l=o.parameters)?void 0:l[e])?(n[e]=null==(i=o.parameters)?void 0:i[e],o.parameters[e]=JSON.stringify(o.parameters[e])):n[e]=JSON.parse((null==(r=o.parameters)?void 0:r[e])||"{}"))})),o.masked_encrypted_extra=JSON.stringify(n),o.engine===U.GSheet&&(o.impersonate_user=!0)}if(null!=o&&null!=(l=o.parameters)&&l.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}})),!1===pa&&(o.ssh_tunnel=null),null!=x&&x.id){if(await N(x.id,o,o.configuration_method===T.DynamicForm)){var h;if(t&&t(),null==(h=ma)||h.onSave(ta,x).then((({error:a})=>{a&&(i=a,e(a))})),i)return void ve(!1);ce||(Na(),a((0,d.t)("Database settings updated")))}}else if(x){if(await D(o,o.configuration_method===T.DynamicForm)){var p;if(J(!0),t&&t(),null==(p=ma)||p.onSave(ta,x).then((({error:a})=>{a&&(i=a,e(a))})),i)return void ve(!1);xa&&(Na(),a((0,d.t)("Database connected")))}}else{if(Re(!0),!(qe[0].originFileObj instanceof File))return;await La(qe[0].originFileObj,Se,De,Fe,Ee,Ue)&&(t&&t(),Na(),a((0,d.t)("Database connected")))}ae(!0),he(!1),ve(!1)},Oa=e=>{if("Other"===e)Y({type:oa.DbSelected,payload:{database_name:e,configuration_method:T.SqlalchemyUri,engine:void 0,engine_information:{supports_file_upload:!0}}});else{const a=null==j?void 0:j.databases.filter((a=>a.name===e))[0],{engine:t,parameters:n,engine_information:l,default_driver:i,sqlalchemy_uri_placeholder:r}=a,o=void 0!==n;Y({type:oa.DbSelected,payload:{database_name:e,engine:t,configuration_method:o?T.DynamicForm:T.SqlalchemyUri,engine_information:l,driver:i,sqlalchemy_uri_placeholder:r}}),t===U.GSheet&&Y({type:oa.AddTableCatalogSheet})}},Ha=()=>{C&&A(C.id),ae(!1),he(!0)},Ra=()=>{ce&&J(!1),Oe&&Re(!1),qa&&(Re(!1),Be(""),Ge([]),Qe([]),We([]),Ze([]),$e({}),Ne({}),ke({}),Te({})),Y({type:oa.Reset}),Le([])},za=()=>x?!Q||ce?(0,$.FD)($.FK,{children:[(0,$.Y)(_e,{onClick:Ra,children:(0,d.t)("Back")},"back"),(0,$.Y)(_e,{buttonStyle:"primary",onClick:Ma,loading:be,children:(0,d.t)("Connect")},"submit")]}):(0,$.FD)($.FK,{children:[(0,$.Y)(_e,{onClick:Ha,children:(0,d.t)("Back")},"back"),(0,$.Y)(_e,{buttonStyle:"primary",onClick:Ma,loading:be,children:(0,d.t)("Finish")},"submit")]}):Oe?(0,$.FD)($.FK,{children:[(0,$.Y)(_e,{onClick:Ra,children:(0,d.t)("Back")},"back"),(0,$.Y)(_e,{buttonStyle:"primary",onClick:Ma,disabled:!!(Pa||ka.length&&!Ue||Ea.length&&"{}"===JSON.stringify(Se)||Ta.length&&"{}"===JSON.stringify(De)||Ua.length&&"{}"===JSON.stringify(Fe)||Ia.length&&"{}"===JSON.stringify(Ee)),loading:be,children:(0,d.t)("Connect")},"submit")]}):(0,$.Y)($.FK,{}),ja=(0,c.useRef)(!0);(0,c.useEffect)((()=>{ja.current?ja.current=!1:Pa||ka.length||Ea.length||Ta.length||Ua.length||Ia.length||be||qa||(Na(),a((0,d.t)("Database connected")))}),[ka,Ea,Pa,qa,Ta,Ua,Ia]),(0,c.useEffect)((()=>{l&&(P("1"),ve(!0),B()),i&&l&&fa&&i&&(w||A(i).catch((a=>e((0,d.t)("Sorry there was an error fetching database information: %s",a.message)))))}),[l,i]),(0,c.useEffect)((()=>{C&&(Y({type:oa.Fetched,payload:C}),de(C.database_name))}),[C]),(0,c.useEffect)((()=>{be&&ve(!1),j&&o&&Oa(o)}),[j]),(0,c.useEffect)((()=>{Oe&&document.getElementsByClassName("ant-upload-list-item-name")[0].scrollIntoView()}),[Oe]),(0,c.useEffect)((()=>{Ge([...Ea])}),[Ea]),(0,c.useEffect)((()=>{Qe([...Ta])}),[Ta]),(0,c.useEffect)((()=>{We([...Ua])}),[Ua]),(0,c.useEffect)((()=>{Ze([...Ia])}),[Ia]),(0,c.useEffect)((()=>{var e;void 0!==(null==x||null==(e=x.parameters)?void 0:e.ssh)&&ua(x.parameters.ssh)}),[null==x||null==(_=x.parameters)?void 0:_.ssh]);const Ba=()=>je?(0,$.Y)(ie,{children:(0,$.Y)(M.A,{errorMessage:je,showDbInstallInstructions:Ve.length>0})}):null,Va=e=>{var a,t;const n=null!=(a=null==(t=e.currentTarget)?void 0:t.value)?a:"";Pe(n.toUpperCase()===(0,d.t)("OVERWRITE"))},Ga=()=>{let e=[];var a;return r()(S)?r()(V)||"GENERIC_DB_ENGINE_ERROR"!==(null==V?void 0:V.error_type)||(e=[(null==V?void 0:V.description)||(null==V?void 0:V.message)]):e="object"==typeof S?Object.values(S):"string"==typeof S?[S]:[],e.length?(0,$.Y)(ia,{children:(0,$.Y)(L.A,{title:(0,d.t)("Database Creation Error"),description:(0,d.t)('We are unable to connect to your database. Click "See more" for database-provided information that may help troubleshoot the issue.'),subtitle:(null==(a=e)?void 0:a[0])||(null==V?void 0:V.description),copyText:null==V?void 0:V.description})}):(0,$.Y)($.FK,{})},Ka=()=>{ve(!0),A(null==C?void 0:C.id).then((e=>{(0,p.SO)(p.Hh.Database,e)}))},Qa=()=>(0,$.Y)(ea,{db:x,onSSHTunnelParametersChange:({target:e})=>{Aa(oa.ParametersSSHTunnelChange,{type:e.type,name:e.name,value:e.value}),$a()},setSSHTunnelLoginMethod:e=>Y({type:oa.SetSSHTunnelLoginMethod,payload:{login_method:e}})}),Ja=()=>(0,$.FD)($.FK,{children:[(0,$.Y)(Me,{isEditMode:fa,db:x,sslForced:!1,dbModel:Ca,onAddTableCatalog:()=>{Y({type:oa.AddTableCatalogSheet})},onQueryChange:({target:e})=>Aa(oa.QueryChange,{name:e.name,value:e.value}),onExtraInputChange:({target:e})=>Aa(oa.ExtraInputChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{Y({type:oa.RemoveTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:Da,onChange:({target:e})=>Aa(oa.TextChange,{name:e.name,value:e.value}),getValidation:()=>G(x),validationErrors:V,getPlaceholder:Sa,clearValidationErrors:$a}),pa&&(0,$.Y)(ra,{children:Qa()})]});if(qe.length>0&&(ka.length||Ve.length||Ke.length||Je.length||Xe.length))return(0,$.FD)(b.A,{centered:!0,css:e=>[Z,ne(e),re(e),oe(e)],footer:za(),maskClosable:!1,name:"database",onHide:Na,onHandledPrimaryAction:Ma,primaryButtonName:(0,d.t)("Connect"),show:l,title:(0,$.Y)("h4",{children:(0,d.t)("Connect a database")}),width:"500px",children:[(0,$.Y)(ze,{db:x,dbName:se,dbModel:Ca,fileList:qe,hasConnectedDb:Q,isEditMode:fa,isLoading:be,useSqlAlchemyForm:_a}),ka.length?(0,$.FD)($.FK,{children:[(0,$.Y)(ie,{children:(0,$.Y)(g.A,{closable:!1,css:e=>(e=>z.AH`
  border: 1px solid ${e.colors.warning.light1};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;
  color: ${e.colors.warning.dark2};

  .ant-alert-message {
    margin: 0;
  }

  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),type:"warning",showIcon:!0,message:"",description:(0,d.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?")})}),(0,$.Y)(q.A,{id:"confirm_overwrite",name:"confirm_overwrite",required:!0,validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.confirm_overwrite,label:(0,d.t)('Type "%s" to confirm',(0,d.t)("OVERWRITE")),onChange:Va,css:te})]}):null,Ba(),Ve.length||Ke.length||Je.length||Xe.length?[...new Set([...Ve,...Ke,...Je,...Xe])].map((e=>(0,$.FD)($.FK,{children:[(0,$.Y)(ie,{children:(0,$.Y)(g.A,{closable:!1,css:e=>le(e),type:"info",showIcon:!0,message:"Database passwords",description:(0,d.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in explore files and should be added manually after the import if they are needed.')})}),(null==Ve?void 0:Ve.indexOf(e))>=0&&(0,$.Y)(q.A,{id:"password_needed",name:"password_needed",required:!0,value:Se[e],onChange:a=>$e({...Se,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.password_needed,label:(0,d.t)("%s PASSWORD",e.slice(10)),css:te}),(null==Ke?void 0:Ke.indexOf(e))>=0&&(0,$.Y)(q.A,{id:"ssh_tunnel_password_needed",name:"ssh_tunnel_password_needed",required:!0,value:De[e],onChange:a=>Ne({...De,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_password_needed,label:(0,d.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),css:te}),(null==Je?void 0:Je.indexOf(e))>=0&&(0,$.Y)(q.A,{id:"ssh_tunnel_private_key_needed",name:"ssh_tunnel_private_key_needed",required:!0,value:Fe[e],onChange:a=>ke({...Fe,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_private_key_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),css:te}),(null==Xe?void 0:Xe.indexOf(e))>=0&&(0,$.Y)(q.A,{id:"ssh_tunnel_private_key_password_needed",name:"ssh_tunnel_private_key_password_needed",required:!0,value:Ee[e],onChange:a=>Te({...Ee,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_private_key_password_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),css:te})]}))):null]});const Wa=fa?(e=>(0,$.FD)($.FK,{children:[(0,$.Y)(_e,{onClick:Na,children:(0,d.t)("Close")},"close"),(0,$.Y)(_e,{buttonStyle:"primary",onClick:Ma,disabled:null==e?void 0:e.is_managed_externally,loading:be,tooltip:null!=e&&e.is_managed_externally?(0,d.t)("This database is managed externally, and can't be edited in Superset"):"",children:(0,d.t)("Finish")},"submit")]}))(x):za();return xa?(0,$.FD)(b.A,{css:e=>[X,Z,ne(e),re(e),oe(e)],name:"database",onHandledPrimaryAction:Ma,onHide:Na,primaryButtonName:fa?(0,d.t)("Save"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,$.Y)("h4",{children:fa?(0,d.t)("Edit database"):(0,d.t)("Connect a database")}),footer:Wa,maskClosable:!1,children:[(0,$.Y)(xe,{children:(0,$.Y)(ge,{children:(0,$.Y)(ze,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:Q,db:x,dbName:se,dbModel:Ca})})}),(0,$.FD)(la,{defaultActiveKey:"1",activeKey:k,onTabClick:e=>P(e),animated:{inkBar:!0,tabPane:!0},children:[(0,$.FD)(u.Ay.TabPane,{tab:(0,$.Y)("span",{children:(0,d.t)("Basic")}),children:[_a?(0,$.FD)(pe,{children:[(0,$.FD)(Ae,{db:x,onInputChange:({target:e})=>Aa(oa.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:ga,testConnection:()=>{var t;if(null==x||!x.sqlalchemy_uri)return void e((0,d.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==x?void 0:x.sqlalchemy_uri)||"",database_name:(null==x||null==(t=x.database_name)?void 0:t.trim())||void 0,impersonate_user:(null==x?void 0:x.impersonate_user)||void 0,extra:null==x?void 0:x.extra,masked_encrypted_extra:(null==x?void 0:x.masked_encrypted_extra)||"",server_cert:(null==x?void 0:x.server_cert)||void 0,ssh_tunnel:!r()(null==x?void 0:x.ssh_tunnel)&&pa?{...x.ssh_tunnel,server_port:Number(x.ssh_tunnel.server_port)}:void 0};Ye(!0),(0,O.ym)(n,(a=>{Ye(!1),e(a)}),(e=>{Ye(!1),a(e)}))},testInProgress:fe,children:[(0,$.Y)(ha,{dbModel:Ca,db:x,changeMethods:{onParametersChange:Da},clearValidationErrors:$a}),pa&&Qa()]}),(Za=(null==x?void 0:x.backend)||(null==x?void 0:x.engine),void 0!==(null==j||null==(et=j.databases)||null==(at=et.find((e=>e.backend===Za||e.engine===Za)))?void 0:at.parameters)&&!fa&&(0,$.FD)("div",{css:e=>ee(e),children:[(0,$.Y)(v.A,{buttonStyle:"link",onClick:()=>Y({type:oa.ConfigMethodChange,payload:{database_name:null==x?void 0:x.database_name,configuration_method:T.DynamicForm,engine:null==x?void 0:x.engine}}),css:e=>(e=>z.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e),children:(0,d.t)("Connect this database using the dynamic form instead")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})]}))]}):Ja(),!fa&&(0,$.Y)(ie,{children:(0,$.Y)(g.A,{closable:!1,css:e=>le(e),message:(0,d.t)("Additional fields may be required"),showIcon:!0,description:(0,$.FD)($.FK,{children:[(0,d.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,$.Y)("a",{href:He,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,d.t)("here")}),"."]}),type:"info"})}),Ya&&Ga()]},"1"),(0,$.Y)(u.Ay.TabPane,{tab:(0,$.Y)("span",{children:(0,d.t)("Advanced")}),children:(0,$.Y)(Ce,{extraExtension:ma,db:x,onInputChange:({target:e})=>Aa(oa.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Aa(oa.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Aa(oa.EditorChange,e),onExtraInputChange:({target:e})=>{Aa(oa.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{Aa(oa.ExtraEditorChange,e)}})},"2")]})]}):(0,$.FD)(b.A,{css:e=>[Z,ne(e),re(e),oe(e)],name:"database",onHandledPrimaryAction:Ma,onHide:Na,primaryButtonName:Q?(0,d.t)("Finish"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,$.Y)("h4",{children:(0,d.t)("Connect a database")}),footer:za(),maskClosable:!1,children:[!be&&Q?(0,$.FD)($.FK,{children:[(0,$.Y)(ze,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:Q,db:x,dbName:se,dbModel:Ca,editNewDb:ce}),W&&(0,$.FD)(da,{children:[(0,$.Y)(v.A,{buttonStyle:"secondary",onClick:()=>{ve(!0),Ka(),Fa("/dataset/add/")},children:(0,d.t)("CREATE DATASET")}),(0,$.Y)(v.A,{buttonStyle:"secondary",onClick:()=>{ve(!0),Ka(),Fa("/sqllab?db=true")},children:(0,d.t)("QUERY DATA IN SQL LAB")})]}),ce?Ja():(0,$.Y)(Ce,{extraExtension:ma,db:x,onInputChange:({target:e})=>Aa(oa.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Aa(oa.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Aa(oa.EditorChange,e),onExtraInputChange:({target:e})=>{Aa(oa.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>Aa(oa.ExtraEditorChange,e)})]}):(0,$.Y)($.FK,{children:!be&&(x?(0,$.FD)($.FK,{children:[(0,$.Y)(ze,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:Q,db:x,dbName:se,dbModel:Ca}),ya&&(()=>{var e,a,t,n,l;const{hostname:i}=window.location;let r=(null==va||null==(e=va.REGIONAL_IPS)?void 0:e.default)||"";const o=(null==va?void 0:va.REGIONAL_IPS)||{};return Object.entries(o).forEach((([e,a])=>{const t=new RegExp(e);i.match(t)&&(r=a)})),(null==x?void 0:x.engine)&&(0,$.Y)(ie,{children:(0,$.Y)(g.A,{closable:!1,css:e=>le(e),type:"info",showIcon:!0,message:(null==(a=na[x.engine])?void 0:a.message)||(null==va||null==(t=va.DEFAULT)?void 0:t.message),description:(null==(n=na[x.engine])?void 0:n.description)||(null==va||null==(l=va.DEFAULT)?void 0:l.description)+r})})})(),Ja(),(0,$.Y)("div",{css:e=>ee(e),children:Ca.engine!==U.GSheet&&(0,$.FD)($.FK,{children:[(0,$.Y)(v.A,{buttonStyle:"link",onClick:()=>Y({type:oa.ConfigMethodChange,payload:{engine:x.engine,configuration_method:T.SqlalchemyUri,database_name:x.database_name}}),css:ue,children:(0,d.t)("Connect this database with a SQLAlchemy URI string instead")}),(0,$.Y)(I.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})]})}),Ya&&Ga()]}):(0,$.FD)(ye,{children:[(0,$.Y)(ze,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:Q,db:x,dbName:se,dbModel:Ca}),(0,$.Y)("div",{className:"preferred",children:null==j||null==(Xa=j.databases)?void 0:Xa.filter((e=>e.preferred)).map((e=>(0,$.Y)(E,{className:"preferred-item",onClick:()=>Oa(e.name),buttonText:e.name,icon:null==ba?void 0:ba[e.engine]},`${e.name}`)))}),(()=>{var e,a;return(0,$.FD)("div",{className:"available",children:[(0,$.Y)("h4",{className:"available-label",children:(0,d.t)("Or choose from a list of other databases we support:")}),(0,$.Y)("div",{className:"control-label",children:(0,d.t)("Supported databases")}),(0,$.FD)(m._P,{className:"available-select",onChange:Oa,placeholder:(0,d.t)("Choose a database..."),showSearch:!0,children:[null==(e=[...(null==j?void 0:j.databases)||[]])?void 0:e.sort(((e,a)=>e.name.localeCompare(a.name))).map(((e,a)=>(0,$.Y)(m._P.Option,{value:e.name,children:e.name},`database-${a}`))),(0,$.Y)(m._P.Option,{value:"Other",children:(0,d.t)("Other")},"Other")]}),(0,$.Y)(g.A,{showIcon:!0,closable:!1,css:e=>le(e),type:"info",message:(null==va||null==(a=va.ADD_DATABASE)?void 0:a.message)||(0,d.t)("Want to add a new database?"),description:null!=va&&va.ADD_DATABASE?(0,$.FD)($.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,$.Y)("a",{href:null==va?void 0:va.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer",children:null==va?void 0:va.ADD_DATABASE.contact_description_link})," ",null==va?void 0:va.ADD_DATABASE.description]}):(0,$.FD)($.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,$.Y)("a",{href:He,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})})]})})(),(0,$.Y)(we,{children:(0,$.Y)(m._O,{name:"databaseFile",id:"databaseFile",accept:".yaml,.json,.yml,.zip",customRequest:()=>{},onChange:async e=>{Be(""),Ge([]),Qe([]),We([]),Ze([]),$e({}),Ne({}),ke({}),Te({}),Re(!0),Le([{...e.file,status:"done"}]),e.file.originFileObj instanceof File&&await La(e.file.originFileObj,Se,De,Fe,Ee,Ue)&&(null==t||t())},onRemove:e=>(Le(qe.filter((a=>a.uid!==e.uid))),!1),children:(0,$.Y)(v.A,{buttonStyle:"link",type:"link",css:me,children:(0,d.t)("Import database from file")})})}),Ba()]}))}),be&&(0,$.Y)(R.A,{})]});var Xa,Za,et,at}))},19980:(e,a,t)=>{t.d(a,{A:()=>H});var n=t(96540),l=t(35742),i=t(51436),r=t(95579),o=t(85861),s=t(46920),d=t(53107),c=t(61693),h=t(15595),p=t(77028),u=t(90868),m=t(58561),g=t.n(m),b=t(5261),v=t(40563),f=t(96453),y=t(17437);const _=(0,f.I4)(v.eI)`
  ${({theme:e})=>y.AH`
    flex: 1;
    margin-top: 0;
    margin-bottom: ${2.5*e.gridUnit}px;
  }
  `}
`,x=f.I4.div`
  display: flex;
  align-items: center;
  margin-top: 0;
`,Y=y.AH`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,w=e=>y.AH`
  .switch-label {
    color: ${e.colors.grayscale.base};
    margin-left: ${4*e.gridUnit}px;
  }
`,C=e=>y.AH`
  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }

  .info-solid-small {
    vertical-align: bottom;
  }
`;var S=t(46740),A=t(2445);const $=f.I4.div`
  //margin-top: 10px;
  //margin-bottom: 10px;
`,D=({columns:e,maxColumnsToShow:a=4})=>{const t=e.map((e=>({name:e})));return(0,A.FD)($,{children:[(0,A.Y)(h.o5.Text,{type:"secondary",children:"Columns:"}),0===e.length?(0,A.Y)("p",{className:"help-block",children:(0,r.t)("Upload file to preview columns")}):(0,A.Y)(S.A,{tags:t,maxTags:a})]})};var N=t(31641);const F=({label:e,tip:a,children:t,name:n,rules:l})=>(0,A.Y)(_,{label:(0,A.FD)("div",{children:[e,(0,A.Y)(N.A,{tooltip:a})]}),name:n,rules:l,children:t}),k=["delimiter","skip_initial_space","skip_blank_lines","day_first","column_data_types","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],E=["sheet_name","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],T=[],U=["rows_to_read","index_column"],I=[...k,...E,...T],P={csv:k,excel:E,columnar:T},q=(e,a)=>P[a].includes(e),L={table_name:"",schema:"",sheet_name:void 0,delimiter:",",already_exists:"fail",skip_initial_space:!1,skip_blank_lines:!1,day_first:!1,decimal_character:".",null_values:[],header_row:"0",rows_to_read:null,skip_rows:"0",column_dates:[],index_column:null,dataframe_index:!1,index_label:"",columns_read:[],column_data_types:""},M={csv:".csv, .tsv",excel:".xls, .xlsx",columnar:".parquet, .zip"},O=({label:e,dataTest:a,children:t,...n})=>(0,A.FD)(x,{children:[(0,A.Y)(d.d,{...n}),(0,A.Y)("div",{className:"switch-label",children:e}),t]}),H=(0,b.Ay)((({addDangerToast:e,addSuccessToast:a,onHide:t,show:d,allowedExtensions:m,type:b="csv"})=>{const[v]=h.Wq.useForm(),[f,x]=(0,n.useState)(0),[S,$]=(0,n.useState)([]),[N,k]=(0,n.useState)([]),[E,T]=(0,n.useState)([]),[H,R]=(0,n.useState)([]),[z,j]=(0,n.useState)(","),[B,V]=(0,n.useState)(!1),[G,K]=(0,n.useState)(),[Q,J]=(0,n.useState)(!1),[W,X]=(0,n.useState)(!0),[Z,ee]=(0,n.useState)(!1),ae={csv:"/api/v1/database/csv_metadata/",excel:"/api/v1/database/excel_metadata/",columnar:"/api/v1/database/columnar_metadata/"},te=(0,n.useMemo)((()=>(e="",a,t)=>{const n=g().encode_uri({filters:[{col:"allow_file_upload",opr:"eq",value:!0}],page:a,page_size:t});return l.A.get({endpoint:`/api/v1/database/?q=${n}`}).then((e=>({data:e.json.result.map((e=>({value:e.id,label:e.database_name}))),totalCount:e.json.count})))}),[]),ne=(0,n.useMemo)((()=>(e="",a,t)=>f?l.A.get({endpoint:`/api/v1/database/${f}/schemas/`}).then((e=>({data:e.json.result.map((e=>({value:e,label:e}))),totalCount:e.json.count}))):Promise.resolve({data:[],totalCount:0})),[f]),le=a=>{const t=v.getFieldsValue(),n={...L,...t},r=new FormData;return r.append("file",a),"csv"===b&&r.append("delimiter",n.delimiter),ee(!0),l.A.post({endpoint:ae[b],body:r,headers:{Accept:"application/json"}}).then((e=>{const{items:a}=e.json.result;if(a&&"excel"!==b)k(a[0].column_names);else{const{allSheetNames:e,sheetColumnNamesMap:t}=a.reduce(((e,a)=>(e.allSheetNames.push(a.sheet_name),e.sheetColumnNamesMap[a.sheet_name]=a.column_names,e)),{allSheetNames:[],sheetColumnNamesMap:{}});k(a[0].column_names),T(e),v.setFieldsValue({sheet_name:e[0]}),R(t)}})).catch((a=>(0,i.h4)(a).then((a=>{e(a.error||"Error"),k([]),v.setFieldsValue({sheet_name:void 0}),T([])})))).finally((()=>{ee(!1)}))},ie=()=>{$([]),k([]),K(""),x(0),T([]),V(!1),j(","),X(!0),ee(!1),R([]),v.resetFields(),t()},re=()=>N.map((e=>({value:e,label:e})));(0,n.useEffect)((()=>{if(N.length>0&&S[0].originFileObj&&S[0].originFileObj instanceof File){if(!W)return;le(S[0].originFileObj).then((e=>e))}}),[z]);const oe={csv:(0,r.t)("CSV Upload"),excel:(0,r.t)("Excel Upload"),columnar:(0,r.t)("Columnar Upload")};return(0,A.Y)(o.A,{css:e=>[Y,C(e),w(e)],primaryButtonLoading:B,name:"database",onHandledPrimaryAction:v.submit,onHide:ie,width:"500px",primaryButtonName:"Upload",centered:!0,show:d,title:(0,A.Y)((()=>{const e=oe[b]||(0,r.t)("Upload");return(0,A.Y)("h4",{children:e})}),{}),children:(0,A.Y)(h.Wq,{form:v,onFinish:()=>{var t;const n=v.getFieldsValue();delete n.database,n.schema=G;const o={...L,...n},s=new FormData,d=null==(t=S[0])?void 0:t.originFileObj;d&&s.append("file",d),((e,a)=>{const t=(()=>{const e=P[b]||[];return[...I].filter((a=>!e.includes(a)))})();Object.entries(a).forEach((([a,n])=>{t.includes(a)||U.includes(a)&&null==n||e.append(a,n)}))})(s,o),V(!0);const c=(h=f,{csv:`/api/v1/database/${h}/csv_upload/`,excel:`/api/v1/database/${h}/excel_upload/`,columnar:`/api/v1/database/${h}/columnar_upload/`})[b];var h;return l.A.post({endpoint:c,body:s,headers:{Accept:"application/json"}}).then((()=>{a((0,r.t)("Data Imported")),V(!1),ie()})).catch((a=>(0,i.h4)(a).then((a=>{e(a.error||"Error")})))).finally((()=>{V(!1)}))},layout:"vertical",initialValues:L,children:(0,A.FD)(c.A,{expandIconPosition:"right",accordion:!0,defaultActiveKey:"general",css:e=>(e=>y.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;
    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.s}px;
    }
  }
  h4 {
    font-size: ${e.typography.sizes.l}px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,r.t)("General information")}),(0,A.Y)("p",{className:"helper",children:(0,r.t)("Upload a file to a database.")})]}),children:[(0,A.FD)(h.fI,{children:[(0,A.Y)(h.fv,{span:12,children:(0,A.Y)(_,{label:(0,r.t)("%(type)s File",{type:b}),name:"file",required:!0,rules:[{validator:(e,a)=>0===S.length?Promise.reject((0,r.t)("Uploading a file is required")):((e,a)=>{const t=e.name.match(/.+\.([^.]+)$/);if(!t)return!1;const n=t[1];return a.includes(n)})(S[0],m)?Promise.resolve():Promise.reject((0,r.t)("Upload a file with a valid extension. Valid: [%s]",m.join(",")))}],children:(0,A.Y)(h._O,{name:"modelFile",id:"modelFile",accept:M[b],fileList:S,onChange:async e=>{$([{...e.file,status:"done"}]),W&&await le(e.file.originFileObj)},onRemove:e=>($(S.filter((a=>a.uid!==e.uid))),k([]),T([]),v.setFieldsValue({sheet_name:void 0}),!1),customRequest:()=>{},children:(0,A.Y)(s.A,{"aria-label":(0,r.t)("Select"),icon:(0,A.Y)(p.A,{}),loading:Z,children:(0,r.t)("Select")})})})}),(0,A.Y)(h.fv,{span:12,children:(0,A.Y)(_,{children:(0,A.Y)(O,{label:(0,r.t)("Preview uploaded file"),dataTest:"previewUploadedFile",onChange:e=>{X(e)},checked:W})})})]}),W&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(D,{columns:N})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Database"),required:!0,name:"database",rules:[{validator:(e,a)=>f?Promise.resolve():Promise.reject((0,r.t)("Selecting a database is required"))}],children:(0,A.Y)(h.DW,{ariaLabel:(0,r.t)("Select a database"),options:te,onChange:e=>{x(null==e?void 0:e.value),K(void 0),v.setFieldsValue({schema:void 0})},allowClear:!0,placeholder:(0,r.t)("Select a database to upload the file to")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Schema"),name:"schema",children:(0,A.Y)(h.DW,{ariaLabel:(0,r.t)("Select a schema"),options:ne,onChange:e=>{K(null==e?void 0:e.value)},allowClear:!0,placeholder:(0,r.t)("Select a schema if the database supports this")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Table Name"),name:"table_name",required:!0,rules:[{required:!0,message:"Table name is required"}],children:(0,A.Y)(u.pd,{"aria-label":(0,r.t)("Table Name"),name:"table_name",type:"text",placeholder:(0,r.t)("Name of table to be created")})})})}),q("delimiter",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Delimiter"),tip:(0,r.t)("Select a delimiter for this data"),name:"delimiter",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose a delimiter"),options:[{value:",",label:'Comma ","'},{value:";",label:'Semicolon ";"'},{value:"\t",label:'Tab "\\t"'},{value:"|",label:"Pipe"}],onChange:e=>{j(e)},allowNewOptions:!0})})})}),q("sheet_name",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Sheet name"),name:"sheet_name",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose sheet name"),options:E.map((e=>({value:e,label:e}))),onChange:e=>{var a;k(null!=(a=H[e])?a:[])},allowNewOptions:!0,placeholder:(0,r.t)("Select a sheet name from the uploaded file")})})})})]},"general"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,r.t)("File Settings")}),(0,A.Y)("p",{className:"helper",children:(0,r.t)("Adjust how spaces, blank lines, null values are handled and other file wide settings.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("If Table Already Exists"),tip:(0,r.t)("What should happen if the table already exists"),name:"already_exists",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose already exists"),options:[{value:"fail",label:"Fail"},{value:"replace",label:"Replace"},{value:"append",label:"Append"}],onChange:()=>{}})})})}),q("column_dates",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Columns To Be Parsed as Dates"),name:"column_dates",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose columns to be parsed as dates"),mode:"multiple",options:re(),allowClear:!0,allowNewOptions:!0,placeholder:(0,r.t)("A comma separated list of columns that should be parsed as dates")})})})}),q("decimal_character",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Decimal Character"),tip:(0,r.t)("Character to interpret as decimal point"),name:"decimal_character",children:(0,A.Y)(u.pd,{type:"text"})})})}),q("null_values",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Null Values"),tip:(0,r.t)("Choose values that should be treated as null. Warning: Hive database supports only a single value"),name:"null_values",children:(0,A.Y)(h.l6,{mode:"multiple",options:[{value:'""',label:'Empty Strings ""'},{value:"None",label:"None"},{value:"nan",label:"nan"},{value:"null",label:"null"},{value:"N/A",label:"N/A"}],allowClear:!0,allowNewOptions:!0})})})}),q("skip_initial_space",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_initial_space",children:(0,A.Y)(O,{label:(0,r.t)("Skip spaces after delimiter"),dataTest:"skipInitialSpace"})})})}),q("skip_blank_lines",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_blank_lines",children:(0,A.Y)(O,{label:(0,r.t)("Skip blank lines rather than interpreting them as Not A Number values"),dataTest:"skipBlankLines"})})})}),q("day_first",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"day_first",children:(0,A.Y)(O,{label:(0,r.t)("DD/MM format dates, international and European format"),dataTest:"dayFirst"})})})})]},"2"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,r.t)("Columns")}),(0,A.Y)("p",{className:"helper",children:(0,r.t)("Adjust column settings such as specifying the columns to read, how duplicates are handled, column data types, and more.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,r.t)("Columns To Read"),name:"columns_read",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose columns to read"),mode:"multiple",options:re(),allowClear:!0,allowNewOptions:!0,placeholder:(0,r.t)("List of the column names that should be read")})})})}),q("column_data_types",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Column Data Types"),tip:(0,r.t)('A dictionary with column names and their data types if you need to change the defaults. Example: {"user_id":"int"}. Check Python\'s Pandas library for supported data types.'),name:"column_data_types",children:(0,A.Y)(u.pd,{"aria-label":(0,r.t)("Column data types"),type:"text"})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"dataframe_index",children:(0,A.Y)(O,{label:(0,r.t)("Create dataframe index"),dataTest:"dataFrameIndex",onChange:J})})})}),Q&&q("index_column",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Index Column"),tip:(0,r.t)("Column to use as the index of the dataframe. If None is given, Index label is used."),name:"index_column",children:(0,A.Y)(h.l6,{ariaLabel:(0,r.t)("Choose index column"),options:N.map((e=>({value:e,label:e}))),allowClear:!0,allowNewOptions:!0})})})}),Q&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{label:(0,r.t)("Index Label"),tip:(0,r.t)("Label for the index column. Don't use an existing column name."),name:"index_label",children:(0,A.Y)(u.pd,{"aria-label":(0,r.t)("Index label"),type:"text"})})})})]},"3"),q("header_row",b)&&q("rows_to_read",b)&&q("skip_rows",b)&&(0,A.Y)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,r.t)("Rows")}),(0,A.Y)("p",{className:"helper",children:(0,r.t)("Set header rows and the number of rows to read or skip.")})]}),children:(0,A.FD)(h.fI,{children:[(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(F,{label:(0,r.t)("Header Row"),tip:(0,r.t)("Row containing the headers to use as column names (0 is first line of data)."),name:"header_row",rules:[{required:!0,message:"Header row is required"}],children:(0,A.Y)(u.YI,{"aria-label":(0,r.t)("Header row"),type:"text",min:0})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(F,{label:(0,r.t)("Rows to Read"),tip:(0,r.t)("Number of rows of file to read. Leave empty (default) to read all rows"),name:"rows_to_read",children:(0,A.Y)(u.YI,{"aria-label":(0,r.t)("Rows to read"),min:1})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(F,{label:(0,r.t)("Skip Rows"),tip:(0,r.t)("Number of rows to skip at start of file."),name:"skip_rows",rules:[{required:!0,message:"Skip rows is required"}],children:(0,A.Y)(u.YI,{"aria-label":(0,r.t)("Skip rows"),min:0})})})]})},"4")]})})})}))},82741:(e,a,t)=>{t.d(a,{A:()=>ie});var n=t(38221),l=t.n(n),i=t(96540),r=t(96453),o=t(17437),s=t(32132),d=t(15595),c=t(6749),h=t(19129),p=t(61574),u=t(71519),m=t(78532),g=t(12249),b=t(35837),v=t(27023),f=t(62193),y=t.n(f),_=t(58561),x=t.n(_),Y=t(61225),w=t(33231),C=t(72391),S=t(95579),A=t(35742),$=t(2738),D=t(84666),N=t(65256),F=t(16817),k=t(19980),E=t(30703),T=t(2445);const U=({version:e="unknownVersion",sha:a="unknownSHA",build:t="unknownBuild"})=>{const n=`https://apachesuperset.gateway.scarf.sh/pixel/0d3461e1-abb1-4691-a0aa-5ed50de66af0/${e}/${a}/${t}`;return(0,T.Y)("img",{referrerPolicy:"no-referrer-when-downgrade",src:n,width:0,height:0,alt:""})},{SubMenu:I}=c.NG,P=r.I4.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,q=r.I4.i`
  margin-top: 2px;
`;function L(e){const{locale:a,languages:t,...n}=e;return(0,T.Y)(I,{"aria-label":"Languages",title:(0,T.Y)("div",{className:"f16",children:(0,T.Y)(q,{className:`flag ${t[a].flag}`})}),icon:(0,T.Y)(g.A.TriangleDown,{}),...n,children:Object.keys(t).map((e=>(0,T.Y)(c.NG.Item,{style:{whiteSpace:"normal",height:"auto"},children:(0,T.FD)(P,{className:"f16",children:[(0,T.Y)("i",{className:`flag ${t[e].flag}`}),(0,T.Y)("a",{href:t[e].url,children:t[e].name})]})},e)))})}var M=t(3139);const O=(0,C.a)(),H=e=>o.AH`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,R=r.I4.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
`,z=e=>o.AH`
  color: ${e.colors.grayscale.light1};
  .ant-menu-item-active {
    color: ${e.colors.grayscale.light1};
    cursor: default;
  }
`,j=r.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
  .ant-menu-submenu-title > svg {
    top: ${({theme:e})=>5.25*e.gridUnit}px;
  }
`,B=r.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`,V=r.I4.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,G=e=>o.AH`
  color: ${e.colors.grayscale.light5};
`,K=e=>o.AH`
  &:hover {
    color: ${e.colors.primary.base} !important;
    cursor: pointer !important;
  }
`,{SubMenu:Q}=c.NG,J=({align:e,settings:a,navbarRight:t,isFrontendRoute:n,environmentTag:l,setQuery:s})=>{const d=(0,Y.d4)((e=>e.user)),p=(0,Y.d4)((e=>{var a;return null==(a=e.dashboardInfo)?void 0:a.id})),m=d||{},{roles:b}=m,{CSV_EXTENSIONS:v,COLUMNAR_EXTENSIONS:f,EXCEL_EXTENSIONS:_,ALLOWED_EXTENSIONS:w,HAS_GSHEETS_INSTALLED:C}=(0,Y.d4)((e=>e.common.conf)),[I,P]=(0,i.useState)(!1),[q,J]=(0,i.useState)(!1),[W,X]=(0,i.useState)(!1),[Z,ee]=(0,i.useState)(!1),[ae,te]=(0,i.useState)(""),ne=(0,D.L)("can_sqllab","Superset",b),le=(0,D.L)("can_write","Dashboard",b),ie=(0,D.L)("can_write","Chart",b),re=(0,D.L)("can_write","Database",b),oe=(0,D.L)("can_write","Dataset",b),{canUploadData:se,canUploadCSV:de,canUploadColumnar:ce,canUploadExcel:he}=(0,E.c8)(b,v,f,_,w),pe=ne||ie||le,[ue,me]=(0,i.useState)(!1),[ge,be]=(0,i.useState)(!1),ve=(0,N.N6)(d),fe=ue||ve,ye=[{label:(0,S.t)("Data"),icon:"fa-database",childs:[{label:(0,S.t)("Connect database"),name:M.$.DbConnection,perm:re&&!ge},{label:(0,S.t)("Create dataset"),name:M.$.DatasetCreation,url:"/dataset/add/",perm:oe&&ge},{label:(0,S.t)("Connect Google Sheet"),name:M.$.GoogleSheets,perm:re&&C},{label:(0,S.t)("Upload CSV to database"),name:M.$.CSVUpload,perm:de&&fe,disable:ve&&!ue},{label:(0,S.t)("Upload Excel to database"),name:M.$.ExcelUpload,perm:he&&fe,disable:ve&&!ue},{label:(0,S.t)("Upload Columnar file to database"),name:M.$.ColumnarUpload,perm:ce&&fe,disable:ve&&!ue}]},{label:(0,S.t)("SQL query"),url:"/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,S.t)("Chart"),url:Number.isInteger(p)?`/chart/add?dashboard_id=${p}`:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,S.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],_e=()=>{A.A.get({endpoint:`/api/v1/database/?q=${x().encode({filters:[{col:"allow_file_upload",opr:"upload_is_enabled",value:!0}]})}`}).then((({json:e})=>{var a;const t=(null==e||null==(a=e.result)?void 0:a.filter((e=>{var a;return null==e||null==(a=e.engine_information)?void 0:a.supports_file_upload})))||[];me((null==t?void 0:t.length)>=1)}))},xe=()=>{A.A.get({endpoint:`/api/v1/database/?q=${x().encode({filters:[{col:"database_name",opr:"neq",value:"examples"}]})}`}).then((({json:e})=>{be(e.count>=1)}))};(0,i.useEffect)((()=>{se&&_e()}),[se]),(0,i.useEffect)((()=>{(re||oe)&&xe()}),[re,oe]);const Ye=e=>(0,T.FD)(T.FK,{children:[(0,T.Y)("i",{className:`fa ${e.icon}`}),e.label]}),we=(0,S.t)("Enable 'Allow file uploads to database' in any database's settings"),Ce=e=>e.disable?(0,T.Y)(c.NG.Item,{css:z,children:(0,T.Y)(h.m,{placement:"top",title:we,children:e.label})},e.name):(0,T.Y)(c.NG.Item,{css:K,children:e.url?(0,T.FD)("a",{href:e.url,children:[" ",e.label," "]}):e.label},e.name),Se=O.get("navbar.right"),Ae=O.get("navbar.right-menu.item.icon"),$e=(0,r.DP)();return(0,T.FD)(j,{align:e,children:[re&&(0,T.Y)(F.Ay,{onHide:()=>{te(""),P(!1)},show:I,dbEngine:ae,onDatabaseAdd:()=>s({databaseAdded:!0})}),de&&(0,T.Y)(k.A,{onHide:()=>J(!1),show:q,allowedExtensions:v,type:"csv"}),he&&(0,T.Y)(k.A,{onHide:()=>X(!1),show:W,allowedExtensions:_,type:"excel"}),ce&&(0,T.Y)(k.A,{onHide:()=>ee(!1),show:Z,allowedExtensions:f,type:"columnar"}),(null==l?void 0:l.text)&&(0,T.Y)($.A,{css:(0,o.AH)({borderRadius:125*$e.gridUnit+"px"},"",""),color:/^#(?:[0-9a-f]{3}){1,2}$/i.test(l.color)?l.color:l.color.split(".").reduce(((e,a)=>e[a]),$e.colors),children:(0,T.Y)("span",{css:G,children:l.text})}),(0,T.FD)(c.NG,{selectable:!1,mode:"horizontal",onClick:e=>{e.key===M.$.DbConnection?P(!0):e.key===M.$.GoogleSheets?(P(!0),te("Google Sheets")):e.key===M.$.CSVUpload?J(!0):e.key===M.$.ExcelUpload?X(!0):e.key===M.$.ColumnarUpload&&ee(!0)},onOpenChange:e=>(e.length>1&&!y()(null==e?void 0:e.filter((e=>{var a;return e.includes(`sub2_${null==ye||null==(a=ye[0])?void 0:a.label}`)})))&&(se&&_e(),(re||oe)&&xe()),null),children:[Se&&(0,T.Y)(Se,{}),!t.user_is_anonymous&&pe&&(0,T.Y)(Q,{title:(0,T.Y)(R,{className:"fa fa-plus"}),icon:(0,T.Y)(g.A.TriangleDown,{}),children:null==ye||null==ye.map?void 0:ye.map((e=>{var a;const t=null==(a=e.childs)?void 0:a.some((e=>"object"==typeof e&&!!e.perm));if(e.childs){var l;if(t)return(0,T.Y)(Q,{className:"data-menu",title:Ye(e),children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map(((e,a)=>"string"!=typeof e&&e.name&&e.perm?(0,T.FD)(i.Fragment,{children:[3===a&&(0,T.Y)(c.NG.Divider,{}),Ce(e)]},e.name):null))},`sub2_${e.label}`);if(!e.url)return null}return(0,D.L)(e.perm,e.view,b)&&(0,T.Y)(c.NG.Item,{children:n(e.url)?(0,T.FD)(u.N_,{to:e.url||"",children:[(0,T.Y)("i",{className:`fa ${e.icon}`})," ",e.label]}):(0,T.FD)("a",{href:e.url,children:[(0,T.Y)("i",{className:`fa ${e.icon}`})," ",e.label]})},e.label)}))}),(0,T.FD)(Q,{title:(0,S.t)("Settings"),icon:(0,T.Y)(g.A.TriangleDown,{iconSize:"xl"}),children:[null==a||null==a.map?void 0:a.map(((e,t)=>{var l;return[(0,T.Y)(c.NG.ItemGroup,{title:e.label,children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map((e=>{if("string"!=typeof e){const a=Ae?(0,T.FD)(B,{children:[e.label,(0,T.Y)(Ae,{menuChild:e})]}):e.label;return(0,T.Y)(c.NG.Item,{children:n(e.url)?(0,T.Y)(u.N_,{to:e.url||"",children:a}):(0,T.Y)("a",{href:e.url,children:a})},`${e.label}`)}return null}))},`${e.label}`),t<a.length-1&&(0,T.Y)(c.NG.Divider,{},`divider_${t}`)]})),!t.user_is_anonymous&&[(0,T.Y)(c.NG.Divider,{},"user-divider"),(0,T.FD)(c.NG.ItemGroup,{title:(0,S.t)("User"),children:[t.user_info_url&&(0,T.Y)(c.NG.Item,{children:(0,T.Y)("a",{href:t.user_info_url,children:(0,S.t)("Info")})},"info"),(0,T.Y)(c.NG.Item,{onClick:()=>{localStorage.removeItem("redux")},children:(0,T.Y)("a",{href:t.user_logout_url,children:(0,S.t)("Logout")})},"logout")]},"user-section")],(t.version_string||t.version_sha)&&[(0,T.Y)(c.NG.Divider,{},"version-info-divider"),(0,T.Y)(c.NG.ItemGroup,{title:(0,S.t)("About"),children:(0,T.FD)("div",{className:"about-section",children:[t.show_watermark&&(0,T.Y)("div",{css:H,children:(0,S.t)("Powered by Apache Superset")}),t.version_string&&(0,T.FD)("div",{css:H,children:[(0,S.t)("Version"),": ",t.version_string]}),t.version_sha&&(0,T.FD)("div",{css:H,children:[(0,S.t)("SHA"),": ",t.version_sha]}),t.build_number&&(0,T.FD)("div",{css:H,children:[(0,S.t)("Build"),": ",t.build_number]})]})},"about-section")]]}),t.show_language_picker&&(0,T.Y)(L,{locale:t.locale,languages:t.languages})]}),t.documentation_url&&(0,T.FD)(T.FK,{children:[(0,T.Y)(V,{href:t.documentation_url,target:"_blank",rel:"noreferrer",title:t.documentation_text||(0,S.t)("Documentation"),children:t.documentation_icon?(0,T.Y)("i",{className:t.documentation_icon}):(0,T.Y)("i",{className:"fa fa-question"})}),(0,T.Y)("span",{children:" "})]}),t.bug_report_url&&(0,T.FD)(T.FK,{children:[(0,T.Y)(V,{href:t.bug_report_url,target:"_blank",rel:"noreferrer",title:t.bug_report_text||(0,S.t)("Report a bug"),children:t.bug_report_icon?(0,T.Y)("i",{className:t.bug_report_icon}):(0,T.Y)("i",{className:"fa fa-bug"})}),(0,T.Y)("span",{children:" "})]}),t.user_is_anonymous&&(0,T.FD)(V,{href:t.user_login_url,children:[(0,T.Y)("i",{className:"fa fa-fw fa-sign-in"}),(0,S.t)("Login")]}),(0,T.Y)(U,{version:t.version_string,sha:t.version_sha,build:t.build_number})]})},W=e=>{const[,a]=(0,w.sq)({databaseAdded:w.sJ,datasetAdded:w.sJ});return(0,T.Y)(J,{setQuery:a,...e})};class X extends i.PureComponent{constructor(...e){super(...e),this.state={hasError:!1},this.noop=()=>{}}static getDerivedStateFromError(){return{hasError:!0}}render(){return this.state.hasError?(0,T.Y)(J,{setQuery:this.noop,...this.props}):this.props.children}}const Z=e=>(0,T.Y)(X,{...e,children:(0,T.Y)(W,{...e})}),ee=r.I4.header`
  ${({theme:e})=>`\n      background-color: ${e.colors.grayscale.light5};\n      margin-bottom: 2px;\n      z-index: 10;\n\n      &:nth-last-of-type(2) nav {\n        margin-bottom: 2px;\n      }\n      .caret {\n        display: none;\n      }\n      .navbar-brand {\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        /* must be exactly the height of the Antd navbar */\n        min-height: 50px;\n        padding: ${e.gridUnit}px\n          ${2*e.gridUnit}px\n          ${e.gridUnit}px\n          ${4*e.gridUnit}px;\n        max-width: ${e.gridUnit*e.brandIconMaxWidth}px;\n        img {\n          height: 100%;\n          object-fit: contain;\n        }\n      }\n      .navbar-brand-text {\n        border-left: 1px solid ${e.colors.grayscale.light2};\n        border-right: 1px solid ${e.colors.grayscale.light2};\n        height: 100%;\n        color: ${e.colors.grayscale.dark1};\n        padding-left: ${4*e.gridUnit}px;\n        padding-right: ${4*e.gridUnit}px;\n        margin-right: ${6*e.gridUnit}px;\n        font-size: ${4*e.gridUnit}px;\n        float: left;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n\n        span {\n          max-width: ${58*e.gridUnit}px;\n          white-space: nowrap;\n          overflow: hidden;\n          text-overflow: ellipsis;\n        }\n        @media (max-width: 1127px) {\n          display: none;\n        }\n      }\n      .main-nav .ant-menu-submenu-title > svg {\n        top: ${5.25*e.gridUnit}px;\n      }\n      @media (max-width: 767px) {\n        .navbar-brand {\n          float: none;\n        }\n      }\n      .ant-menu-horizontal .ant-menu-item {\n        height: 100%;\n        line-height: inherit;\n      }\n      .ant-menu > .ant-menu-item > a {\n        padding: ${4*e.gridUnit}px;\n      }\n      @media (max-width: 767px) {\n        .ant-menu-item {\n          padding: 0 ${6*e.gridUnit}px 0\n            ${3*e.gridUnit}px !important;\n        }\n        .ant-menu > .ant-menu-item > a {\n          padding: 0px;\n        }\n        .main-nav .ant-menu-submenu-title > svg:nth-of-type(1) {\n          display: none;\n        }\n        .ant-menu-item-active > a {\n          &:hover {\n            color: ${e.colors.primary.base} !important;\n            background-color: transparent !important;\n          }\n        }\n      }\n      .ant-menu-item a {\n        &:hover {\n          color: ${e.colors.grayscale.dark1};\n          background-color: ${e.colors.primary.light5};\n          border-bottom: none;\n          margin: 0;\n          &:after {\n            opacity: 1;\n            width: 100%;\n          }\n        }\n      }\n  `}
`,ae=e=>o.AH`
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light.ant-menu-submenu-placement-bottomLeft {
    border-radius: 0px;
  }
  .ant-menu-submenu.ant-menu-submenu-popup.ant-menu.ant-menu-light {
    border-radius: 0px;
  }
  .ant-menu-vertical > .ant-menu-submenu.data-menu > .ant-menu-submenu-title {
    height: 28px;
    i {
      padding-right: ${2*e.gridUnit}px;
      margin-left: ${1.75*e.gridUnit}px;
    }
  }
  .ant-menu-item-selected {
    background-color: transparent;
    &:not(.ant-menu-item-active) {
      color: inherit;
      border-bottom-color: transparent;
      & > a {
        color: inherit;
      }
    }
  }
  .ant-menu-horizontal > .ant-menu-item:has(> .is-active) {
    color: ${e.colors.primary.base};
    border-bottom-color: ${e.colors.primary.base};
    & > a {
      color: ${e.colors.primary.base};
    }
  }
  .ant-menu-vertical > .ant-menu-item:has(> .is-active) {
    background-color: ${e.colors.primary.light5};
    & > a {
      color: ${e.colors.primary.base};
    }
  }
`,{SubMenu:te}=c.NG,{useBreakpoint:ne}=d.xA;function le({data:{menu:e,brand:a,navbar_right:t,settings:n,environment_tag:f},isFrontendRoute:y=(()=>!1)}){const[_,x]=(0,i.useState)("horizontal"),Y=ne(),w=(0,b.Q1)(),C=(0,r.DP)();let S;(0,i.useEffect)((()=>{function e(){window.innerWidth<=767?x("inline"):x("horizontal")}e();const a=l()((()=>e()),10);return window.addEventListener("resize",a),()=>window.removeEventListener("resize",a)}),[]),function(e){e.Explore="/explore",e.Dashboard="/dashboard",e.Chart="/chart",e.Datasets="/tablemodelview"}(S||(S={}));const A=[],[$,D]=(0,i.useState)(A),N=(0,p.zy)();return(0,i.useEffect)((()=>{const e=N.pathname;switch(!0){case e.startsWith(S.Dashboard):D(["Dashboards"]);break;case e.startsWith(S.Chart)||e.startsWith(S.Explore):D(["Charts"]);break;case e.startsWith(S.Datasets):D(["Datasets"]);break;default:D(A)}}),[N.pathname]),(0,s.P3)(v.vX.standalone)||w.hideNav?(0,T.Y)(T.FK,{}):(0,T.FD)(ee,{className:"top",id:"main-menu",role:"navigation",children:[(0,T.Y)(o.mL,{styles:ae(C)}),(0,T.FD)(d.fI,{children:[(0,T.FD)(d.fv,{md:16,xs:24,children:[(0,T.Y)(h.m,{id:"brand-tooltip",placement:"bottomLeft",title:a.tooltip,arrowPointAtCenter:!0,children:y(window.location.pathname)?(0,T.Y)(m.K,{className:"navbar-brand",to:a.path,tabIndex:-1,children:(0,T.Y)("img",{src:a.icon,alt:a.alt})}):(0,T.Y)("a",{className:"navbar-brand",href:a.path,tabIndex:-1,children:(0,T.Y)("img",{src:a.icon,alt:a.alt})})}),a.text&&(0,T.Y)("div",{className:"navbar-brand-text",children:(0,T.Y)("span",{children:a.text})}),(0,T.Y)(c.NG,{mode:_,className:"main-nav",selectedKeys:$,children:e.map(((e,a)=>{var t;return(({label:e,childs:a,url:t,index:n,isFrontendRoute:l})=>t&&l?(0,T.Y)(c.NG.Item,{role:"presentation",children:(0,T.Y)(u.k2,{role:"button",to:t,activeClassName:"is-active",children:e})},e):t?(0,T.Y)(c.NG.Item,{children:(0,T.Y)("a",{href:t,children:e})},e):(0,T.Y)(te,{title:e,icon:"inline"===_?(0,T.Y)(T.FK,{}):(0,T.Y)(g.A.TriangleDown,{}),children:null==a?void 0:a.map(((a,t)=>"string"==typeof a&&"-"===a&&"Data"!==e?(0,T.Y)(c.NG.Divider,{},`$${t}`):"string"!=typeof a?(0,T.Y)(c.NG.Item,{children:a.isFrontendRoute?(0,T.Y)(u.k2,{to:a.url||"",exact:!0,activeClassName:"is-active",children:a.label}):(0,T.Y)("a",{href:a.url,children:a.label})},`${a.label}`):null))},n))({index:a,...e,isFrontendRoute:y(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:y(e.url)}))})}))})]}),(0,T.Y)(d.fv,{md:8,xs:24,children:(0,T.Y)(Z,{align:Y.md?"flex-end":"flex-start",settings:n,navbarRight:t,isFrontendRoute:y,environmentTag:f})})]})]})}function ie({data:e,...a}){const t={...e},n={Data:!0,Security:!0,Manage:!0},l=[],i=[];return t.menu.forEach((e=>{if(!e)return;const a=[],t={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&a.push(e)})),t.childs=a),n.hasOwnProperty(e.name)?i.push(t):l.push(t)})),t.menu=l,t.settings=i,(0,T.Y)(le,{data:t,...a})}},62221:(e,a,t)=>{var n;function l(e,a){try{const t=localStorage.getItem(e);return null===t?a:JSON.parse(t)}catch{return a}}function i(e,a){try{localStorage.setItem(e,JSON.stringify(a))}catch{}}function r(e,a){return l(e,a)}function o(e,a){i(e,a)}t.d(a,{Gq:()=>r,Hh:()=>n,SO:()=>o,SX:()=>l,Wr:()=>i}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.SqllabIsRenderHtmlEnabled="sqllab__is_render_html_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(n||(n={}))}}]);
//# sourceMappingURL=2741.25c098b171be5765550a.entry.js.map