"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4233],{62703:(e,t,n)=>{n.d(t,{A:()=>Ke});var r,a=n(61225),i=n(82960),o=n(2514),s=n(7735),l=n(5556),d=n.n(l),c=n(96540),u=n(95579),h=n(96453),p=n(5362),m=n(27366),g=n(62952),b=n(73212),v=n(17444),f=n(87196),y=n(49544),x=n(35700),C=n(27023),S=n(32132),A=n(92201);!function(e){e.Explore="explore",e.Dashboard="dashboard"}(r||(r={}));var T,w=n(86274),D=n(88055),_=n.n(D),F=n(2404),Y=n.n(F),I=n(4124),$=n.n(I),E=n(58863),M=n(80145),R=n(28846),N=n(17437),k=n(28290),O=n(84666),U=n(6749),q=n(15595),L=n(95004),z=n(44230),H=n(83537),P=n(67429),j=n(38221),W=n.n(j),V=n(72391),B=n(87843),G=n(58561),K=n.n(G),Q=n(5373),X=n(12249),J=n(90868),Z=n(5261),ee=n(35233),te=n(13270),ne=n(71519),re=n(85861),ae=n(46920),ie=n(94229),oe=n(60237),se=n(59838),le=n(55976),de=n(25946),ce=n(85183);!function(e){e[e.Chart=0]="Chart",e[e.Table=1]="Table"}(T||(T={}));var ue=n(2445);function he({formData:e,result:t,dataset:n,onContextMenu:r,inContextMenu:a}){const i=(0,c.useMemo)((()=>({onContextMenu:r})),[r]);return(0,ue.Y)("div",{css:N.AH`
        width: 100%;
        height: 100%;
        min-height: 0;
      `,children:(0,ue.Y)(R.A,{disableErrorBoundary:!0,chartType:e.viz_type,enableNoResults:!0,datasource:n,formData:e,queriesData:t,hooks:i,inContextMenu:a,height:"100%",width:"100%"})})}var pe=n(78697),me=n(15151);const ge=(0,h.I4)(q.BD.Item)`
  ${({theme:e,isClickable:t,isHidden:n})=>N.AH`
    cursor: ${t?"pointer":"auto"};
    color: ${e.colors.grayscale.light1};
    transition: color ease-in ${e.transitionTiming}s;
    .ant-breadcrumb > span:last-child > & {
      color: ${e.colors.grayscale.dark1};
    }
    &:hover {
      color: ${t?e.colors.grayscale.dark1:"inherit"};
    }
    visibility: ${n?"hidden":"visible"};
  `}
`;var be=n(8877),ve=n(48327);const fe=h.I4.div`
  ${({theme:e})=>N.AH`
    & .pagination-container {
      bottom: ${4*-e.gridUnit}px;
    }
  `}
