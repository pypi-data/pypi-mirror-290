"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9854],{6094:(e,t,a)=>{a.d(t,{c:()=>n,l:()=>o});var l=a(78362),r=a(96453);const i=l.A.RangePicker,n=(0,r.I4)(i)`
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,o=l.A},39854:(e,t,a)=>{a.d(t,{t:()=>ce,A:()=>de});var l=a(96453),r=a(95579),i=a(96540),n=a(25946),o=a(46942),s=a.n(o),d=a(46920),c=a(12249),u=a(85994),g=a(47251),p=a(73204),h=a(35742),m=a(40563),f=a(85861),b=a(49756),v=a(3932),y=a(2445);const w=l.I4.div`
  .bulk-tag-text {
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }
`,x=({show:e,selected:t=[],onHide:a,refreshData:l,resourceName:n,addSuccessToast:o,addDangerToast:s})=>{(0,i.useEffect)((()=>{}),[]);const[c,u]=(0,i.useState)([]);return(0,y.Y)(f.A,{title:(0,r.t)("Bulk tag"),show:e,onHide:()=>{u([]),a()},footer:(0,y.FD)("div",{children:[(0,y.Y)(d.A,{buttonStyle:"secondary",onClick:a,children:(0,r.t)("Cancel")}),(0,y.Y)(d.A,{buttonStyle:"primary",onClick:async()=>{await h.A.post({endpoint:"/api/v1/tag/bulk_create",jsonPayload:{tags:c.map((e=>({name:e.value,objects_to_tag:t.map((e=>[n,+e.original.id]))})))}}).then((({json:e={}})=>{const t=e.result.objects_skipped,a=e.result.objects_tagged;t.length>0&&o((0,r.t)("%s items could not be tagged because you don’t have edit permissions to all selected objects.",t.length,n)),o((0,r.t)("Tagged %s %ss",a.length,n))})).catch((e=>{s((0,r.t)("Failed to tag items"))})),l(),a(),u([])},children:(0,r.t)("Save")})]}),children:(0,y.FD)(w,{children:[(0,y.Y)("div",{className:"bulk-tag-text",children:(0,r.t)("You are adding tags to %s %ss",t.length,n)}),(0,y.Y)(m.lR,{children:(0,r.t)("tags")}),(0,y.Y)(b.A,{ariaLabel:"tags",value:c,options:v.m,onHide:a,onChange:e=>u(e),placeholder:(0,r.t)("Select Tags"),mode:"multiple"})]})})},S=l.I4.div`
  ${({theme:e,showThumbnails:t})=>`\n    display: grid;\n    grid-gap: ${12*e.gridUnit}px ${4*e.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    margin-top: ${-6*e.gridUnit}px;\n    padding: ${t?`${8*e.gridUnit+3}px ${9*e.gridUnit}px`:`${8*e.gridUnit+1}px ${9*e.gridUnit}px`};\n  `}
`,C=l.I4.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;function T({bulkSelectEnabled:e,loading:t,prepareRow:a,renderCard:l,rows:r,showThumbnails:i}){return l?(0,y.FD)(S,{showThumbnails:i,children:[t&&0===r.length&&[...new Array(25)].map(((e,a)=>(0,y.Y)("div",{children:l({loading:t})},a))),r.length>0&&r.map((r=>l?(a(r),(0,y.Y)(C,{className:s()({"card-selected":e&&r.isSelected,"bulk-select":e}),onClick:t=>{return a=t,l=r.toggleRowSelected,void(e&&(a.preventDefault(),a.stopPropagation(),l()));var a,l},role:"none",children:l({...r.original,loading:t})},r.id)):null))]}):null}var F=a(65339),I=a(15595),Y=a(2404),$=a.n(Y),_=a(38914),k=a(33231),A=a(58561),D=a.n(A);const R={encode:e=>void 0===e?void 0:D().encode(e).replace(/%/g,"%25").replace(/&/g,"%26").replace(/\+/g,"%2B").replace(/#/g,"%23"),decode:e=>void 0===e||Array.isArray(e)?void 0:D().decode(e)};class B extends Error{constructor(...e){super(...e),this.name="ListViewError"}}function N(e,t){return e.map((({id:e,urlDisplay:a,operator:l})=>({id:e,urlDisplay:a,operator:l,value:t[a||e]})))}function U(e,t){const a=[],l={};return Object.keys(e).forEach((t=>{const r={id:t,value:e[t]};l[t]=r,a.push(r)})),t.forEach((e=>{const t=e.urlDisplay||e.id,a=l[t];a&&(a.operator=e.operator,a.id=e.id)})),a}var P=a(31641);const M=l.I4.div`
  width: ${200}px;
`,E=(0,l.I4)(c.A.Search)`
  color: ${({theme:e})=>e.colors.grayscale.light1};
`,V=(0,l.I4)(I.k2)`
  border-radius: ${({theme:e})=>e.gridUnit}px;
`;function H({Header:e,name:t,initialValue:a,toolTipDescription:l,onSubmit:n},o){const[s,d]=(0,i.useState)(a||""),c=()=>{s&&n(s.trim())};return(0,i.useImperativeHandle)(o,(()=>({clearFilter:()=>{d(""),n("")}}))),(0,y.FD)(M,{children:[(0,y.Y)(m.lR,{children:e}),l&&(0,y.Y)(P.A,{tooltip:l,viewBox:"0 -7 28 28"}),(0,y.Y)(V,{allowClear:!0,placeholder:(0,r.t)("Type a value"),name:t,value:s,onChange:e=>{d(e.currentTarget.value),""===e.currentTarget.value&&n("")},onPressEnter:c,onBlur:c,prefix:(0,y.Y)(E,{iconSize:"l"})})]})}const z=(0,i.forwardRef)(H),O=l.I4.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  width: ${200}px;
`;function j({Header:e,name:t,fetchSelects:a,initialValue:l,onSelect:n,selects:o=[]},s){const[d,c]=(0,i.useState)(l),u=e=>{n(e?{label:e.label,value:e.value}:void 0),c(e)},g=()=>{n(void 0,!0),c(void 0)};(0,i.useImperativeHandle)(s,(()=>({clearFilter:()=>{g()}})));const p=(0,i.useMemo)((()=>async(e,t,l)=>{if(a){const r=await a(e,t,l);return{data:r.data,totalCount:r.totalCount}}return{data:[],totalCount:0}}),[a]);return(0,y.Y)(O,{children:a?(0,y.Y)(b.A,{allowClear:!0,ariaLabel:"string"==typeof e?e:t||(0,r.t)("Filter"),header:(0,y.Y)(m.lR,{children:e}),onChange:u,onClear:g,options:p,placeholder:(0,r.t)("Select or type a value"),showSearch:!0,value:d}):(0,y.Y)(I.l6,{allowClear:!0,ariaLabel:"string"==typeof e?e:t||(0,r.t)("Filter"),header:(0,y.Y)(m.lR,{children:e}),labelInValue:!0,onChange:u,onClear:g,options:o,placeholder:(0,r.t)("Select or type a value"),showSearch:!0,value:d})})}const q=(0,i.forwardRef)(j);var L=a(95093),W=a.n(L),G=a(6094);const K=l.I4.div`
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  width: 360px;
`;function Q({Header:e,initialValue:t,onSubmit:a},l){const[n,o]=(0,i.useState)(null!=t?t:null),s=(0,i.useMemo)((()=>!n||Array.isArray(n)&&!n.length?null:[W()(n[0]),W()(n[1])]),[n]);return(0,i.useImperativeHandle)(l,(()=>({clearFilter:()=>{o(null),a([])}}))),(0,y.FD)(K,{children:[(0,y.Y)(m.lR,{children:e}),(0,y.Y)(G.c,{placeholder:[(0,r.t)("Start date"),(0,r.t)("End date")],showTime:!0,value:s,onChange:e=>{var t,l,r,i;if(!e)return o(null),void a([]);const n=[null!=(t=null==(l=e[0])?void 0:l.valueOf())?t:0,null!=(r=null==(i=e[1])?void 0:i.valueOf())?r:0];o(n),a(n)}})]})}const J=(0,i.forwardRef)(Q);function X({filters:e,internalFilters:t=[],updateFilterValue:a},l){const r=(0,i.useMemo)((()=>Array.from({length:e.length},(()=>(0,i.createRef)()))),[e.length]);return(0,i.useImperativeHandle)(l,(()=>({clearFilters:()=>{r.forEach((e=>{var t;null==(t=e.current)||null==t.clearFilter||t.clearFilter()}))}}))),(0,y.Y)(y.FK,{children:e.map((({Header:e,fetchSelects:l,key:i,id:n,input:o,paginate:s,selects:d,toolTipDescription:c,onFilterUpdate:u},g)=>{var p;const h=null==t||null==(p=t[g])?void 0:p.value;return"select"===o?(0,y.Y)(q,{ref:r[g],Header:e,fetchSelects:l,initialValue:h,name:n,onSelect:(e,t)=>{u&&(t||u(e)),a(g,e)},paginate:s,selects:d},i):"search"===o&&"string"==typeof e?(0,y.Y)(z,{ref:r[g],Header:e,initialValue:h,name:n,toolTipDescription:c,onSubmit:e=>{u&&u(e),a(g,e)}},i):"datetime_range"===o?(0,y.Y)(J,{ref:r[g],Header:e,initialValue:h,name:n,onSubmit:e=>a(g,e)},i):null}))})}const Z=(0,F.b)((0,i.forwardRef)(X)),ee=l.I4.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
  text-align: left;
  width: ${200}px;
`,te=({initialSort:e,onChange:t,options:a})=>{const l=e&&a.find((({id:t,desc:a})=>t===e[0].id&&a===e[0].desc))||a[0],[n,o]=(0,i.useState)({label:l.label,value:l.value}),s=(0,i.useMemo)((()=>a.map((e=>({label:e.label,value:e.value})))),[a]);return(0,y.Y)(ee,{children:(0,y.Y)(I.l6,{ariaLabel:(0,r.t)("Sort"),header:(0,y.Y)(m.lR,{children:(0,r.t)("Sort")}),labelInValue:!0,onChange:e=>{o(e);const l=a.find((({value:t})=>t===e.value));if(l){const e=[{id:l.id,desc:l.desc}];t(e)}},options:s,showSearch:!0,value:n})})};var ae=a(87196);const le=l.I4.div`
  text-align: center;

  .superset-list-view {
    text-align: left;
    border-radius: 4px 0;
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;

    .header {
      display: flex;
      padding-bottom: ${({theme:e})=>4*e.gridUnit}px;

      & .controls {
        display: flex;
        flex-wrap: wrap;
        column-gap: ${({theme:e})=>6*e.gridUnit}px;
        row-gap: ${({theme:e})=>4*e.gridUnit}px;
      }
    }

    .body.empty table {
      margin-bottom: 0;
    }

    .body {
      overflow-x: auto;
    }

    .ant-empty {
      .ant-empty-image {
        height: auto;
      }
    }
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,re=(0,l.I4)(n.A)`
  ${({theme:e})=>`\n    border-radius: 0;\n    margin-bottom: 0;\n    color: ${e.colors.grayscale.dark1};\n    background-color: ${e.colors.primary.light4};\n\n    .selectedCopy {\n      display: inline-block;\n      padding: ${2*e.gridUnit}px 0;\n    }\n\n    .deselect-all, .tag-btn {\n      color: ${e.colors.primary.base};\n      margin-left: ${4*e.gridUnit}px;\n    }\n\n    .divider {\n      margin: ${2*-e.gridUnit}px 0 ${2*-e.gridUnit}px ${4*e.gridUnit}px;\n      width: 1px;\n      height: ${8*e.gridUnit}px;\n      box-shadow: inset -1px 0px 0px ${e.colors.grayscale.light2};\n      display: inline-flex;\n      vertical-align: middle;\n      position: relative;\n    }\n\n    .ant-alert-close-icon {\n      margin-top: ${1.5*e.gridUnit}px;\n    }\n  `}
`,ie={Cell:({row:e})=>(0,y.Y)(u.A,{...e.getToggleRowSelectedProps(),id:e.id}),Header:({getToggleAllRowsSelectedProps:e})=>(0,y.Y)(u.A,{...e(),id:"header-toggle-all"}),id:"selection",size:"sm"},ne=l.I4.div`
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>5*e.gridUnit+1}px;
  white-space: nowrap;
  display: inline-block;

  .toggle-button {
    display: inline-block;
    border-radius: ${({theme:e})=>e.gridUnit/2}px;
    padding: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>.5*e.gridUnit}px;

    &:first-of-type {
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  .active {
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    svg {
      color: ${({theme:e})=>e.colors.grayscale.light5};
    }
  }
`,oe=l.I4.div`
  padding: ${({theme:e})=>40*e.gridUnit}px 0;

  &.table {
    background: ${({theme:e})=>e.colors.grayscale.light5};
  }
`,se=({mode:e,setMode:t})=>(0,y.FD)(ne,{children:[(0,y.Y)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("card")},className:s()("toggle-button",{active:"card"===e}),children:(0,y.Y)(c.A.CardView,{})}),(0,y.Y)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("table")},className:s()("toggle-button",{active:"table"===e}),children:(0,y.Y)(c.A.ListView,{})})]}),de=function({columns:e,data:t,count:a,pageSize:l,fetchData:n,refreshData:o,loading:s,initialSort:c=[],className:u="",filters:h=[],bulkActions:m=[],bulkSelectEnabled:f=!1,disableBulkSelect:b=(()=>{}),renderBulkSelectCopy:v=(e=>(0,r.t)("%s Selected",e.length)),renderCard:w,showThumbnails:S,cardSortSelectOptions:C,defaultViewMode:F="card",highlightRowId:I,emptyState:Y,columnsForWrapText:A,enableBulkTag:D=!1,bulkTagResourceName:P,addSuccessToast:M,addDangerToast:E}){const{getTableProps:V,getTableBodyProps:H,headerGroups:z,rows:O,prepareRow:j,pageCount:q=1,gotoPage:L,applyFilterValue:W,setSortBy:G,selectedFlatRows:K,toggleAllRowsSelected:Q,setViewMode:J,state:{pageIndex:X,pageSize:ee,internalFilters:ne,sortBy:de,viewMode:ce},query:ue}=function({fetchData:e,columns:t,data:a,count:l,initialPageSize:r,initialFilters:n=[],initialSort:o=[],bulkSelectMode:s=!1,bulkSelectColumnConfig:d,renderCard:c=!1,defaultViewMode:u="card"}){const[g,p]=(0,k.sq)({filters:R,pageIndex:k.hc,sortColumn:k.fr,sortOrder:k.fr,viewMode:k.fr}),h=(0,i.useMemo)((()=>g.sortColumn&&g.sortOrder?[{id:g.sortColumn,desc:"desc"===g.sortOrder}]:o),[o,g.sortColumn,g.sortOrder]),m={filters:g.filters?U(g.filters,n):[],pageIndex:g.pageIndex||0,pageSize:r,sortBy:h},[f,b]=(0,i.useState)(g.viewMode||(c?u:"table")),v=(0,i.useMemo)((()=>{const e=t.map((e=>({...e,filter:"exact"})));return s?[d,...e]:e}),[s,t]),{getTableProps:y,getTableBodyProps:w,headerGroups:x,rows:S,prepareRow:C,canPreviousPage:T,canNextPage:F,pageCount:I,gotoPage:Y,setAllFilters:A,setSortBy:D,selectedFlatRows:B,toggleAllRowsSelected:P,state:{pageIndex:M,pageSize:E,sortBy:V,filters:H}}=(0,_.useTable)({columns:v,count:l,data:a,disableFilters:!0,disableSortRemove:!0,initialState:m,manualFilters:!0,manualPagination:!0,manualSortBy:!0,autoResetFilters:!1,pageCount:Math.ceil(l/r)},_.useFilters,_.useSortBy,_.usePagination,_.useRowState,_.useRowSelect),[z,O]=(0,i.useState)(g.filters&&n.length?N(n,g.filters):[]);return(0,i.useEffect)((()=>{n.length&&O(N(n,g.filters?g.filters:{}))}),[n]),(0,i.useEffect)((()=>{const t={};z.forEach((e=>{if(void 0!==e.value&&("string"!=typeof e.value||e.value.length>0)){const a=e.urlDisplay||e.id;t[a]=e.value}}));const a={filters:Object.keys(t).length?t:void 0,pageIndex:M};V[0]&&(a.sortColumn=V[0].id,a.sortOrder=V[0].desc?"desc":"asc"),c&&(a.viewMode=f);const l=void 0!==g.pageIndex&&a.pageIndex!==g.pageIndex?"push":"replace";p(a,l),e({pageIndex:M,pageSize:E,sortBy:V,filters:H})}),[e,M,E,V,H]),(0,i.useEffect)((()=>{$()(m.pageIndex,M)||Y(m.pageIndex)}),[g]),{canNextPage:F,canPreviousPage:T,getTableBodyProps:w,getTableProps:y,gotoPage:Y,headerGroups:x,pageCount:I,prepareRow:C,rows:S,selectedFlatRows:B,setAllFilters:A,setSortBy:D,state:{pageIndex:M,pageSize:E,sortBy:V,filters:H,internalFilters:z,viewMode:f},toggleAllRowsSelected:P,applyFilterValue:(e,t)=>{O((a=>{if(a[e].value===t)return a;const l={...a[e],value:t},r=function(e,t,a){const l=e.find(((e,a)=>t===a));return[...e.slice(0,t),{...l,...a},...e.slice(t+1)]}(a,e,l);return A(r.filter((e=>!(void 0===e.value||Array.isArray(e.value)&&!e.value.length))).map((({value:e,operator:t,id:a})=>"between"===t&&Array.isArray(e)?[{value:e[0],operator:"gt",id:a},{value:e[1],operator:"lt",id:a}]:{value:e,operator:t,id:a})).flat()),Y(0),r}))},setViewMode:b,query:g}}({bulkSelectColumnConfig:ie,bulkSelectMode:f&&Boolean(m.length),columns:e,count:a,data:t,fetchData:n,initialPageSize:l,initialSort:c,initialFilters:h,renderCard:Boolean(w),defaultViewMode:F}),ge=P&&D,pe=Boolean(h.length);if(pe){const t=e.reduce(((e,t)=>({...e,[t.id||t.accessor]:!0})),{});h.forEach((e=>{if(!t[e.id])throw new B(`Invalid filter config, ${e.id} is not present in columns`)}))}const he=(0,i.useRef)(null),me=(0,i.useCallback)((()=>{var e;ue.filters&&(null==(e=he.current)||e.clearFilters())}),[ue.filters]),fe=Boolean(w),[be,ve]=(0,i.useState)(!1);return(0,i.useEffect)((()=>{f||Q(!1)}),[f,Q]),(0,i.useEffect)((()=>{!s&&X>q-1&&q>0&&L(0)}),[L,s,q,X]),(0,y.FD)(le,{children:[ge&&(0,y.Y)(x,{show:be,selected:K,refreshData:o,resourceName:P,addSuccessToast:M,addDangerToast:E,onHide:()=>ve(!1)}),(0,y.FD)("div",{className:`superset-list-view ${u}`,children:[(0,y.FD)("div",{className:"header",children:[fe&&(0,y.Y)(se,{mode:ce,setMode:J}),(0,y.FD)("div",{className:"controls",children:[pe&&(0,y.Y)(Z,{ref:he,filters:h,internalFilters:ne,updateFilterValue:W}),"card"===ce&&C&&(0,y.Y)(te,{initialSort:de,onChange:e=>G(e),options:C})]})]}),(0,y.FD)("div",{className:"body "+(0===O.length?"empty":""),children:[f&&(0,y.Y)(re,{type:"info",closable:!0,showIcon:!1,onClose:b,message:(0,y.FD)(y.FK,{children:[(0,y.Y)("div",{className:"selectedCopy",children:v(K)}),Boolean(K.length)&&(0,y.FD)(y.FK,{children:[(0,y.Y)("span",{role:"button",tabIndex:0,className:"deselect-all",onClick:()=>Q(!1),children:(0,r.t)("Deselect all")}),(0,y.Y)("div",{className:"divider"}),m.map((e=>(0,y.Y)(d.A,{buttonStyle:e.type,cta:!0,onClick:()=>e.onSelect(K.map((e=>e.original))),children:e.name},e.key))),D&&(0,y.Y)("span",{role:"button",tabIndex:0,className:"tag-btn",onClick:()=>ve(!0),children:(0,r.t)("Add Tag")})]})]})}),"card"===ce&&(0,y.Y)(T,{bulkSelectEnabled:f,prepareRow:j,renderCard:w,rows:O,loading:s,showThumbnails:S}),"table"===ce&&(0,y.Y)(p.A,{getTableProps:V,getTableBodyProps:H,prepareRow:j,headerGroups:z,rows:O,columns:e,loading:s,highlightRowId:I,columnsForWrapText:A}),!s&&0===O.length&&(0,y.Y)(oe,{className:ce,children:ue.filters?(0,y.Y)(ae.nw,{title:(0,r.t)("No results match your filter criteria"),description:(0,r.t)("Try different criteria to display results."),image:"filter-results.svg",buttonAction:()=>me(),buttonText:(0,r.t)("clear all filters")}):(0,y.Y)(ae.nw,{...Y,title:(null==Y?void 0:Y.title)||(0,r.t)("No Data"),image:(null==Y?void 0:Y.image)||"filter-results.svg"})})]})]}),O.length>0&&(0,y.FD)("div",{className:"pagination-container",children:[(0,y.Y)(g.A,{totalPages:q||0,currentPage:q&&X<q?X+1:0,onChange:e=>L(e-1),hideFirstAndLastPageLinks:!0}),(0,y.Y)("div",{className:"row-count-container",children:!s&&(0,r.t)("%s-%s of %s",ee*X+(O.length&&1),ee*X+O.length,a)})]})]})};var ce;!function(e){e.StartsWith="sw",e.EndsWith="ew",e.Contains="ct",e.Equals="eq",e.NotStartsWith="nsw",e.NotEndsWith="new",e.NotContains="nct",e.NotEquals="neq",e.GreaterThan="gt",e.LessThan="lt",e.RelationManyMany="rel_m_m",e.RelationOneMany="rel_o_m",e.TitleOrSlug="title_or_slug",e.NameOrDescription="name_or_description",e.AllText="all_text",e.ChartAllText="chart_all_text",e.DatasetIsNullOrEmpty="dataset_is_null_or_empty",e.Between="between",e.DashboardIsFav="dashboard_is_favorite",e.ChartIsFav="chart_is_favorite",e.ChartIsCertified="chart_is_certified",e.DashboardIsCertified="dashboard_is_certified",e.DatasetIsCertified="dataset_is_certified",e.DashboardHasCreatedBy="dashboard_has_created_by",e.ChartHasCreatedBy="chart_has_created_by",e.DashboardTagByName="dashboard_tags",e.DashboardTagById="dashboard_tag_id",e.ChartTagByName="chart_tags",e.ChartTagById="chart_tag_id",e.SavedQueryTagByName="saved_query_tags",e.SavedQueryTagById="saved_query_tag_id"}(ce||(ce={}))}}]);
//# sourceMappingURL=813c15ea64365be5b159.chunk.js.map