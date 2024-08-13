"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9428],{70175:(e,t,i)=>{var n;i.d(t,{Q:()=>n}),function(e){e.Dashboards="dashboards",e.Description="description",e.LastModified="lastModified",e.Owner="owner",e.Rows="rows",e.Sql="sql",e.Table="table",e.Tags="tags"}(n||(n={}))},13917:(e,t,i)=>{i.d(t,{QD:()=>v.Q,Ay:()=>$});var n=i(9063),l=i.n(n),a=i(96540),r=i(98250),o=i(96453),s=i(19129),d=i(62952),c=i(95579),p=i(12249),u=i(2445);const h=o.I4.div`
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,g=({text:e,header:t})=>{const i=(0,d.A)(e);return(0,u.FD)(u.FK,{children:[t&&(0,u.Y)(h,{children:t}),i.map((e=>(0,u.Y)("div",{children:e},e)))]})},m=16,f={dashboards:0,table:1,sql:2,rows:3,tags:4,description:5,owner:6,lastModified:7},b=o.I4.div`
  ${({theme:e,count:t})=>`\n    display: flex;\n    align-items: center;\n    padding: 8px 12px;\n    background-color: ${e.colors.grayscale.light4};\n    color: ${e.colors.grayscale.base};\n    font-size: ${e.typography.sizes.s}px;\n    min-width: ${24+32*t-m}px;\n    border-radius: ${e.borderRadius}px;\n    line-height: 1;\n  `}
`,x=o.I4.div`
  ${({theme:e,collapsed:t,last:i,onClick:n})=>`\n    display: flex;\n    align-items: center;\n    max-width: ${174+(i?0:m)}px;\n    min-width: ${t?16+(i?0:m):94+(i?0:m)}px;\n    padding-right: ${i?0:m}px;\n    cursor: ${n?"pointer":"default"};\n    & .metadata-icon {\n      color: ${n&&t?e.colors.primary.base:e.colors.grayscale.base};\n      padding-right: ${t?0:8}px;\n      & .anticon {\n        line-height: 0;\n      }\n    }\n    & .metadata-text {\n      min-width: 70px;\n      overflow: hidden;\n      text-overflow: ${t?"unset":"ellipsis"};\n      white-space: nowrap;\n      text-decoration: ${n?"underline":"none"};\n      line-height: 1.4;\n    }\n  `}
`,y=o.I4.div`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,w=({barWidth:e,contentType:t,collapsed:i,last:n=!1,tooltipPlacement:l})=>{const{icon:r,title:o,tooltip:d=o}=(e=>{const{type:t}=e;switch(t){case v.Q.Dashboards:return{icon:p.A.FundProjectionScreenOutlined,title:e.title,tooltip:e.description?(0,u.Y)("div",{children:(0,u.Y)(g,{header:e.title,text:e.description})}):void 0};case v.Q.Description:return{icon:p.A.BookOutlined,title:e.value};case v.Q.LastModified:return{icon:p.A.EditOutlined,title:e.value,tooltip:(0,u.FD)("div",{children:[(0,u.Y)(g,{header:(0,c.t)("Last modified"),text:e.value}),(0,u.Y)(g,{header:(0,c.t)("Modified by"),text:e.modifiedBy})]})};case v.Q.Owner:return{icon:p.A.UserOutlined,title:e.createdBy,tooltip:(0,u.FD)("div",{children:[(0,u.Y)(g,{header:(0,c.t)("Created by"),text:e.createdBy}),!!e.owners&&(0,u.Y)(g,{header:(0,c.t)("Owners"),text:e.owners}),(0,u.Y)(g,{header:(0,c.t)("Created on"),text:e.createdOn})]})};case v.Q.Rows:return{icon:p.A.InsertRowBelowOutlined,title:e.title,tooltip:e.title};case v.Q.Sql:return{icon:p.A.ConsoleSqlOutlined,title:e.title,tooltip:e.title};case v.Q.Table:return{icon:p.A.Table,title:e.title,tooltip:e.title};case v.Q.Tags:return{icon:p.A.TagsOutlined,title:e.values.join(", "),tooltip:(0,u.Y)("div",{children:(0,u.Y)(g,{header:(0,c.t)("Tags"),text:e.values})})};default:throw Error(`Invalid type provided: ${t}`)}})(t),[h,m]=(0,a.useState)(!1),f=(0,a.useRef)(null),b=r,{type:w,onClick:$}=t;(0,a.useEffect)((()=>{m(!!f.current&&f.current.scrollWidth>f.current.clientWidth)}),[e,m,t]);const S=(0,u.FD)(x,{collapsed:i,last:n,onClick:$?()=>$(w):void 0,role:$?"button":void 0,children:[(0,u.Y)(b,{iconSize:"l",className:"metadata-icon"}),!i&&(0,u.Y)("span",{ref:f,className:"metadata-text",children:o})]});return h||i||d&&d!==o?(0,u.Y)(s.m,{placement:l,title:(0,u.Y)(y,{children:d}),children:S}):S};var v=i(70175);const $=({items:e,tooltipPlacement:t="top"})=>{const[i,n]=(0,a.useState)(),[o,s]=(0,a.useState)(!1),d=l()(e,((e,t)=>e.type===t.type)).sort(((e,t)=>f[e.type]-f[t.type])),c=d.length;if(c<2)throw Error("The minimum number of items for the metadata bar is 2.");if(c>6)throw Error("The maximum number of items for the metadata bar is 6.");const p=(0,a.useCallback)((e=>{const t=110*c-m;n(e),s(Boolean(e&&e<t))}),[c]),{ref:h}=(0,r.uZ)({onResize:p});return(0,u.Y)(b,{ref:h,count:c,children:d.map(((e,n)=>(0,u.Y)(w,{barWidth:i,contentType:e,collapsed:o,last:n===c-1,tooltipPlacement:t},n)))})}},51848:(e,t,i)=>{i.d(t,{U:()=>v});var n=i(17437),l=i(96453),a=i(95579),r=i(15595),o=i(96540),s=i(19129),d=i(98250),c=i(2445);const p=e=>n.AH`
  display: flex;
  font-size: ${e.typography.sizes.xl}px;
  font-weight: ${e.typography.weights.bold};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  & .dynamic-title,
  & .dynamic-title-input {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  & .dynamic-title {
    cursor: default;
  }
  & .dynamic-title-input {
    border: none;
    padding: 0;
    outline: none;

    &::placeholder {
      color: ${e.colors.grayscale.light1};
    }
  }

  & .input-sizer {
    position: absolute;
    left: -9999px;
    display: inline-block;
    white-space: pre;
  }
`,u=(0,o.memo)((({title:e,placeholder:t,onSave:i,canEdit:l,label:r})=>{const[u,h]=(0,o.useState)(!1),[g,m]=(0,o.useState)(e||""),f=(0,o.useRef)(null),[b,x]=(0,o.useState)(!1),{width:y,ref:w}=(0,d.uZ)(),{width:v,ref:$}=(0,d.uZ)({refreshMode:"debounce"});(0,o.useEffect)((()=>{m(e)}),[e]),(0,o.useEffect)((()=>{if(u&&null!=f&&f.current&&(f.current.focus(),f.current.setSelectionRange)){const{length:e}=f.current.value;f.current.setSelectionRange(e,e),f.current.scrollLeft=f.current.scrollWidth}}),[u]),(0,o.useLayoutEffect)((()=>{null!=w&&w.current&&(w.current.textContent=g||t)}),[g,t,w]),(0,o.useEffect)((()=>{f.current&&f.current.scrollWidth>f.current.clientWidth?x(!0):x(!1)}),[y,v]);const S=(0,o.useCallback)((()=>{l&&!u&&h(!0)}),[l,u]),P=(0,o.useCallback)((()=>{if(!l)return;const t=g.trim();m(t),e!==t&&i(t),h(!1)}),[l,g,i,e]),Y=(0,o.useCallback)((e=>{l&&u&&m(e.target.value)}),[l,u]),k=(0,o.useCallback)((e=>{var t;l&&"Enter"===e.key&&(e.preventDefault(),null==(t=f.current)||t.blur())}),[l]);return(0,c.FD)("div",{css:p,ref:$,children:[(0,c.Y)(s.m,{id:"title-tooltip",title:b&&g&&!u?g:null,children:l?(0,c.Y)("input",{className:"dynamic-title-input","aria-label":null!=r?r:(0,a.t)("Title"),ref:f,onChange:Y,onBlur:P,onClick:S,onKeyPress:k,placeholder:t,value:g,css:n.AH`
                cursor: ${u?"text":"pointer"};

                ${y&&y>0&&n.AH`
                  width: ${y+1}px;
                `}
              `}):(0,c.Y)("span",{className:"dynamic-title","aria-label":null!=r?r:(0,a.t)("Title"),ref:f,children:g})}),(0,c.Y)("span",{ref:w,className:"input-sizer","aria-hidden":!0,tabIndex:-1})]})}));var h=i(58132),g=i(94704),m=i(12249),f=i(46920);const b=e=>n.AH`
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
  &:focus-visible {
    outline: 2px solid ${e.colors.primary.dark2};
  }
`,x=e=>n.AH`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-between;
  background-color: ${e.colors.grayscale.light5};
  height: ${16*e.gridUnit}px;
  padding: 0 ${4*e.gridUnit}px;

  .editable-title {
    overflow: hidden;

    & > input[type='button'],
    & > span {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      white-space: nowrap;
    }
  }

  span[role='button'] {
    display: flex;
    height: 100%;
  }

  .title-panel {
    display: flex;
    align-items: center;
    min-width: 0;
    margin-right: ${12*e.gridUnit}px;
  }

  .right-button-panel {
    display: flex;
    align-items: center;
  }
`,y=e=>n.AH`
  display: flex;
  align-items: center;
  padding-left: ${2*e.gridUnit}px;

  & .fave-unfave-icon {
    padding: 0 ${e.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,w=e=>n.AH`
  margin-left: ${2*e.gridUnit}px;
`,v=({editableTitleProps:e,showTitlePanelItems:t,certificatiedBadgeProps:i,showFaveStar:n,faveStarProps:o,titlePanelAdditionalItems:s,rightPanelAdditionalItems:d,additionalActionsMenu:p,menuDropdownProps:v,showMenuDropdown:$=!0,tooltipProps:S})=>{const P=(0,l.DP)();return(0,c.FD)("div",{css:x,className:"header-with-actions",children:[(0,c.FD)("div",{className:"title-panel",children:[(0,c.Y)(u,{...e}),t&&(0,c.FD)("div",{css:y,children:[(null==i?void 0:i.certifiedBy)&&(0,c.Y)(h.A,{...i}),n&&(0,c.Y)(g.A,{...o}),s]})]}),(0,c.FD)("div",{className:"right-button-panel",children:[d,(0,c.Y)("div",{css:w,children:$&&(0,c.Y)(r.rM,{trigger:["click"],overlay:p,...v,children:(0,c.Y)(f.A,{css:b,buttonStyle:"tertiary","aria-label":(0,a.t)("Menu actions trigger"),tooltip:null==S?void 0:S.text,placement:null==S?void 0:S.placement,children:(0,c.Y)(m.A.MoreHoriz,{iconColor:P.colors.primary.dark2,iconSize:"l"})})})})]})]})}},54016:(e,t,i)=>{i.d(t,{A:()=>x,V:()=>n});var n,l=i(2404),a=i.n(l),r=i(96540),o=i(96453),s=i(95579),d=i(38914),c=i(15595),p=i(47251),u=i(73204),h=i(2445);!function(e){e.Default="Default",e.Small="Small"}(n||(n={}));const g=o.I4.div`
  margin: ${({theme:e})=>40*e.gridUnit}px 0;
`,m=o.I4.div`
  ${({scrollTable:e,theme:t})=>e&&`\n    flex: 1 1 auto;\n    margin-bottom: ${4*t.gridUnit}px;\n    overflow: auto;\n  `}

  .table-row {
    ${({theme:e,small:t})=>!t&&`height: ${11*e.gridUnit-1}px;`}

    .table-cell {
      ${({theme:e,small:t})=>t&&`\n        padding-top: ${e.gridUnit+1}px;\n        padding-bottom: ${e.gridUnit+1}px;\n        line-height: 1.45;\n      `}
    }
  }

  th[role='columnheader'] {
    z-index: 1;
    border-bottom: ${({theme:e})=>`${e.gridUnit-2}px solid ${e.colors.grayscale.light2}`};
    ${({small:e})=>e&&"padding-bottom: 0;"}
  }
`,f=o.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};

  ${({isPaginationSticky:e})=>e&&"\n        position: sticky;\n        bottom: 0;\n        left: 0;\n    "};

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,b=({columns:e,data:t,pageSize:i,totalCount:l=t.length,initialPageIndex:o,initialSortBy:b=[],loading:x=!1,withPagination:y=!0,emptyWrapperType:w=n.Default,noDataText:v,showRowCount:$=!0,serverPagination:S=!1,columnsForWrapText:P,onServerPagination:Y=(()=>{}),scrollTopOnPagination:k=!1,...A})=>{const T={pageSize:null!=i?i:10,pageIndex:null!=o?o:0,sortBy:b},{getTableProps:D,getTableBodyProps:E,headerGroups:I,page:C,rows:F,prepareRow:B,pageCount:U,gotoPage:M,state:{pageIndex:z,pageSize:R,sortBy:N}}=(0,d.useTable)({columns:e,data:t,initialState:T,manualPagination:S,manualSortBy:S,pageCount:Math.ceil(l/T.pageSize)},d.useFilters,d.useSortBy,d.usePagination),O=y?C:F;let Q;switch(w){case n.Small:Q=({children:e})=>(0,h.Y)(h.FK,{children:e});break;case n.Default:default:Q=({children:e})=>(0,h.Y)(g,{children:e})}const W=!x&&0===O.length,L=U>1&&y,H=(0,r.useRef)(null);return(0,r.useEffect)((()=>{S&&z!==T.pageIndex&&Y({pageIndex:z})}),[z]),(0,r.useEffect)((()=>{S&&!a()(N,T.sortBy)&&Y({pageIndex:0,sortBy:N})}),[N]),(0,h.FD)(h.FK,{children:[(0,h.FD)(m,{...A,ref:H,children:[(0,h.Y)(u.A,{getTableProps:D,getTableBodyProps:E,prepareRow:B,headerGroups:I,rows:O,columns:e,loading:x,columnsForWrapText:P}),W&&(0,h.Y)(Q,{children:v?(0,h.Y)(c.Sv,{image:c.Sv.PRESENTED_IMAGE_SIMPLE,description:v}):(0,h.Y)(c.Sv,{image:c.Sv.PRESENTED_IMAGE_SIMPLE})})]}),L&&(0,h.FD)(f,{className:"pagination-container",isPaginationSticky:A.isPaginationSticky,children:[(0,h.Y)(p.A,{totalPages:U||0,currentPage:U?z+1:0,onChange:e=>(e=>{var t;k&&(null==H||null==(t=H.current)||t.scroll(0,0)),M(e)})(e-1),hideFirstAndLastPageLinks:!0}),$&&(0,h.Y)("div",{className:"row-count-container",children:!x&&(0,s.t)("%s-%s of %s",R*z+(C.length&&1),R*z+C.length,l)})]})]})},x=(0,r.memo)(b)},50217:(e,t,i)=>{i.d(t,{A:()=>n.A,V:()=>n.V});var n=i(54016)}}]);
//# sourceMappingURL=4fc7408216c8dc5a5635.chunk.js.map