`,ye="adhoc_filters",xe=({formData:e,closeModal:t})=>{const n=(0,a.wA)(),{addDangerToast:r}=(0,Z.Yf)(),i=(0,h.DP)(),[o,l]=(0,c.useState)(""),d=(0,c.useContext)(ie.DashboardPageIdContext),p=(0,c.useCallback)((()=>{n((0,s.logEvent)(x.Ro,{slice_id:e.slice_id}))}),[n,e.slice_id]),m=(0,a.d4)((e=>{var t;return(0,O.L)("can_explore","Superset",null==(t=e.user)?void 0:t.roles)})),[g,b]=e.datasource.split("__");(0,c.useEffect)((()=>{(0,oe.T3)(Number(g),b,e,0).then((e=>{l(`/explore/?form_data_key=${e}&dashboard_page_id=${d}`)})).catch((()=>{r((0,u.t)("Failed to generate chart edit URL"))}))}),[r,d,g,b,e]);const v=!o||!m;return(0,ue.FD)(ue.FK,{children:[(0,ue.Y)(ae.A,{buttonStyle:"secondary",buttonSize:"small",onClick:p,disabled:v,tooltip:v?(0,u.t)("You do not have sufficient permissions to edit the chart"):void 0,children:(0,ue.Y)(ne.N_,{css:N.AH`
            &:hover {
              text-decoration: none;
            }
          `,to:o,children:(0,u.t)("Edit chart")})}),(0,ue.Y)(ae.A,{buttonStyle:"primary",buttonSize:"small",onClick:t,css:N.AH`
          margin-left: ${2*i.gridUnit}px;
        `,children:(0,u.t)("Close")})]})};function Ce({column:e,dataset:t,drillByConfig:n,formData:r,onHideModal:i,canDownload:l}){const d=(0,a.wA)(),p=(0,h.DP)(),{addDangerToast:m}=(0,Z.Yf)(),[b,f]=(0,c.useState)(!0),[y,C]=(0,c.useState)([{...n,column:e}]);(0,c.useEffect)((()=>{d((0,s.logEvent)(x.bD,{slice_id:r.slice_id}))}),[d,r.slice_id]);const{column:S,groupbyFieldName:A=n.groupbyFieldName}=y[y.length-1]||{},w=(0,c.useMemo)((()=>(0,g.A)(r[A]).map((e=>{var n;return null==(n=t.columns)?void 0:n.find((t=>t.column_name===e))})).filter(te.A)),[t.columns,r,A]),{displayModeToggle:D,drillByDisplayMode:_}=(()=>{const[e,t]=(0,c.useState)(T.Chart);return{displayModeToggle:(0,c.useMemo)((()=>(0,ue.Y)("div",{css:e=>N.AH`
          margin-bottom: ${6*e.gridUnit}px;
          .ant-radio-button-wrapper-checked:not(
              .ant-radio-button-wrapper-disabled
            ):focus-within {
            box-shadow: none;
          }
        `,children:(0,ue.FD)(pe.s.Group,{onChange:({target:{value:e}})=>{t(e)},defaultValue:T.Chart,children:[(0,ue.Y)(pe.s.Button,{value:T.Chart,children:(0,u.t)("Chart")}),(0,ue.Y)(pe.s.Button,{value:T.Table,children:(0,u.t)("Table")})]})})),[]),drillByDisplayMode:e}})(),[F,Y]=(0,c.useState)(),I=((e,t,n)=>(0,te.A)(e)?1===e.length?(0,ue.Y)(fe,{children:(0,ue.Y)(be.U,{colnames:e[0].colnames,coltypes:e[0].coltypes,rowcount:e[0].sql_rowcount,data:e[0].data,dataSize:15,datasourceId:t,isVisible:!0,canDownload:n})}):(0,ue.Y)(ve.Ay,{fullWidth:!1,children:e.map(((e,r)=>(0,ue.Y)(ve.Ay.TabPane,{tab:(0,u.t)("Results %s",r+1),children:(0,ue.Y)(fe,{children:(0,ue.Y)(be.U,{colnames:e.colnames,coltypes:e.coltypes,data:e.data,rowcount:e.sql_rowcount,dataSize:15,datasourceId:t,isVisible:!0,canDownload:n})})},r)))}):(0,ue.Y)("div",{}))(F,r.datasource,l),[$,E]=(0,c.useState)(r),[M,R]=(0,c.useState)([...w,e].filter(te.A)),[k,O]=(0,c.useState)([{groupby:w,filters:n.filters},{groupby:e||[]}]),U=(0,c.useCallback)(((e,t=A)=>Array.isArray(r[t])?[e.column_name]:e.column_name),[r,A]),L=(0,c.useCallback)((e=>e.reduce(((e,t)=>{null!=t&&t.groupbyFieldName&&t.column&&(e.formData[t.groupbyFieldName]=U(t.column,t.groupbyFieldName),e.overridenGroupbyFields.add(t.groupbyFieldName));const n=(null==t?void 0:t.adhocFilterFieldName)||ye;return e.formData[n]=[...(0,g.A)(e[n]),...(0,g.A)(t.filters).map((e=>(0,se.r)(e)))],e.overridenAdhocFilterFields.add(n),e}),{formData:{},overridenGroupbyFields:new Set,overridenAdhocFilterFields:new Set})),[U]),z=(0,c.useCallback)((()=>y.reduce(((e,t)=>{const n=t.adhocFilterFieldName||ye;return e[n]=[...e[n]||[],...t.filters.map((e=>(0,se.r)(e)))],e}),{})),[y]),H=((e,t=me.fZ)=>(0,c.useMemo)((()=>{const n=t=>t<e.length-1,r=e=>`${(0,g.A)(e.groupby).map((e=>e.verbose_name||e.column_name)).join(", ")} ${e.filters?`(${e.filters.map((e=>e.formattedVal||e.val)).join(", ")})`:""}`;return(0,ue.Y)(q.BD,{css:e=>N.AH`
          margin: ${2*e.gridUnit}px 0 ${4*e.gridUnit}px;
        `,children:e.map(((e,a)=>{return(0,ue.Y)(ge,{isClickable:n(a),isHidden:(i=e,0===(0,g.A)(i.groupby).length&&0===(0,g.A)(i.filters).length),onClick:n(a)?()=>t(e,a):me.fZ,children:r(e)},a);var i})).filter((e=>!1===e.props.isHidden))})}),[e,t]))(k,(0,c.useCallback)(((e,t)=>{d((0,s.logEvent)(x.g$,{slice_id:r.slice_id})),C((e=>e.slice(0,t))),O((e=>{const n=e.slice(0,t+1);return delete n[n.length-1].filters,n})),R((e=>e.slice(0,t))),E((()=>{if(0===t)return r;const{formData:e,overridenAdhocFilterFields:n}=L(y.slice(0,t)),a={...r,...e};return n.forEach((t=>({...a,[t]:[...r[t],...e[t]]}))),a}))}),[d,y,r,L])),P=(0,c.useMemo)((()=>{let e={...$};S&&A&&(e[A]=U(S));const t=z();return Object.keys(t).forEach((n=>{e={...e,[n]:[...(0,g.A)(r[n]),...t[n]]}})),e.slice_id=0,delete e.slice_name,delete e.dashboards,e}),[$,S,A,z,U,r]);(0,c.useEffect)((()=>{R((e=>!S||e.some((e=>e.column_name===S.column_name))?e:[...e,S]))}),[S]);const j=(0,c.useCallback)(((e,t)=>{d((0,s.logEvent)(x.gi,{drill_depth:y.length+1,slice_id:r.slice_id})),E(P),C((n=>[...n,{...t,column:e}])),O((n=>{const r=[...n,{groupby:e}];return r[r.length-2].filters=t.filters,r}))}),[d,y.length,P,r.slice_id]),W=(0,c.useMemo)((()=>({drillBy:{excludedColumns:M,openNewModal:!1}})),[M]),{contextMenu:V,inContextMenu:B,onContextMenu:G}=((e,t,n,r,a)=>{const i=(0,c.useRef)(null),[o,s]=(0,c.useState)(!1),l=(0,c.useCallback)(((...e)=>{s(!1),null==n||n(...e)}),[n]),d=(0,c.useCallback)((()=>{s(!1)}),[]);return{contextMenu:(0,c.useMemo)((()=>(0,ue.Y)(Fe,{ref:i,id:0,formData:t,onSelection:l,onClose:d,displayedItems:r,additionalConfig:a})),[a,0,r,t,d,l]),inContextMenu:o,onContextMenu:(e,t,n)=>{var r;null==(r=i.current)||r.open(e,t,n),s(!0)}}})(0,$,j,De.DrillBy,W),K=(0,a.d4)((e=>{const t=Object.values(e.dashboardLayout.present).find((e=>{var t;return(null==(t=e.meta)?void 0:t.chartId)===r.slice_id}));return(null==t?void 0:t.meta.sliceNameOverride)||(null==t?void 0:t.meta.sliceName)}));(0,c.useEffect)((()=>{if(P){const[e]=(0,ce.Mp)(P);f(!0),Y(void 0),(0,o.getChartDataRequest)({formData:P}).then((({response:t,json:n})=>(0,o.handleChartDataResponse)(t,n,e))).then((e=>{Y(e)})).catch((()=>{m((0,u.t)("Failed to load chart data."))})).finally((()=>{f(!1)}))}}),[m,P]);const{metadataBar:Q}=(0,le.M)({dataset:t});return(0,ue.Y)(re.A,{css:N.AH`
        .ant-modal-footer {
          border-top: none;
        }
      `,show:!0,onHide:null!=i?i:()=>null,title:(0,u.t)("Drill by: %s",K),footer:(0,ue.Y)(xe,{formData:P}),responsive:!0,resizable:!0,resizableConfig:{minHeight:128*p.gridUnit,minWidth:128*p.gridUnit,defaultSize:{width:"auto",height:"80vh"}},draggable:!0,destroyOnClose:!0,maskClosable:!1,children:(0,ue.FD)("div",{css:N.AH`
          display: flex;
          flex-direction: column;
          height: 100%;
        `,children:[Q,H,D,b&&(0,ue.Y)(v.A,{}),!b&&!F&&(0,ue.Y)(de.A,{type:"error",message:(0,u.t)("There was an error loading the chart data")}),_===T.Chart&&F&&(0,ue.Y)(he,{dataset:t,formData:P,result:F,onContextMenu:G,inContextMenu:B}),_===T.Table&&F&&I,V]})})}var Se=n(28543);const Ae=(0,V.a)().get("load.drillby.options"),Te=K().encode({columns:["table_name","owners.first_name","owners.last_name","created_by.first_name","created_by.last_name","created_on_humanized","changed_by.first_name","changed_by.last_name","changed_on_humanized","columns.column_name","columns.verbose_name","columns.groupby"]}),we=({drillByConfig:e,formData:t,contextMenuY:n=0,submenuIndex:r=0,onSelection:a=(()=>{}),onClick:i=(()=>{}),excludedColumns:o,openNewModal:s=!0,canDownload:l,open:d,...m})=>{const b=(0,h.DP)(),{addDangerToast:f}=(0,Z.Yf)(),[y,x]=(0,c.useState)(!0),[C,S]=(0,c.useState)(""),[A,T]=(0,c.useState)(),[w,D]=(0,c.useState)([]),[_,F]=(0,c.useState)(!1),[Y,I]=(0,c.useState)(),$=(0,c.useRef)(null),R=Ae||w.length>10,k=(0,c.useCallback)(((t,n)=>{i(t),a(n,e),I(n),s&&F(!0)}),[e,i,a,s]),O=(0,c.useCallback)((()=>{F(!1)}),[]);(0,c.useEffect)((()=>{var e,t;d?null==(e=$.current)||e.input.focus():(null==(t=$.current)||t.setValue(""),S(""))}),[d]);const q=null==e?void 0:e.groupbyFieldName,L=(0,c.useMemo)((()=>{var e;return null==(e=(0,M.A)().get(t.viz_type))?void 0:e.behaviors.find((e=>e===E.nS.DrillBy))}),[t.viz_type]),z=(e=>{const t={};return(0,g.A)(null==e?void 0:e.columns).forEach((e=>{t[e.column_name]=e.verbose_name||e.column_name})),(0,g.A)(null==e?void 0:e.metrics).forEach((e=>{t[e.metric_name]=e.verbose_name||e.metric_name})),t})(A);(0,c.useEffect)((()=>{L&&q&&async function(){const n=Number(t.datasource.split("__")[0]);try{let r;x(!0),r=Ae?await Ae(n,t):await(0,ee.w)({endpoint:`/api/v1/dataset/${n}?q=${Te}`});const{json:a}=r,{result:i}=a;T(i),D((0,g.A)(i.columns).filter((e=>e.groupby)).filter((n=>{var r,a;return!(0,g.A)(t[null!=(r=null==e?void 0:e.groupbyFieldName)?r:""]).includes(n.column_name)&&n.column_name!==t.x_axis&&(null==(a=(0,g.A)(o))?void 0:a.every((e=>e.column_name!==n.column_name)))})))}catch(e){p.A.error(e),ee.e.delete(`/api/v1/dataset/${n}`),f((0,u.t)("Failed to load dimensions for drill by"))}finally{x(!1)}}()}),[f,null==e?void 0:e.groupbyFieldName,o,t,L,q]);const j=W()((e=>S(e)),B.j),V=(0,c.useMemo)((()=>w.filter((e=>(e.verbose_name||e.column_name).toLowerCase().includes(C.toLowerCase())))),[w,C]),G=(0,c.useMemo)((()=>(0,H.Gs)(n,V.length||1,r,200,R?48:0)),[n,V.length,r,R]);let K;return L?q||(K=(0,u.t)("Drill by is not available for this data point")):K=(0,u.t)("Drill by is not yet supported for this chart type"),L&&q?(0,ue.FD)(ue.FK,{children:[(0,ue.Y)(U.W1.SubMenu,{title:(0,u.t)("Drill by"),popupClassName:"chart-context-submenu",popupOffset:[0,G],...m,children:(0,ue.FD)("div",{children:[R&&(0,ue.Y)(J.pd,{ref:$,prefix:(0,ue.Y)(X.A.Search,{iconSize:"l",iconColor:b.colors.grayscale.light1}),onChange:e=>{e.stopPropagation(),j(e.target.value)},placeholder:(0,u.t)("Search columns"),onClick:e=>{e.nativeEvent.stopImmediatePropagation()},allowClear:!0,css:N.AH`
                width: auto;
                max-width: 100%;
                margin: ${2*b.gridUnit}px ${3*b.gridUnit}px;
                box-shadow: none;
              `}),y?(0,ue.Y)("div",{css:N.AH`
                padding: ${3*b.gridUnit}px 0;
              `,children:(0,ue.Y)(v.A,{position:"inline-centered"})}):V.length?(0,ue.Y)(Q.Y1,{width:"100%",height:200,itemSize:35,itemCount:V.length,itemData:{columns:V,...m},overscanCount:20,children:({index:e,data:t,style:n})=>{const{columns:r,...a}=t,i=r[e];return(0,ue.Y)(Se.o,{tooltipText:i.verbose_name||i.column_name,...a,onClick:e=>k(e,i),style:n,children:i.verbose_name||i.column_name},`drill-by-item-${i.column_name}`)}}):(0,ue.Y)(U.W1.Item,{disabled:!0,...m,children:(0,u.t)("No columns found")},"no-drill-by-columns-found")]})}),_&&(0,ue.Y)(Ce,{column:Y,drillByConfig:e,formData:t,onHideModal:O,dataset:{...A,verbose_map:z},canDownload:l})]}):(0,ue.Y)(U.W1.Item,{disabled:!0,...m,children:(0,ue.FD)("div",{children:[(0,u.t)("Drill by"),(0,ue.Y)(P.C,{title:K})]})},"drill-by-disabled")};var De;!function(e){e[e.CrossFilter=0]="CrossFilter",e[e.DrillToDetail=1]="DrillToDetail",e[e.DrillBy=2]="DrillBy",e[e.All=3]="All"}(De||(De={}));const _e=({id:e,formData:t,onSelection:n,onClose:r,displayedItems:i=De.All,additionalConfig:o},s)=>{var l,d;const p=(0,h.DP)(),b=(0,a.wA)(),v=(0,a.d4)((e=>{var t;return(0,O.L)("can_explore","Superset",null==(t=e.user)?void 0:t.roles)})),f=(0,a.d4)((e=>{var t;return(0,O.L)("can_write","ExploreFormDataRestApi",null==(t=e.user)?void 0:t.roles)})),y=(0,a.d4)((e=>{var t;return(0,O.L)("can_samples","Datasource",null==(t=e.user)?void 0:t.roles)})),x=(0,a.d4)((e=>{var t;return(0,O.L)("can_csv","Superset",null==(t=e.user)?void 0:t.roles)})),C=(0,a.d4)((e=>{var t;return(0,O.L)("can_drill","Dashboard",null==(t=e.user)?void 0:t.roles)})),S=(v||C)&&f,A=(v||C)&&y,T=(0,a.d4)((({dashboardInfo:e})=>e.crossFiltersEnabled)),[w,D]=(0,c.useState)([]),_=e=>i===De.All||(0,g.A)(i).includes(e),[{filters:F,clientX:Y,clientY:I},$]=(0,c.useState)({clientX:0,clientY:0}),[R,j]=(0,c.useState)(!1),W=[],V=(0,m.G7)(m.TO.DrillToDetail)&&A&&_(De.DrillToDetail),B=(0,m.G7)(m.TO.DrillBy)&&S&&_(De.DrillBy),G=(0,m.G7)(m.TO.DashboardCrossFilters)&&_(De.CrossFilter),K=null==(l=(0,M.A)().get(t.viz_type))||null==(d=l.behaviors)?void 0:d.includes(E.nS.InteractiveChart);let Q=0;if(G&&(Q+=1),V&&(Q+=2),B&&(Q+=1),0===Q&&(Q=1),G){var X;const t=!K||!T||!(null!=F&&F.crossFilter);let n=null;t?T?K?null!=F&&F.crossFilter||(n=(0,ue.Y)(ue.FK,{children:(0,ue.Y)("div",{children:(0,u.t)("You can't apply cross-filter on this data point.")})})):n=(0,ue.Y)(ue.FK,{children:(0,ue.Y)("div",{children:(0,u.t)("This visualization type does not support cross-filtering.")})}):n=(0,ue.Y)(ue.FK,{children:(0,ue.Y)("div",{children:(0,u.t)("Cross-filtering is not enabled for this dashboard.")})}):n=(0,ue.FD)(ue.FK,{children:[(0,ue.Y)("div",{children:(0,u.t)("Cross-filter will be applied to all of the charts that use this dataset.")}),(0,ue.Y)("div",{children:(0,u.t)("You can also just click on the chart to apply cross-filter.")})]}),W.push((0,ue.FD)(ue.FK,{children:[(0,ue.Y)(U.W1.Item,{disabled:t,onClick:()=>{null!=F&&F.crossFilter&&b((0,L.Mv)(e,F.crossFilter.dataMask))},children:null!=F&&null!=(X=F.crossFilter)&&X.isCurrentValueSelected?(0,u.t)("Remove cross-filter"):(0,ue.FD)("div",{children:[(0,u.t)("Add cross-filter"),(0,ue.Y)(P.C,{title:n,color:t?void 0:p.colors.grayscale.base})]})},"cross-filtering-menu-item"),Q>1&&(0,ue.Y)(U.W1.Divider,{})]}))}if(V&&W.push((0,ue.Y)(z.k,{chartId:e,formData:t,filters:null==F?void 0:F.drillToDetail,isContextMenu:!0,contextMenuY:I,onSelection:n,submenuIndex:G?2:1,showModal:R,setShowModal:j,...(null==o?void 0:o.drillToDetail)||{}})),B){let e=0;G&&(e+=1),V&&(e+=2),W.push((0,ue.Y)(we,{drillByConfig:null==F?void 0:F.drillBy,onSelection:n,formData:t,contextMenuY:I,submenuIndex:e,canDownload:x,open:w.includes("drill-by-submenu"),...(null==o?void 0:o.drillBy)||{}},"drill-by-submenu"))}const J=(0,c.useCallback)(((t,n,r)=>{var a;const i=(0,H.x4)(n,Q);$({clientX:t,clientY:i,filters:r}),null==(a=document.getElementById(`hidden-span-${e}`))||a.click()}),[e,Q]);return(0,c.useImperativeHandle)(s,(()=>({open:J})),[J]),k.createPortal((0,ue.Y)(q.rM,{overlay:(0,ue.Y)(U.W1,{className:"chart-context-menu",onOpenChange:e=>{D(e)},children:W.length?W:(0,ue.Y)(U.W1.Item,{disabled:!0,children:"No actions"})}),trigger:["click"],onVisibleChange:e=>!e&&r(),children:(0,ue.Y)("span",{id:`hidden-span-${e}`,css:(0,N.AH)({visibility:"hidden",position:"fixed",top:I,left:Y,width:1,height:1},"","")})}),document.body)},Fe=(0,c.forwardRef)(_e),Ye={annotationData:d().object,actions:d().object,chartId:d().number.isRequired,datasource:d().object,initialValues:d().object,formData:d().object.isRequired,latestQueryFormData:d().object,labelsColor:d().object,labelsColorMap:d().object,height:d().number,width:d().number,setControlValue:d().func,vizType:d().string.isRequired,triggerRender:d().bool,chartAlert:d().string,chartStatus:d().string,queriesResponse:d().arrayOf(d().object),triggerQuery:d().bool,chartIsStale:d().bool,addFilter:d().func,setDataMask:d().func,onFilterMenuOpen:d().func,onFilterMenuClose:d().func,ownState:d().object,postTransformProps:d().func,source:d().oneOf([r.Dashboard,r.Explore]),emitCrossFilters:d().bool},Ie={},$e=[E.nS.InteractiveChart],Ee={addFilter:()=>Ie,onFilterMenuOpen:()=>Ie,onFilterMenuClose:()=>Ie,initialValues:Ie,setControlValue(){},triggerRender:!1};class Me extends c.Component{constructor(e){super(e),this.state={showContextMenu:e.source===r.Dashboard&&((0,m.G7)(m.TO.DrillToDetail)||(0,m.G7)(m.TO.DashboardCrossFilters)),inContextMenu:!1,legendState:void 0},this.hasQueryResponseChange=!1,this.contextMenuRef=(0,c.createRef)(),this.handleAddFilter=this.handleAddFilter.bind(this),this.handleRenderSuccess=this.handleRenderSuccess.bind(this),this.handleRenderFailure=this.handleRenderFailure.bind(this),this.handleSetControlValue=this.handleSetControlValue.bind(this),this.handleOnContextMenu=this.handleOnContextMenu.bind(this),this.handleContextMenuSelected=this.handleContextMenuSelected.bind(this),this.handleContextMenuClosed=this.handleContextMenuClosed.bind(this),this.handleLegendStateChanged=this.handleLegendStateChanged.bind(this),this.onContextMenuFallback=this.onContextMenuFallback.bind(this),this.hooks={onAddFilter:this.handleAddFilter,onContextMenu:this.state.showContextMenu?this.handleOnContextMenu:void 0,onError:this.handleRenderFailure,setControlValue:this.handleSetControlValue,onFilterMenuOpen:this.props.onFilterMenuOpen,onFilterMenuClose:this.props.onFilterMenuClose,onLegendStateChanged:this.handleLegendStateChanged,setDataMask:e=>{var t;null==(t=this.props.actions)||t.updateDataMask(this.props.chartId,e)}},this.mutableQueriesResponse=_()(this.props.queriesResponse)}shouldComponentUpdate(e,t){var n,r;return!(!(e.queriesResponse&&["success","rendered"].indexOf(e.chartStatus)>-1)||null!=(n=e.queriesResponse)&&null!=(r=n[0])&&r.error)&&(!Y()(this.state,t)||(this.hasQueryResponseChange=e.queriesResponse!==this.props.queriesResponse,this.hasQueryResponseChange&&(this.mutableQueriesResponse=_()(e.queriesResponse)),this.hasQueryResponseChange||!Y()(e.datasource,this.props.datasource)||e.annotationData!==this.props.annotationData||e.ownState!==this.props.ownState||e.filterState!==this.props.filterState||e.height!==this.props.height||e.width!==this.props.width||e.triggerRender||e.labelsColor!==this.props.labelsColor||e.labelsColorMap!==this.props.labelsColorMap||e.formData.color_scheme!==this.props.formData.color_scheme||e.formData.stack!==this.props.formData.stack||e.cacheBusterProp!==this.props.cacheBusterProp||e.emitCrossFilters!==this.props.emitCrossFilters))}handleAddFilter(e,t,n=!0,r=!0){this.props.addFilter(e,t,n,r)}handleRenderSuccess(){const{actions:e,chartStatus:t,chartId:n,vizType:r}=this.props;["loading","rendered"].indexOf(t)<0&&e.chartRenderingSucceeded(n),this.hasQueryResponseChange&&e.logEvent(x.tE,{slice_id:n,viz_type:r,start_offset:this.renderStartTime,ts:(new Date).getTime(),duration:x.Vy.getTimestamp()-this.renderStartTime})}handleRenderFailure(e,t){const{actions:n,chartId:r}=this.props;p.A.warn(e),n.chartRenderingFailed(e.toString(),r,t?t.componentStack:null),this.hasQueryResponseChange&&n.logEvent(x.tE,{slice_id:r,has_err:!0,error_details:e.toString(),start_offset:this.renderStartTime,ts:(new Date).getTime(),duration:x.Vy.getTimestamp()-this.renderStartTime})}handleSetControlValue(...e){const{setControlValue:t}=this.props;t&&t(...e)}handleOnContextMenu(e,t,n){this.contextMenuRef.current.open(e,t,n),this.setState({inContextMenu:!0})}handleContextMenuSelected(){this.setState({inContextMenu:!1})}handleContextMenuClosed(){this.setState({inContextMenu:!1})}handleLegendStateChanged(e){this.setState({legendState:e})}onContextMenuFallback(e){this.state.inContextMenu||(e.preventDefault(),this.handleOnContextMenu(e.clientX,e.clientY))}render(){var e;const{chartAlert:t,chartStatus:n,chartId:a,emitCrossFilters:i}=this.props;if("loading"===n||t||null===n)return null;this.renderStartTime=x.Vy.getTimestamp();const{width:o,height:s,datasource:l,annotationData:d,initialValues:c,ownState:h,filterState:p,chartIsStale:m,formData:g,latestQueryFormData:b,postTransformProps:v}=this.props,y=m&&b?b:g,C=y.viz_type||this.props.vizType,S=$()(C),A="table"===C?`superset-chart-${S}`:S;let T;const w=(0,u.t)("No results were returned for this query"),D=this.props.source===r.Explore?(0,u.t)("Make sure that the controls are configured properly and the datasource contains data for the selected time range"):void 0,_="chart.svg";T=o>300&&s>220?(0,ue.Y)(f.nw,{title:w,description:D,image:_}):(0,ue.Y)(f.u7,{title:w,image:_});const F=null!=(e=(0,M.A)().get(g.viz_type))&&e.behaviors.find((e=>e===E.nS.DrillToDetail))?{inContextMenu:this.state.inContextMenu}:{};return(0,ue.FD)(ue.FK,{children:[this.state.showContextMenu&&(0,ue.Y)(Fe,{ref:this.contextMenuRef,id:a,formData:y,onSelection:this.handleContextMenuSelected,onClose:this.handleContextMenuClosed}),(0,ue.Y)("div",{onContextMenu:this.state.showContextMenu?this.onContextMenuFallback:void 0,children:(0,ue.Y)(R.A,{disableErrorBoundary:!0,id:`chart-id-${a}`,className:A,chartType:C,width:o,height:s,annotationData:d,datasource:l,initialValues:c,formData:y,ownState:h,filterState:p,hooks:this.hooks,behaviors:$e,queriesData:this.mutableQueriesResponse,onRenderSuccess:this.handleRenderSuccess,onRenderFailure:this.handleRenderFailure,noResults:T,postTransformProps:v,emitCrossFilters:i,legendState:this.state.legendState,...F},`${a}`)})]})}}Me.propTypes=Ye,Me.defaultProps=Ee;const Re=Me;var Ne=n(71478),ke=n(79427);const Oe=({chartId:e,error:t,...n})=>{const{result:r}=(0,Ne.RG)(e),a=t&&{...t,extra:{...t.extra,owners:r}};return(0,ue.Y)(ke.A,{...n,error:a})};var Ue=n(21357);const qe={annotationData:d().object,actions:d().object,chartId:d().number.isRequired,datasource:d().object,dashboardId:d().number,initialValues:d().object,formData:d().object.isRequired,labelsColor:d().object,labelsColorMap:d().object,width:d().number,height:d().number,setControlValue:d().func,timeout:d().number,vizType:d().string.isRequired,triggerRender:d().bool,force:d().bool,isFiltersInitialized:d().bool,chartAlert:d().string,chartStatus:d().string,chartStackTrace:d().string,queriesResponse:d().arrayOf(d().object),triggerQuery:d().bool,chartIsStale:d().bool,errorMessage:d().node,addFilter:d().func,onQuery:d().func,onFilterMenuOpen:d().func,onFilterMenuClose:d().func,ownState:d().object,postTransformProps:d().func,datasetsStatus:d().oneOf(["loading","error","complete"]),isInView:d().bool,emitCrossFilters:d().bool},Le={},ze=(0,u.t)("The dataset associated with this chart no longer exists"),He={addFilter:()=>Le,onFilterMenuOpen:()=>Le,onFilterMenuClose:()=>Le,initialValues:Le,setControlValue(){},triggerRender:!1,dashboardId:null,chartStackTrace:null,force:!1,isInView:!0},Pe=h.I4.div`
  min-height: ${e=>e.height}px;
  position: relative;
  text-align: center;

  .chart-tooltip {
    opacity: 0.75;
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .slice_container {
    display: flex;
    flex-direction: column;
    justify-content: center;

    height: ${e=>e.height}px;

    .pivot_table tbody tr {
      font-feature-settings: 'tnum' 1;
    }

    .alert {
      margin: ${({theme:e})=>2*e.gridUnit}px;
    }
  }
`,je=h.I4.div`
  position: absolute;
  left: 50%;
  top: 50%;
  width: 80%;
  transform: translate(-50%, -50%);
`,We=h.I4.span`
  display: block;
  margin: ${({theme:e})=>4*e.gridUnit}px auto;
  width: fit-content;
  color: ${({theme:e})=>e.colors.grayscale.base};
`,Ve=h.I4.div`
  font-family: ${({theme:e})=>e.typography.families.monospace};
  word-break: break-word;
  overflow-x: auto;
  white-space: pre-wrap;
`;class Be extends c.PureComponent{constructor(e){super(e),this.handleRenderContainerFailure=this.handleRenderContainerFailure.bind(this)}componentDidMount(){this.props.triggerQuery&&this.runQuery()}componentDidUpdate(){this.props.triggerQuery&&this.runQuery()}runQuery(){this.props.actions.postChartFormData(this.props.formData,Boolean(this.props.force||(0,S.P3)(C.vX.force)),this.props.timeout,this.props.chartId,this.props.dashboardId,this.props.ownState)}handleRenderContainerFailure(e,t){const{actions:n,chartId:r}=this.props;p.A.warn(e),n.chartRenderingFailed(e.toString(),r,t?t.componentStack:null),n.logEvent(x.tE,{slice_id:r,has_err:!0,error_details:e.toString(),start_offset:this.renderStartTime,ts:(new Date).getTime(),duration:x.Vy.getTimestamp()-this.renderStartTime})}renderErrorMessage(e){var t;const{chartId:n,chartAlert:a,chartStackTrace:i,datasource:o,dashboardId:s,height:l,datasetsStatus:d}=this.props,c=null==e||null==(t=e.errors)?void 0:t[0],u=a||(null==e?void 0:e.message);return void 0!==a&&a!==ze&&o===b.As&&d!==w.bk.Error?(0,ue.Y)(Pe,{"data-ui-anchor":"chart",className:"chart-container",height:l,children:(0,ue.Y)(v.A,{})},n):(0,ue.Y)(Oe,{chartId:n,error:c,subtitle:(0,ue.Y)(Ve,{children:u}),copyText:u,link:e?e.link:null,source:s?r.Dashboard:r.Explore,stackTrace:i},n)}renderSpinner(e){const t=e?(0,u.t)("Waiting on %s",e):(0,u.t)("Waiting on database...");return(0,ue.FD)(je,{children:[(0,ue.Y)(v.A,{position:"inline-centered"}),(0,ue.Y)(We,{children:t})]})}renderChartContainer(){return(0,ue.Y)("div",{className:"slice_container",children:this.props.isInView||!(0,m.G7)(m.TO.DashboardVirtualization)||(0,A.a)()?(0,ue.Y)(Re,{...this.props,source:this.props.dashboardId?"dashboard":"explore"}):(0,ue.Y)(v.A,{})})}render(){var e;const{height:t,chartAlert:n,chartStatus:r,datasource:a,errorMessage:i,chartIsStale:o,queriesResponse:s=[],width:l}=this.props,d=null==a||null==(e=a.database)?void 0:e.name,c="loading"===r;return this.renderContainerStartTime=x.Vy.getTimestamp(),"failed"===r?s.map((e=>this.renderErrorMessage(e))):i&&0===(0,g.A)(s).length?(0,ue.Y)(f.nw,{title:(0,u.t)("Add required control values to preview chart"),description:(0,Ue.w)(!0),image:"chart.svg"}):c||n||i||!o||0!==(0,g.A)(s).length?(0,ue.Y)(y.A,{onError:this.handleRenderContainerFailure,showMessage:!1,children:(0,ue.Y)(Pe,{"data-ui-anchor":"chart",className:"chart-container",height:t,width:l,children:c?this.renderSpinner(d):this.renderChartContainer()})}):(0,ue.Y)(f.nw,{title:(0,u.t)("Your chart is ready to go!"),description:(0,ue.FD)("span",{children:[(0,u.t)('Click on "Create chart" button in the control panel on the left to preview a visualization or')," ",(0,ue.Y)("span",{role:"button",tabIndex:0,onClick:this.props.onQuery,children:(0,u.t)("click here")}),"."]}),image:"chart.svg"})}}Be.propTypes=qe,Be.defaultProps=He;const Ge=Be,Ke=(0,a.Ng)(null,(function(e){return{actions:(0,i.zH)({...o,updateDataMask:L.Mv,logEvent:s.logEvent},e)}}))(Ge)},90422:(e,t,n)=>{n.d(t,{A:()=>s});var r=n(95483),a=n(71191),i=n(2511);const o=[...r.Wy].map((e=>r.nS[e].operation));class s{constructor(e){var t;this.expressionType=e.expressionType||i.A.Simple,this.expressionType===i.A.Simple?(this.subject=e.subject,this.operator=null==(t=e.operator)?void 0:t.toUpperCase(),this.operatorId=e.operatorId,this.comparator=e.comparator,[r.ux.IsTrue,r.ux.IsFalse].indexOf(e.operatorId)>=0&&(this.comparator=e.operatorId===r.ux.IsTrue),[r.ux.IsNull,r.ux.IsNotNull].indexOf(e.operatorId)>=0&&(this.comparator=null),this.clause=e.clause||i.v.Where,this.sqlExpression=null):this.expressionType===i.A.Sql&&(this.sqlExpression="string"==typeof e.sqlExpression?e.sqlExpression:(0,a.e)(e,{useSimple:!0}),this.clause=e.clause,e.operator&&o.indexOf(e.operator)>=0?(this.subject=e.subject,this.operator=e.operator,this.operatorId=e.operatorId):(this.subject=null,this.operator=null),this.comparator=null),this.isExtra=!!e.isExtra,this.isNew=!!e.isNew,this.datasourceWarning=!!e.datasourceWarning,this.filterOptionName=e.filterOptionName||`filter_${Math.random().toString(36).substring(2,15)}_${Math.random().toString(36).substring(2,15)}`}duplicateWith(e){return new s({...this,isNew:!1,...e})}equals(e){return e.clause===this.clause&&e.expressionType===this.expressionType&&e.sqlExpression===this.sqlExpression&&e.operator===this.operator&&e.operatorId===this.operatorId&&e.comparator===this.comparator&&e.subject===this.subject}isValid(){const e=[r.ux.IsNotNull,r.ux.IsNull].map((e=>r.nS[e].operation)),t=[r.ux.IsTrue,r.ux.IsFalse].map((e=>r.nS[e].operation));if(this.expressionType===i.A.Simple){if(e.indexOf(this.operator)>=0)return!(!this.operator||!this.subject);if(t.indexOf(this.operator)>=0)return!(!this.subject||null===this.comparator);if(this.operator&&this.subject&&this.clause)if(Array.isArray(this.comparator)){if(this.comparator.length>0)return!0}else if(null!==this.comparator)return!0}else if(this.expressionType===i.A.Sql)return!(!this.sqlExpression||!this.clause);return!1}getDefaultLabel(){const e=this.translateToSql();return e.length<43?e:`${e.substring(0,40)}...`}getTooltipTitle(){return this.translateToSql()}translateToSql(){return(0,a.e)(this)}}},25671:(e,t,n)=>{n.d(t,{A:()=>N});var r=n(96540),a=n(5556),i=n.n(a),o=n(35742),s=n(5362),l=n(95579),d=n(62952),c=n(65339),u=n(50317),h=n(8901),p=n(32291),m=n(17093),g=n(95483),b=n(84064),v=n(72652),f=n(12249),y=n(85861),x=n(23133),C=n(28254),S=n(59638),A=n(2445);function T({adhocFilter:e,options:t,datasource:n,onFilterEdit:r,onRemoveFilter:a,partitionColumn:i,onMoveLabel:o,onDropLabel:s,index:l,sections:d,operators:c}){const{actualTimeRange:u,title:h}=(0,S.K)(e);return(0,A.Y)(x.A,{sections:d,operators:c,adhocFilter:e,options:t,datasource:n,onFilterEdit:r,partitionColumn:i,children:(0,A.Y)(v.Px,{label:null!=u?u:e.getDefaultLabel(),tooltipTitle:null!=h?h:e.getTooltipTitle(),onRemove:a,onMoveLabel:o,onDropLabel:s,index:l,type:C.S.FilterOption,withCaret:!0,isExtra:e.isExtra})})}var w=n(90422),D=n(2511);const _=i().oneOfType([i().shape({expressionType:i().oneOf([D.A.Simple]).isRequired,clause:i().oneOf([D.v.Having,D.v.Where]).isRequired,subject:i().string.isRequired,comparator:i().oneOfType([i().string,i().arrayOf(i().string)]).isRequired}),i().shape({expressionType:i().oneOf([D.A.Sql]).isRequired,clause:i().oneOf([D.v.Where,D.v.Having]).isRequired,sqlExpression:i().string.isRequired})]);var F=n(21062),Y=n(32132);const{warning:I}=y.A,$=i().oneOfType([i().string,h.A]),E={label:i().oneOfType([i().object,i().string]),name:i().string,sections:i().arrayOf(i().string),operators:i().arrayOf(i().string),onChange:i().func,value:i().arrayOf(_),datasource:i().object,columns:i().arrayOf(F.A),savedMetrics:i().arrayOf(p.A),selectedMetrics:i().oneOfType([$,i().arrayOf($)]),isLoading:i().bool,canDelete:i().func};function M(e){return e&&!(e instanceof w.A)&&e.expressionType}class R extends r.Component{constructor(e){super(e),this.optionsForSelect=this.optionsForSelect.bind(this),this.onRemoveFilter=this.onRemoveFilter.bind(this),this.onNewFilter=this.onNewFilter.bind(this),this.onFilterEdit=this.onFilterEdit.bind(this),this.moveLabel=this.moveLabel.bind(this),this.onChange=this.onChange.bind(this),this.mapOption=this.mapOption.bind(this),this.getMetricExpression=this.getMetricExpression.bind(this),this.removeFilter=this.removeFilter.bind(this);const t=(this.props.value||[]).map((e=>M(e)?new w.A(e):e));this.optionRenderer=e=>(0,A.Y)(b.A,{option:e}),this.valueRenderer=(e,t)=>(0,A.Y)(T,{index:t,adhocFilter:e,onFilterEdit:this.onFilterEdit,options:this.state.options,sections:this.props.sections,operators:this.props.operators,datasource:this.props.datasource,onRemoveFilter:e=>{e.stopPropagation(),this.onRemoveFilter(t)},onMoveLabel:this.moveLabel,onDropLabel:()=>this.props.onChange(this.state.values),partitionColumn:this.state.partitionColumn},t),this.state={values:t,options:this.optionsForSelect(this.props),partitionColumn:null}}componentDidMount(){const{datasource:e}=this.props;if(e&&"table"===e.type){var t;const n=null==(t=e.database)?void 0:t.id,{datasource_name:r,catalog:a,schema:i,is_sqllab_view:l}=e;!l&&n&&r&&i&&o.A.get({endpoint:`/api/v1/database/${n}/table_metadata/extra/${(0,Y.zJ)({name:r,catalog:a,schema:i})}`}).then((({json:e})=>{if(e&&e.partitions){const{partitions:t}=e;t&&t.cols&&1===Object.keys(t.cols).length&&this.setState({partitionColumn:t.cols[0]})}})).catch((e=>{s.A.error("fetch extra_table_metadata:",e.statusText)}))}}UNSAFE_componentWillReceiveProps(e){this.props.columns!==e.columns&&this.setState({options:this.optionsForSelect(e)}),this.props.value!==e.value&&this.setState({values:(e.value||[]).map((e=>M(e)?new w.A(e):e))})}removeFilter(e){const t=[...this.state.values];t.splice(e,1),this.setState((e=>({...e,values:t}))),this.props.onChange(t)}onRemoveFilter(e){const{canDelete:t}=this.props,{values:n}=this.state,r=null==t?void 0:t(n[e],n);"string"!=typeof r?this.removeFilter(e):I({title:(0,l.t)("Warning"),content:r})}onNewFilter(e){const t=this.mapOption(e);t&&this.setState((e=>({...e,values:[...e.values,t]})),(()=>{this.props.onChange(this.state.values)}))}onFilterEdit(e){this.props.onChange(this.state.values.map((t=>t.filterOptionName===e.filterOptionName?e:t)))}onChange(e){const t=(e||[]).map((e=>this.mapOption(e))).filter((e=>e));this.props.onChange(t)}getMetricExpression(e){return this.props.savedMetrics.find((t=>t.metric_name===e)).expression}moveLabel(e,t){const{values:n}=this.state,r=[...n];[r[t],r[e]]=[r[e],r[t]],this.setState({values:r})}mapOption(e){return e instanceof w.A?e:e.saved_metric_name?new w.A({expressionType:D.A.Sql,subject:this.getMetricExpression(e.saved_metric_name),operator:g.nS[g.ux.GreaterThan].operation,comparator:0,clause:D.v.Having}):e.label?new w.A({expressionType:D.A.Sql,subject:new m.A(e).translateToSql(),operator:g.nS[g.ux.GreaterThan].operation,comparator:0,clause:D.v.Having}):e.column_name?new w.A({expressionType:D.A.Simple,subject:e.column_name,operator:g.nS[g.ux.Equals].operation,comparator:"",clause:D.v.Where,isNew:!0}):null}optionsForSelect(e){return[...e.columns,...(0,d.A)(e.selectedMetrics).map((e=>e&&("string"==typeof e?{saved_metric_name:e}:new m.A(e))))].filter((e=>e)).reduce(((e,t)=>(t.saved_metric_name?e.push({...t,filterOptionName:t.saved_metric_name}):t.column_name?e.push({...t,filterOptionName:`_col_${t.column_name}`}):t instanceof m.A&&e.push({...t,filterOptionName:`_adhocmetric_${t.label}`}),e)),[]).sort(((e,t)=>(e.saved_metric_name||e.column_name||e.label).localeCompare(t.saved_metric_name||t.column_name||t.label)))}addNewFilterPopoverTrigger(e){return(0,A.Y)(x.A,{operators:this.props.operators,sections:this.props.sections,adhocFilter:new w.A({}),datasource:this.props.datasource,options:this.state.options,onFilterEdit:this.onNewFilter,partitionColumn:this.state.partitionColumn,children:e})}render(){const{theme:e}=this.props;return(0,A.FD)("div",{className:"metrics-select",children:[(0,A.FD)(v.B3,{children:[(0,A.Y)(u.A,{...this.props}),this.addNewFilterPopoverTrigger((0,A.Y)(v.XB,{children:(0,A.Y)(f.A.PlusLarge,{iconSize:"s",iconColor:e.colors.grayscale.light5})}))]}),(0,A.Y)(v.p6,{children:this.state.values.length>0?this.state.values.map(((e,t)=>this.valueRenderer(e,t))):this.addNewFilterPopoverTrigger((0,A.FD)(v.JG,{children:[(0,A.Y)(f.A.PlusSmall,{iconColor:e.colors.grayscale.light1}),(0,l.t)("Add filter")]}))})]})}}R.propTypes=E,R.defaultProps={name:"",onChange:()=>{},columns:[],savedMetrics:[],selectedMetrics:[]};const N=(0,c.b)(R)},21062:(e,t,n)=>{n.d(t,{A:()=>i});var r=n(5556),a=n.n(r);const i=a().shape({column_name:a().string.isRequired,type:a().string})},17093:(e,t,n)=>{n.d(t,{A:()=>s,t:()=>a});var r=n(95483);const a={SIMPLE:"SIMPLE",SQL:"SQL"};function i(e){if(e.sqlExpression&&r.Vw.test(e.sqlExpression)){const t=e.sqlExpression.indexOf(")"),n=e.sqlExpression.substring(0,t).lastIndexOf("(");if(t>0&&n>0)return e.sqlExpression.substring(n+1,t)}return null}function o(e){if(e.sqlExpression&&r.Vw.test(e.sqlExpression)){const t=e.sqlExpression.indexOf("(");if(t>0)return e.sqlExpression.substring(0,t)}return null}class s{constructor(e){if(this.expressionType=e.expressionType||a.SIMPLE,this.expressionType===a.SIMPLE){const t=i(e);this.column=e.column||t&&{column_name:t},this.aggregate=e.aggregate||o(e),this.sqlExpression=null}else this.expressionType===a.SQL&&(this.sqlExpression=e.sqlExpression,this.column=null,this.aggregate=null);this.datasourceWarning=!!e.datasourceWarning,this.hasCustomLabel=!(!e.hasCustomLabel||!e.label),this.label=this.hasCustomLabel?e.label:this.getDefaultLabel(),this.optionName=e.optionName||`metric_${Math.random().toString(36).substring(2,15)}_${Math.random().toString(36).substring(2,15)}`}getDefaultLabel(){return this.translateToSql({useVerboseName:!0})}translateToSql(e={useVerboseName:!1,transformCountDistinct:!1}){if(this.expressionType===a.SIMPLE){var t,n;const a=this.aggregate||"",i=e.useVerboseName&&null!=(t=this.column)&&t.verbose_name?`(${this.column.verbose_name})`:null!=(n=this.column)&&n.column_name?`(${this.column.column_name})`:"";return e.transformCountDistinct&&a===r.dq.COUNT_DISTINCT&&/^\(.*\)$/.test(i)?`COUNT(DISTINCT ${i.slice(1,-1)})`:a+i}return this.expressionType===a.SQL?this.sqlExpression:""}duplicateWith(e){return new s({...this,...e})}equals(e){return e.label===this.label&&e.expressionType===this.expressionType&&e.sqlExpression===this.sqlExpression&&e.aggregate===this.aggregate&&(e.column&&e.column.column_name)===(this.column&&this.column.column_name)}isValid(){return this.expressionType===a.SIMPLE?!(!this.column||!this.aggregate):this.expressionType===a.SQL&&!!this.sqlExpression}inferSqlExpressionAggregate(){return o(this)}inferSqlExpressionColumn(){return i(this)}}},84064:(e,t,n)=>{n.d(t,{A:()=>c});var r=n(5556),a=n.n(r),i=n(74792),o=n(8901),s=n(84080),l=n(2445);const d={option:a().oneOfType([i.A,a().shape({saved_metric_name:a().string.isRequired}),o.A]).isRequired};function c({option:e}){return e.saved_metric_name?(0,l.Y)(s.V,{column:{column_name:e.saved_metric_name,type:"expression"},showType:!0}):e.column_name?(0,l.Y)(s.V,{column:e,showType:!0}):e.label?(0,l.Y)(s.V,{column:{column_name:e.label,type:"expression"},showType:!0}):null}c.propTypes=d},8901:(e,t,n)=>{n.d(t,{A:()=>l});var r=n(5556),a=n.n(r),i=n(95483),o=n(74792),s=n(17093);const l=a().oneOfType([a().shape({expressionType:a().oneOf([s.t.SIMPLE]).isRequired,column:o.A.isRequired,aggregate:a().oneOf(Object.keys(i.dq)).isRequired,label:a().string.isRequired}),a().shape({expressionType:a().oneOf([s.t.SQL]).isRequired,sqlExpression:a().string.isRequired,label:a().string.isRequired})])},74792:(e,t,n)=>{n.d(t,{A:()=>i});var r=n(5556),a=n.n(r);const i=a().shape({column_name:a().string.isRequired,type:a().string})},32291:(e,t,n)=>{n.d(t,{A:()=>i});var r=n(5556),a=n.n(r);const i=a().shape({metric_name:a().string,verbose_name:a().string,expression:a().string})},15700:(e,t,n)=>{n.d(t,{t3:()=>P,oU:()=>W});var r=n(96540),a=n(61225),i=n(96453),o=n(17437),s=n(95579),l=n(27366),d=n(12249),c=n(6749),u=n(18301),h=n(46920),p=n(5261),m=n(85183),g=n(72965),b=n(32132),v=n(73135),f=n(32850),y=n(7735),x=n(35700),C=n(17432),S=n(90868),A=n(19966),T=n(27023),w=n(39091),D=n(2445);const _=(0,i.I4)(w.i8)`
  && {
    margin: 0 0 ${({theme:e})=>e.gridUnit}px;
  }
`,F=({formData:e,addDangerToast:t})=>{const[n,a]=(0,r.useState)("400"),[i,l]=(0,r.useState)("600"),[d,c]=(0,r.useState)(""),[u,h]=(0,r.useState)(""),p=(0,r.useCallback)((e=>{const{value:t,name:n}=e.currentTarget;"width"===n&&l(t),"height"===n&&a(t)}),[]),m=(0,r.useCallback)((()=>{c(""),(0,b.Kx)(e).then((e=>{c(e),h("")})).catch((()=>{h((0,s.t)("Error")),t((0,s.t)("Sorry, something went wrong. Try again later."))}))}),[t,e]);(0,r.useEffect)((()=>{m()}),[]);const g=(0,r.useMemo)((()=>{if(!d)return"";const e=`${d}?${T.vX.standalone.name}=1&height=${n}`;return`<iframe\n  width="${i}"\n  height="${n}"\n  seamless\n  frameBorder="0"\n  scrolling="no"\n  src="${e}"\n>\n</iframe>`}),[n,d,i]),v=u||g||(0,s.t)("Generating link, please wait..");return(0,D.FD)("div",{id:"embed-code-popover",children:[(0,D.FD)("div",{css:o.AH`
          display: flex;
          flex-direction: column;
        `,children:[(0,D.Y)(A.A,{shouldShowText:!1,text:g,copyNode:(0,D.Y)(_,{buttonSize:"xsmall",children:(0,D.Y)("i",{className:"fa fa-clipboard"})})}),(0,D.Y)(S.fs,{name:"embedCode",disabled:!g,value:v,rows:"4",readOnly:!0,css:e=>o.AH`
            resize: vertical;
            padding: ${2*e.gridUnit}px;
            font-size: ${e.typography.sizes.s}px;
            border-radius: 4px;
            background-color: ${e.colors.secondary.light5};
          `})]}),(0,D.FD)("div",{css:e=>o.AH`
          display: flex;
          margin-top: ${4*e.gridUnit}px;
          & > div {
            margin-right: ${2*e.gridUnit}px;
          }
          & > div:last-of-type {
            margin-right: 0;
            margin-left: ${2*e.gridUnit}px;
          }
        `,children:[(0,D.FD)("div",{children:[(0,D.Y)("label",{htmlFor:"embed-height",children:(0,s.t)("Chart height")}),(0,D.Y)(S.pd,{type:"text",defaultValue:n,name:"height",onChange:p})]}),(0,D.FD)("div",{children:[(0,D.Y)("label",{htmlFor:"embed-width",children:(0,s.t)("Chart width")}),(0,D.Y)(S.pd,{type:"text",defaultValue:i,name:"width",onChange:p,id:"embed-width"})]})]})]})};var Y=n(71519);const I=({chartId:e,dashboards:t=[],...n})=>{const a=(0,i.DP)(),[l,u]=(0,r.useState)(),[h,p]=(0,r.useState)(),m=t.length>10,g=t.filter((e=>!l||e.dashboard_title.toLowerCase().includes(l.toLowerCase()))),b=0===t.length,v=l&&0===g.length,f=e?`?focused_chart=${e}`:"";return(0,D.FD)(D.FK,{children:[m&&(0,D.Y)(S.pd,{allowClear:!0,placeholder:(0,s.t)("Search"),prefix:(0,D.Y)(d.A.Search,{iconSize:"l"}),css:o.AH`
            width: ${220}px;
            margin: ${2*a.gridUnit}px ${3*a.gridUnit}px;
          `,value:l,onChange:e=>u(e.currentTarget.value)}),(0,D.FD)("div",{css:o.AH`
          max-height: ${300}px;
          overflow: auto;
        `,children:[g.map((e=>(0,D.Y)(c.W1.Item,{onMouseEnter:()=>p(e.id),onMouseLeave:()=>{h===e.id&&p(null)},...n,children:(0,D.Y)(Y.N_,{target:"_blank",rel:"noreferer noopener",to:`/superset/dashboard/${e.id}${f}`,children:(0,D.FD)("div",{css:o.AH`
                  display: flex;
                  flex-direction: row;
                  align-items: center;
                  max-width: ${220}px;
                `,children:[(0,D.Y)("div",{css:o.AH`
                    white-space: normal;
                  `,children:e.dashboard_title}),(0,D.Y)(d.A.Full,{iconSize:"l",iconColor:a.colors.grayscale.base,css:o.AH`
                    margin-left: ${2*a.gridUnit}px;
                    visibility: ${h===e.id?"visible":"hidden"};
                  `})]})})},String(e.id)))),v&&(0,D.Y)("div",{css:o.AH`
              margin-left: ${3*a.gridUnit}px;
              margin-bottom: ${a.gridUnit}px;
            `,children:(0,s.t)("No results found")}),b&&(0,D.Y)(c.W1.Item,{disabled:!0,css:o.AH`
              min-width: ${220}px;
            `,...n,children:(0,s.t)("None")})]})]})},$="edit_properties",E="export_to_csv",M="export_to_csv_pivoted",R="export_to_json",N="export_to_xlsx",k="download_as_image",O="copy_permalink",U="embed_code",q="share_by_email",L="view_query",z="run_in_sql_lab",H=["pivot_table_v2"],P=i.I4.div`
  ${({theme:e})=>o.AH`
    display: flex;
    align-items: center;

    & svg {
      width: ${3*e.gridUnit}px;
      height: ${3*e.gridUnit}px;
    }

    & span[role='checkbox'] {
      display: inline-flex;
      margin-right: ${e.gridUnit}px;
    }
  `}
`,j=((0,i.I4)(h.A)`
  ${({theme:e})=>o.AH`
    width: ${8*e.gridUnit}px;
    height: ${8*e.gridUnit}px;
    padding: 0;
    border: 1px solid ${e.colors.primary.dark2};

    &.ant-btn > span.anticon {
      line-height: 0;
      transition: inherit;
    }

    &:hover:not(:focus) > span.anticon {
      color: ${e.colors.primary.light1};
    }
  `}
`,o.AH`
  .ant-dropdown-menu-item > & > .anticon:first-child {
    margin-right: 0;
    vertical-align: 0;
  }
`),W=(e,t,n,o,h,S,A,...T)=>{const w=(0,i.DP)(),{addDangerToast:_,addSuccessToast:Y}=(0,p.Yf)(),P=(0,a.wA)(),[W,V]=(0,r.useState)(null),[B,G]=(0,r.useState)(!1),K=(0,a.d4)((e=>{var t;return null==(t=e.charts)?void 0:t[(0,m.kD)(e.explore)]})),{datasource:Q}=e,X=(0,r.useCallback)((async()=>{try{const t=(0,s.t)("Superset Chart"),n=await(0,b.Kx)(e),r=encodeURIComponent((0,s.t)("%s%s","Check out this chart: ",n));window.location.href=`mailto:?Subject=${t}%20&Body=${r}`}catch(e){_((0,s.t)("Sorry, something went wrong. Try again later."))}}),[_,e]),J=(0,r.useCallback)((()=>t?(0,m.RY)({formData:e,ownState:S,resultType:"full",resultFormat:"csv"}):null),[t,e]),Z=(0,r.useCallback)((()=>t?(0,m.RY)({formData:e,resultType:"post_processed",resultFormat:"csv"}):null),[t,e]),ee=(0,r.useCallback)((()=>t?(0,m.RY)({formData:e,resultType:"results",resultFormat:"json"}):null),[t,e]),te=(0,r.useCallback)((()=>t?(0,m.RY)({formData:e,resultType:"results",resultFormat:"xlsx"}):null),[t,e]),ne=(0,r.useCallback)((async()=>{try{if(!e)throw new Error;await(0,v.A)((()=>(0,b.Kx)(e))),Y((0,s.t)("Copied to clipboard!"))}catch(e){_((0,s.t)("Sorry, something went wrong. Try again later."))}}),[_,Y,e]),re=(0,r.useCallback)((({key:t,domEvent:r})=>{var a;switch(t){case $:h(),G(!1);break;case E:J(),G(!1),P((0,y.logEvent)(x.xb,{chartId:null==n?void 0:n.slice_id,chartName:null==n?void 0:n.slice_name}));break;case M:Z(),G(!1),P((0,y.logEvent)(x.vp,{chartId:null==n?void 0:n.slice_id,chartName:null==n?void 0:n.slice_name}));break;case R:ee(),G(!1),P((0,y.logEvent)(x.v2,{chartId:null==n?void 0:n.slice_id,chartName:null==n?void 0:n.slice_name}));break;case N:te(),G(!1),P((0,y.logEvent)(x.k8,{chartId:null==n?void 0:n.slice_id,chartName:null==n?void 0:n.slice_name}));break;case k:(0,g.A)(".panel-body .chart-container",null!=(a=null==n?void 0:n.slice_name)?a:(0,s.t)("New chart"),!0)(r),G(!1),P((0,y.logEvent)(x.C7,{chartId:null==n?void 0:n.slice_id,chartName:null==n?void 0:n.slice_name}));break;case O:ne(),G(!1);break;case U:G(!1);break;case q:X(),G(!1);break;case L:G(!1);break;case z:o(e,r.metaKey),G(!1)}}),[ne,J,Z,ee,e,o,h,X,null==n?void 0:n.slice_name]);return[(0,r.useMemo)((()=>(0,D.FD)(c.W1,{onClick:re,selectable:!1,...T,children:[(0,D.FD)(D.FK,{children:[n&&(0,D.Y)(c.W1.Item,{children:(0,s.t)("Edit chart properties")},$),(0,D.Y)(c.W1.SubMenu,{title:(0,s.t)("On dashboards"),children:(0,D.Y)(I,{chartId:null==n?void 0:n.slice_id,dashboards:A})},"dashboards_added_to"),(0,D.Y)(c.W1.Divider,{})]}),(0,D.FD)(c.W1.SubMenu,{title:(0,s.t)("Download"),children:[H.includes(e.viz_type)?(0,D.FD)(D.FK,{children:[(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileOutlined,{css:j}),disabled:!t,children:(0,s.t)("Export to original .CSV")},E),(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileOutlined,{css:j}),disabled:!t,children:(0,s.t)("Export to pivoted .CSV")},M)]}):(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileOutlined,{css:j}),disabled:!t,children:(0,s.t)("Export to .CSV")},E),(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileOutlined,{css:j}),disabled:!t,children:(0,s.t)("Export to .JSON")},R),(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileImageOutlined,{css:j}),children:(0,s.t)("Download as image")},k),(0,D.Y)(c.W1.Item,{icon:(0,D.Y)(d.A.FileOutlined,{css:j}),disabled:!t,children:(0,s.t)("Export to Excel")},N)]},"download_submenu"),(0,D.FD)(c.W1.SubMenu,{title:(0,s.t)("Share"),children:[(0,D.Y)(c.W1.Item,{children:(0,s.t)("Copy permalink to clipboard")},O),(0,D.Y)(c.W1.Item,{children:(0,s.t)("Share chart by email")},q),(0,l.G7)(l.TO.EmbeddableCharts)?(0,D.Y)(c.W1.Item,{children:(0,D.Y)(u.A,{triggerNode:(0,D.Y)("span",{children:(0,s.t)("Embed code")}),modalTitle:(0,s.t)("Embed code"),modalBody:(0,D.Y)(F,{formData:e,addDangerToast:_}),maxWidth:100*w.gridUnit+"px",destroyOnClose:!0,responsive:!0})},U):null]},"share_submenu"),(0,D.Y)(c.W1.Divider,{}),W?(0,D.FD)(D.FK,{children:[(0,D.Y)(c.W1.SubMenu,{title:(0,s.t)("Manage email report"),children:(0,D.Y)(f.A,{chart:K,setShowReportSubMenu:V,showReportSubMenu:W,setIsDropdownVisible:G,isDropdownVisible:B,useTextMenu:!0})}),(0,D.Y)(c.W1.Divider,{})]}):(0,D.Y)(c.W1,{children:(0,D.Y)(f.A,{chart:K,setShowReportSubMenu:V,setIsDropdownVisible:G,isDropdownVisible:B,useTextMenu:!0})}),(0,D.Y)(c.W1.Item,{children:(0,D.Y)(u.A,{triggerNode:(0,D.Y)("span",{children:(0,s.t)("View query")}),modalTitle:(0,s.t)("View query"),modalBody:(0,D.Y)(C.A,{latestQueryFormData:e}),draggable:!0,resizable:!0,responsive:!0})},L),Q&&(0,D.Y)(c.W1.Item,{children:(0,s.t)("Run in SQL Lab")},z)]})),[_,t,K,A,re,B,e,W,n,w.gridUnit]),B,G]}},28274:(e,t,n)=>{n.d(t,{A:()=>a});var r=n(67553);const a=["AND","AS","ASC","AVG","BY","CASE","COUNT","CREATE","CROSS","DATABASE","DEFAULT","DELETE","DESC","DISTINCT","DROP","ELSE","END","FOREIGN","FROM","GRANT","GROUP","HAVING","IF","INNER","INSERT","JOIN","KEY","LEFT","LIMIT","MAX","MIN","NATURAL","NOT","NULL","OFFSET","ON","OR","ORDER","OUTER","PRIMARY","REFERENCES","RIGHT","SELECT","SUM","TABLE","THEN","TYPE","UNION","UPDATE","WHEN","WHERE"].concat(["BIGINT","BINARY","BIT","CHAR","DATE","DECIMAL","DOUBLE","FLOAT","INT","INTEGER","MONEY","NUMBER","NUMERIC","REAL","SET","TEXT","TIMESTAMP","VARCHAR"]).map((e=>({meta:"sql",name:e,score:r.lI,value:e})))},67429:(e,t,n)=>{n.d(t,{C:()=>s});var r=n(17437),a=n(12249),i=n(19129),o=n(2445);const s=({title:e,color:t})=>(0,o.Y)(i.m,{title:e,placement:"top",children:(0,o.Y)(a.A.InfoCircleOutlined,{css:e=>r.AH`
        color: ${t||e.colors.text.label};
        margin-left: ${2*e.gridUnit}px;
        &.anticon {
          font-size: unset;
          .anticon {
            line-height: unset;
            vertical-align: unset;
          }
        }
      `})})},44230:(e,t,n)=>{n.d(t,{k:()=>de});var r=n(62193),a=n.n(r),i=n(96540),o=n(95579),s=n(17437),l=n(58642),d=n(96453),c=n(80145),u=n(58863),h=n(46302),p=n(61225),m=n(6749),g=n(61574),b=n(85861),v=n(46920),f=n(94229),y=n(84666),x=n(87903),C=n(62952),S=n(98250),A=n(17444),T=n(27023),w=n(2445);const D=function({value:e}){return(0,w.Y)("span",{children:e?T.bU:T.y2})},_=function(){return(0,w.Y)("span",{css:e=>s.AH`
        color: ${e.colors.grayscale.light1};
      `,children:T.bV})};var F=n(85170),Y=n(7349);const I=function({format:e=F.A.DATABASE_DATETIME,value:t}){return t?(0,w.Y)("span",{children:(0,Y.mo)(e).format(t)}):(0,w.Y)(_,{})};var $=n(87196),E=n(2514),M=n(51003),R=n(78697),N=n(15595),k=n(12249),O=n(10044);const U=function(e){const{headerTitle:t,groupTitle:n,groupOptions:r,value:a,onChange:o}=e,l=(0,d.DP)(),[c,u]=(0,i.useState)(!1);return(0,w.FD)("div",{css:s.AH`
        display: flex;
        align-items: center;
      `,children:[(0,w.Y)(O.A,{trigger:"click",visible:c,content:(0,w.FD)("div",{children:[(0,w.Y)("div",{css:s.AH`
                font-weight: ${l.typography.weights.bold};
                margin-bottom: ${l.gridUnit}px;
              `,children:n}),(0,w.Y)(R.s.Group,{value:a,onChange:e=>{o(e.target.value),u(!1)},children:(0,w.Y)(N.$x,{direction:"vertical",children:r.map((e=>(0,w.Y)(R.s,{value:e.value,children:e.label},e.value)))})})]}),placement:"bottomLeft",arrowPointAtCenter:!0,children:(0,w.Y)(k.A.SettingOutlined,{iconSize:"m",iconColor:l.colors.grayscale.light1,css:s.AH`
            margin-top: 3px; // we need exactly 3px to align the icon
            margin-right: ${l.gridUnit}px;
          `,onClick:()=>u(!0)})}),t]})};var q=n(86274),L=n(55976),z=n(66270),H=n(70700),P=n(26761);function j({filters:e,setFilters:t,totalCount:n,loading:r,onReload:a}){const l=(0,d.DP)(),c=(0,i.useMemo)((()=>Object.assign({},...e.map((e=>({[(0,H.q0)(e.col)?e.col.label:e.col]:e}))))),[e]),u=(0,i.useCallback)((e=>{const n={...c};delete n[e],t([...Object.values(n)])}),[c,t]),h=(0,i.useMemo)((()=>Object.entries(c).map((([e,{val:t,formattedVal:n}])=>({colName:e,val:null!=n?n:t}))).sort(((e,t)=>e.colName.localeCompare(t.colName)))),[c]);return(0,w.FD)("div",{css:s.AH`
        display: flex;
        justify-content: space-between;
        padding: ${l.gridUnit/2}px 0;
        margin-bottom: ${2*l.gridUnit}px;
      `,children:[(0,w.Y)("div",{css:s.AH`
          display: flex;
          flex-wrap: wrap;
          margin-bottom: -${4*l.gridUnit}px;
        `,children:h.map((({colName:e,val:t})=>(0,w.FD)(z.A,{closable:!0,onClose:u.bind(null,e),css:s.AH`
              height: ${6*l.gridUnit}px;
              display: flex;
              align-items: center;
              padding: ${l.gridUnit/2}px ${2*l.gridUnit}px;
              margin-right: ${4*l.gridUnit}px;
              margin-bottom: ${4*l.gridUnit}px;
              line-height: 1.2;
            `,children:[(0,w.Y)("span",{css:s.AH`
                margin-right: ${l.gridUnit}px;
              `,children:e}),(0,w.Y)("strong",{children:t})]},e)))}),(0,w.FD)("div",{css:s.AH`
          display: flex;
          align-items: center;
          height: min-content;
        `,children:[(0,w.Y)(P.A,{loading:r&&!n,rowcount:n}),(0,w.Y)(k.A.ReloadOutlined,{iconColor:l.colors.grayscale.light1,iconSize:"l","aria-label":(0,o.t)("Reload"),role:"button",onClick:a})]})]})}var W=n(90179),V=n.n(W),B=n(26632);const G=50;var K,Q={name:"82a6rk",styles:"flex:1"};function X({children:e}){const{ref:t,height:n}=(0,S.uZ)();return(0,w.Y)("div",{ref:t,css:Q,children:(0,i.cloneElement)(e,{height:n})})}function J({formData:e,initialFilters:t}){var n;const r=(0,d.DP)(),[a,l]=(0,i.useState)(0),c=(0,i.useRef)(a),[u,h]=(0,i.useState)(t),[m,g]=(0,i.useState)(!1),[b,v]=(0,i.useState)(""),[f,y]=(0,i.useState)(new Map),[S,T]=(0,i.useState)({}),F=(0,p.d4)((e=>e.common.conf.SAMPLES_ROW_LIMIT)),[Y,R]=(0,i.useMemo)((()=>e.datasource.split("__")),[e.datasource]),{metadataBar:N,status:k}=(0,L.M)({datasetId:Y}),O=(0,i.useMemo)((()=>{const e=f.get(a);return e?(c.current=a,e):f.get(c.current)}),[a,f]),z=(0,i.useMemo)((()=>(null==O?void 0:O.colNames.map(((e,t)=>({key:e,dataIndex:e,title:(null==O?void 0:O.colTypes[t])===x.s.Temporal?(0,w.Y)(U,{headerTitle:e,groupTitle:(0,o.t)("Formatting"),groupOptions:[{label:(0,o.t)("Original value"),value:K.Original},{label:(0,o.t)("Formatted value"),value:K.Formatted}],value:S[e]===K.Original?K.Original:K.Formatted,onChange:t=>T((n=>({...n,[e]:t})))}):e,render:n=>!0===n||!1===n?(0,w.Y)(D,{value:n}):null===n?(0,w.Y)(_,{}):(null==O?void 0:O.colTypes[t])===x.s.Temporal&&S[e]!==K.Original&&("number"==typeof n||n instanceof Date)?(0,w.Y)(I,{value:n}):String(n),width:150}))))||[]),[null==O?void 0:O.colNames,null==O?void 0:O.colTypes,S]),H=(0,i.useMemo)((()=>(null==O?void 0:O.data.map(((e,t)=>null==O?void 0:O.colNames.reduce(((t,n)=>({...t,[n]:e[n]})),{key:t}))))||[]),[null==O?void 0:O.colNames,null==O?void 0:O.data]),P=(0,i.useCallback)((()=>{v(""),y(new Map),l(0)}),[]);(0,i.useEffect)((()=>{v(""),y(new Map),l(0)}),[u]),(0,i.useEffect)((()=>{if(f.has(a)&&[...f.keys()].at(-1)!==a){const e=new Map(f);e.delete(a),y(e.set(a,f.get(a)))}}),[a,f]),(0,i.useEffect)((()=>{if(!b&&!m&&!f.has(a)){var t;g(!0);const n=null!=(t=function(e,t){if(!e)return;const n=(0,B.A)(e),r=V()(n.extras,"having"),a=[...(0,C.A)(n.filters),...(0,C.A)(t).map((e=>V()(e,"formattedVal")))];return{granularity:n.granularity,time_range:n.time_range,filters:a,extras:r}}(e,u))?t:{},r=Math.ceil(F/G);(0,E.getDatasourceSamples)(R,Y,!1,n,G,a+1).then((e=>{y(new Map([...[...f.entries()].slice(1-r),[a,{total:e.total_count,data:e.data,colNames:(0,C.A)(e.colnames),colTypes:(0,C.A)(e.coltypes)}]])),v("")})).catch((e=>{v(`${e.name}: ${e.message}`)})).finally((()=>{g(!1)}))}}),[F,Y,R,u,e,m,a,b,f]);const W=!b&&!f.size||k===q.bk.Loading,Q=null==(n=e.allow_render_html)||n;let J=null;if(b)J=(0,w.Y)("pre",{css:s.AH`
          margin-top: ${4*r.gridUnit}px;
        `,children:b});else if(W)J=(0,w.Y)(A.A,{});else if(0===(null==O?void 0:O.total)){const e=(0,o.t)("No rows were returned for this dataset");J=(0,w.Y)($.uq,{image:"document.svg",title:e})}else J=(0,w.Y)(X,{children:(0,w.Y)(M.Ay,{data:H,columns:z,size:M.QS.Small,defaultPageSize:G,recordCount:null==O?void 0:O.total,usePagination:!0,loading:m,onChange:e=>l(e.current?e.current-1:0),resizable:!0,virtualize:!0,allowHTML:Q})});return(0,w.FD)(w.FK,{children:[!W&&N,!W&&(0,w.Y)(j,{filters:u,setFilters:h,totalCount:null==O?void 0:O.total,loading:m,onReload:P}),J]})}!function(e){e[e.Original=0]="Original",e[e.Formatted=1]="Formatted"}(K||(K={}));const Z=({canExplore:e,closeModal:t,exploreChart:n})=>{const r=(0,d.DP)();return(0,w.FD)(w.FK,{children:[(0,w.Y)(v.A,{buttonStyle:"secondary",buttonSize:"small",onClick:n,disabled:!e,tooltip:e?void 0:(0,o.t)("You do not have sufficient permissions to edit the chart"),children:(0,o.t)("Edit chart")}),(0,w.Y)(v.A,{buttonStyle:"primary",buttonSize:"small",onClick:t,css:s.AH`
          margin-left: ${2*r.gridUnit}px;
        `,children:(0,o.t)("Close")})]})};function ee({chartId:e,formData:t,initialFilters:n,showModal:r,onHideModal:a}){const l=(0,d.DP)(),c=(0,g.W6)(),u=(0,i.useContext)(f.DashboardPageIdContext),{slice_name:h}=(0,p.d4)((t=>t.sliceEntities.slices[e])),m=(0,p.d4)((e=>{var t;return(0,y.L)("can_explore","Superset",null==(t=e.user)?void 0:t.roles)})),v=(0,i.useMemo)((()=>`/explore/?dashboard_page_id=${u}&slice_id=${e}`),[e,u]),x=(0,i.useCallback)((()=>{c.push(v)}),[v,c]);return(0,w.Y)(b.A,{show:r,onHide:null!=a?a:()=>null,css:s.AH`
        .ant-modal-body {
          display: flex;
          flex-direction: column;
        }
      `,title:(0,o.t)("Drill to detail: %s",h),footer:(0,w.Y)(Z,{exploreChart:x,canExplore:m}),responsive:!0,resizable:!0,resizableConfig:{minHeight:128*l.gridUnit,minWidth:128*l.gridUnit,defaultSize:{width:"auto",height:"75vh"}},draggable:!0,destroyOnClose:!0,maskClosable:!1,children:(0,w.Y)(J,{formData:t,initialFilters:n})})}var te=n(83537),ne=n(67429),re=n(28543);const ae=(0,o.t)("Drill to detail"),ie=(0,o.t)("Drill to detail by"),oe={DATABASE:(0,o.t)("Drill to detail is disabled for this database. Change the database settings to enable it."),NO_AGGREGATIONS:(0,o.t)("Drill to detail is disabled because this chart does not group data by dimension value."),NO_FILTERS:(0,o.t)("Right-click on a dimension value to drill to detail by that value."),NOT_SUPPORTED:(0,o.t)("Drill to detail by value is not yet supported for this chart type.")},se=({children:e,...t})=>(0,w.Y)(m.W1.Item,{disabled:!0,...t,children:(0,w.Y)("div",{css:s.AH`
        white-space: normal;
        max-width: 160px;
      `,children:e})}),le=(0,d.I4)((({children:e,stripHTML:t=!1})=>{const n=t&&"string"==typeof e?(0,l.zF)(e):e;return(0,w.Y)("span",{children:n})}))`
  ${({theme:e})=>`\n     font-weight: ${e.typography.weights.bold};\n     color: ${e.colors.primary.base};\n   `}
`,de=({chartId:e,formData:t,filters:n=[],isContextMenu:r=!1,contextMenuY:l=0,onSelection:d=(()=>null),onClick:g=(()=>null),submenuIndex:b=0,showModal:v,setShowModal:f,drillToDetailMenuRef:y,...x})=>{const C=(0,p.d4)((({datasources:e})=>{var n,r;return null==(n=e[t.datasource])||null==(r=n.database)?void 0:r.disable_drill_to_detail})),[S,A]=(0,i.useState)([]),T=(0,i.useCallback)(((e,t)=>{g(t),d(),A(e),f(!0)}),[g,d]),D=(0,i.useCallback)((()=>{f(!1)}),[]),_=(0,i.useMemo)((()=>{var e;return null==(e=(0,c.A)().get(t.viz_type))?void 0:e.behaviors.find((e=>e===u.nS.DrillToDetail))}),[t.viz_type]),F=(0,i.useMemo)((()=>{const{metrics:e}=(0,h.A)(t);return a()(e)}),[t]),Y=(0,i.useMemo)((()=>(0,te.Gs)(l,n.length>1?n.length+1:n.length,b)),[l,n.length,b]);let I,$;C?(I=oe.DATABASE,$=oe.DATABASE):_?F?(I=oe.NO_AGGREGATIONS,$=oe.NO_AGGREGATIONS):null!=n&&n.length||($=oe.NO_FILTERS):$=oe.NOT_SUPPORTED;const E=I?(0,s.n)(se,{...x,key:"drill-to-detail-disabled"},ae,(0,w.Y)(ne.C,{title:I})):(0,s.n)(m.W1.Item,{...x,key:"drill-to-detail",onClick:T.bind(null,[]),ref:y},ae),M=$?(0,s.n)(se,{...x,key:"drill-to-detail-by-disabled"},ie,(0,w.Y)(ne.C,{title:$})):(0,w.Y)(m.W1.SubMenu,{...x,popupOffset:[0,Y],popupClassName:"chart-context-submenu",title:ie,children:(0,w.FD)("div",{children:[n.map(((e,t)=>(0,s.n)(re.o,{...x,tooltipText:`${ie} ${e.formattedVal}`,key:`drill-detail-filter-${t}`,onClick:T.bind(null,[e])},`${ie} `,(0,w.Y)(le,{stripHTML:!0,children:e.formattedVal})))),n.length>1&&(0,s.n)(m.W1.Item,{...x,key:"drill-detail-filter-all",onClick:T.bind(null,n)},(0,w.FD)("div",{children:[`${ie} `,(0,w.Y)(le,{stripHTML:!1,children:(0,o.t)("all")})]}))]})});return(0,w.FD)(w.FK,{children:[E,r&&M,(0,w.Y)(ee,{chartId:e,formData:t,initialFilters:S,showModal:v,onHideModal:D})]})}},28543:(e,t,n)=>{n.d(t,{o:()=>l});var r=n(37827),a=n(17437),i=n(6749),o=n(19129),s=n(2445);const l=({tooltipText:e,children:t,...n})=>{const[l,d]=(0,r.A)();return(0,s.Y)(i.W1.Item,{css:a.AH`
        display: flex;
      `,...n,children:(0,s.Y)(o.m,{title:d?e:null,children:(0,s.Y)("div",{ref:l,css:a.AH`
            max-width: 100%;
            ${r.P};
          `,children:t})})})}},83537:(e,t,n)=>{n.d(t,{Gs:()=>a,x4:()=>r});const r=(e,t,n=Number.MAX_SAFE_INTEGER,r=0)=>{const a=Math.max(document.documentElement.clientHeight||0,window.innerHeight||0),i=Math.min(32*t,n)+32+r;return a-e<i?a-i:e},a=(e,t,n=0,a=Number.MAX_SAFE_INTEGER,i=0)=>{const o=e+4+32*n+4;return r(o,t,a,i)-o}},50068:(e,t,n)=>{n.d(t,{Dj:()=>s.Dj,cp:()=>s.cp,Ay:()=>o});var r=n(96453),a=n(2445);const i=r.I4.span`
  &,
  & svg {
    vertical-align: top;
  }
`;function o({checked:e,onChange:t,style:n,className:r}){return(0,a.Y)(i,{style:n,onClick:()=>{t(!e)},role:"checkbox",tabIndex:0,"aria-checked":e,"aria-label":"Checkbox",className:r||"",children:e?(0,a.Y)(s.Dj,{}):(0,a.Y)(s.cp,{})})}var s=n(75264)},93103:(e,t,n)=>{n.d(t,{R2:()=>p,ms:()=>h});var r=n(96540),a=n(15595),i=n(96453),o=n(12249),s=n(2445);const l=i.I4.div`
  width: ${({theme:e})=>.75*e.gridUnit}px;
  height: ${({theme:e})=>.75*e.gridUnit}px;
  border-radius: 50%;
  background-color: ${({theme:e})=>e.colors.grayscale.light1};

  font-weight: ${({theme:e})=>e.typography.weights.normal};
  display: inline-flex;
  position: relative;

  &:hover {
    background-color: ${({theme:e})=>e.colors.primary.base};

    &::before,
    &::after {
      background-color: ${({theme:e})=>e.colors.primary.base};
    }
  }

  &::before,
  &::after {
    position: absolute;
    content: ' ';
    width: ${({theme:e})=>.75*e.gridUnit}px;
    height: ${({theme:e})=>.75*e.gridUnit}px;
    border-radius: 50%;
    background-color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  &::before {
    top: ${({theme:e})=>e.gridUnit}px;
  }

  &::after {
    bottom: ${({theme:e})=>e.gridUnit}px;
  }
`,d=i.I4.div`
  display: flex;
  align-items: center;
  padding: ${({theme:e})=>2*e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`;var c;!function(e){e.Vertical="vertical",e.Horizontal="horizontal"}(c||(c={}));const u=(e=c.Vertical)=>e===c.Horizontal?(0,s.Y)(o.A.MoreHoriz,{iconSize:"xl"}):(0,s.Y)(l,{}),h=({overlay:e,iconOrientation:t=c.Vertical,...n})=>(0,s.Y)(a.rM,{overlay:e,...n,children:(0,s.Y)(d,{children:u(t)})}),p=e=>{const{children:t,onBlur:n,onKeyDown:i,...o}=e,l=(0,r.cloneElement)(t,{onBlur:n,onKeyDown:i});return(0,s.Y)(a.rM,{overlayStyle:e.overlayStyle,...o,children:l})}},25062:(e,t,n)=>{n.d(t,{J8:()=>m,Kg:()=>f,Pz:()=>y,pY:()=>p,px:()=>g,tg:()=>h});var r=n(96627),a=n(58863),i=n(27366),o=n(95579),s=n(88488),l=n(49588),d=n(81151),c=n(38708);const u=()=>{var e,t;const n=(0,c.A)();return(null==n||null==(e=n.common)||null==(t=e.conf)?void 0:t.NATIVE_FILTER_DEFAULT_ROW_LIMIT)||1e3},h=({datasetId:e,dependencies:t={},groupby:n,defaultDataMask:r,controlValues:a,filterType:i,sortMetric:o,adhoc_filters:l,time_range:d,granularity_sqla:c,type:h,dashboardId:p,id:m})=>{var g;const b={};return e&&(b.datasource=`${e}__table`),n&&(b.groupby=[n]),o&&(b.sortMetric=o),{...a,...b,adhoc_filters:null!=l?l:[],extra_filters:[],extra_form_data:t,granularity_sqla:c,metrics:["count"],row_limit:u(),showSearch:!0,defaultValue:null==r||null==(g=r.filterState)?void 0:g.value,time_range:d,url_params:(0,s.A)("regular"),inView:!0,viz_type:i,type:h,dashboardId:p,native_filter_id:m}};function p(e={},t={}){const n={};return r.t1.forEach((r=>{const a=[...e[r]||[],...t[r]||[]];a.length&&(n[r]=a)})),r.zk.forEach((r=>{const a=e[r];void 0!==a&&(n[r]=a);const i=t[r];void 0!==i&&(n[r]=i)})),n}function m(e,t){let n={};return t.forEach((t=>{var r,a;n=p(n,null!=(r=null==(a=e[t])?void 0:a.extraFormData)?r:{})})),n}function g(e){return!e.includes(a.nS.NativeFilter)||(0,i.G7)(i.TO.DashboardCrossFilters)&&e.includes(a.nS.InteractiveChart)}const b=(e,t)=>{var n;return(null==e||null==(n=e[t])?void 0:n.type)===l.B8},v=(e,t,n,r,a,i)=>{var o,s,d,c,u,h;i.has(n)||(i.add(n),(null==e||null==(o=e[n])?void 0:o.type)===l.oT&&t.includes(null==(s=e[n])||null==(d=s.meta)?void 0:d.chartId)&&r.forEach(a.add,a),0===(null==e||null==(c=e[n])||null==(u=c.children)?void 0:u.length)||b(e,n)&&a.has(n)||null==(h=e[n])||h.children.forEach((n=>v(e,t,n,b(e,n)?[...r,n]:r,a,i))))},f=(e,t)=>{const n=e[d.wv].children[0],r=n!==d.mK,a=new Set,i=new Set;var o,s;return r?null==(o=e[n])||null==(s=o.children)||s.forEach((n=>v(e,t,n,[n],a,i))):Object.values(e).filter((e=>(null==e?void 0:e.type)===l.B8)).forEach((n=>v(e,t,n.id,[n.id],a,i))),a},y=e=>null==e?"":"string"==typeof e||"number"==typeof e?`${e}`:Array.isArray(e)?e.join(", "):"object"==typeof e?JSON.stringify(e):(0,o.t)("Unknown value")},76295:(e,t,n)=>{n.d(t,{A:()=>d});var r=n(25062),a=n(35839);function i(e){return Object.entries(e).map((([e,t])=>({col:e,op:Array.isArray(t)?"IN":"==",val:t}))).filter((e=>null!==e.val))}var o=n(92008);const s={},l={};function d({chart:e,filters:t,nativeFilters:n,chartConfiguration:d,colorScheme:c,colorNamespace:u,sliceId:h,dataMask:p,extraControls:m,labelsColor:g,labelsColorMap:b,allSliceIds:v}){const f=l[h];if(s[h]===t&&(0,a.r$)(null==f?void 0:f.color_scheme,c,{ignoreUndefined:!0})&&(0,a.r$)(null==f?void 0:f.color_namespace,u,{ignoreUndefined:!0})&&(0,a.r$)(null==f?void 0:f.label_colors,g,{ignoreUndefined:!0})&&(0,a.r$)(null==f?void 0:f.shared_label_colors,b,{ignoreUndefined:!0})&&f&&(0,a.r$)(null==f?void 0:f.dataMask,p,{ignoreUndefined:!0})&&(0,a.r$)(null==f?void 0:f.extraControls,m,{ignoreUndefined:!0}))return f;let y={};const x=(0,o.R)({chartConfiguration:d,dataMask:p,nativeFilters:n,allSliceIds:v}),C=Object.entries(x).filter((([,{scope:t}])=>t.includes(e.id))).map((([e])=>e));C.length&&(y={extra_form_data:(0,r.J8)(p,C)});const S={...e.form_data,label_colors:g,shared_label_colors:b,...c&&{color_scheme:c},extra_filters:i(t),...y,...m};return s[h]=t,l[h]={...S,dataMask:p,extraControls:m},S}},39091:(e,t,n)=>{n.d(t,{$r:()=>M,TN:()=>D,XS:()=>N,ZY:()=>_,i8:()=>w});var r=n(17437),a=n(38221),i=n.n(a),o=n(96540),s=n(96453),l=n(95579),d=n(7349),c=n(85170),u=n(87903),h=n(58642),p=n(15595),m=n(90868),g=n(27023),b=n(78697),v=n(12249),f=n(46920),y=n(10044),x=n(15151),C=n(19966),S=n(86832),A=n(2445);const T=(0,s.I4)("span")`
  color: ${({theme:e})=>e.colors.grayscale.light1};
`,w=(0,s.I4)(f.A)`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;

  // needed to override button's first-of-type margin: 0
  && {
    margin: 0 ${({theme:e})=>2*e.gridUnit}px;
  }

  i {
    padding: 0 ${({theme:e})=>e.gridUnit}px;
  }
`,D=({data:e,columns:t})=>{const n=(0,s.DP)();return(0,A.Y)(C.A,{text:e&&t?(0,x.L)(e,t):"",wrapped:!1,copyNode:(0,A.Y)(v.A.CopyOutlined,{iconColor:n.colors.grayscale.base,iconSize:"l","aria-label":(0,l.t)("Copy"),role:"button",css:r.AH`
            &.anticon > * {
              line-height: 0;
            }
          `})})},_=({onChangeHandler:e,shouldFocus:t=!1})=>{const n=(0,o.useRef)(null);(0,o.useEffect)((()=>{n.current&&t&&n.current.focus()}),[]);const a=(0,s.DP)(),d=i()(e,g.Qs);return(0,A.Y)(m.pd,{prefix:(0,A.Y)(v.A.Search,{iconColor:a.colors.grayscale.base}),placeholder:(0,l.t)("Search"),onChange:e=>{const t=e.target.value;d(t)},css:r.AH`
        width: 200px;
        margin-right: ${2*a.gridUnit}px;
      `,ref:n})};var F;!function(e){e.Formatted="formatted",e.Original="original"}(F||(F={}));const Y=({onChange:e,value:t})=>(0,A.Y)(b.s.Group,{value:t,onChange:e,children:(0,A.FD)(p.$x,{direction:"vertical",children:[(0,A.Y)(b.s,{value:F.Formatted,children:(0,l.t)("Formatted date")}),(0,A.Y)(b.s,{value:F.Original,children:(0,l.t)("Original value")})]})}),I=s.I4.div`
  display: flex;
  flex-direction: column;

  padding: ${({theme:e})=>4*e.gridUnit+"px"};
`,$=s.I4.span`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,E=({columnName:e,onTimeColumnChange:t,datasourceId:n,isOriginalTimeColumn:a})=>{const i=(0,s.DP)(),d=n=>{t(e,n.target.value)},c=(0,o.useMemo)((()=>n?(0,A.FD)(I,{onClick:e=>e.stopPropagation(),children:[(0,A.Y)(r.mL,{styles:r.AH`
              .column-formatting-popover .ant-popover-inner-content {
                padding: 0;
              }
            `}),(0,A.Y)($,{children:(0,l.t)("Column Formatting")}),(0,A.Y)(Y,{onChange:d,value:a?F.Original:F.Formatted})]}):null),[n,a]);return n?(0,A.FD)("span",{children:[(0,A.Y)(y.A,{overlayClassName:"column-formatting-popover",trigger:"click",content:c,placement:"bottomLeft",arrowPointAtCenter:!0,children:(0,A.Y)(v.A.SettingOutlined,{iconSize:"m",iconColor:i.colors.grayscale.light1,css:(0,r.AH)({marginRight:`${i.gridUnit}px`},"",""),onClick:e=>e.stopPropagation()})}),e]}):(0,A.Y)("span",{children:e})},M=(e,t)=>{const n=(0,o.useMemo)((()=>{var e;return null!=(e=null==t?void 0:t.map((e=>Object.values(e).map((e=>e?e.toString().toLowerCase():(0,l.t)("N/A"))))))?e:[]}),[t]);return(0,o.useMemo)((()=>null!=t&&t.length?t.filter(((t,r)=>n[r].some((t=>null==t?void 0:t.includes(e.toLowerCase()))))):[]),[t,e,n])},R=(0,d.mo)(c.A.DATABASE_DATETIME),N=(e,t,n,r,a,i,s)=>{const[l,d]=(0,o.useState)((0,S.p)(r)),c=(e,t)=>{if(r)if(t!==F.Original||l.includes(e)){if(t===F.Formatted&&l.includes(e)){const t=(0,S.p)(r);t.splice(t.indexOf(e),1),(0,S.J)(r,t),d(t)}}else{const t=(0,S.p)(r);t.push(e),(0,S.J)(r,t),d(t)}};return(0,o.useEffect)((()=>{a&&d((0,S.p)(r))}),[r,a]),(0,o.useMemo)((()=>e&&null!=n&&n.length?e.filter((e=>Object.keys(n[0]).includes(e))).map(((e,a)=>{const o=null==t?void 0:t[a],d=n[0][e],p=o===u.s.Temporal?l.indexOf(e):-1,m=l.includes(e);return{id:e||a,accessor:t=>t[e],Header:o===u.s.Temporal&&"string"!=typeof d?(0,A.Y)(E,{columnName:e,datasourceId:r,onTimeColumnChange:c,isOriginalTimeColumn:m}):e,Cell:({value:e})=>!0===e?g.bU:!1===e?g.y2:null===e?(0,A.Y)(T,{children:g.bV}):o===u.s.Temporal&&-1===p&&"number"==typeof e?R(e):"string"==typeof e&&s?(0,h.nn)(e):String(e),...null==i?void 0:i[e]}})):[]),[e,n,t,r,i,l])}},86832:(e,t,n)=>{n.d(t,{J:()=>o,p:()=>i});var r=n(62952),a=n(62221);const i=e=>{const t=(0,a.Gq)(a.Hh.ExploreDataTableOriginalFormattedTimeColumns,{});return void 0===e?[]:(0,r.A)(t[e])},o=(e,t)=>{const n=(0,a.Gq)(a.Hh.ExploreDataTableOriginalFormattedTimeColumns,{});(0,a.SO)(a.Hh.ExploreDataTableOriginalFormattedTimeColumns,{...n,[e]:t})}},80493:(e,t,n)=>{n.d(t,{x:()=>g,y:()=>m});var r=n(65611),a=n.n(r),i=n(96540),o=n(96453),s=n(87903),l=n(17437),d=n(39091),c=n(15151),u=n(86832),h=n(26761),p=n(2445);const m=o.I4.div`
  ${({theme:e})=>`\n    display: flex;\n    align-items: center;\n    justify-content: space-between;\n    margin-bottom: ${2*e.gridUnit}px;\n\n    span {\n      flex-shrink: 0;\n    }\n  `}
`,g=({data:e,datasourceId:t,onInputChange:n,columnNames:r,columnTypes:o,rowcount:g,isLoading:b,canDownload:v})=>{const f=(0,u.p)(t),y=a()(r,o).filter((([e,t])=>t===s.s.Temporal&&e&&!f.includes(e))).map((([e])=>e)),x=(0,i.useMemo)((()=>(0,c.bE)(e,y)),[e,y]);return(0,p.FD)(m,{children:[(0,p.Y)(d.ZY,{onChangeHandler:n,shouldFocus:!0}),(0,p.FD)("div",{css:l.AH`
          display: flex;
          align-items: center;
        `,children:[(0,p.Y)(h.A,{rowcount:g,loading:b}),v&&(0,p.Y)(d.TN,{data:x,columns:r})]})]})}},8877:(e,t,n)=>{n.d(t,{U:()=>d});var r=n(96540),a=n(95579),i=n(50217),o=n(39091),s=n(80493),l=n(2445);const d=({data:e,colnames:t,coltypes:n,rowcount:d,datasourceId:c,dataSize:u=50,isVisible:h,canDownload:p})=>{const[m,g]=(0,r.useState)(""),b=(0,o.XS)(t,n,e,c,h,{},!0),v=(0,o.$r)(m,e);return(0,l.FD)(l.FK,{children:[(0,l.Y)(s.x,{data:v,columnNames:t,columnTypes:n,rowcount:d,datasourceId:c,onInputChange:e=>g(e),isLoading:!1,canDownload:p}),(0,l.Y)(i.A,{columns:b,data:v,pageSize:u,noDataText:(0,a.t)("No results"),emptyWrapperType:i.V.Small,className:"table-condensed",isPaginationSticky:!0,showRowCount:!1,small:!0})]})}},8786:(e,t,n)=>{n.d(t,{_h:()=>$,ih:()=>T});var r,a=n(96540),i=n(96453),o=n(27366),s=n(95579),l=n(12249),d=n(48327),c=n(62221);!function(e){e.Results="results",e.Samples="samples"}(r||(r={}));var u=n(80145),h=n(62952),p=n(51436),m=n(17444),g=n(87196),b=n(2514),v=n(8877),f=n(80493),y=n(2445);const x=i.I4.pre`
  margin-top: ${({theme:e})=>4*e.gridUnit+"px"};
`,C=new WeakMap,S=({isRequest:e,queryFormData:t,queryForce:n,ownState:r,errorMessage:i,actions:o,isVisible:l,dataSize:d=50,canDownload:c})=>{var S;const A=(0,u.A)().get((null==t?void 0:t.viz_type)||(null==t?void 0:t.vizType)),[T,w]=(0,a.useState)([]),[D,_]=(0,a.useState)(!0),[F,Y]=(0,a.useState)(""),I=null!=(S=null==A?void 0:A.queryObjectCount)?S:1;if((0,a.useEffect)((()=>{i||(e&&C.has(t)&&(w((0,h.A)(C.get(t))),Y(""),n&&o&&o.setForceQuery(!1),_(!1)),e&&!C.has(t)&&(_(!0),(0,b.getChartDataRequest)({formData:t,force:n,resultFormat:"json",resultType:"results",ownState:r}).then((({json:e})=>{w((0,h.A)(e.result)),Y(""),C.set(t,e.result),n&&o&&o.setForceQuery(!1)})).catch((e=>{(0,p.h4)(e).then((({error:e,message:t})=>{Y(e||t||(0,s.t)("Sorry, an error occurred"))}))})).finally((()=>{_(!1)}))))}),[t,e]),(0,a.useEffect)((()=>{i&&_(!1)}),[i]),D)return Array(I).fill((0,y.Y)(m.A,{}));if(i){const e=(0,s.t)("Run a query to display results");return Array(I).fill((0,y.Y)(g.uq,{image:"document.svg",title:e}))}if(F){const e=(0,y.FD)(y.FK,{children:[(0,y.Y)(f.x,{data:[],columnNames:[],columnTypes:[],rowcount:0,datasourceId:t.datasource,onInputChange:()=>{},isLoading:!1,canDownload:c}),(0,y.Y)(x,{children:F})]});return Array(I).fill(e)}if(0===T.length){const e=(0,s.t)("No results were returned for this query");return Array(I).fill((0,y.Y)(g.uq,{image:"document.svg",title:e}))}return T.slice(0,I).map(((e,n)=>(0,y.Y)(v.U,{data:e.data,colnames:e.colnames,coltypes:e.coltypes,rowcount:e.rowcount,dataSize:d,datasourceId:t.datasource,isVisible:l,canDownload:c},n)))},A=i.I4.div`
  display: flex;
  flex-direction: column;
  height: 100%;

  .ant-tabs {
    height: 100%;
  }

  .ant-tabs-content {
    height: 100%;
  }

  .ant-tabs-tabpane {
    display: flex;
    flex-direction: column;
  }

  .table-condensed {
    overflow: auto;
  }
`,T=({isRequest:e,queryFormData:t,queryForce:n,ownState:a,errorMessage:i,actions:o,isVisible:l,dataSize:c=50,canDownload:u})=>{const h=S({errorMessage:i,queryFormData:t,queryForce:n,ownState:a,isRequest:e,actions:o,dataSize:c,isVisible:l,canDownload:u});if(1===h.length)return(0,y.Y)(A,{children:h[0]});const p=h.map(((e,t)=>0===t?(0,y.Y)(d.Ay.TabPane,{tab:(0,s.t)("Results"),children:e},r.Results):(0,y.Y)(d.Ay.TabPane,{tab:(0,s.t)("Results %s",t+1),children:e},`${r.Results} ${t+1}`)));return(0,y.Y)(A,{children:(0,y.Y)(d.Ay,{fullWidth:!1,children:p})})};var w=n(50217),D=n(39091);const _=i.I4.pre`
  margin-top: ${({theme:e})=>4*e.gridUnit+"px"};
`,F=new WeakSet,Y=({isRequest:e,datasource:t,queryForce:n,actions:r,dataSize:i=50,isVisible:o,canDownload:l})=>{const[d,c]=(0,a.useState)(""),[u,p]=(0,a.useState)([]),[v,x]=(0,a.useState)([]),[C,S]=(0,a.useState)([]),[A,T]=(0,a.useState)(!1),[Y,I]=(0,a.useState)(0),[$,E]=(0,a.useState)(""),M=(0,a.useMemo)((()=>`${t.id}__${t.type}`),[t]);(0,a.useEffect)((()=>{e&&n&&F.delete(t),e&&!F.has(t)&&(T(!0),(0,b.getDatasourceSamples)(t.type,t.id,n,{}).then((e=>{p((0,h.A)(e.data)),x((0,h.A)(e.colnames)),S((0,h.A)(e.coltypes)),I(e.rowcount),E(""),F.add(t),n&&r&&r.setForceQuery(!1)})).catch((e=>{p([]),x([]),S([]),E(`${e.name}: ${e.message}`)})).finally((()=>{T(!1)})))}),[t,e,n]);const R=(0,D.XS)(v,C,u,M,o,{},!0),N=(0,D.$r)(d,u);if(A)return(0,y.Y)(m.A,{});if($)return(0,y.FD)(y.FK,{children:[(0,y.Y)(f.x,{data:N,columnNames:v,columnTypes:C,rowcount:Y,datasourceId:M,onInputChange:e=>c(e),isLoading:A,canDownload:l}),(0,y.Y)(_,{children:$})]});if(0===u.length){const e=(0,s.t)("No samples were returned for this dataset");return(0,y.Y)(g.uq,{image:"document.svg",title:e})}return(0,y.FD)(y.FK,{children:[(0,y.Y)(f.x,{data:N,columnNames:v,columnTypes:C,rowcount:Y,datasourceId:M,onInputChange:e=>c(e),isLoading:A,canDownload:l}),(0,y.Y)(w.A,{columns:R,data:N,pageSize:i,noDataText:(0,s.t)("No results"),emptyWrapperType:w.V.Small,className:"table-condensed",isPaginationSticky:!0,showRowCount:!1,small:!0})]})},I=i.I4.div`
  ${({theme:e})=>`\n    position: relative;\n    background-color: ${e.colors.grayscale.light5};\n    z-index: 5;\n    overflow: hidden;\n\n    .ant-tabs {\n      height: 100%;\n    }\n\n    .ant-tabs-content-holder {\n      height: 100%;\n    }\n\n    .ant-tabs-content {\n      height: 100%;\n    }\n\n    .ant-tabs-tabpane {\n      display: flex;\n      flex-direction: column;\n      height: 100%;\n\n      .table-condensed {\n        height: 100%;\n        overflow: auto;\n        margin-bottom: ${4*e.gridUnit}px;\n\n        .table {\n          margin-bottom: ${2*e.gridUnit}px;\n        }\n      }\n\n      .pagination-container > ul[role='navigation'] {\n        margin-top: 0;\n      }\n    }\n  `}
`,$=({queryFormData:e,datasource:t,queryForce:n,onCollapseChange:u,chartStatus:h,ownState:p,errorMessage:m,actions:g,canDownload:b})=>{const v=(0,i.DP)(),[x,C]=(0,a.useState)(r.Results),[A,T]=(0,a.useState)({results:!1,samples:!1}),[w,D]=(0,a.useState)(!(0,o.G7)(o.TO.DatapanelClosedByDefault)&&(0,c.Gq)(c.Hh.IsDatapanelOpen,!1));(0,a.useEffect)((()=>{(0,o.G7)(o.TO.DatapanelClosedByDefault)||(0,c.SO)(c.Hh.IsDatapanelOpen,w)}),[w]),(0,a.useEffect)((()=>{w||T({results:!1,samples:!1}),w&&x.startsWith(r.Results)&&h&&"loading"!==h&&T({results:!0,samples:!1}),w&&x===r.Samples&&T({results:!1,samples:!0})}),[w,x,h]);const _=(0,a.useCallback)((e=>{u(e),D(e)}),[u]),F=(0,a.useCallback)(((e,t)=>{w?e===x&&(t.preventDefault(),_(!1)):_(!0),C(e)}),[x,_,w]),$=(0,a.useMemo)((()=>{const e=w?(0,y.Y)(l.A.CaretUp,{iconColor:v.colors.grayscale.base,"aria-label":(0,s.t)("Collapse data panel")}):(0,y.Y)(l.A.CaretDown,{iconColor:v.colors.grayscale.base,"aria-label":(0,s.t)("Expand data panel")});return(0,y.Y)(f.y,{children:w?(0,y.Y)("span",{role:"button",tabIndex:0,onClick:()=>_(!1),children:e}):(0,y.Y)("span",{role:"button",tabIndex:0,onClick:()=>_(!0),children:e})})}),[_,w,v.colors.grayscale.base]),E=S({errorMessage:m,queryFormData:e,queryForce:n,ownState:p,isRequest:A.results,actions:g,isVisible:r.Results===x,canDownload:b}).map(((e,t)=>0===t?(0,y.Y)(d.Ay.TabPane,{tab:(0,s.t)("Results"),children:e},r.Results):t>0?(0,y.Y)(d.Ay.TabPane,{tab:(0,s.t)("Results %s",t+1),children:e},`${r.Results} ${t+1}`):null));return(0,y.Y)(I,{children:(0,y.FD)(d.Ay,{fullWidth:!1,tabBarExtraContent:$,activeKey:w?x:"",onTabClick:F,children:[E,(0,y.Y)(d.Ay.TabPane,{tab:(0,s.t)("Samples"),children:(0,y.Y)(Y,{datasource:t,queryForce:n,isRequest:A.samples,actions:g,isVisible:r.Samples===x,canDownload:b})},r.Samples)]})})}},28254:(e,t,n)=>{var r;n.d(t,{S:()=>r}),function(e){e.Column="column",e.ColumnOption="columnOption",e.AdhocColumnOption="adhocColumn",e.Metric="metric",e.MetricOption="metricOption",e.AdhocMetricOption="adhocMetric",e.FilterOption="filterOption"}(r||(r={}))},16238:(e,t,n)=>{n.d(t,{y:()=>r});const r=n(96453).I4.div`
  .edit-popover-resize {
    transform: scaleX(-1);
    float: right;
    margin-top: ${({theme:e})=>4*e.gridUnit}px;
    margin-right: ${({theme:e})=>-2*e.gridUnit}px;
    cursor: nwse-resize;
  }
  .filter-sql-editor {
    border: ${({theme:e})=>e.colors.grayscale.light2} solid thin;
  }
`},26761:(e,t,n)=>{n.d(t,{A:()=>d});var r=n(95579),a=n(32142),i=n(2738),o=n(19129),s=n(2445);const l=(0,r.t)("The row limit set for the chart was reached. The chart may show partial data.");function d(e){const{rowcount:t=0,limit:n=null,loading:d}=e,c=n&&t>=n,u=c||0===t&&!d?"danger":"default",h=(0,a.gV)()(t),p=(0,s.Y)(i.A,{type:u,children:d?(0,r.t)("Loading..."):(0,s.Y)("span",{children:(0,r.tn)("%s row","%s rows",t,h)})});return c?(0,s.Y)(o.m,{id:"tt-rowcount-tooltip",title:(0,s.Y)("span",{children:l}),children:p}):p}},23133:(e,t,n)=>{n.d(t,{A:()=>J});var r=n(96540),a=n(5556),i=n.n(a),o=n(46920),s=n(96453),l=n(95579),d=n(49544),c=n(48327),u=n(8901),h=n(90422),p=n(86523),m=n(15595),g=n(13270),b=n(35742),v=n(27366),f=n(95483),y=n(84064),x=n(19129),C=n(90868),S=n(15151),A=n(67984),T=n(38221),w=n.n(T),D=n(62952),_=n(58561),F=n.n(_);const Y={parsedAdvancedDataType:"",advancedDataTypeOperatorList:[],errorMessage:""};var I=n(59638),$=n(39942),E=n(2511),M=n(2445);const R=(0,s.I4)(C.pd)`
  margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
`,N=((0,s.I4)(p.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,(0,s.I4)(m.l6)`
  .ant-select-selector::after {
    content: ${({labelText:e})=>e||"\\A0"};
    display: inline-block;
    white-space: nowrap;
    color: ${({theme:e})=>e.colors.grayscale.light1};
    width: max-content;
  }
`),k=e=>{var t,n;const{onSubjectChange:a,onOperatorChange:i,isOperatorRelevant:o,onComparatorChange:s,onDatePickerChange:d}=(e=>{const t=(0,$.IM)(),n=(t,n)=>{var r;const a=null==(r=e.datasource.columns)?void 0:r.find((e=>e.column_name===n)),i=!!a&&("BOOL"===a.type||"BOOLEAN"===a.type),o=!!a&&("INT"===a.type||"INTEGER"===a.type),s=!!a&&!!a.expression;if(t&&t===f.ux.LatestPartition){const{partitionColumn:t}=e;return t&&n&&n===t}return(!t||t!==f.ux.TemporalRange)&&(t===f.ux.IsTrue||t===f.ux.IsFalse?i||o||s:i?t===f.ux.IsNull||t===f.ux.IsNotNull:e.adhocFilter.clause!==E.v.Having||-1!==f._T.indexOf(t))};return{onSubjectChange:r=>{const a=e.options.find((e=>"column_name"in e&&e.column_name===r||"optionName"in e&&e.optionName===r));let i,o="";a&&"column_name"in a?(o=a.column_name,i=E.v.Where):a&&"saved_metric_name"in a?(o=a.saved_metric_name,i=E.v.Having):null!=a&&a.label&&(o=a.label,i=E.v.Having);let{operator:s,operatorId:l,comparator:d}=e.adhocFilter;s=s&&l&&n(l,o)?f.nS[l].operation:null,(0,g.A)(s)||(s=f.ux.In,l=f.ux.In,d=void 0),(0,A.D)(r,e.datasource)&&(o=r,s=f.ux.TemporalRange,l=f.ux.TemporalRange,d=t),e.onChange(e.adhocFilter.duplicateWith({subject:o,clause:i,operator:s,expressionType:E.A.Simple,operatorId:l,comparator:d}))},onOperatorChange:t=>{const n=e.adhocFilter.comparator;let r;r=f.sJ.has(t)?Array.isArray(n)?n:[n].filter((e=>e)):Array.isArray(n)?n[0]:n,t!==f.ux.IsTrue&&t!==f.ux.IsFalse||(r=f.ux.IsTrue===t),t&&f.Wy.has(t)?e.onChange(e.adhocFilter.duplicateWith({subject:e.adhocFilter.subject,clause:E.v.Where,operatorId:t,operator:f.nS[t].operation,expressionType:E.A.Sql,datasource:e.datasource})):e.onChange(e.adhocFilter.duplicateWith({operatorId:t,operator:f.nS[t].operation,comparator:r,expressionType:E.A.Simple}))},onComparatorChange:t=>{e.onChange(e.adhocFilter.duplicateWith({comparator:t,expressionType:E.A.Simple}))},isOperatorRelevant:n,clearOperator:()=>{e.onChange(e.adhocFilter.duplicateWith({operatorId:void 0,operator:void 0}))},onDatePickerChange:(t,n)=>{e.onChange(e.adhocFilter.duplicateWith({subject:t,operator:f.ux.TemporalRange,comparator:n,expressionType:E.A.Simple}))}}})(e),[c,u]=(0,r.useState)([]),[h,p]=(0,r.useState)(e.adhocFilter.comparator),[C,T]=(0,r.useState)(!1),{advancedDataTypesState:_,subjectAdvancedDataType:k,fetchAdvancedDataTypeValueCallback:O,fetchSubjectAdvancedDataType:U}=(e=>{const[t,n]=(0,r.useState)(Y),[a,i]=(0,r.useState)(),o=(0,r.useCallback)(((t,r,a)=>{const i=(0,D.A)(t);a?w()((()=>{const t=`/api/v1/advanced_data_type/convert?q=${F().encode({type:a,values:i})}`;b.A.get({endpoint:t}).then((({json:t})=>{n({parsedAdvancedDataType:t.result.display_value,advancedDataTypeOperatorList:t.result.valid_filter_operators,errorMessage:t.result.error_message}),e(!t.result.error_message)})).catch((()=>{n({parsedAdvancedDataType:"",advancedDataTypeOperatorList:r.advancedDataTypeOperatorList,errorMessage:(0,l.t)("Failed to retrieve advanced type")}),e(!1)}))}),600)():n(Y)}),[e]);return{advancedDataTypesState:t,subjectAdvancedDataType:a,setAdvancedDataTypesState:n,fetchAdvancedDataTypeValueCallback:o,fetchSubjectAdvancedDataType:e=>{const t=e.options.find((t=>"column_name"in t&&t.column_name===e.adhocFilter.subject||"optionName"in t&&t.optionName===e.adhocFilter.subject));t&&"advanced_data_type"in t?i(t.advanced_data_type):e.validHandler(!0)}}})(e.validHandler),q=(e,t)=>k?o(e,t)&&_.advancedDataTypeOperatorList.includes(e):o(e,t),L=()=>{const e=(()=>{var e;const t=Array.isArray(h)?h.filter((e=>c.includes(e))).length:0;return null!=(e=(null==c?void 0:c.length)-t)?e:0})(),t=(0,l.t)("%s option(s)",e);return e?t:""};let z=e.options;const{subject:H,operator:P,operatorId:j}=e.adhocFilter,W={ariaLabel:(0,l.t)("Select subject"),value:null!=H?H:void 0,onChange:e=>{p(void 0),a(e)},notFoundContent:(0,l.t)("No such column found. To filter on a metric, try the Custom SQL tab."),autoFocus:!H,placeholder:""};W.placeholder=e.adhocFilter.clause===E.v.Where?(0,l.t)("%s column(s)",z.length):(0,l.t)("To filter on a metric, use Custom SQL tab."),z=e.options.filter((e=>"column_name"in e&&e.column_name));const V={placeholder:(0,l.t)("%s operator(s)",(null!=(t=e.operators)?t:f.RX).filter((e=>q(e,H))).length),value:j,onChange:i,autoFocus:!!W.value&&!P,ariaLabel:(0,l.t)("Select operator")},B=!!W.value&&!!V.value,G={allowClear:!0,allowNewOptions:!0,ariaLabel:(0,l.t)("Comparator option"),mode:f.sJ.has(j)?"multiple":"single",loading:C,value:h,onChange:s,notFoundContent:(0,l.t)("Type a value here"),disabled:f.Sd.includes(j),placeholder:L(),autoFocus:B},K=h&&h.length>0&&L(),Q=(0,I.w)({columnName:e.adhocFilter.subject,timeRange:e.adhocFilter.operator===f.ux.TemporalRange?e.adhocFilter.comparator:void 0,datasource:e.datasource,onChange:d});(0,r.useEffect)((()=>{Q||(()=>{const{datasource:t}=e,n=e.adhocFilter.subject,r=e.adhocFilter.clause===E.v.Having;if(n&&t&&t.filter_select&&!r){const e=new AbortController,{signal:r}=e;C&&e.abort(),T(!0),b.A.get({signal:r,endpoint:`/api/v1/datasource/${t.type}/${t.id}/column/${n}/values/`}).then((({json:e})=>{u(e.result.map((e=>({value:e,label:(0,S.ed)(e)})))),T(!1)})).catch((()=>{u([]),T(!1)}))}})()}),[e.adhocFilter.subject]),(0,r.useEffect)((()=>{(0,v.G7)(v.TO.EnableAdvancedDataTypes)&&U(e)}),[e.adhocFilter.subject]),(0,r.useEffect)((()=>{(0,v.G7)(v.TO.EnableAdvancedDataTypes)&&O(void 0===h?"":h,_,k)}),[h,k,O]),(0,r.useEffect)((()=>{(0,v.G7)(v.TO.EnableAdvancedDataTypes)&&p(e.adhocFilter.comparator)}),[e.adhocFilter.comparator]);const X=(0,M.Y)(m.l6,{css:e=>({marginTop:4*e.gridUnit,marginBottom:4*e.gridUnit}),options:z.map((e=>{return{value:"column_name"in e&&e.column_name||"optionName"in e&&e.optionName||"",label:"saved_metric_name"in e&&e.saved_metric_name||"column_name"in e&&e.column_name||"label"in e&&e.label,key:"id"in e&&e.id||"optionName"in e&&e.optionName||void 0,customLabel:(t=e,(0,M.Y)(y.A,{option:t}))};var t})),...W}),J=(0,M.FD)(M.FK,{children:[(0,M.Y)(m.l6,{css:e=>({marginBottom:4*e.gridUnit}),options:(null!=(n=e.operators)?n:f.RX).filter((e=>q(e,H))).map(((e,t)=>({value:e,label:f.nS[e].display,key:e,order:t}))),...V}),f.sJ.has(j)||c.length>0?(0,M.Y)(x.m,{title:_.errorMessage||_.parsedAdvancedDataType,children:(0,M.Y)(N,{labelText:K,options:c,...G})}):(0,M.Y)(x.m,{title:_.errorMessage||_.parsedAdvancedDataType,children:(0,M.Y)(R,{name:"filter-value",ref:e=>{e&&B&&e.focus()},onChange:e=>{const{value:t}=e.target;p(t),s(t)},value:h,placeholder:(0,l.t)("Filter value (case sensitive)"),disabled:f.Sd.includes(j)})})]});return(0,M.FD)(M.FK,{children:[X,null!=Q?Q:J]})};var O=n(24976),U=n(28274),q=n(92013),L=n(21062);const z={adhocFilter:i().instanceOf(h.A).isRequired,onChange:i().func.isRequired,options:i().arrayOf(i().oneOfType([L.A,i().shape({saved_metric_name:i().string.isRequired}),u.A])).isRequired,height:i().number.isRequired},H=(0,s.I4)(m.l6)`
  ${({theme:e})=>`\n    width: ${30*e.gridUnit}px;\n    marginRight: ${e.gridUnit}px;\n  `}
`;class P extends r.Component{constructor(e){super(e),this.onSqlExpressionChange=this.onSqlExpressionChange.bind(this),this.onSqlExpressionClauseChange=this.onSqlExpressionClauseChange.bind(this),this.handleAceEditorRef=this.handleAceEditorRef.bind(this)}componentDidUpdate(){this.aceEditorRef&&this.aceEditorRef.editor.resize()}onSqlExpressionClauseChange(e){this.props.onChange(this.props.adhocFilter.duplicateWith({clause:e,expressionType:E.A.Sql}))}onSqlExpressionChange(e){this.props.onChange(this.props.adhocFilter.duplicateWith({sqlExpression:e,expressionType:E.A.Sql}))}handleAceEditorRef(e){e&&(this.aceEditorRef=e)}render(){const{adhocFilter:e,height:t,options:n}=this.props,r=U.A.concat((0,q.r)(n.filter((e=>e.column_name)))),a=Object.values(E.v).map((e=>({label:e,value:e})));return(0,M.FD)("span",{children:[(0,M.FD)("div",{className:"filter-edit-clause-section",children:[(0,M.Y)("div",{children:(0,M.Y)(H,{options:a,ariaLabel:(0,l.t)("Select column"),placeholder:(0,l.t)("choose WHERE or HAVING..."),value:e.clause,onChange:this.onSqlExpressionClauseChange})}),(0,M.FD)("span",{className:"filter-edit-clause-info",children:[(0,M.Y)("strong",{children:"WHERE"})," ",(0,l.t)("Filters by columns"),(0,M.Y)("br",{}),(0,M.Y)("strong",{children:"HAVING"})," ",(0,l.t)("Filters by metrics")]})]}),(0,M.Y)("div",{css:e=>({marginTop:4*e.gridUnit}),children:(0,M.Y)(O.YU,{ref:this.handleAceEditorRef,keywords:r,height:t-130+"px",onChange:this.onSqlExpressionChange,width:"100%",showGutter:!1,value:e.sqlExpression||e.translateToSql(),editorProps:{$blockScrolling:!0},enableLiveAutocompletion:!0,className:"filter-sql-editor",wrapEnabled:!0})})]})}}P.propTypes=z;const j={adhocFilter:i().instanceOf(h.A).isRequired,onChange:i().func.isRequired,onClose:i().func.isRequired,onResize:i().func.isRequired,options:i().arrayOf(i().oneOfType([L.A,i().shape({saved_metric_name:i().string.isRequired}),u.A])).isRequired,datasource:i().object,partitionColumn:i().string,theme:i().object,sections:i().arrayOf(i().string),operators:i().arrayOf(i().string),requireSave:i().bool},W=s.I4.i`
  margin-left: ${({theme:e})=>2*e.gridUnit}px;
`,V=s.I4.div`
  .adhoc-filter-edit-tabs > .nav-tabs {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;

    & > li > a {
      padding: ${({theme:e})=>e.gridUnit}px;
    }
  }

  #filter-edit-popover {
    max-width: none;
  }

  .filter-edit-clause-info {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
  }

  .filter-edit-clause-section {
    display: flex;
    flex-direction: row;
    gap: ${({theme:e})=>5*e.gridUnit}px;
  }

  .adhoc-filter-simple-column-dropdown {
    margin-top: ${({theme:e})=>5*e.gridUnit}px;
  }
`,B=s.I4.div`
  margin-top: ${({theme:e})=>2*e.gridUnit}px;
`;class G extends r.Component{constructor(e){var t,n;super(e),this.onSave=this.onSave.bind(this),this.onDragDown=this.onDragDown.bind(this),this.onMouseMove=this.onMouseMove.bind(this),this.onMouseUp=this.onMouseUp.bind(this),this.onAdhocFilterChange=this.onAdhocFilterChange.bind(this),this.setSimpleTabIsValid=this.setSimpleTabIsValid.bind(this),this.adjustHeight=this.adjustHeight.bind(this),this.onTabChange=this.onTabChange.bind(this),this.state={adhocFilter:this.props.adhocFilter,width:f._R,height:f.Z_,activeKey:(null==(t=this.props)||null==(n=t.adhocFilter)?void 0:n.expressionType)||"SIMPLE",isSimpleTabValid:!0},this.popoverContentRef=(0,r.createRef)()}componentDidMount(){document.addEventListener("mouseup",this.onMouseUp)}componentWillUnmount(){document.removeEventListener("mouseup",this.onMouseUp),document.removeEventListener("mousemove",this.onMouseMove)}onAdhocFilterChange(e){this.setState({adhocFilter:e})}setSimpleTabIsValid(e){this.setState({isSimpleTabValid:e})}onSave(){this.props.onChange(this.state.adhocFilter),this.props.onClose()}onDragDown(e){this.dragStartX=e.clientX,this.dragStartY=e.clientY,this.dragStartWidth=this.state.width,this.dragStartHeight=this.state.height,document.addEventListener("mousemove",this.onMouseMove)}onMouseMove(e){this.props.onResize(),this.setState({width:Math.max(this.dragStartWidth+(e.clientX-this.dragStartX),f._R),height:Math.max(this.dragStartHeight+(e.clientY-this.dragStartY),f.Z_)})}onMouseUp(){document.removeEventListener("mousemove",this.onMouseMove)}onTabChange(e){this.setState({activeKey:e})}adjustHeight(e){this.setState((t=>({height:t.height+e})))}render(){const{adhocFilter:e,options:t,onChange:n,onClose:r,onResize:a,datasource:i,partitionColumn:s,theme:u,operators:h,requireSave:p,...m}=this.props,{adhocFilter:g}=this.state,b=g.isValid(),v=p||!g.equals(e);return(0,M.FD)(V,{id:"filter-edit-popover",...m,ref:this.popoverContentRef,children:[(0,M.FD)(c.Ay,{id:"adhoc-filter-edit-tabs",defaultActiveKey:g.expressionType,className:"adhoc-filter-edit-tabs",style:{minHeight:this.state.height,width:this.state.width},allowOverflow:!0,onChange:this.onTabChange,children:[(0,M.Y)(c.Ay.TabPane,{className:"adhoc-filter-edit-tab",tab:(0,l.t)("Simple"),children:(0,M.Y)(d.A,{children:(0,M.Y)(k,{operators:h,adhocFilter:this.state.adhocFilter,onChange:this.onAdhocFilterChange,options:t,datasource:i,onHeightChange:this.adjustHeight,partitionColumn:s,popoverRef:this.popoverContentRef.current,validHandler:this.setSimpleTabIsValid})})},E.A.Simple),(0,M.Y)(c.Ay.TabPane,{className:"adhoc-filter-edit-tab",tab:(0,l.t)("Custom SQL"),children:(0,M.Y)(d.A,{children:(0,M.Y)(P,{adhocFilter:this.state.adhocFilter,onChange:this.onAdhocFilterChange,options:this.props.options,height:this.state.height,activeKey:this.state.activeKey})})},E.A.Sql)]}),(0,M.FD)(B,{children:[(0,M.Y)(o.A,{buttonSize:"small",onClick:this.props.onClose,cta:!0,children:(0,l.t)("Close")}),(0,M.Y)(o.A,{disabled:!b||!this.state.isSimpleTabValid||!v,buttonStyle:"primary",buttonSize:"small",className:"m-r-5",onClick:this.onSave,cta:!0,children:(0,l.t)("Save")}),(0,M.Y)(W,{role:"button","aria-label":"Resize",tabIndex:0,onMouseDown:this.onDragDown,className:"fa fa-expand edit-popover-resize text-muted"})]})]})}}G.propTypes=j;var K=n(16238),Q=n(22533);class X extends r.PureComponent{constructor(e){super(e),this.onPopoverResize=this.onPopoverResize.bind(this),this.closePopover=this.closePopover.bind(this),this.togglePopover=this.togglePopover.bind(this),this.state={popoverVisible:!1}}onPopoverResize(){this.forceUpdate()}closePopover(){this.togglePopover(!1)}togglePopover(e){this.setState({popoverVisible:e})}render(){const{adhocFilter:e,isControlledComponent:t}=this.props,{visible:n,togglePopover:r,closePopover:a}=t?{visible:this.props.visible,togglePopover:this.props.togglePopover,closePopover:this.props.closePopover}:{visible:this.state.popoverVisible,togglePopover:this.togglePopover,closePopover:this.closePopover},i=(0,M.Y)(K.y,{children:(0,M.Y)(G,{adhocFilter:e,options:this.props.options,datasource:this.props.datasource,partitionColumn:this.props.partitionColumn,onResize:this.onPopoverResize,onClose:a,sections:this.props.sections,operators:this.props.operators,onChange:this.props.onFilterEdit,requireSave:this.props.requireSave})});return(0,M.Y)(Q.A,{trigger:"click",content:i,defaultVisible:n,visible:n,onVisibleChange:r,destroyTooltipOnHide:!0,children:this.props.children})}}const J=X},2511:(e,t,n)=>{var r,a;n.d(t,{A:()=>r,v:()=>a}),function(e){e.Simple="SIMPLE",e.Sql="SQL"}(r||(r={})),function(e){e.Having="HAVING",e.Where="WHERE"}(a||(a={}))},59638:(e,t,n)=>{n.d(t,{w:()=>m,K:()=>l});var r=n(96540),a=n(96627),i=n(77189),o=n(95483),s=n(2511);const l=e=>{const[t,n]=(0,r.useState)({});return(0,r.useEffect)((()=>{e.operator===o.ux.TemporalRange&&e.expressionType===s.A.Simple||n({}),e.operator===o.ux.TemporalRange&&e.comparator===a.WC&&n({actualTimeRange:`${e.subject} (${a.WC})`,title:a.WC}),e.operator===o.ux.TemporalRange&&e.expressionType===s.A.Simple&&e.comparator!==a.WC&&t.title!==e.comparator&&(0,i.x9)(e.comparator,e.subject).then((({value:t,error:r})=>{n(r?{actualTimeRange:`${e.subject} (${e.comparator})`,title:r}:{actualTimeRange:null!=t?t:"",title:e.comparator})}))}),[e]),t};var d=n(95579),c=n(67984),u=n(45267),h=n(50317),p=n(2445);const m=({columnName:e,timeRange:t,datasource:n,onChange:r})=>(0,c.D)(e,n)?(0,p.FD)(p.FK,{children:[(0,p.Y)(h.A,{label:(0,d.t)("Time Range")}),(0,p.Y)(u.A,{value:t,name:"time_range",onChange:t=>r(e,t),overlayStyle:"Modal"})]}):void 0},71191:(e,t,n)=>{n.d(t,{e:()=>s});var r=n(808),a=n(95483),i=n(85183);const o={"==":"=","!=":"<>",">":">","<":"<",">=":">=","<=":"<=",IN:"IN","NOT IN":"NOT IN",LIKE:"LIKE",ILIKE:"ILIKE",REGEX:"REGEX","IS NOT NULL":"IS NOT NULL","IS NULL":"IS NULL","IS TRUE":"IS TRUE","IS FALSE":"IS FALSE","LATEST PARTITION":({datasource:e})=>`= '{{ presto.latest_partition('${e.schema}.${e.datasource_name}') }}'`},s=(e,{useSimple:t}={useSimple:!1})=>{if((0,r.md)(e)||t){const{subject:t,operator:n}=e,r="comparator"in e?e.comparator:void 0,s=n&&n===a.nS[a.ux.LatestPartition].operation?o[n](e):o[n];return(0,i.zJ)(t,s,r)}return(0,r.wF)(e)?e.sqlExpression:""}},72652:(e,t,n)=>{n.d(t,{B3:()=>C,Bt:()=>f,Gh:()=>y,JG:()=>w,JU:()=>b,Px:()=>_,XB:()=>D,a2:()=>g,f$:()=>T,p6:()=>S,yJ:()=>m});var r=n(96540),a=n(26206),i=n(30535),o=n(96453),s=n(17437),l=n(95579),d=n(66537),c=n(19129),u=n(12249),h=n(84080),p=n(2445);const m=o.I4.div`
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
  :last-child {
    margin-bottom: 0;
  }
`,g=o.I4.div`
  display: flex;
  align-items: center;
  width: 100%;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  height: ${({theme:e})=>6*e.gridUnit}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light3};
  border-radius: 3px;
  cursor: ${({withCaret:e})=>e?"pointer":"default"};
`,b=o.I4.div`
  ${({theme:e})=>`\n    display: flex;\n    width: 100%;\n    overflow: hidden;\n    text-overflow: ellipsis;\n    align-items: center;\n    white-space: nowrap;\n    padding-left: ${e.gridUnit}px;\n    svg {\n      margin-right: ${e.gridUnit}px;\n    }\n    .type-label {\n      margin-right: ${2*e.gridUnit}px;\n      margin-left: ${e.gridUnit}px;\n      font-weight: ${e.typography.weights.normal};\n      width: auto;\n    }\n    .option-label {\n      display: inline;\n    }\n  `}
`,v=o.I4.span`
  overflow: hidden;
  text-overflow: ellipsis;
`,f=o.I4.div`
  height: 100%;
  border-left: solid 1px ${({theme:e})=>e.colors.grayscale.dark2}0C;
  margin-left: auto;
`,y=o.I4.div`
  height: 100%;
  width: ${({theme:e})=>6*e.gridUnit}px;
  border-right: solid 1px ${({theme:e})=>e.colors.grayscale.dark2}0C;
  cursor: pointer;
`,x=(0,o.I4)(d.W)`
  margin: 0 ${({theme:e})=>e.gridUnit}px;
`,C=o.I4.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`,S=o.I4.div`
  padding: ${({theme:e})=>e.gridUnit}px;
  border: solid 1px ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,A=s.i7`
  0% {
    right: 100%;
  }
  50% {
    left: 4px;
  }
  90% {
    right: 4px;
  }
  100% {
    left: 100%;
  }
`,T=o.I4.div`
  ${({theme:e,isLoading:t,canDrop:n,isDragging:r,isOver:a})=>`\n  position: relative;\n  padding: ${e.gridUnit}px;\n  border: ${!t&&r?`dashed 1px ${n?e.colors.info.dark1:e.colors.error.dark1}`:`solid 1px ${t&&r?e.colors.warning.light1:e.colors.grayscale.light2}`};\n  border-radius: ${e.gridUnit}px;\n  &:before,\n  &:after {\n    content: ' ';\n    position: absolute;\n    border-radius: ${e.gridUnit}px;\n  }\n  &:before {\n    display: ${r||t?"block":"none"};\n    background-color: ${n?e.colors.primary.base:e.colors.error.light1};\n    z-index: ${e.zIndex.aboveDashboardCharts};\n    opacity: ${e.opacity.light};\n    top: 1px;\n    right: 1px;\n    bottom: 1px;\n    left: 1px;\n  }\n  &:after {\n    display: ${t||n&&a?"block":"none"};\n    background-color: ${t?e.colors.grayscale.light3:e.colors.primary.base};\n    z-index: ${e.zIndex.dropdown};\n    opacity: ${e.opacity.mediumLight};\n    top: ${-e.gridUnit}px;\n    right: ${-e.gridUnit}px;\n    bottom: ${-e.gridUnit}px;\n    left: ${-e.gridUnit}px;\n    cursor: ${t?"wait":"auto"};\n  }\n  `}

  &:before {
    ${({theme:e,isLoading:t})=>t&&s.AH`
        animation: ${A} 2s ease-in infinite;
        background: linear-gradient(currentColor 0 0) 0 100%/0% 3px no-repeat;
        background-size: 100% ${e.gridUnit/2}px;
        top: auto;
        right: ${e.gridUnit}px;
        left: ${e.gridUnit}px;
        bottom: -${e.gridUnit/2}px;
        height: ${e.gridUnit/2}px;
      `};
  }
`,w=o.I4.div`
  display: flex;
  align-items: center;
  width: 100%;
  height: ${({theme:e})=>6*e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.light1};
  border: dashed 1px ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
  cursor: ${({cancelHover:e})=>e?"inherit":"pointer"};

  :hover {
    background-color: ${({cancelHover:e,theme:t})=>e?"inherit":t.colors.grayscale.light4};
  }

  :active {
    background-color: ${({cancelHover:e,theme:t})=>e?"inherit":t.colors.grayscale.light3};
  }
`,D=o.I4.button`
  display: flex;
  align-items: center;
  justify-content: center;
  height: ${({theme:e})=>4*e.gridUnit}px;
  width: ${({theme:e})=>4*e.gridUnit}px;
  padding: 0;
  background-color: ${({theme:e})=>e.colors.primary.dark1};
  border: none;
  border-radius: 2px;

  :disabled {
    cursor: not-allowed;
    background-color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`,_=({label:e,savedMetric:t,adhocMetric:n,onRemove:s,onMoveLabel:d,onDropLabel:C,withCaret:S,isFunction:A,type:T,index:w,isExtra:D,datasourceWarningMessage:_,tooltipTitle:F,multi:Y=!0,...I})=>{const $=(0,o.DP)(),E=(0,r.useRef)(null),M=(0,r.useRef)(null),R=null==t?void 0:t.metric_name,[,N]=(0,a.H)({accept:T,drop(){Y&&(null==C||C())},hover(e,t){var n;if(!Y)return;if(!E.current)return;const{dragIndex:r}=e,a=w;if(r===a)return;const i=null==(n=E.current)?void 0:n.getBoundingClientRect(),o=(i.bottom-i.top)/2,s=t.getClientOffset(),l=null!=s&&s.y?(null==s?void 0:s.y)-i.top:0;r<a&&l<o||r>a&&l>o||(null==d||d(r,a),e.dragIndex=a)}}),[{isDragging:k},O]=(0,i.i)({item:{type:T,dragIndex:w,value:null!=t&&t.metric_name?t:n},collect:e=>({isDragging:e.isDragging()})});return O(N(E)),(0,p.Y)(m,{ref:E,children:(0,p.FD)(g,{withCaret:S,...I,children:[(0,p.Y)(y,{role:"button",onClick:s,children:(0,p.Y)(u.A.XSmall,{iconColor:$.colors.grayscale.light1})}),(0,p.FD)(b,{children:[A&&(0,p.Y)(u.A.FieldDerived,{}),(()=>{const n=!k&&"string"==typeof e&&F&&e&&F!==e||!k&&M&&M.current&&M.current.scrollWidth>M.current.clientWidth;return t&&R?(0,p.Y)(h.b,{metric:t,labelRef:M,shouldShowTooltip:!k}):n?(0,p.Y)(c.m,{title:F||e,children:(0,p.Y)(v,{ref:M,children:e})}):(0,p.Y)(v,{ref:M,children:e})})()]}),(!!_||D)&&(0,p.Y)(x,{icon:"exclamation-triangle",placement:"top",bsStyle:"warning",tooltip:_||(0,l.t)("\n                This filter was inherited from the dashboard's context.\n                It won't be saved when saving the chart.\n              ")}),S&&(0,p.Y)(f,{children:(0,p.Y)(u.A.CaretRight,{iconColor:$.colors.grayscale.light1})})]})})}},91643:(e,t,n)=>{n.d(t,{A:()=>b});var r=n(96453),a=n(45738),i=n(10286),o=n(19966),s=n(39091),l=n(8143),d=n(69633),c=n(78360),u=n(69172),h=n(2445);const p=(0,r.I4)(s.i8)`
  && {
    margin: 0 0 ${({theme:e})=>e.gridUnit}px;
  }
`;a.A.registerLanguage("markdown",l.A),a.A.registerLanguage("html",d.A),a.A.registerLanguage("sql",c.A),a.A.registerLanguage("json",u.A);const m=r.I4.div`
  height: 100%;
  display: flex;
  flex-direction: column;
`,g=(0,r.I4)(a.A)`
  flex: 1;
`,b=e=>{const{sql:t,language:n="sql"}=e;return(0,h.FD)(m,{children:[(0,h.Y)(o.A,{text:t,shouldShowText:!1,copyNode:(0,h.Y)(p,{buttonSize:"xsmall",children:(0,h.Y)("i",{className:"fa fa-clipboard"})})}),(0,h.Y)(g,{language:n,style:i.A,children:t})]},t)}},17432:(e,t,n)=>{n.d(t,{A:()=>p});var r=n(96540),a=n(96453),i=n(62952),o=n(51436),s=n(95579),l=n(17444),d=n(2514),c=n(91643),u=n(2445);const h=a.I4.div`
  height: 100%;
  display: flex;
  flex-direction: column;
`,p=e=>{const[t,n]=(0,r.useState)([]),[a,p]=(0,r.useState)(!1),[m,g]=(0,r.useState)(null);return(0,r.useEffect)((()=>{p(!0),(0,d.getChartDataRequest)({formData:e.latestQueryFormData,resultFormat:"json",resultType:"query"}).then((({json:e})=>{n((0,i.A)(e.result)),p(!1),g(null)})).catch((e=>{(0,o.h4)(e).then((({error:t,message:n})=>{g(t||n||e.statusText||(0,s.t)("Sorry, An error occurred")),p(!1)}))}))}),[JSON.stringify(e.latestQueryFormData)]),a?(0,u.Y)(l.A,{}):m?(0,u.Y)("pre",{children:m}):(0,u.Y)(h,{children:t.map((e=>e.query?(0,u.Y)(c.A,{sql:e.query,language:e.language||void 0}):null))})}},92013:(e,t,n)=>{n.d(t,{r:()=>s});var r=n(95579),a=n(24976),i=n(67553),o=n(2445);function s(e){return e.map((({column_name:e,verbose_name:t,is_certified:n,certified_by:s,description:l,type:d})=>({name:t||e,value:e,docHTML:(0,a.jS)({title:e,meta:d?`column: ${d}`:"column",body:`${null!=l?l:""}`,footer:n?(0,o.Y)(o.FK,{children:(0,r.t)("Certified by %s",s)}):void 0}),score:i.v9,meta:"column"})))}},60237:(e,t,n)=>{n.d(t,{T3:()=>c,cL:()=>u,kV:()=>s});var r=n(90179),a=n.n(r),i=n(35742);const o=["url_params"],s=e=>a()(e,o),l=(e,t)=>{let n="api/v1/explore/form_data";return e&&(n=n.concat(`/${e}`)),t&&(n=n.concat(`?tab_id=${t}`)),n},d=(e,t,n,r)=>{const a={datasource_id:e,datasource_type:t,form_data:JSON.stringify(s(n))};return r&&(a.chart_id=r),a},c=(e,t,n,r,a)=>i.A.post({endpoint:l(void 0,a),jsonPayload:d(e,t,n,r)}).then((e=>e.json.key)),u=(e,t,n,r,a,o)=>i.A.put({endpoint:l(n,o),jsonPayload:d(e,t,r,a)}).then((e=>e.json.message))},55976:(e,t,n)=>{n.d(t,{M:()=>p});var r=n(96540),a=n(96453),i=n(95579),o=n(17437),s=n(25946),l=n(13917),d=n(70175),c=n(86274),u=n(35233),h=n(2445);const p=({dataset:e,datasetId:t})=>{const n=(0,a.DP)(),[p,m]=(0,r.useState)(),[g,b]=(0,r.useState)(e?c.bk.Complete:c.bk.Loading);return(0,r.useEffect)((()=>{!e&&t&&(0,u.w)({endpoint:`/api/v1/dataset/${t}`}).then((({json:{result:e}})=>{m(e),b(c.bk.Complete)})).catch((()=>{b(c.bk.Error)}))}),[t,e]),{metadataBar:(0,r.useMemo)((()=>{const t=[],r=e||p;if(r){var a,u;const{changed_on_humanized:e,created_on_humanized:n,description:o,table_name:s,changed_by:l,created_by:c,owners:h}=r,p=(0,i.t)("Not available"),m=`${null!=(a=null==c?void 0:c.first_name)?a:""} ${null!=(u=null==c?void 0:c.last_name)?u:""}`.trim()||p,g=l?`${l.first_name} ${l.last_name}`:p,b=(null==h?void 0:h.length)>0?h.map((e=>`${e.first_name} ${e.last_name}`)):[p];t.push({type:d.Q.Table,title:s}),t.push({type:d.Q.LastModified,value:e,modifiedBy:g}),t.push({type:d.Q.Owner,createdBy:m,owners:b,createdOn:n}),o&&t.push({type:d.Q.Description,value:o})}return(0,h.FD)("div",{css:o.AH`
          display: flex;
          margin-bottom: ${4*n.gridUnit}px;
        `,children:[g===c.bk.Complete&&(0,h.Y)(l.Ay,{items:t,tooltipPlacement:"bottom"}),g===c.bk.Error&&(0,h.Y)(s.A,{type:"error",message:(0,i.t)("There was an error loading the dataset metadata")})]})}),[e,p,g,n.gridUnit]),status:g}}},32850:(e,t,n)=>{n.d(t,{v:()=>oe,A:()=>ce});var r,a,i=n(17437),o=n(62193),s=n.n(o),l=n(96540),d=n(61225),c=n(72391),u=n(96453),h=n(27366),p=n(83505),m=n(95579),g=n(12249),b=n(53107),v=n(6749),f=n(50068),y=n(15151),x=n(93103),C=n(37020),S=n(51436),A=n(93491),T=n(25946),w=n(17466),D=n(97987),_=n(90868),F=n(5261);!function(e){e.Dashboards="dashboards",e.Charts="charts"}(r||(r={})),function(e){e.Text="TEXT",e.PNG="PNG",e.CSV="CSV"}(a||(a={}));var Y=n(50500),I=n(19968),$=n(85861),E=n(46920),M=n(78697),R=n(51647);const N=(0,u.I4)($.A)`
  .ant-modal-body {
    padding: 0;
  }
`,k=u.I4.div`
  padding: ${({theme:e})=>`${3*e.gridUnit}px ${4*e.gridUnit}px ${2*e.gridUnit}px`};
  label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`,O=u.I4.div`
  border-top: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  padding: ${({theme:e})=>`${4*e.gridUnit}px ${4*e.gridUnit}px ${6*e.gridUnit}px`};
  .ant-select {
    width: 100%;
  }
  .control-label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`,U=u.I4.span`
  span {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
    vertical-align: middle;
  }
  .text {
    vertical-align: middle;
  }
`,q=u.I4.div`
  margin-bottom: ${({theme:e})=>7*e.gridUnit}px;

  h4 {
    margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  }
`,L=(0,u.I4)(R.l5)`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  width: ${({theme:e})=>120*e.gridUnit}px;
`,z=u.I4.p`
  color: ${({theme:e})=>e.colors.error.base};
`,H=i.AH`
  margin-bottom: 0;
`,P=(0,u.I4)(E.A)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,j=e=>i.AH`
  margin: ${3*e.gridUnit}px 0 ${2*e.gridUnit}px;
`,W=u.I4.div`
  margin: ${({theme:e})=>8*e.gridUnit}px 0
    ${({theme:e})=>4*e.gridUnit}px;
`,V=(0,u.I4)(M.s)`
  display: block;
  line-height: ${({theme:e})=>8*e.gridUnit}px;
`,B=(0,u.I4)(M.s.Group)`
  margin-left: ${({theme:e})=>.5*e.gridUnit}px;
`;var G=n(2445);const K=["pivot_table_v2","table","paired_ttest"],Q={crontab:"0 12 * * 1"},X={},J=(0,F.Ay)((function({onHide:e,show:t=!1,dashboardId:n,chart:r,userId:o,userEmail:s,ccEmail:c,bccEmail:u,creationMethod:h,dashboardName:p,chartName:b}){var v;const f=null==r||null==(v=r.sliceFormData)?void 0:v.viz_type,y=!!r,x=y&&f&&K.includes(f),C=x?a.Text:a.PNG,F=p||b,$=(0,l.useMemo)((()=>({...Q,name:F?(0,m.t)("Weekly Report for %s",F):(0,m.t)("Weekly Report")})),[F]),E=(0,l.useCallback)(((e,t)=>"reset"===t?$:{...e,...t}),[$]),[M,R]=(0,l.useReducer)(E,$),[J,Z]=(0,l.useState)(),ee=(0,d.wA)(),te=(0,d.d4)((e=>{const t=n?oe.Dashboards:oe.Charts;return(0,Y.oi)(e,t,n||(null==r?void 0:r.id))||X})),ne=te&&Object.keys(te).length;(0,l.useEffect)((()=>{R(ne?te:"reset")}),[ne,te]);const re=(0,G.FD)(U,{children:[(0,G.Y)(g.A.Calendar,{}),(0,G.Y)("span",{className:"text",children:ne?(0,m.t)("Edit email report"):(0,m.t)("Schedule a new email report")})]}),ae=(0,G.FD)(G.FK,{children:[(0,G.Y)(P,{onClick:e,children:(0,m.t)("Cancel")},"back"),(0,G.Y)(P,{buttonStyle:"primary",onClick:async()=>{const t={type:"Report",active:!0,force_screenshot:!1,custom_width:M.custom_width,creation_method:h,dashboard:n,chart:null==r?void 0:r.id,owners:[o],recipients:[{recipient_config_json:{target:s,ccTarget:c,bccTarget:u},type:"Email"}],name:M.name,description:M.description,crontab:M.crontab,report_format:M.report_format||C,timezone:M.timezone};R({isSubmitting:!0,error:void 0});try{ne?await ee((0,A.Zp)(M.id,t)):await ee((0,A.ef)(t)),e()}catch(e){const{error:t}=await(0,S.h4)(e);R({error:t})}R({isSubmitting:!1})},disabled:!M.name,loading:M.isSubmitting,children:ne?(0,m.t)("Save"):(0,m.t)("Add")},"submit")]}),ie=(0,G.FD)(G.FK,{children:[(0,G.Y)(W,{children:(0,G.Y)("h4",{children:(0,m.t)("Message content")})}),(0,G.Y)("div",{className:"inline-container",children:(0,G.FD)(B,{onChange:e=>{R({report_format:e.target.value})},value:M.report_format||C,children:[x&&(0,G.Y)(V,{value:a.Text,children:(0,m.t)("Text embedded in email")}),(0,G.Y)(V,{value:a.PNG,children:(0,m.t)("Image (PNG) embedded in email")}),(0,G.Y)(V,{value:a.CSV,children:(0,m.t)("Formatted CSV attached in email")})]})})]}),se=(0,G.FD)(I.tu,{children:[(0,G.Y)("div",{className:"control-label",css:j,children:(0,m.t)("Screenshot width")}),(0,G.Y)("div",{className:"input-container",children:(0,G.Y)(_.pd,{type:"number",name:"custom_width",value:(null==M?void 0:M.custom_width)||"",placeholder:(0,m.t)("Input custom width in pixels"),onChange:e=>{R({custom_width:parseInt(e.target.value,10)||null})}})})]});return(0,G.FD)(N,{show:t,onHide:e,title:re,footer:ae,width:"432",centered:!0,children:[(0,G.FD)(k,{children:[(0,G.Y)(D.A,{id:"name",name:"name",value:M.name||"",placeholder:$.name,required:!0,validationMethods:{onChange:({target:e})=>R({name:e.value})},label:(0,m.t)("Report Name")}),(0,G.Y)(D.A,{id:"description",name:"description",value:(null==M?void 0:M.description)||"",validationMethods:{onChange:({target:e})=>{R({description:e.value})}},label:(0,m.t)("Description"),placeholder:(0,m.t)("Include a description that will be sent with your report"),css:H})]}),(0,G.FD)(O,{children:[(0,G.FD)(q,{children:[(0,G.Y)("h4",{css:e=>(e=>i.AH`
  margin: ${3*e.gridUnit}px 0;
`)(e),children:(0,m.t)("Schedule")}),(0,G.Y)("p",{children:(0,m.t)("The report will be sent to your email at")})]}),(0,G.Y)(L,{clearButton:!1,value:M.crontab||"0 12 * * 1",setValue:e=>{R({crontab:e})},onError:Z}),(0,G.Y)(z,{children:J}),(0,G.Y)("div",{className:"control-label",css:e=>(e=>i.AH`
  margin: ${3*e.gridUnit}px 0 ${2*e.gridUnit}px;
`)(e),children:(0,m.t)("Timezone")}),(0,G.Y)(w.A,{timezone:M.timezone,onTimezoneChange:e=>{R({timezone:e})}}),y&&ie,(!y||!x)&&se]}),M.error&&(0,G.Y)(T.A,{type:"error",css:e=>(e=>i.AH`
  border: ${e.colors.error.base} 1px solid;
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px;
  margin-top: 0;
  color: ${e.colors.error.dark2};
  .ant-alert-message {
    font-size: ${e.typography.sizes.m}px;
    font-weight: bold;
  }
  .ant-alert-description {
    font-size: ${e.typography.sizes.m}px;
    line-height: ${4*e.gridUnit}px;
    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`)(e),message:ne?(0,m.t)("Failed to update report"):(0,m.t)("Failed to create report"),description:M.error})]})}));var Z=n(15700);const ee=(0,c.a)(),te=e=>i.AH`
  color: ${e.colors.error.base};
`,ne=e=>i.AH`
  & .ant-menu-item {
    padding: 5px 12px;
    margin-top: 0px;
    margin-bottom: 4px;
    :hover {
      color: ${e.colors.grayscale.dark1};
    }
  }
  :hover {
    background-color: ${e.colors.secondary.light5};
  }
`,re=e=>i.AH`
  &:hover {
    color: ${e.colors.grayscale.dark1};
    background-color: ${e.colors.secondary.light5};
  }
`,ae=u.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  > *:first-child {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`,ie=ee.get("report-modal.dropdown.item.icon");var oe;!function(e){e.Charts="charts",e.Dashboards="dashboards"}(oe||(oe={}));const se={};var le={name:"1e1ncky",styles:"border:none"},de={name:"833hqy",styles:"width:200px"};function ce({dashboardId:e,chart:t,useTextMenu:n=!1,setShowReportSubMenu:r,setIsDropdownVisible:a,isDropdownVisible:o,...c}){const S=(0,d.wA)(),T=(0,d.d4)((n=>{const r=e?oe.Dashboards:oe.Charts;return(0,Y.oi)(n,r,e||(null==t?void 0:t.id))||se})),w=(null==T?void 0:T.active)||!1,D=(0,d.d4)((e=>e.user)),_=()=>!!(0,h.G7)(h.TO.AlertReports)&&(!(null==D||!D.userId)&&(!!(e||null!=t&&t.id)&&Object.keys(D.roles||[]).map((e=>D.roles[e].filter((e=>"menu_access"===e[0]&&"Manage"===e[1])))).some((e=>e.length>0)))),[F,I]=(0,l.useState)(null),$=(0,u.DP)(),E=(0,p.Z)(e),[M,R]=(0,l.useState)(!1),N=async(e,t)=>{null!=e&&e.id&&S((0,A.PM)(e,t))},k=_()&&!!(e&&E!==e||null!=t&&t.id);(0,l.useEffect)((()=>{k&&S((0,A.LQ)({userId:D.userId,filterField:e?"dashboard_id":"chart_id",creationMethod:e?"dashboards":"charts",resourceId:e||(null==t?void 0:t.id)}))}),[]);const O=T&&r&&_();(0,l.useEffect)((()=>{O?r(!0):!T&&r&&r(!1)}),[T]);const U=()=>{a&&(a(!1),R(!0))};return(0,G.Y)(G.FK,{children:_()&&(0,G.FD)(G.FK,{children:[(0,G.Y)(J,{userId:D.userId,show:M,onHide:()=>R(!1),userEmail:D.email,dashboardId:e,chart:t,creationMethod:e?oe.Dashboards:oe.Charts}),n?s()(T)?(0,G.FD)(v.W1,{selectable:!1,...c,css:ne,children:[(0,G.Y)(v.W1.Item,{onClick:U,children:ie?(0,G.FD)(ae,{children:[(0,G.Y)("div",{children:(0,m.t)("Set up an email report")}),(0,G.Y)(ie,{})]}):(0,m.t)("Set up an email report")}),(0,G.Y)(v.W1.Divider,{})]}):o&&(0,G.FD)(v.W1,{selectable:!1,css:le,children:[(0,G.Y)(v.W1.Item,{css:re,onClick:()=>N(T,!w),children:(0,G.FD)(Z.t3,{children:[(0,G.Y)(f.Ay,{checked:w,onChange:y.fZ}),(0,m.t)("Email reports active")]})}),(0,G.Y)(v.W1.Item,{css:re,onClick:U,children:(0,m.t)("Edit email report")}),(0,G.Y)(v.W1.Item,{css:re,onClick:()=>{a&&(a(!1),I(T))},children:(0,m.t)("Delete email report")})]}):s()(T)?(0,G.Y)("span",{role:"button",title:(0,m.t)("Schedule email report"),tabIndex:0,className:"action-button action-schedule-report",onClick:()=>R(!0),children:(0,G.Y)(g.A.Calendar,{})}):(0,G.Y)(G.FK,{children:(0,G.Y)(x.R2,{overlay:(0,G.FD)(v.W1,{selectable:!1,css:de,children:[(0,G.FD)(v.W1.Item,{children:[(0,m.t)("Email reports active"),(0,G.Y)(b.d,{checked:w,onClick:e=>N(T,e),size:"small",css:(0,i.AH)({marginLeft:2*$.gridUnit},"","")})]}),(0,G.Y)(v.W1.Item,{onClick:()=>R(!0),children:(0,m.t)("Edit email report")}),(0,G.Y)(v.W1.Item,{onClick:()=>I(T),css:te,children:(0,m.t)("Delete email report")})]}),overlayStyle:{zIndex:99,animationDuration:"0s"},trigger:["click"],getPopupContainer:e=>e.closest(".action-button"),children:(0,G.Y)("span",{role:"button",className:"action-button action-schedule-report",tabIndex:0,children:(0,G.Y)(g.A.Calendar,{})})})}),F&&(0,G.Y)(C.A,{description:(0,m.t)("This action will permanently delete %s.",null==F?void 0:F.name),onConfirm:()=>{F&&(async e=>{await S((0,A.i7)(e)),I(null)})(F)},onHide:()=>I(null),open:!0,title:(0,m.t)("Delete Report?")})]})})}},48422:(e,t,n)=>{n.d(t,{w:()=>o});var r=n(96540),a=n(43561);const i=new BroadcastChannel("tab_id_channel");function o(){const[e,t]=(0,r.useState)();return(0,r.useEffect)((()=>{if(!function(){try{return window.localStorage&&window.sessionStorage}catch(e){return!1}}())return void(e||t((0,a.Ak)()));const n=()=>{let e;try{e=window.localStorage.getItem("last_tab_id")}catch(e){}const n=String(e?Number.parseInt(e,10)+1:1);try{window.sessionStorage.setItem("tab_id",n),window.localStorage.setItem("last_tab_id",n)}catch(e){}t(n)};let r;try{r=window.sessionStorage.getItem("tab_id")}catch(e){}r?(i.postMessage({type:"REQUESTING_TAB_ID",tabId:r}),t(r)):n(),i.onmessage=t=>{if(t.data.tabId===e)if("REQUESTING_TAB_ID"===t.data.type){const e={type:"TAB_ID_DENIED",tabId:t.data.tabId};i.postMessage(e)}else"TAB_ID_DENIED"===t.data.type&&n()}}),[e]),e}},35233:(e,t,n)=>{n.d(t,{e:()=>i,w:()=>o});var r=n(35742),a=n(43859);const i=new Map,o=(0,a.K)(r.A.get,i,(({endpoint:e})=>e||""))},72965:(e,t,n)=>{n.d(t,{A:()=>u});var r=n(20249),a=n.n(r),i=n(67390),o=n.n(i),s=n(95579),l=n(96453),d=n(95272);const c=(e,t=new Date)=>`${a()(e)}-${t.toISOString().replace(/[: ]/g,"-")}`;function u(e,t,n=!1){return r=>{const a=n?document.querySelector(e):r.currentTarget.closest(e);return a?o().toJpeg(a,{bgcolor:l.TT.colors.grayscale.light4,filter:e=>"string"!=typeof e.className||"mapboxgl-control-container"!==e.className&&!e.className.includes("header-controls")}).then((e=>{const n=document.createElement("a");n.download=`${c(t)}.jpg`,n.href=e,n.click()})).catch((e=>{console.error("Creating image failed",e)})):(0,d.Zd)((0,s.t)("Image download failed, please refresh and try again."))}}},21357:(e,t,n)=>{n.d(t,{w:()=>o});var r=n(95579);const a=(0,r.t)("Create chart"),i=(0,r.t)("Update chart"),o=e=>(0,r.t)("Select values in highlighted field(s) in the control panel. Then run the query by clicking on the %s button.",`"${e?a:i}"`)},59838:(e,t,n)=>{n.d(t,{r:()=>s});var r=n(70700),a=n(2511),i=n(95483),o=n(71191);const s=(e,t=a.v.Where)=>{let n;var s;return n=(0,r.q0)(e.col)?{expressionType:"SQL",clause:t,sqlExpression:(0,o.e)({expressionType:a.A.Simple,subject:`(${e.col.sqlExpression})`,operator:e.op,comparator:"val"in e?e.val:void 0})}:{expressionType:"SIMPLE",clause:t,operator:e.op,operatorId:null==(s=Object.entries(i.nS).find((t=>t[1].operation===e.op)))?void 0:s[0],subject:e.col,comparator:"val"in e?e.val:void 0},e.isExtra&&Object.assign(n,{isExtra:!0,filterOptionName:`filter_${Math.random().toString(36).substring(2,15)}_${Math.random().toString(36).substring(2,15)}`}),n}}}]);
//# sourceMappingURL=d539454b5342f8f14579.chunk.js.map