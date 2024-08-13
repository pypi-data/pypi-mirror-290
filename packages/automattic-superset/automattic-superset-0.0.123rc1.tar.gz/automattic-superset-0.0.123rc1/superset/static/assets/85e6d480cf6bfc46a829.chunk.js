"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9915],{10044:(e,t,r)=>{r.d(t,{A:()=>i});var a=r(16146),s=r(2445);const i=e=>(0,s.Y)(a.A,{...e})},93514:(e,t,r)=>{r.d(t,{F:()=>s});var a=r(95579);const s={name:(0,a.t)("SQL"),tabs:[{name:"Saved queries",label:(0,a.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,a.t)("Query history"),url:"/sqllab/history/",usesRouter:!0}]}},11188:(e,t,r)=>{r.d(t,{A:()=>m});var a=r(96453),s=r(95579),i=r(78360),n=r(69633),l=r(8143),o=r(69172),c=r(10286),d=r(45738),u=r(12249),h=r(73135),g=r(2445);d.A.registerLanguage("sql",i.A),d.A.registerLanguage("markdown",l.A),d.A.registerLanguage("html",n.A),d.A.registerLanguage("json",o.A);const p=a.I4.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`;function m({addDangerToast:e,addSuccessToast:t,children:r,...a}){return(0,g.FD)(p,{children:[(0,g.Y)(u.A.Copy,{tabIndex:0,role:"button",onClick:a=>{var i;a.preventDefault(),a.currentTarget.blur(),i=r,(0,h.A)((()=>Promise.resolve(i))).then((()=>{t&&t((0,s.t)("SQL Copied!"))})).catch((()=>{e&&e((0,s.t)("Sorry, your browser does not support copying."))}))}}),(0,g.Y)(d.A,{style:c.A,...a,children:r})]})}},14318:(e,t,r)=>{r.d(t,{A:()=>s});var a=r(96540);function s({queries:e,fetchData:t,currentQueryId:r}){const s=e.findIndex((e=>e.id===r)),[i,n]=(0,a.useState)(s),[l,o]=(0,a.useState)(!1),[c,d]=(0,a.useState)(!1);function u(){o(0===i),d(i===e.length-1)}function h(r){const a=i+(r?-1:1);a>=0&&a<e.length&&(t(e[a].id),n(a),u())}return(0,a.useEffect)((()=>{u()})),{handleKeyPress:function(t){i>=0&&i<e.length&&("ArrowDown"===t.key||"k"===t.key?(t.preventDefault(),h(!1)):"ArrowUp"!==t.key&&"j"!==t.key||(t.preventDefault(),h(!0)))},handleDataChange:h,disablePrevious:l,disableNext:c}}},52825:(e,t,r)=>{r.r(t),r.d(t,{default:()=>J});var a=r(96540),s=r(61574),i=r(71519),n=r(96453),l=r(95579),o=r(35742),c=r(69108),d=r(95093),u=r.n(d),h=r(30703),g=r(5261),p=r(50500),m=r(2738),y=r(51713),b=r(10044),f=r(93514),v=r(39854),A=r(19129),x=r(45738),S=r(78360),q=r(10286),k=r(27023),w=r(23193),C=r(12249),Y=r(85861),D=r(46942),H=r.n(D),$=r(46920),F=r(11188),T=r(14318),I=r(2445);const z=n.I4.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin-bottom: 0;
`,L=n.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
  padding: 4px 0 24px 0;
`,U=n.I4.div`
  margin: 0 0 ${({theme:e})=>6*e.gridUnit}px 0;
`,Q=n.I4.div`
  display: inline;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  margin-right: ${({theme:e})=>4*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.secondary.dark1};

  &.active,
  &:focus,
  &:hover {
    background: ${({theme:e})=>e.colors.secondary.light4};
    border-bottom: none;
    border-radius: ${({theme:e})=>e.borderRadius}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &:hover:not(.active) {
    background: ${({theme:e})=>e.colors.secondary.light5};
  }
`,R=(0,n.I4)(Y.A)`
  .ant-modal-body {
    padding: ${({theme:e})=>6*e.gridUnit}px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`,_=(0,g.Ay)((function({onHide:e,openInSqlLab:t,queries:r,query:s,fetchData:i,show:n,addDangerToast:o,addSuccessToast:c}){const{handleKeyPress:d,handleDataChange:u,disablePrevious:h,disableNext:g}=(0,T.A)({queries:r,currentQueryId:s.id,fetchData:i}),[p,m]=(0,a.useState)("user"),{id:y,sql:b,executed_sql:f}=s;return(0,I.Y)("div",{role:"none",onKeyUp:d,children:(0,I.FD)(R,{onHide:e,show:n,title:(0,l.t)("Query preview"),footer:(0,I.FD)(I.FK,{children:[(0,I.Y)($.A,{disabled:h,onClick:()=>u(!0),children:(0,l.t)("Previous")},"previous-query"),(0,I.Y)($.A,{disabled:g,onClick:()=>u(!1),children:(0,l.t)("Next")},"next-query"),(0,I.Y)($.A,{buttonStyle:"primary",onClick:()=>t(y),children:(0,l.t)("Open in SQL Lab")},"open-in-sql-lab")]}),children:[(0,I.Y)(z,{children:(0,l.t)("Tab name")}),(0,I.Y)(L,{children:s.tab_name}),(0,I.FD)(U,{children:[(0,I.Y)(Q,{role:"button",className:H()({active:"user"===p}),onClick:()=>m("user"),children:(0,l.t)("User query")}),(0,I.Y)(Q,{role:"button",className:H()({active:"executed"===p}),onClick:()=>m("executed"),children:(0,l.t)("Executed query")})]}),(0,I.Y)(F.A,{addDangerToast:o,addSuccessToast:c,language:"sql",children:("user"===p?b:f)||""})]})})}));var N=r(95272),Z=r(25106);const P=(0,n.I4)(v.A)`
  table .table-cell {
    vertical-align: top;
  }
`;x.A.registerLanguage("sql",S.A);const K=(0,n.I4)(x.A)`
  height: ${({theme:e})=>26*e.gridUnit}px;
  overflow: hidden !important; /* needed to override inline styles */
  text-overflow: ellipsis;
  white-space: nowrap;
`,O=n.I4.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,B=n.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`,E=(0,n.I4)(m.A)`
  text-align: left;
  font-family: ${({theme:e})=>e.typography.families.monospace};
