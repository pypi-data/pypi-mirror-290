"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3195],{58132:(e,t,i)=>{i.d(t,{A:()=>s});var l=i(96453),r=i(95579),n=i(12249),a=i(19129),o=i(2445);const s=function({certifiedBy:e,details:t,size:i="l"}){const s=(0,l.DP)();return(0,o.Y)(a.m,{id:"certified-details-tooltip",title:(0,o.FD)(o.FK,{children:[e&&(0,o.Y)("div",{children:(0,o.Y)("strong",{children:(0,r.t)("Certified by %s",e)})}),(0,o.Y)("div",{children:t})]}),children:(0,o.Y)(n.A.Certified,{iconColor:s.colors.primary.base,iconSize:i})})}},75264:(e,t,i)=>{i.d(t,{Dj:()=>n,cE:()=>a,cp:()=>o});var l=i(96453),r=i(2445);const n=()=>{const e=(0,l.DP)();return(0,r.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,r.Y)("path",{d:"M16 0H2C0.89 0 0 0.9 0 2V16C0 17.1 0.89 18 2 18H16C17.11 18 18 17.1 18 16V2C18 0.9 17.11 0 16 0Z",fill:e.colors.primary.base}),(0,r.Y)("path",{d:"M7 14L2 9L3.41 7.59L7 11.17L14.59 3.58L16 5L7 14Z",fill:"white"})]})},a=()=>{const e=(0,l.DP)();return(0,r.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,r.Y)("path",{d:"M16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0Z",fill:e.colors.grayscale.light1}),(0,r.Y)("path",{d:"M14 10H4V8H14V10Z",fill:"white"})]})},o=()=>{const e=(0,l.DP)();return(0,r.FD)("svg",{width:"18",height:"18",viewBox:"0 0 18 18",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[(0,r.Y)("path",{d:"M16 0H2C0.9 0 0 0.9 0 2V16C0 17.1 0.9 18 2 18H16C17.1 18 18 17.1 18 16V2C18 0.9 17.1 0 16 0Z",fill:e.colors.grayscale.light2}),(0,r.Y)("path",{d:"M16 2V16H2V2H16V2Z",fill:"white"})]})}},37020:(e,t,i)=>{i.d(t,{A:()=>p});var l=i(96453),r=i(95579),n=i(96540),a=i(90868),o=i(85861),s=i(40563),c=i(2445);const d=l.I4.div`
  padding-top: 8px;
  width: 50%;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,h=l.I4.div`
  line-height: ${({theme:e})=>4*e.gridUnit}px;
  padding-top: 16px;
`;function p({description:e,onConfirm:t,onHide:i,open:l,title:p}){const[u,m]=(0,n.useState)(!0),[g,f]=(0,n.useState)(""),b=()=>{f(""),t()};return(0,c.FD)(o.A,{disablePrimaryButton:u,onHide:()=>{f(""),i()},onHandledPrimaryAction:b,primaryButtonName:(0,r.t)("delete"),primaryButtonType:"danger",show:l,title:p,children:[(0,c.Y)(h,{children:e}),(0,c.FD)(d,{children:[(0,c.Y)(s.lR,{htmlFor:"delete",children:(0,r.t)('Type "%s" to confirm',(0,r.t)("DELETE"))}),(0,c.Y)(a.pd,{type:"text",id:"delete",autoComplete:"off",value:g,onChange:e=>{var t;const i=null!=(t=e.target.value)?t:"";m(i.toUpperCase()!==(0,r.t)("DELETE")),f(i)},onPressEnter:()=>{u||b()}})]})]})}},94704:(e,t,i)=>{i.d(t,{A:()=>h});var l=i(96540),r=i(96453),n=i(17437),a=i(95579),o=i(19129),s=i(12249),c=i(2445);const d=r.I4.a`
  ${({theme:e})=>n.AH`
    font-size: ${e.typography.sizes.xl}px;
    display: flex;
    padding: 0 0 0 ${2*e.gridUnit}px;
  `};
`,h=({itemId:e,isStarred:t,showTooltip:i,saveFaveStar:r,fetchFaveStar:n})=>{(0,l.useEffect)((()=>{null==n||n(e)}),[n,e]);const h=(0,l.useCallback)((i=>{i.preventDefault(),r(e,!!t)}),[t,e,r]),p=(0,c.Y)(d,{href:"#",onClick:h,className:"fave-unfave-icon",role:"button",children:t?(0,c.Y)(s.A.FavoriteSelected,{}):(0,c.Y)(s.A.FavoriteUnselected,{})});return i?(0,c.Y)(o.m,{id:"fave-unfave-tooltip",title:(0,a.t)("Click to favorite/unfavorite"),children:p}):p}},29307:(e,t,i)=>{i.d(t,{A:()=>s});var l=i(96540),r=i(96453),n=i(5362),a=i(2445);const o=r.I4.div`
  background-image: url(${({src:e})=>e});
  background-size: cover;
  background-position: center ${({position:e})=>e};
  display: inline-block;
  height: calc(100% - 1px);
  width: calc(100% - 2px);
  margin: 1px 1px 0 1px;
`;function s({src:e,fallback:t,isLoading:i,position:r,...s}){const[c,d]=(0,l.useState)(t);return(0,l.useEffect)((()=>(e&&fetch(e).then((e=>e.blob())).then((e=>{if(/image/.test(e.type)){const t=URL.createObjectURL(e);d(t)}})).catch((e=>{n.A.error(e),d(t)})),()=>{d(t)})),[e,t]),(0,a.Y)(o,{src:i?t:c,...s,position:r})}},18301:(e,t,i)=>{i.d(t,{A:()=>o});var l=i(96540),r=i(85861),n=i(46920),a=i(2445);const o=(0,l.forwardRef)(((e,t)=>{const[i,o]=(0,l.useState)(!1),{beforeOpen:s=(()=>{}),onExit:c=(()=>{}),isButton:d=!1,resizable:h=!1,draggable:p=!1,className:u="",tooltip:m,modalFooter:g,triggerNode:f,destroyOnClose:b=!0,modalBody:v,draggableConfig:F={},resizableConfig:x={},modalTitle:y,responsive:C,width:S,maxWidth:w}=e,k=()=>{o(!1),null==c||c()},Y=e=>{e.preventDefault(),null==s||s(),o(!0)};return t&&(t.current={close:k,open:Y,showModal:i}),(0,a.FD)(a.FK,{children:[d&&(0,a.Y)(n.A,{className:"modal-trigger",tooltip:m,onClick:Y,children:f}),!d&&(0,a.Y)("span",{onClick:Y,role:"button",children:f}),(0,a.Y)(r.A,{className:u,show:i,onHide:k,title:y,footer:g,hideFooter:!g,width:S,maxWidth:w,responsive:C,resizable:h,resizableConfig:x,draggable:p,draggableConfig:F,destroyOnClose:b,children:v})]})}))},3932:(e,t,i)=>{i.d(t,{m:()=>p});var l=i(35742),r=i(95579),n=i(51436),a=i(58561),o=i.n(a),s=i(43859);const c=new Map,d=(0,s.K)(l.A.get,c,(({endpoint:e})=>e||"")),h=e=>({value:e.id,label:e.name,key:e.id}),p=async(e,t,i)=>{const l="name",a=o().encode({filters:[{col:l,opr:"ct",value:e},{col:"type",opr:"custom_tag",value:!0}],page:t,page_size:i,order_column:l,order_direction:"asc"});return d({endpoint:`/api/v1/tag/?q=${a}`}).then((e=>({data:e.json.result.map(h),totalCount:e.json.count}))).catch((async e=>{const t=(({error:e,message:t})=>{let i=t||e||(0,r.t)("An error has occurred");return"Forbidden"===t&&(i=(0,r.t)("You do not have permission to read tags")),i})(await(0,n.h4)(e));throw new Error(t)}))}},8706:(e,t,i)=>{i.d(t,{A:()=>j});var l=i(90179),r=i.n(l),n=i(96540),a=i(90868),o=i(40563),s=i(75086),c=i.n(s),d=i(46920),h=i(15595),p=i(58561),u=i.n(p),m=i(96453),g=i(95579),f=i(76968),b=i(51436),v=i(35742),F=i(62952),x=i(27366),y=i(85861),C=i(24976),S=i(5556),w=i.n(S),k=i(76125),Y=i(2445);const $={onChange:w().func,labelMargin:w().number,colorScheme:w().string,hasCustomLabelsColor:w().bool};class A extends n.PureComponent{constructor(e){super(e),this.state={hovered:!1},this.categoricalSchemeRegistry=(0,f.A)(),this.choices=this.categoricalSchemeRegistry.keys().map((e=>[e,e])),this.schemes=this.categoricalSchemeRegistry.getMap()}setHover(e){this.setState({hovered:e})}render(){const{colorScheme:e,labelMargin:t=0,hasCustomLabelsColor:i}=this.props;return(0,Y.Y)(k.A,{description:(0,g.t)("Any color palette selected here will override the colors applied to this dashboard's individual charts"),labelMargin:t,name:"color_scheme",onChange:this.props.onChange,value:e,choices:this.choices,clearable:!0,schemes:this.schemes,hovered:this.state.hovered,hasCustomLabelsColor:i})}}A.propTypes=$,A.defaultProps={hasCustomLabelsColor:!1,colorScheme:void 0,onChange:()=>{}};const N=A;var I=i(888),D=i(5261),T=i(97567),E=i(3932),O=i(55556);const U=(0,m.I4)(o.eI)`
  margin-bottom: 0;
`,M=(0,m.I4)(C.iN)`
  border-radius: ${({theme:e})=>e.borderRadius}px;
  border: 1px solid ${({theme:e})=>e.colors.secondary.light2};
`;var _={name:"1blj7km",styles:"margin-top:1em"};const j=(0,D.Ay)((({addSuccessToast:e,addDangerToast:t,colorScheme:i,dashboardId:l,dashboardInfo:s,dashboardTitle:p,onHide:m=(()=>{}),onlyApply:S=!1,onSubmit:w=(()=>{}),show:k=!1})=>{const[$]=h.Wq.useForm(),[A,D]=(0,n.useState)(!1),[j,R]=(0,n.useState)(!1),[L,H]=(0,n.useState)(i),[z,q]=(0,n.useState)(""),[B,K]=(0,n.useState)(),[P,V]=(0,n.useState)([]),[W,J]=(0,n.useState)([]),G=S?(0,g.t)("Apply"):(0,g.t)("Save"),[Z,Q]=(0,n.useState)([]),X=(0,f.A)(),ee=(0,n.useMemo)((()=>Z.map((e=>({value:e.id,label:e.name})))),[Z.length]),te=async e=>{const{error:t,statusText:i,message:l}=await(0,b.h4)(e);let r=t||i||(0,g.t)("An error has occurred");"object"==typeof l&&"json_metadata"in l?r=l.json_metadata:"string"==typeof l&&(r=l,"Forbidden"===l&&(r=(0,g.t)("You do not have permission to edit this dashboard"))),y.A.error({title:(0,g.t)("Error"),content:r,okButtonProps:{danger:!0,className:"btn-danger"}})},ie=(0,n.useCallback)(((e="owners",t="",i,l)=>{const r=u().encode({filter:t,page:i,page_size:l});return v.A.get({endpoint:`/api/v1/dashboard/related/${e}?q=${r}`}).then((e=>({data:e.json.result.filter((e=>void 0===e.extra.active||e.extra.active)).map((e=>({value:e.value,label:e.text}))),totalCount:e.json.count})))}),[]),le=(0,n.useCallback)((e=>{const{id:t,dashboard_title:i,slug:l,certified_by:n,certification_details:a,owners:o,roles:s,metadata:d,is_managed_externally:h}=e,p={id:t,title:i,slug:l||"",certifiedBy:n||"",certificationDetails:a||"",isManagedExternally:h||!1};$.setFieldsValue(p),K(p),V(o),J(s),H(d.color_scheme);const u=r()(d,["positions","shared_label_colors","color_scheme_domain"]);q(u?c()(u):"")}),[$]),re=(0,n.useCallback)((()=>{D(!0),v.A.get({endpoint:`/api/v1/dashboard/${l}`}).then((e=>{var t;const i=e.json.result,l=null!=(t=i.json_metadata)&&t.length?JSON.parse(i.json_metadata):{};le({...i,metadata:l}),D(!1)}),te)}),[l,le]),ne=()=>{try{return null!=z&&z.length?JSON.parse(z):{}}catch(e){return{}}},ae=e=>{const t=(0,F.A)(e).map((e=>({id:e.value,full_name:e.label})));V(t)},oe=e=>{const t=(0,F.A)(e).map((e=>({id:e.value,name:e.label})));J(t)},se=()=>(P||[]).map((e=>({value:e.id,label:e.full_name||`${e.first_name} ${e.last_name}`}))),ce=(e="",{updateMetadata:t=!0}={})=>{const i=X.keys(),l=ne();if(e&&!i.includes(e))throw y.A.error({title:(0,g.t)("Error"),content:(0,g.t)("A valid color scheme is required"),okButtonProps:{danger:!0,className:"btn-danger"}}),new Error("A valid color scheme is required");t&&(l.color_scheme=e,l.label_colors=l.label_colors||{},q(c()(l))),H(e)};return(0,n.useEffect)((()=>{k&&(s?le(s):re()),C.iN.preload()}),[s,re,le,k]),(0,n.useEffect)((()=>{p&&B&&B.title!==p&&$.setFieldsValue({...B,title:p})}),[B,p,$]),(0,n.useEffect)((()=>{if((0,x.G7)(x.TO.TaggingSystem))try{(0,T.un)({objectType:T.iQ.DASHBOARD,objectId:l,includeTypes:!1},(e=>Q(e)),(e=>{t(`Error fetching tags: ${e.text}`)}))}catch(e){te(e)}}),[l]),(0,Y.Y)(y.A,{show:k,onHide:m,title:(0,g.t)("Dashboard properties"),footer:(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(d.A,{htmlType:"button",buttonSize:"small",onClick:m,cta:!0,children:(0,g.t)("Cancel")}),(0,Y.Y)(d.A,{onClick:$.submit,buttonSize:"small",buttonStyle:"primary",className:"m-r-5",cta:!0,disabled:null==B?void 0:B.isManagedExternally,tooltip:null!=B&&B.isManagedExternally?(0,g.t)("This dashboard is managed externally, and can't be edited in Superset"):"",children:G})]}),responsive:!0,children:(0,Y.FD)(h.Wq,{form:$,onFinish:()=>{var i,r,n,a;const{title:o,slug:s,certifiedBy:d,certificationDetails:h}=$.getFieldsValue();let p,u=L,f=z;try{if(!f.startsWith("{")||!f.endsWith("}"))throw new Error;p=JSON.parse(f)}catch(e){return void t((0,g.t)("JSON metadata is invalid!"))}const b={...p},F=(0,O.Z6)(null==(i=p)?void 0:i.color_namespace);u=(null==(r=p)?void 0:r.color_scheme)||L,null!=(n=p)&&n.shared_label_colors&&delete p.shared_label_colors,null!=(a=p)&&a.color_scheme_domain&&delete p.color_scheme_domain,(0,O.D2)(b,!0),f=c()(p),ce(u,{updateMetadata:!1});const y={},C={};(0,x.G7)(x.TO.DashboardRbac)&&(y.roles=W,C.roles=(W||[]).map((e=>e.id))),(0,x.G7)(x.TO.TaggingSystem)&&(C.tags=Z.map((e=>e.id)));const k={id:l,title:o,slug:s,jsonMetadata:f,owners:P,colorScheme:u,colorNamespace:F,certifiedBy:d,certificationDetails:h,...y};S?(w(k),m(),e((0,g.t)("Dashboard properties updated"))):v.A.put({endpoint:`/api/v1/dashboard/${l}`,headers:{"Content-Type":"application/json"},body:JSON.stringify({dashboard_title:o,slug:s||null,json_metadata:f||null,owners:(P||[]).map((e=>e.id)),certified_by:d||null,certification_details:d&&h?h:null,...C})}).then((()=>{w(k),m(),e((0,g.t)("The dashboard has been saved"))}),te)},layout:"vertical",initialValues:B,children:[(0,Y.Y)(h.fI,{children:(0,Y.Y)(h.fv,{xs:24,md:24,children:(0,Y.Y)("h3",{children:(0,g.t)("Basic information")})})}),(0,Y.FD)(h.fI,{gutter:16,children:[(0,Y.Y)(h.fv,{xs:24,md:12,children:(0,Y.Y)(o.eI,{label:(0,g.t)("Name"),name:"title",children:(0,Y.Y)(a.pd,{type:"text",disabled:A})})}),(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{label:(0,g.t)("URL slug"),name:"slug",children:(0,Y.Y)(a.pd,{type:"text",disabled:A})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("A readable URL for your dashboard")})]})]}),(0,x.G7)(x.TO.DashboardRbac)?(()=>{const e=ne(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(h.fI,{children:(0,Y.Y)(h.fv,{xs:24,md:24,children:(0,Y.Y)("h3",{style:{marginTop:"1em"},children:(0,g.t)("Access")})})}),(0,Y.FD)(h.fI,{gutter:16,children:[(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{label:(0,g.t)("Owners"),children:(0,Y.Y)(h.DW,{allowClear:!0,allowNewOptions:!0,ariaLabel:(0,g.t)("Owners"),disabled:A,mode:"multiple",onChange:ae,options:(e,t,i)=>ie("owners",e,t,i),value:se()})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username.")})]}),(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{label:(0,g.t)("Roles"),children:(0,Y.Y)(h.DW,{allowClear:!0,ariaLabel:(0,g.t)("Roles"),disabled:A,mode:"multiple",onChange:oe,options:(e,t,i)=>ie("roles",e,t,i),value:(W||[]).map((e=>({value:e.id,label:`${e.name}`})))})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("Roles is a list which defines access to the dashboard. Granting a role access to a dashboard will bypass dataset level checks. If no roles are defined, regular access permissions apply.")})]})]}),(0,Y.Y)(h.fI,{children:(0,Y.Y)(h.fv,{xs:24,md:12,children:(0,Y.Y)(N,{hasCustomLabelsColor:t,onChange:ce,colorScheme:L,labelMargin:4})})})]})})():(()=>{const e=ne(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,Y.FD)(h.fI,{gutter:16,children:[(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)("h3",{style:{marginTop:"1em"},children:(0,g.t)("Access")}),(0,Y.Y)(U,{label:(0,g.t)("Owners"),children:(0,Y.Y)(h.DW,{allowClear:!0,ariaLabel:(0,g.t)("Owners"),disabled:A,mode:"multiple",onChange:ae,options:(e,t,i)=>ie("owners",e,t,i),value:se()})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username.")})]}),(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)("h3",{style:{marginTop:"1em"},children:(0,g.t)("Colors")}),(0,Y.Y)(N,{hasCustomLabelsColor:t,onChange:ce,colorScheme:L,labelMargin:4})]})]})})(),(0,Y.Y)(h.fI,{children:(0,Y.Y)(h.fv,{xs:24,md:24,children:(0,Y.Y)("h3",{children:(0,g.t)("Certification")})})}),(0,Y.FD)(h.fI,{gutter:16,children:[(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{label:(0,g.t)("Certified by"),name:"certifiedBy",children:(0,Y.Y)(a.pd,{type:"text",disabled:A})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("Person or group that has certified this dashboard.")})]}),(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{label:(0,g.t)("Certification details"),name:"certificationDetails",children:(0,Y.Y)(a.pd,{type:"text",disabled:A})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("Any additional detail to show in the certification tooltip.")})]})]}),(0,x.G7)(x.TO.TaggingSystem)?(0,Y.Y)(h.fI,{gutter:16,children:(0,Y.Y)(h.fv,{xs:24,md:12,children:(0,Y.Y)("h3",{css:_,children:(0,g.t)("Tags")})})}):null,(0,x.G7)(x.TO.TaggingSystem)?(0,Y.Y)(h.fI,{gutter:16,children:(0,Y.FD)(h.fv,{xs:24,md:12,children:[(0,Y.Y)(U,{children:(0,Y.Y)(h.DW,{ariaLabel:"Tags",mode:"multiple",value:ee,options:E.m,onChange:e=>{const t=(0,F.A)(e).map((e=>({id:e.value,name:e.label})));Q(t)},allowClear:!0})}),(0,Y.Y)("p",{className:"help-block",children:(0,g.t)("A list of tags that have been applied to this chart.")})]})}):null,(0,Y.Y)(h.fI,{children:(0,Y.FD)(h.fv,{xs:24,md:24,children:[(0,Y.Y)("h3",{style:{marginTop:"1em"},children:(0,Y.FD)(d.A,{buttonStyle:"link",onClick:()=>R(!j),children:[(0,Y.Y)("i",{className:"fa fa-angle-"+(j?"down":"right"),style:{minWidth:"1em"}}),(0,g.t)("Advanced")]})}),j&&(0,Y.FD)(Y.FK,{children:[(0,Y.Y)(U,{label:(0,g.t)("JSON metadata"),children:(0,Y.Y)(M,{showLoadingForImport:!0,name:"json_metadata",value:z,onChange:q,tabSize:2,width:"100%",height:"200px",wrapEnabled:!0})}),(0,Y.FD)("p",{className:"help-block",children:[(0,g.t)("This JSON object is generated dynamically when clicking the save or overwrite button in the dashboard view. It is exposed here for reference and for power users who may want to alter specific parameters."),S&&(0,Y.FD)(Y.FK,{children:[" ",(0,g.t)('Please DO NOT overwrite the "filter_scopes" key.')," ",(0,Y.Y)(I.A,{triggerNode:(0,Y.Y)("span",{className:"alert-link",children:(0,g.t)('Use "%(menuName)s" menu instead.',{menuName:(0,g.t)("Set filter mapping")})})})]})]})]})]})})]})})}))},888:(e,t,i)=>{i.d(t,{A:()=>fe});var l=i(96540),r=i(96453),n=i(18301),a=i(61225),o=i(82960),s=i(78130),c=i(72173),d=i(5556),h=i.n(d),p=i(46942),u=i.n(p),m=i(46920),g=i(17437),f=i(95579),b=i(62193),v=i.n(b),F=i(81151),x=i(49588);const y=[x.B8,x.tq];function C({currentNode:e={},components:t={},filterFields:i=[],selectedChartId:l}){if(!e)return null;const{type:r}=e;if(x.oT===r&&e&&e.meta&&e.meta.chartId)return{value:e.meta.chartId,label:e.meta.sliceName||`${r} ${e.meta.chartId}`,type:r,showCheckbox:l!==e.meta.chartId,children:[]};let n=[];if(e.children&&e.children.length&&e.children.forEach((e=>{const r=C({currentNode:t[e],components:t,filterFields:i,selectedChartId:l}),a=t[e].type;y.includes(a)?n.push(r):n=n.concat(r)})),y.includes(r)){let t=null;return t=r===x.tq?(0,f.t)("All charts"):e.meta&&e.meta.text?e.meta.text:`${r} ${e.id}`,{value:e.id,label:t,type:r,children:n}}return n}function S({components:e={},filterFields:t=[],selectedChartId:i}){return v()(e)?[]:[{...C({currentNode:e[F.wv],components:e,filterFields:t,selectedChartId:i})}]}function w(e=[],t=-1){const i=[],l=(e,r)=>{e&&e.children&&(-1===t||r<t)&&(i.push(e.value),e.children.forEach((e=>l(e,r+1))))};return e.length>0&&e.forEach((e=>{l(e,0)})),i}var k=i(12066);function Y({activeFilterField:e,checkedFilterFields:t}){return(0,k.J)(e?[e]:t)}var $=i(24647);function A({activeFilterField:e,checkedFilterFields:t}){if(e)return(0,$.w)(e).chartId;if(t.length){const{chartId:e}=(0,$.w)(t[0]);return t.some((t=>(0,$.w)(t).chartId!==e))?null:e}return null}function N({checkedFilterFields:e=[],activeFilterField:t,filterScopeMap:i={},layout:l={}}){const r=Y({checkedFilterFields:e,activeFilterField:t}),n=t?[t]:e,a=S({components:l,filterFields:n,selectedChartId:A({checkedFilterFields:e,activeFilterField:t})}),o=new Set;n.forEach((e=>{(i[e].checked||[]).forEach((t=>{o.add(`${t}:${e}`)}))}));const s=[...o],c=i[r]?i[r].expanded:w(a,1);return{[r]:{nodes:a,nodesFiltered:[...a],checked:s,expanded:c}}}var I=i(47307),D=i.n(I),T=i(89143),E=i.n(T),O=i(8209),U=i.n(O),M=i(89899),_=i.n(M);function j({tabScopes:e,parentNodeValue:t,forceAggregate:i=!1,hasChartSiblings:l=!1,tabChildren:r=[],immuneChartSiblings:n=[]}){if(i||!l&&Object.entries(e).every((([e,{scope:t}])=>t&&t.length&&e===t[0]))){const i=function({tabs:e=[],tabsInScope:t=[]}){const i=[];return e.forEach((({value:e,children:l})=>{l&&!t.includes(e)&&l.forEach((({value:e,children:l})=>{l&&!t.includes(e)&&i.push(...l.filter((({type:e})=>e===x.oT)))}))})),i.map((({value:e})=>e))}({tabs:r,tabsInScope:D()(e,(({scope:e})=>e))}),l=D()(Object.values(e),(({immune:e})=>e));return{scope:[t],immune:[...new Set([...i,...l])]}}const a=Object.values(e).filter((({scope:e})=>e&&e.length));return{scope:D()(a,(({scope:e})=>e)),immune:a.length?D()(a,(({immune:e})=>e)):D()(Object.values(e),(({immune:e})=>e)).concat(n)}}function R({currentNode:e={},filterId:t,checkedChartIds:i=[]}){if(!e)return{};const{value:l,children:r}=e,n=r.filter((({type:e})=>e===x.oT)),a=r.filter((({type:e})=>e===x.B8)),o=n.filter((({value:e})=>t!==e&&!i.includes(e))).map((({value:e})=>e)),s=_()(U()((e=>e.value)),E()((e=>R({currentNode:e,filterId:t,checkedChartIds:i}))))(a);if(!v()(n)&&n.some((({value:e})=>i.includes(e)))){if(v()(a))return{scope:[l],immune:o};const{scope:e,immune:t}=j({tabScopes:s,parentNodeValue:l,forceAggregate:!0,tabChildren:a});return{scope:e,immune:o.concat(t)}}return a.length?j({tabScopes:s,parentNodeValue:l,hasChartSiblings:!v()(n),tabChildren:a,immuneChartSiblings:o}):{scope:[],immune:o}}function L({filterKey:e,nodes:t=[],checkedChartIds:i=[]}){if(t.length){const{chartId:l}=(0,$.w)(e);return R({currentNode:t[0],filterId:l,checkedChartIds:i})}return{}}var H=i(68921),z=i(4881),q=i(38491),B=i.n(q),K=i(12249),P=i(2445);const V=(0,r.I4)(K.A.BarChartOutlined)`
  ${({theme:e})=>`\n    position: relative;\n    top: ${e.gridUnit-1}px;\n    color: ${e.colors.primary.base};\n    margin-right: ${2*e.gridUnit}px;\n  `}
`;function W({currentNode:e={},selectedChartId:t}){if(!e)return null;const{label:i,value:l,type:r,children:n}=e;if(n&&n.length){const a=n.map((e=>W({currentNode:e,selectedChartId:t})));return{...e,label:(0,P.FD)("span",{className:u()(`filter-scope-type ${r.toLowerCase()}`,{"selected-filter":t===l}),children:[r===x.oT&&(0,P.Y)(V,{}),i]}),children:a}}return{...e,label:(0,P.Y)("span",{className:u()(`filter-scope-type ${r.toLowerCase()}`,{"selected-filter":t===l}),children:i})}}function J({nodes:e,selectedChartId:t}){return e?e.map((e=>W({currentNode:e,selectedChartId:t}))):[]}var G=i(75264);const Z={check:(0,P.Y)(G.Dj,{}),uncheck:(0,P.Y)(G.cp,{}),halfCheck:(0,P.Y)(G.cE,{}),expandClose:(0,P.Y)("span",{className:"rct-icon rct-icon-expand-close"}),expandOpen:(0,P.Y)("span",{className:"rct-icon rct-icon-expand-open"}),expandAll:(0,P.Y)("span",{className:"rct-icon rct-icon-expand-all",children:(0,f.t)("Expand all")}),collapseAll:(0,P.Y)("span",{className:"rct-icon rct-icon-collapse-all",children:(0,f.t)("Collapse all")}),parentClose:(0,P.Y)("span",{className:"rct-icon rct-icon-parent-close"}),parentOpen:(0,P.Y)("span",{className:"rct-icon rct-icon-parent-open"}),leaf:(0,P.Y)("span",{className:"rct-icon rct-icon-leaf"})},Q={nodes:h().arrayOf(z.QU).isRequired,checked:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,expanded:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,onCheck:h().func.isRequired,onExpand:h().func.isRequired,selectedChartId:h().number},X=()=>{};function ee({nodes:e=[],checked:t=[],expanded:i=[],onCheck:l,onExpand:r,selectedChartId:n}){return(0,P.Y)(B(),{showExpandAll:!0,expandOnClick:!0,showNodeIcon:!1,nodes:J({nodes:e,selectedChartId:n}),checked:t,expanded:i,onCheck:l,onExpand:r,onClick:X,icons:Z})}ee.propTypes=Q,ee.defaultProps={selectedChartId:null};var te=i(40563);const ie={label:h().string.isRequired,isSelected:h().bool.isRequired};function le({label:e,isSelected:t}){return(0,P.Y)("span",{className:u()("filter-field-item filter-container",{"is-selected":t}),children:(0,P.Y)(te.lR,{htmlFor:e,children:e})})}function re({nodes:e,activeKey:t}){if(!e)return[];const i=e[0],l=i.children.map((e=>({...e,children:e.children.map((e=>{const{label:i,value:l}=e;return{...e,label:(0,P.Y)(le,{isSelected:l===t,label:i})}}))})));return[{...i,label:(0,P.Y)("span",{className:"root",children:i.label}),children:l}]}le.propTypes=ie;const ne={activeKey:h().string,nodes:h().arrayOf(z.QU).isRequired,checked:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,expanded:h().arrayOf(h().oneOfType([h().number,h().string])).isRequired,onCheck:h().func.isRequired,onExpand:h().func.isRequired,onClick:h().func.isRequired};function ae({activeKey:e,nodes:t=[],checked:i=[],expanded:l=[],onClick:r,onCheck:n,onExpand:a}){return(0,P.Y)(B(),{showExpandAll:!0,showNodeIcon:!1,expandOnClick:!0,nodes:re({nodes:t,activeKey:e}),checked:i,expanded:l,onClick:r,onCheck:n,onExpand:a,icons:Z})}ae.propTypes=ne,ae.defaultProps={activeKey:null};const oe={dashboardFilters:h().objectOf(z.d2).isRequired,layout:h().object.isRequired,updateDashboardFiltersScope:h().func.isRequired,setUnsavedChanges:h().func.isRequired,onCloseModal:h().func.isRequired},se=r.I4.div`
  ${({theme:e})=>g.AH`
    display: flex;
    flex-direction: column;
    height: 80%;
    margin-right: ${-6*e.gridUnit}px;
    font-size: ${e.typography.sizes.m}px;

    & .nav.nav-tabs {
      border: none;
    }

    & .filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*e.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }

    & .warning-message {
      padding: ${6*e.gridUnit}px;
    }
  `}
`,ce=r.I4.div`
  ${({theme:e})=>g.AH`
    &.filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*e.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }
  `}
`,de=r.I4.div`
  ${({theme:e})=>g.AH`
    height: ${16*e.gridUnit}px;
    border-bottom: 1px solid ${e.colors.grayscale.light2};
    padding-left: ${6*e.gridUnit}px;
    margin-left: ${-6*e.gridUnit}px;

    h4 {
      margin-top: 0;
    }

    .selected-fields {
      margin: ${3*e.gridUnit}px 0 ${4*e.gridUnit}px;
      visibility: hidden;

      &.multi-edit-mode {
        visibility: visible;
      }

      .selected-scopes {
        padding-left: ${e.gridUnit}px;
      }
    }
  `}
`,he=r.I4.div`
  ${({theme:e})=>g.AH`
    &.filters-scope-selector {
      display: flex;
      flex-direction: row;
      position: relative;
      height: 100%;

      a,
      a:active,
      a:hover {
        color: inherit;
        text-decoration: none;
      }

      .react-checkbox-tree .rct-icon.rct-icon-expand-all,
      .react-checkbox-tree .rct-icon.rct-icon-collapse-all {
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
        color: ${e.colors.primary.base};

        &::before {
          content: '';
        }

        &:hover {
          text-decoration: underline;
        }

        &:focus {
          outline: none;
        }
      }

      .filter-field-pane {
        position: relative;
        width: 40%;
        padding: ${4*e.gridUnit}px;
        padding-left: 0;
        border-right: 1px solid ${e.colors.grayscale.light2};

        .filter-container label {
          font-weight: ${e.typography.weights.normal};
          margin: 0 0 0 ${4*e.gridUnit}px;
          word-break: break-all;
        }

        .filter-field-item {
          height: ${9*e.gridUnit}px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 ${6*e.gridUnit}px;
          margin-left: ${-6*e.gridUnit}px;

          &.is-selected {
            border: 1px solid ${e.colors.text.label};
            border-radius: ${e.borderRadius}px;
            background-color: ${e.colors.grayscale.light4};
            margin-left: ${-6*e.gridUnit}px;
          }
        }

        .react-checkbox-tree {
          .rct-title .root {
            font-weight: ${e.typography.weights.bold};
          }

          .rct-text {
            height: ${10*e.gridUnit}px;
          }
        }
      }

      .filter-scope-pane {
        position: relative;
        flex: 1;
        padding: ${4*e.gridUnit}px;
        padding-right: ${6*e.gridUnit}px;
      }

      .react-checkbox-tree {
        flex-direction: column;
        color: ${e.colors.grayscale.dark1};
        font-size: ${e.typography.sizes.m}px;

        .filter-scope-type {
          padding: ${2*e.gridUnit}px 0;
          display: flex;
          align-items: center;

          &.chart {
            font-weight: ${e.typography.weights.normal};
          }

          &.selected-filter {
            padding-left: ${7*e.gridUnit}px;
            position: relative;
            color: ${e.colors.text.label};

            &::before {
              content: ' ';
              position: absolute;
              left: 0;
              top: 50%;
              width: ${4*e.gridUnit}px;
              height: ${4*e.gridUnit}px;
              border-radius: ${e.borderRadius}px;
              margin-top: ${-2*e.gridUnit}px;
              box-shadow: inset 0 0 0 2px ${e.colors.grayscale.light2};
              background: ${e.colors.grayscale.light3};
            }
          }

          &.root {
            font-weight: ${e.typography.weights.bold};
          }
        }

        .rct-checkbox {
          svg {
            position: relative;
            top: 3px;
            width: ${4.5*e.gridUnit}px;
          }
        }

        .rct-node-leaf {
          .rct-bare-label {
            &::before {
              padding-left: ${e.gridUnit}px;
            }
          }
        }

        .rct-options {
          text-align: left;
          margin-left: 0;
          margin-bottom: ${2*e.gridUnit}px;
        }

        .rct-text {
          margin: 0;
          display: flex;
        }

        .rct-title {
          display: block;
        }

        // disable style from react-checkbox-trees.css
        .rct-node-clickable:hover,
        .rct-node-clickable:focus,
        label:hover,
        label:active {
          background: none !important;
        }
      }

      .multi-edit-mode {
        .filter-field-item {
          padding: 0 ${4*e.gridUnit}px 0 ${12*e.gridUnit}px;
          margin-left: ${-12*e.gridUnit}px;

          &.is-selected {
            margin-left: ${-13*e.gridUnit}px;
          }
        }
      }

      .scope-search {
        position: absolute;
        right: ${4*e.gridUnit}px;
        top: ${4*e.gridUnit}px;
        border-radius: ${e.borderRadius}px;
        border: 1px solid ${e.colors.grayscale.light2};
        padding: ${e.gridUnit}px ${2*e.gridUnit}px;
        font-size: ${e.typography.sizes.m}px;
        outline: none;

        &:focus {
          border: 1px solid ${e.colors.primary.base};
        }
      }
    }
  `}
`,pe=r.I4.div`
  ${({theme:e})=>`\n    height: ${16*e.gridUnit}px;\n\n    border-top: ${e.gridUnit/4}px solid ${e.colors.primary.light3};\n    padding: ${6*e.gridUnit}px;\n    margin: 0 0 0 ${6*-e.gridUnit}px;\n    text-align: right;\n\n    .btn {\n      margin-right: ${4*e.gridUnit}px;\n\n      &:last-child {\n        margin-right: 0;\n      }\n    }\n  `}
`;class ue extends l.PureComponent{constructor(e){super(e);const{dashboardFilters:t,layout:i}=e;if(Object.keys(t).length>0){const e=function({dashboardFilters:e={}}){const t=Object.values(e).map((e=>{const{chartId:t,filterName:i,columns:l,labels:r}=e,n=Object.keys(l).map((e=>({value:(0,$.s)({chartId:t,column:e}),label:r[e]||e})));return{value:t,label:i,children:n,showCheckbox:!0}}));return[{value:F.zf,type:x.tq,label:(0,f.t)("All filters"),children:t}]}({dashboardFilters:t}),l=e[0].children;this.allfilterFields=[],l.forEach((({children:e})=>{e.forEach((e=>{this.allfilterFields.push(e.value)}))})),this.defaultFilterKey=l[0].children[0].value;const r=Object.values(t).reduce(((e,{chartId:l,columns:r})=>({...e,...Object.keys(r).reduce(((e,r)=>{const n=(0,$.s)({chartId:l,column:r}),a=S({components:i,filterFields:[n],selectedChartId:l}),o=w(a,1),s=((0,H._i)({filterScope:t[l].scopes[r]})||[]).filter((e=>e!==l));return{...e,[n]:{nodes:a,nodesFiltered:[...a],checked:s,expanded:o}}}),{})})),{}),{chartId:n}=(0,$.w)(this.defaultFilterKey),a=[],o=this.defaultFilterKey,s=[F.zf].concat(n),c=N({checkedFilterFields:a,activeFilterField:o,filterScopeMap:r,layout:i});this.state={showSelector:!0,activeFilterField:o,searchText:"",filterScopeMap:{...r,...c},filterFieldNodes:e,checkedFilterFields:a,expandedFilterIds:s}}else this.state={showSelector:!1};this.filterNodes=this.filterNodes.bind(this),this.onChangeFilterField=this.onChangeFilterField.bind(this),this.onCheckFilterScope=this.onCheckFilterScope.bind(this),this.onExpandFilterScope=this.onExpandFilterScope.bind(this),this.onSearchInputChange=this.onSearchInputChange.bind(this),this.onCheckFilterField=this.onCheckFilterField.bind(this),this.onExpandFilterField=this.onExpandFilterField.bind(this),this.onClose=this.onClose.bind(this),this.onSave=this.onSave.bind(this)}onCheckFilterScope(e=[]){const{activeFilterField:t,filterScopeMap:i,checkedFilterFields:l}=this.state,r=Y({activeFilterField:t,checkedFilterFields:l}),n=t?[t]:l,a={...i[r],checked:e},o=function({checked:e=[],filterFields:t=[],filterScopeMap:i={}}){const l=e.reduce(((e,t)=>{const[i,l]=t.split(":");return{...e,[l]:(e[l]||[]).concat(parseInt(i,10))}}),{});return t.reduce(((e,t)=>({...e,[t]:{...i[t],checked:l[t]||[]}})),{})}({checked:e,filterFields:n,filterScopeMap:i});this.setState((()=>({filterScopeMap:{...i,...o,[r]:a}})))}onExpandFilterScope(e=[]){const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:l}=this.state,r=Y({activeFilterField:t,checkedFilterFields:i}),n={...l[r],expanded:e};this.setState((()=>({filterScopeMap:{...l,[r]:n}})))}onCheckFilterField(e=[]){const{layout:t}=this.props,{filterScopeMap:i}=this.state,l=N({checkedFilterFields:e,activeFilterField:null,filterScopeMap:i,layout:t});this.setState((()=>({activeFilterField:null,checkedFilterFields:e,filterScopeMap:{...i,...l}})))}onExpandFilterField(e=[]){this.setState((()=>({expandedFilterIds:e})))}onChangeFilterField(e={}){const{layout:t}=this.props,i=e.value,{activeFilterField:l,checkedFilterFields:r,filterScopeMap:n}=this.state;if(i===l){const e=N({checkedFilterFields:r,activeFilterField:null,filterScopeMap:n,layout:t});this.setState({activeFilterField:null,filterScopeMap:{...n,...e}})}else if(this.allfilterFields.includes(i)){const e=N({checkedFilterFields:r,activeFilterField:i,filterScopeMap:n,layout:t});this.setState({activeFilterField:i,filterScopeMap:{...n,...e}})}}onSearchInputChange(e){this.setState({searchText:e.target.value},this.filterTree)}onClose(){this.props.onCloseModal()}onSave(){const{filterScopeMap:e}=this.state,t=this.allfilterFields.reduce(((t,i)=>{const{nodes:l}=e[i];return{...t,[i]:L({filterKey:i,nodes:l,checkedChartIds:e[i].checked})}}),{});this.props.updateDashboardFiltersScope(t),this.props.setUnsavedChanges(!0),this.props.onCloseModal()}filterTree(){if(this.state.searchText){const e=e=>{const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:l}=e,r=Y({activeFilterField:t,checkedFilterFields:i}),n=l[r].nodes.reduce(this.filterNodes,[]),a=w([...n]),o={...l[r],nodesFiltered:n,expanded:a};return{filterScopeMap:{...l,[r]:o}}};this.setState(e)}else this.setState((e=>{const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:l}=e,r=Y({activeFilterField:t,checkedFilterFields:i}),n={...l[r],nodesFiltered:l[r].nodes};return{filterScopeMap:{...l,[r]:n}}}))}filterNodes(e=[],t={}){const{searchText:i}=this.state,l=(t.children||[]).reduce(this.filterNodes,[]);return(t.label.toLocaleLowerCase().indexOf(i.toLocaleLowerCase())>-1||l.length)&&e.push({...t,children:l}),e}renderFilterFieldList(){const{activeFilterField:e,filterFieldNodes:t,checkedFilterFields:i,expandedFilterIds:l}=this.state;return(0,P.Y)(ae,{activeKey:e,nodes:t,checked:i,expanded:l,onClick:this.onChangeFilterField,onCheck:this.onCheckFilterField,onExpand:this.onExpandFilterField})}renderFilterScopeTree(){const{filterScopeMap:e,activeFilterField:t,checkedFilterFields:i,searchText:l}=this.state,r=Y({activeFilterField:t,checkedFilterFields:i}),n=A({activeFilterField:t,checkedFilterFields:i});return(0,P.FD)(P.FK,{children:[(0,P.Y)("input",{className:"filter-text scope-search multi-edit-mode",placeholder:(0,f.t)("Search..."),type:"text",value:l,onChange:this.onSearchInputChange}),(0,P.Y)(ee,{nodes:e[r].nodesFiltered,checked:e[r].checked,expanded:e[r].expanded,onCheck:this.onCheckFilterScope,onExpand:this.onExpandFilterScope,selectedChartId:n})]})}renderEditingFiltersName(){const{dashboardFilters:e}=this.props,{activeFilterField:t,checkedFilterFields:i}=this.state,l=[].concat(t||i).map((t=>{const{chartId:i,column:l}=(0,$.w)(t);return e[i].labels[l]||l}));return(0,P.FD)("div",{className:"selected-fields multi-edit-mode",children:[0===l.length&&(0,f.t)("No filter is selected."),1===l.length&&(0,f.t)("Editing 1 filter:"),l.length>1&&(0,f.t)("Batch editing %d filters:",l.length),(0,P.Y)("span",{className:"selected-scopes",children:l.join(", ")})]})}render(){const{showSelector:e}=this.state;return(0,P.FD)(se,{children:[(0,P.FD)(de,{children:[(0,P.Y)("h4",{children:(0,f.t)("Configure filter scopes")}),e&&this.renderEditingFiltersName()]}),(0,P.Y)(ce,{className:"filter-scope-body",children:e?(0,P.FD)(he,{className:"filters-scope-selector",children:[(0,P.Y)("div",{className:u()("filter-field-pane multi-edit-mode"),children:this.renderFilterFieldList()}),(0,P.Y)("div",{className:"filter-scope-pane multi-edit-mode",children:this.renderFilterScopeTree()})]}):(0,P.Y)("div",{className:"warning-message",children:(0,f.t)("There are no filters in this dashboard.")})}),(0,P.FD)(pe,{children:[(0,P.Y)(m.A,{buttonSize:"small",onClick:this.onClose,children:(0,f.t)("Close")}),e&&(0,P.Y)(m.A,{buttonSize:"small",buttonStyle:"primary",onClick:this.onSave,children:(0,f.t)("Save")})]})]})}}ue.propTypes=oe;const me=(0,a.Ng)((function({dashboardLayout:e,dashboardFilters:t}){return{dashboardFilters:t,layout:e.present}}),(function(e){return(0,o.zH)({updateDashboardFiltersScope:s.B8,setUnsavedChanges:c.MR},e)}))(ue),ge=r.I4.div((({theme:{gridUnit:e}})=>({padding:2*e,paddingBottom:3*e})));class fe extends l.PureComponent{constructor(e){super(e),this.modal=void 0,this.modal=(0,l.createRef)(),this.handleCloseModal=this.handleCloseModal.bind(this)}handleCloseModal(){var e,t;null==this||null==(e=this.modal)||null==(t=e.current)||null==t.close||t.close()}render(){const e={onCloseModal:this.handleCloseModal};return(0,P.Y)(n.A,{ref:this.modal,triggerNode:this.props.triggerNode,modalBody:(0,P.Y)(ge,{children:(0,P.Y)(me,{...e})}),width:"80%"})}}},50317:(e,t,i)=>{i.d(t,{A:()=>u});var l=i(96540),r=i(17437),n=i(96453),a=i(95579),o=i(66537),s=i(19129),c=i(40563),d=i(12249),h=i(2445);const p=r.AH`
  &.anticon {
    font-size: unset;
    .anticon {
      line-height: unset;
      vertical-align: unset;
    }
  }
`,u=({name:e,label:t,description:i,validationErrors:u=[],renderTrigger:m=!1,rightNode:g,leftNode:f,onClick:b,hovered:v=!1,tooltipOnClick:F=(()=>{}),warning:x,danger:y})=>{const{gridUnit:C,colors:S}=(0,n.DP)(),w=(0,l.useRef)(!1),k=(0,l.useMemo)((()=>(u.length||(w.current=!0),w.current?u.length?S.error.base:"unset":S.alert.base)),[S.error.base,S.alert.base,u.length]);return t?(0,h.FD)("div",{className:"ControlHeader",children:[(0,h.Y)("div",{className:"pull-left",children:(0,h.FD)(c.lR,{css:e=>r.AH`
            margin-bottom: ${.5*e.gridUnit}px;
            position: relative;
          `,children:[f&&(0,h.Y)("span",{children:f}),(0,h.Y)("span",{role:"button",tabIndex:0,onClick:b,style:{cursor:b?"pointer":""},children:t})," ",x&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:x,children:(0,h.Y)(d.A.AlertSolid,{iconColor:S.alert.base,iconSize:"s"})})," "]}),y&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:y,children:(0,h.Y)(d.A.ErrorSolid,{iconColor:S.error.base,iconSize:"s"})})," "]}),(null==u?void 0:u.length)>0&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"error-tooltip",placement:"top",title:null==u?void 0:u.join(" "),children:(0,h.Y)(d.A.ExclamationCircleOutlined,{css:r.AH`
                    ${p};
                    color: ${k};
                  `})})," "]}),v?(0,h.FD)("span",{css:()=>r.AH`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${C}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `,children:[i&&(0,h.FD)("span",{children:[(0,h.Y)(s.m,{id:"description-tooltip",title:i,placement:"top",children:(0,h.Y)(d.A.InfoCircleOutlined,{css:p,onClick:F})})," "]}),m&&(0,h.FD)("span",{children:[(0,h.Y)(o.W,{label:(0,a.t)("bolt"),tooltip:(0,a.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," "]})]}):null]})}),g&&(0,h.Y)("div",{className:"pull-right",children:g}),(0,h.Y)("div",{className:"clearfix"})]}):null}},76125:(e,t,i)=>{i.d(t,{A:()=>Y});var l=i(33031),r=i.n(l),n=i(1882),a=i.n(n),o=i(96540),s=i(96453),c=i(95579),d=i(63756),h=i(17437),p=i(83307),u=i(50317),m=i(19129),g=i(12249),f=i(6308),b=i(3175),v=i(2445);function F(e){const{id:t,label:i,colors:l}=e,[r,n]=(0,o.useState)(!1),a=(0,o.useRef)(null),s=(0,o.useRef)(null),c=()=>l.map(((e,i)=>(0,v.Y)("span",{css:t=>h.AH`
          padding-left: ${t.gridUnit/2}px;
          :before {
            content: '';
            display: inline-block;
            background-color: ${e};
            border: 1px solid ${"white"===e?"black":e};
            width: 9px;
            height: 10px;
          }
        `},`${t}-${i}`)));return(0,v.Y)(m.m,{"data-testid":"tooltip",overlayClassName:"color-scheme-tooltip",title:()=>(0,v.FD)(v.FK,{children:[(0,v.Y)("span",{children:i}),(0,v.Y)("div",{children:c()})]}),visible:r,children:(0,v.FD)("span",{className:"color-scheme-option",onMouseEnter:()=>{const e=a.current,t=s.current;e&&t&&(e.scrollWidth>e.offsetWidth||e.scrollHeight>e.offsetHeight||t.scrollWidth>t.offsetWidth||t.scrollHeight>t.offsetHeight)&&n(!0)},onMouseLeave:()=>{n(!1)},css:h.AH`
          display: flex;
          align-items: center;
          justify-content: flex-start;
        `,children:[(0,v.Y)("span",{className:"color-scheme-label",ref:a,css:e=>h.AH`
            min-width: 125px;
            padding-right: ${2*e.gridUnit}px;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
          `,children:i}),(0,v.Y)("span",{ref:s,css:e=>h.AH`
            flex: 100%;
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
            padding-right: ${e.gridUnit}px;
          `,children:c()})]})},t)}const{Option:x,OptGroup:y}=p.default,C=(0,s.I4)(g.A.AlertSolid)`
  color: ${({theme:e})=>e.colors.alert.base};
`,S=(0,c.t)("This color scheme is being overridden by custom label colors.\n    Check the JSON metadata in the Advanced settings"),w=(0,c.t)("The color scheme is determined by the related dashboard.\n        Edit the color scheme in the dashboard properties."),k=({label:e,hasCustomLabelsColor:t,dashboardId:i})=>{if(t||i){const i=t?S:w;return(0,v.FD)(v.FK,{children:[e," ",(0,v.Y)(m.m,{title:i,children:(0,v.Y)(C,{iconSize:"s"})})]})}return(0,v.Y)(v.FK,{children:e})},Y=({hasCustomLabelsColor:e=!1,dashboardId:t,label:i=(0,c.t)("Color scheme"),onChange:l=(()=>{}),value:n,clearable:p=!1,defaultScheme:g,choices:C=[],schemes:S={},isLinear:Y,...$})=>{const A=(0,s.DP)(),N=(0,o.useMemo)((()=>{if(t)return"dashboard";let e=n||g;if("SUPERSET_DEFAULT"===e){var i;const t=a()(S)?S():S;e=null==t||null==(i=t.SUPERSET_DEFAULT)?void 0:i.id}return e}),[t,g,S,n]),I=(0,o.useMemo)((()=>{if(t)return[(0,v.Y)(x,{value:"dashboard",label:(0,c.t)("dashboard"),children:(0,v.Y)(m.m,{title:w,children:(0,c.t)("Dashboard scheme")})},"dashboard")];const e=a()(S)?S():S,i=a()(C)?C():C,l=[],n=i.filter((e=>{const t=e[0],i="SUPERSET_DEFAULT"!==t&&!l.includes(t);return l.push(t),i})).reduce(((t,[i])=>{var l,r;const n=e[i];let a=[];n&&(a=Y?n.getColors(10):n.colors);const o={customLabel:(0,v.Y)(F,{id:n.id,label:n.label,colors:a}),label:(null==e||null==(l=e[i])?void 0:l.label)||i,value:i};return t[null!=(r=n.group)?r:d.w.Other].options.push(o),t}),{[d.w.Custom]:{title:d.w.Custom,label:(0,c.t)("Custom color palettes"),options:[]},[d.w.Featured]:{title:d.w.Featured,label:(0,c.t)("Featured color palettes"),options:[]},[d.w.Other]:{title:d.w.Other,label:(0,c.t)("Other color palettes"),options:[]}}),o=Object.values(n).filter((e=>e.options.length>0)).map((e=>({...e,options:r()(e.options,(e=>e.label))})));return 1===o.length&&o[0].title===d.w.Other?o[0].options.map(((e,t)=>(0,v.Y)(x,{value:e.value,label:e.label,children:e.customLabel},t))):o.map(((e,t)=>(0,v.Y)(y,{label:e.label,children:e.options.map(((e,i)=>(0,v.Y)(x,{value:e.value,label:e.label,children:e.customLabel},`${t}-${i}`)))},t)))}),[C,t,Y,S]);return(0,v.FD)(v.FK,{children:[(0,v.Y)(u.A,{...$,label:(0,v.Y)(k,{label:i,hasCustomLabelsColor:e,dashboardId:t})}),(0,v.Y)(f.Iu,{css:h.AH`
          width: 100%;
          & .ant-select-item.ant-select-item-group {
            padding-left: ${A.gridUnit}px;
            font-size: ${A.typography.sizes.m}px;
          }
          & .ant-select-item-option-grouped {
            padding-left: ${3*A.gridUnit}px;
          }
        `,"aria-label":(0,c.t)("Select color scheme"),allowClear:p,disabled:!!t,onChange:e=>l(e),placeholder:(0,c.t)("Select scheme"),value:N,getPopupContainer:e=>e.parentNode,showSearch:!0,filterOption:(e,t)=>(0,b.qY)(e,t,["label","value"],!0),children:I})]})}},97567:(e,t,i)=>{i.d(t,{FA:()=>s,Ik:()=>h,dH:()=>d,iQ:()=>o,un:()=>c});var l=i(35742),r=i(58561),n=i.n(r);const a=Object.freeze(["dashboard","chart","saved_query"]),o=Object.freeze({DASHBOARD:"dashboard",CHART:"chart",QUERY:"saved_query"});function s(e,t,i){l.A.get({endpoint:`/api/v1/tag/${e}`}).then((({json:e})=>t(e.result))).catch((e=>i(e)))}function c({objectType:e,objectId:t,includeTypes:i=!1},r,n){if(void 0===e||void 0===t)throw new Error("Need to specify objectType and objectId");if(!a.includes(e))throw new Error(`objectType ${e} is invalid`);l.A.get({endpoint:`/api/v1/${e}/${t}`}).then((({json:e})=>r(e.result.tags.filter((e=>1===e.type))))).catch((e=>n(e)))}function d(e,t,i){const r=e.map((e=>e.name));l.A.delete({endpoint:`/api/v1/tag/?q=${n().encode(r)}`}).then((({json:e})=>e.message?t(e.message):t("Successfully Deleted Tag"))).catch((e=>{const t=e.message;return i(t||"Error Deleting Tag")}))}function h({tagIds:e=[],types:t},i,r){let n=`/api/v1/tag/get_objects/?tagIds=${e}`;t&&(n+=`&types=${t}`),l.A.get({endpoint:n}).then((({json:e})=>i(e.result))).catch((e=>r(e)))}},43859:(e,t,i)=>{i.d(t,{K:()=>l});const l=(e,t,i=((...e)=>JSON.stringify([...e])))=>(...l)=>{const r=i(...l);if(t.has(r))return t.get(r);const n=e(...l);return t.set(r,n),n}}}]);
//# sourceMappingURL=3195.6e3b3f2bbe6179a79765.entry.js.map