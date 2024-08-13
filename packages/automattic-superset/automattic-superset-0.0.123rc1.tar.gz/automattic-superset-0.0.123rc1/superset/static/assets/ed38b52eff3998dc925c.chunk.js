"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1003],{51003:(e,t,n)=>{n.d(t,{Kn:()=>E,un:()=>D,XI:()=>N,QS:()=>R,Ay:()=>A});var l=n(96540),o=n(58609),i=n(76421),r=n(96453),s=n(95579),a=n(5362),d=n(17444);const u=(e,t,n)=>{let l=!1;const o=t-e;return o>0&&o<=n&&(l=!0),l};class c{constructor(e,t,n){this.tableRef=void 0,this.columnRef=void 0,this.setDerivedColumns=void 0,this.isDragging=void 0,this.resizable=void 0,this.reorderable=void 0,this.derivedColumns=void 0,this.RESIZE_INDICATOR_THRESHOLD=void 0,this.clearListeners=()=>{document.removeEventListener("mouseup",this.handleMouseup),this.initializeResizableColumns(!1,this.tableRef),this.initializeDragDropColumns(!1,this.tableRef)},this.setTableRef=e=>{this.tableRef=e},this.getColumnIndex=()=>{var e;let t=-1;const n=null==(e=this.columnRef)?void 0:e.parentNode;return n&&(t=Array.prototype.indexOf.call(n.children,this.columnRef)),t},this.handleColumnDragStart=e=>{var t;const n=null==e?void 0:e.currentTarget;n&&(this.columnRef=n),this.isDragging=!0;const l=this.getColumnIndex(),o={index:l,columnData:this.derivedColumns[l]};null==e||null==(t=e.dataTransfer)||t.setData(D,JSON.stringify(o))},this.handleDragDrop=e=>{var t;if(null==(t=e.dataTransfer)||null==t.getData?void 0:t.getData(D)){var n;e.preventDefault();const t=null==(n=e.currentTarget)?void 0:n.parentNode,l=Array.prototype.indexOf.call(t.children,e.currentTarget),o=this.getColumnIndex(),i=[...this.derivedColumns],r=i.slice(o,o+1);i.splice(o,1),i.splice(l,0,r[0]),this.derivedColumns=[...i],this.setDerivedColumns(i)}},this.allowDrop=e=>{e.preventDefault()},this.handleMouseDown=e=>{const t=null==e?void 0:e.currentTarget;t&&(this.columnRef=t,e&&u(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?(t.mouseDown=!0,t.oldX=e.x,t.oldWidth=t.offsetWidth,t.draggable=!1):this.reorderable&&(t.draggable=!0))},this.handleMouseMove=e=>{if(!0===this.resizable&&!this.isDragging){const t=e.currentTarget;e&&u(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?t.style.cursor="col-resize":t.style.cursor="default";const n=this.columnRef;if(null!=n&&n.mouseDown){let t=n.oldWidth;const l=e.x-n.oldX;n.oldWidth+(e.x-n.oldX)>0&&(t=n.oldWidth+l);const o=this.getColumnIndex();if(!Number.isNaN(o)){const e={...this.derivedColumns[o]};e.width=t,this.derivedColumns[o]=e,this.setDerivedColumns([...this.derivedColumns])}}}},this.handleMouseup=()=>{this.columnRef&&(this.columnRef.mouseDown=!1,this.columnRef.style.cursor="default",this.columnRef.draggable=!1),this.isDragging=!1},this.initializeResizableColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const o=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(o){const{cells:t}=o,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.resizable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("mousemove",this.handleMouseMove,!0)):(this.resizable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("mousemove",this.handleMouseMove,!0))}}},this.initializeDragDropColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const o=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(o){const{cells:t}=o,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.reorderable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("dragover",this.allowDrop),n.addEventListener("dragstart",this.handleColumnDragStart),n.addEventListener("drop",this.handleDragDrop)):(this.reorderable=!1,n.draggable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("dragover",this.allowDrop),n.removeEventListener("dragstart",this.handleColumnDragStart),n.removeEventListener("drop",this.handleDragDrop))}}},this.setDerivedColumns=n,this.tableRef=e,this.isDragging=!1,this.RESIZE_INDICATOR_THRESHOLD=8,this.resizable=!1,this.reorderable=!1,this.derivedColumns=[...t],document.addEventListener("mouseup",this.handleMouseup)}}var h=n(46942),g=n.n(h),f=n(98250),p=n(5373),m=n(58642),v=n(2445);const b=(0,r.I4)("div")((({theme:e,height:t})=>`\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  padding-left: ${2*e.gridUnit}px;\n  padding-right: ${e.gridUnit}px;\n  border-bottom: 1px solid ${e.colors.grayscale.light3};\n  transition: background 0.3s;\n  line-height: ${t}px;\n  box-sizing: border-box;\n`)),w=(0,r.I4)(o.A)((({theme:e})=>`\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n      }\n    }\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n`)),D="superset/table-column";var C,E,R;!function(e){e.Disabled="disabled",e.Single="single",e.Multi="multi"}(C||(C={})),function(e){e.Paginate="paginate",e.Sort="sort",e.Filter="filter"}(E||(E={})),function(e){e.Small="small",e.Middle="middle"}(R||(R={}));const y=[],S=40,x=68,T=(0,r.I4)(o.A)((({theme:e,height:t})=>`\n    .ant-table-body {\n      overflow: auto;\n      height: ${t?`${t}px`:void 0};\n    }\n\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-table-tbody > tr > td {\n      user-select: none;\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n      border-bottom: 1px solid ${e.colors.grayscale.light3};\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n    }\n\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n  `)),z=(0,r.I4)((e=>{var t;const{columns:n,pagination:o,onChange:i,height:s,scroll:a,size:d,allowHTML:u=!1}=e,[c,h]=(0,l.useState)(0),D=(0,l.useCallback)((e=>{h(e)}),[]),{ref:C}=(0,f.uZ)({onResize:D}),y=(0,r.DP)(),S=37*(null==y?void 0:y.gridUnit)||150,x=n.filter((({width:e})=>!e)).length;let T=0;null==n||n.forEach((e=>{e.width&&(T+=e.width)}));let z=0;const L=Math.max(Math.floor((c-T)/x),50),I=null!=(t=null==n||null==n.map?void 0:n.map((e=>{const t={...e};return e.width||(t.width=L),z+=t.width,t})))?t:[];if(z<c){const e=I[I.length-1];e.width=e.width+Math.floor(c-z)}const M=(0,l.useRef)(),[N]=(0,l.useState)((()=>{const e={};return Object.defineProperty(e,"scrollLeft",{get:()=>{var e,t;return M.current?null==(e=M.current)||null==(t=e.state)?void 0:t.scrollLeft:null},set:e=>{M.current&&M.current.scrollTo({scrollLeft:e})}}),e})),A=()=>{var e;null==(e=M.current)||e.resetAfterIndices({columnIndex:0,shouldForceUpdate:!0})};(0,l.useEffect)((()=>A),[c,n,d]);const O={...o,onChange:(e,t)=>{var n;null==(n=M.current)||null==n.scrollTo||n.scrollTo({scrollTop:0}),null==i||i({...o,current:e,pageSize:t},{},{},{action:E.Paginate,currentDataSource:[]})}};return(0,v.Y)("div",{ref:C,children:(0,v.Y)(w,{...e,sticky:!1,className:"virtual-table",columns:I,components:{body:(e,{ref:t,onScroll:n})=>{t.current=N;const l=d===R.Middle?47:39;return(0,v.Y)(p.cB,{ref:M,className:"virtual-grid",columnCount:I.length,columnWidth:e=>{const{width:t=S}=I[e];return t},height:s||a.y,rowCount:e.length,rowHeight:()=>l,width:c,onScroll:({scrollLeft:e})=>{n({scrollLeft:e})},children:({columnIndex:t,rowIndex:n,style:o})=>{var i,r;const s=null==e?void 0:e[n];let a=null==s?void 0:s[null==I||null==(i=I[t])?void 0:i.dataIndex];const d=null==(r=I[t])?void 0:r.render;return"function"==typeof d&&(a=d(a,s,n)),u&&"string"==typeof a&&(a=(0,m.nn)(a)),(0,v.Y)(b,{className:g()("virtual-table-cell",{"virtual-table-cell-last":t===I.length-1}),style:o,title:"string"==typeof a?a:void 0,theme:y,height:l,children:a})}})}},pagination:!!o&&O})})}))((({theme:e})=>`\n  .virtual-table .ant-table-container:before,\n  .virtual-table .ant-table-container:after {\n    display: none;\n  }\n  .virtual-table-cell {\n    box-sizing: border-box;\n    padding: ${4*e.gridUnit}px;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n  }\n`)),L={filterTitle:(0,s.t)("Filter menu"),filterConfirm:(0,s.t)("OK"),filterReset:(0,s.t)("Reset"),filterEmptyText:(0,s.t)("No filters"),filterCheckall:(0,s.t)("Select all items"),filterSearchPlaceholder:(0,s.t)("Search in filters"),emptyText:(0,s.t)("No data"),selectAll:(0,s.t)("Select current page"),selectInvert:(0,s.t)("Invert current page"),selectNone:(0,s.t)("Clear all data"),selectionAll:(0,s.t)("Select all data"),sortTitle:(0,s.t)("Sort"),expand:(0,s.t)("Expand row"),collapse:(0,s.t)("Collapse row"),triggerDesc:(0,s.t)("Click to sort descending"),triggerAsc:(0,s.t)("Click to sort ascending"),cancelSort:(0,s.t)("Click to cancel sorting")},I={},M=()=>{};function N(e){const{data:t,bordered:n,columns:o,selectedRows:s=y,handleRowSelection:u,size:h=R.Small,selectionType:g=C.Disabled,sticky:f=!0,loading:p=!1,resizable:m=!1,reorderable:b=!1,usePagination:w=!0,defaultPageSize:D=15,pageSizeOptions:E=["5","15","25","50","100"],hideData:N=!1,emptyComponent:A,locale:O,height:k,virtualize:$=!1,onChange:H=M,recordCount:P,onRow:Y,allowHTML:W=!1,childrenColumnName:X}=e,_=(0,l.useRef)(null),[U,F]=(0,l.useState)(o),[Z,B]=(0,l.useState)(D),[K,j]=(0,l.useState)({...L}),[J,Q]=(0,l.useState)(s),q=(0,l.useRef)(null),G=I[g],V={type:G,selectedRowKeys:J,onChange:e=>{Q(e),null==u||u(e)}};(0,l.useEffect)((()=>{!0===b&&a.A.warn('EXPERIMENTAL FEATURE ENABLED: The "reorderable" prop of Table is experimental and NOT recommended for use in production deployments.'),!0===m&&a.A.warn('EXPERIMENTAL FEATURE ENABLED: The "resizable" prop of Table is experimental and NOT recommended for use in production deployments.')}),[b,m]),(0,l.useEffect)((()=>{let e;e=O?{...L,...O}:{...L},j(e)}),[O]),(0,l.useEffect)((()=>F(o)),[o]),(0,l.useEffect)((()=>{var e,t;q.current&&(null==(t=q.current)||t.clearListeners());const n=null==(e=_.current)?void 0:e.getElementsByTagName("table")[0];var l,o;n&&(q.current=new c(n,U,F),b&&(null==q||null==(l=q.current)||l.initializeDragDropColumns(b,n)),m&&(null==q||null==(o=q.current)||o.initializeResizableColumns(m,n)));return()=>{var e;null==q||null==(e=q.current)||null==e.clearListeners||e.clearListeners()}}),[_,b,m,$,q]);const ee=(0,r.DP)(),te=!!w&&{hideOnSinglePage:!0,pageSize:Z,pageSizeOptions:E,onShowSizeChange:(e,t)=>B(t)};te&&P&&(te.total=P);let ne=k;ne&&(ne-=x,w&&P&&P>Z&&(ne-=S));const le={loading:{spinning:null!=p&&p,indicator:(0,v.Y)(d.A,{})},hasData:!N&&t,columns:U,dataSource:N?void 0:t,size:h,pagination:te,locale:K,showSorterTooltip:!1,onChange:H,onRow:Y,theme:ee,height:ne,bordered:n,expandable:{childrenColumnName:X}};return(0,v.Y)(i.default,{renderEmpty:()=>null!=A?A:(0,v.Y)("div",{children:K.emptyText}),children:(0,v.FD)("div",{ref:_,children:[!$&&(0,v.Y)(T,{...le,rowSelection:G?V:void 0,sticky:f}),$&&(0,v.Y)(z,{...le,scroll:{y:300,x:"100vw",...!1},allowHTML:W})]})})}I[C.Multi]="checkbox",I[C.Single]="radio",I[C.Disabled]=null;const A=N}}]);
//# sourceMappingURL=ed38b52eff3998dc925c.chunk.js.map