`,J=(0,g.Ay)((function({addDangerToast:e}){const{state:{loading:t,resourceCount:r,resourceCollection:d},fetchData:g}=(0,p.RU)("query",(0,l.t)("Query history"),e,!1),[m,x]=(0,a.useState)(),S=(0,n.DP)(),Y=(0,s.W6)(),D=(0,a.useCallback)((t=>{o.A.get({endpoint:`/api/v1/query/${t}`}).then((({json:e={}})=>{x({...e.result})}),(0,h.JF)((t=>e((0,l.t)("There was an issue previewing the selected query. %s",t)))))}),[e]),H={activeChild:"Query history",...f.F},$=[{id:w.H.StartTime,desc:!0}],F=(0,a.useMemo)((()=>[{Cell:({row:{original:{status:e}}})=>{const t={name:null,label:""};return e===c.kZ.Success?(t.name=(0,I.Y)(C.A.Check,{iconColor:S.colors.success.base}),t.label=(0,l.t)("Success")):e===c.kZ.Failed||e===c.kZ.Stopped?(t.name=(0,I.Y)(C.A.XSmall,{iconColor:e===c.kZ.Failed?S.colors.error.base:S.colors.grayscale.base}),t.label=(0,l.t)("Failed")):e===c.kZ.Running?(t.name=(0,I.Y)(C.A.Running,{iconColor:S.colors.primary.base}),t.label=(0,l.t)("Running")):e===c.kZ.TimedOut?(t.name=(0,I.Y)(C.A.Offline,{iconColor:S.colors.grayscale.light1}),t.label=(0,l.t)("Offline")):e!==c.kZ.Scheduled&&e!==c.kZ.Pending||(t.name=(0,I.Y)(C.A.Queued,{iconColor:S.colors.grayscale.base}),t.label=(0,l.t)("Scheduled")),(0,I.Y)(A.m,{title:t.label,placement:"bottom",children:(0,I.Y)("span",{children:t.name})})},accessor:w.H.Status,size:"xs",disableSortBy:!0},{accessor:w.H.StartTime,Header:(0,l.t)("Time"),size:"xl",Cell:({row:{original:{start_time:e}}})=>{const t=u().utc(e).local().format(k.QU).split(" ");return(0,I.FD)(I.FK,{children:[t[0]," ",(0,I.Y)("br",{}),t[1]]})}},{Header:(0,l.t)("Duration"),size:"xl",Cell:({row:{original:{status:e,start_time:t,end_time:r}}})=>{const a=e===c.kZ.Failed?"danger":e,s=r?u()(u().utc(r-t)).format(k.os):"00:00:00.000";return(0,I.Y)(E,{type:a,role:"timer",children:s})}},{accessor:w.H.TabName,Header:(0,l.t)("Tab name"),size:"xl"},{accessor:w.H.DatabaseName,Header:(0,l.t)("Database"),size:"xl"},{accessor:w.H.Database,hidden:!0},{accessor:w.H.Schema,Header:(0,l.t)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=e.map((e=>e.table)),r=t.length>0?t.shift():"";return t.length?(0,I.FD)(O,{children:[(0,I.Y)("span",{children:r}),(0,I.Y)(b.A,{placement:"right",title:(0,l.t)("TABLES"),trigger:"click",content:(0,I.Y)(I.FK,{children:t.map((e=>(0,I.Y)(B,{children:e},e)))}),children:(0,I.FD)("span",{className:"count",children:["(+",t.length,")"]})})]}):r},accessor:w.H.SqlTables,Header:(0,l.t)("Tables"),size:"xl",disableSortBy:!0},{accessor:w.H.UserFirstName,Header:(0,l.t)("User"),size:"xl",Cell:({row:{original:{user:e}}})=>(0,Z.A)(e)},{accessor:w.H.User,hidden:!0},{accessor:w.H.Rows,Header:(0,l.t)("Rows"),size:"md"},{accessor:w.H.Sql,Header:(0,l.t)("SQL"),Cell:({row:{original:e,id:t}})=>(0,I.Y)("div",{tabIndex:0,role:"button",onClick:()=>x(e),children:(0,I.Y)(K,{language:"sql",style:q.A,children:(0,h.s4)(e.sql,4)})})},{Header:(0,l.t)("Actions"),id:"actions",disableSortBy:!0,Cell:({row:{original:{id:e}}})=>(0,I.Y)(A.m,{title:(0,l.t)("Open query in SQL Lab"),placement:"bottom",children:(0,I.Y)(i.N_,{to:`/sqllab?queryId=${e}`,children:(0,I.Y)(C.A.Full,{iconColor:S.colors.grayscale.base})})})}]),[]),T=(0,a.useMemo)((()=>[{Header:(0,l.t)("Database"),key:"database",id:"database",input:"select",operator:v.t.RelationOneMany,unfilteredLabel:(0,l.t)("All"),fetchSelects:(0,h.u1)("query","database",(0,h.JF)((t=>e((0,l.t)("An error occurred while fetching database values: %s",t))))),paginate:!0},{Header:(0,l.t)("State"),key:"state",id:"status",input:"select",operator:v.t.Equals,unfilteredLabel:"All",fetchSelects:(0,h.$C)("query","status",(0,h.JF)((t=>e((0,l.t)("An error occurred while fetching schema values: %s",t))))),paginate:!0},{Header:(0,l.t)("User"),key:"user",id:"user",input:"select",operator:v.t.RelationOneMany,unfilteredLabel:"All",fetchSelects:(0,h.u1)("query","user",(0,h.JF)((t=>e((0,l.t)("An error occurred while fetching user values: %s",t))))),paginate:!0},{Header:(0,l.t)("Time range"),key:"start_time",id:"start_time",input:"datetime_range",operator:v.t.Between},{Header:(0,l.t)("Search by query text"),key:"sql",id:"sql",input:"search",operator:v.t.Contains}]),[e]);return(0,I.FD)(I.FK,{children:[(0,I.Y)(y.A,{...H}),m&&(0,I.Y)(_,{onHide:()=>x(void 0),query:m,queries:d,fetchData:D,openInSqlLab:e=>Y.push(`/sqllab?queryId=${e}`),show:!0}),(0,I.Y)(P,{className:"query-history-list-view",columns:F,count:r,data:d,fetchData:g,filters:T,initialSort:$,loading:t,pageSize:25,highlightRowId:null==m?void 0:m.id,refreshData:()=>{},addDangerToast:e,addSuccessToast:N.WR})]})}))},25106:(e,t,r)=>{function a(e){return e?`${e.first_name} ${e.last_name}`:""}r.d(t,{A:()=>a})}}]);
//# sourceMappingURL=85e6d480cf6bfc46a829.chunk.js.map