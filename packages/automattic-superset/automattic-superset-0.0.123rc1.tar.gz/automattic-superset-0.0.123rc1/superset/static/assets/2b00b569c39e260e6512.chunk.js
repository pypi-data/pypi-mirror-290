"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2976],{4881:(e,a,r)=>{r.d(a,{QU:()=>g,U_:()=>h,VE:()=>u,d2:()=>c,lJ:()=>b,nB:()=>n,tb:()=>d});var t=r(5556),s=r.n(t),i=r(49588),o=r(56837),l=r(44672);const n=s().shape({id:s().string.isRequired,type:s().oneOf(Object.values(i.Ay)).isRequired,parents:s().arrayOf(s().string),children:s().arrayOf(s().string),meta:s().shape({width:s().number,height:s().number,headerSize:s().oneOf(l.A.map((e=>e.value))),background:s().oneOf(o.A.map((e=>e.value))),chartId:s().number})}),d=s().shape({id:s().number.isRequired,chartAlert:s().string,chartStatus:s().string,chartUpdateEndTime:s().number,chartUpdateStartTime:s().number,latestQueryFormData:s().object,queryController:s().shape({abort:s().func}),queriesResponse:s().arrayOf(s().object),triggerQuery:s().bool,lastRendered:s().number}),u=s().shape({slice_id:s().number.isRequired,slice_url:s().string.isRequired,slice_name:s().string.isRequired,datasource:s().string,datasource_name:s().string,datasource_link:s().string,changed_on:s().number.isRequired,modified:s().string,viz_type:s().string.isRequired,description:s().string,description_markeddown:s().string,owners:s().arrayOf(s().string)}),c=s().shape({chartId:s().number.isRequired,componentId:s().string.isRequired,filterName:s().string.isRequired,datasourceId:s().string.isRequired,directPathToFilter:s().arrayOf(s().string).isRequired,isDateFilter:s().bool.isRequired,isInstantFilter:s().bool.isRequired,columns:s().object,labels:s().object,scopes:s().object}),h=s().shape({sliceIds:s().arrayOf(s().number),expandedSlices:s().object,editMode:s().bool,isPublished:s().bool,colorNamespace:s().string,colorScheme:s().string,updatedColorScheme:s().bool,hasUnsavedChanges:s().bool}),b=s().shape({id:s().number,metadata:s().object,slug:s().string,dash_edit_perm:s().bool,dash_save_perm:s().bool,common:s().object,userId:s().string}),m=s().shape({value:s().oneOfType([s().number,s().string]).isRequired,label:s().string.isRequired}),p={value:s().oneOfType([s().number,s().string]).isRequired,label:s().string.isRequired,children:s().arrayOf(s().oneOfType([s().shape((_=()=>p,()=>_().apply(void 0,arguments))),m]))};var _;const g=s().oneOfType([s().shape(p),m])},56837:(e,a,r)=>{r.d(a,{A:()=>i});var t=r(95579),s=r(81151);const i=[{value:s.kn,label:(0,t.t)("Transparent"),className:"background--transparent"},{value:s.X0,label:(0,t.t)("White"),className:"background--white"}]},44672:(e,a,r)=>{r.d(a,{A:()=>i});var t=r(95579),s=r(81151);const i=[{value:s.It,label:(0,t.t)("Small"),className:"header-style-option header-small"},{value:s.W9,label:(0,t.t)("Medium"),className:"header-style-option header-medium"},{value:s.GY,label:(0,t.t)("Large"),className:"header-style-option header-large"}]},62221:(e,a,r)=>{var t;function s(e,a){try{const r=localStorage.getItem(e);return null===r?a:JSON.parse(r)}catch{return a}}function i(e,a){try{localStorage.setItem(e,JSON.stringify(a))}catch{}}function o(e,a){return s(e,a)}function l(e,a){i(e,a)}r.d(a,{Gq:()=>o,Hh:()=>t,SO:()=>l,SX:()=>s,Wr:()=>i}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.SqllabIsRenderHtmlEnabled="sqllab__is_render_html_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(t||(t={}))}}]);
//# sourceMappingURL=2b00b569c39e260e6512.chunk.js.map