"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[749],{92830:(t,e,o)=>{function n(t){var e=t.getBoundingClientRect(),o=document.documentElement;return{left:e.left+(window.pageXOffset||o.scrollLeft)-(o.clientLeft||document.body.clientLeft||0),top:e.top+(window.pageYOffset||o.scrollTop)-(o.clientTop||document.body.clientTop||0)}}o.d(e,{A3:()=>n})},17613:(t,e,o)=>{var n=o(24994).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function t(e){var o=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=[];return r.default.Children.forEach(e,(function(e){(null!=e||o.keepEmpty)&&(Array.isArray(e)?n=n.concat(t(e)):(0,i.isFragment)(e)&&e.props?n=n.concat(t(e.props.children,o)):n.push(e))})),n};var r=n(o(96540)),i=o(66351)},11161:(t,e,o)=>{var n=o(24994).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t,e,o,n){var i=r.default.unstable_batchedUpdates?function(t){r.default.unstable_batchedUpdates(o,t)}:o;return null!=t&&t.addEventListener&&t.addEventListener(e,i,n),{remove:function(){null!=t&&t.removeEventListener&&t.removeEventListener(e,i,n)}}};var r=n(o(28290))},33265:(t,e)=>{Object.defineProperty(e,"__esModule",{value:!0}),e.get=function(t,e){var l=arguments.length,a=i(t);return e=r[e]?"cssFloat"in t.style?"cssFloat":"styleFloat":e,1===l?a:function(t,e,r){if(e=e.toLowerCase(),"auto"===r){if("height"===e)return t.offsetHeight;if("width"===e)return t.offsetWidth}return e in n||(n[e]=o.test(e)),n[e]?parseFloat(r)||0:r}(t,e,a[e]||t.style[e])},e.getClientSize=function(){return{width:document.documentElement.clientWidth,height:window.innerHeight||document.documentElement.clientHeight}},e.getDocSize=function(){return{width:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),height:Math.max(document.documentElement.scrollHeight,document.body.scrollHeight)}},e.getOffset=function(t){var e=t.getBoundingClientRect(),o=document.documentElement;return{left:e.left+(window.pageXOffset||o.scrollLeft)-(o.clientLeft||document.body.clientLeft||0),top:e.top+(window.pageYOffset||o.scrollTop)-(o.clientTop||document.body.clientTop||0)}},e.getOuterHeight=function(t){return t===document.body?window.innerHeight||document.documentElement.clientHeight:t.offsetHeight},e.getOuterWidth=function(t){return t===document.body?document.documentElement.clientWidth:t.offsetWidth},e.getScroll=function(){return{scrollLeft:Math.max(document.documentElement.scrollLeft,document.body.scrollLeft),scrollTop:Math.max(document.documentElement.scrollTop,document.body.scrollTop)}},e.set=function t(e,n,l){var a=arguments.length;if(n=r[n]?"cssFloat"in e.style?"cssFloat":"styleFloat":n,3===a)return"number"==typeof l&&o.test(n)&&(l="".concat(l,"px")),e.style[n]=l,l;for(var s in n)n.hasOwnProperty(s)&&t(e,s,n[s]);return i(e)};var o=/margin|padding|width|height|max|min|offset/,n={left:!0,top:!0},r={cssFloat:1,styleFloat:1,float:1};function i(t){return 1===t.nodeType?t.ownerDocument.defaultView.getComputedStyle(t,null):{}}},17584:(t,e)=>{Object.defineProperty(e,"__esModule",{value:!0}),e.default=void 0,e.default=function(t){if(!t)return!1;if(t instanceof Element){if(t.offsetParent)return!0;if(t.getBBox){var e=t.getBBox(),o=e.width,n=e.height;if(o||n)return!0}if(t.getBoundingClientRect){var r=t.getBoundingClientRect(),i=r.width,l=r.height;if(i||l)return!0}}return!1}},85266:(t,e,o)=>{Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t){return"undefined"==typeof document?0:((t||void 0===n)&&(n=i()),n.width)},e.getTargetScrollBarSize=function(t){return"undefined"!=typeof document&&t&&t instanceof Element?i(t):{width:0,height:0}};var n,r=o(80084);function i(t){var e="rc-scrollbar-measure-".concat(Math.random().toString(36).substring(7)),o=document.createElement("div");o.id=e;var n,i,l=o.style;if(l.position="absolute",l.left="0",l.top="0",l.width="100px",l.height="100px",l.overflow="scroll",t){var a=getComputedStyle(t);l.scrollbarColor=a.scrollbarColor,l.scrollbarWidth=a.scrollbarWidth;var s=getComputedStyle(t,"::-webkit-scrollbar"),c=parseInt(s.width,10),u=parseInt(s.height,10);try{var d=c?"width: ".concat(s.width,";"):"",f=u?"height: ".concat(s.height,";"):"";(0,r.updateCSS)("\n#".concat(e,"::-webkit-scrollbar {\n").concat(d,"\n").concat(f,"\n}"),e)}catch(t){console.error(t),n=c,i=u}}document.body.appendChild(o);var h=t&&n&&!isNaN(n)?n:o.offsetWidth-o.clientWidth,p=t&&i&&!isNaN(i)?i:o.offsetHeight-o.clientHeight;return document.body.removeChild(o),(0,r.removeCSS)(e),{width:h,height:p}}},14773:(t,e,o)=>{var n=o(6305).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t){var e=r.useRef();return e.current=t,r.useCallback((function(){for(var t,o=arguments.length,n=new Array(o),r=0;r<o;r++)n[r]=arguments[r];return null===(t=e.current)||void 0===t?void 0:t.call.apply(t,[e].concat(n))}),[])};var r=n(o(96540))},34482:(t,e,o)=>{var n=o(24994).default,r=o(6305).default;Object.defineProperty(e,"__esModule",{value:!0}),e.useLayoutUpdateEffect=e.default=void 0;var i=r(o(96540)),l=(0,n(o(83477)).default)()?i.useLayoutEffect:i.useEffect,a=function(t,e){var o=i.useRef(!0);l((function(){return t(o.current)}),e),l((function(){return o.current=!1,function(){o.current=!0}}),[])};e.useLayoutUpdateEffect=function(t,e){a((function(e){if(!e)return t()}),e)},e.default=a},96680:(t,e,o)=>{var n=o(24994).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t,e){var o=e||{},n=o.defaultValue,c=o.value,u=o.onChange,d=o.postState,f=(0,a.default)((function(){return s(c)?c:s(n)?"function"==typeof n?n():n:"function"==typeof t?t():t})),h=(0,r.default)(f,2),p=h[0],m=h[1],v=void 0!==c?c:p,g=d?d(v):v,S=(0,i.default)(u),w=(0,a.default)([v]),I=(0,r.default)(w,2),_=I[0],y=I[1];return(0,l.useLayoutUpdateEffect)((function(){var t=_[0];p!==t&&S(p,t)}),[_]),(0,l.useLayoutUpdateEffect)((function(){s(c)||m(c)}),[c]),[g,(0,i.default)((function(t,e){m(t,e),y([v],e)}))]};var r=n(o(85715)),i=n(o(14773)),l=o(34482),a=n(o(43312));function s(t){return void 0!==t}},43312:(t,e,o)=>{var n=o(6305).default,r=o(24994).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t){var e=l.useRef(!1),o=l.useState(t),n=(0,i.default)(o,2),r=n[0],a=n[1];return l.useEffect((function(){return e.current=!1,function(){e.current=!0}}),[]),[r,function(t,o){o&&e.current||a(t)}]};var i=r(o(85715)),l=n(o(96540))},5373:(t,e,o)=>{o.d(e,{Y1:()=>O,cB:()=>M});var n=o(58168),r=o(9417),i=o(77387),l=o(41811),a=o(96540),s="object"==typeof performance&&"function"==typeof performance.now?function(){return performance.now()}:function(){return Date.now()};function c(t){cancelAnimationFrame(t.id)}function u(t,e){var o=s(),n={id:requestAnimationFrame((function r(){s()-o>=e?t.call(null):n.id=requestAnimationFrame(r)}))};return n}var d=-1;function f(t){if(void 0===t&&(t=!1),-1===d||t){var e=document.createElement("div"),o=e.style;o.width="50px",o.height="50px",o.overflow="scroll",document.body.appendChild(e),d=e.offsetWidth-e.clientWidth,document.body.removeChild(e)}return d}var h=null;function p(t){if(void 0===t&&(t=!1),null===h||t){var e=document.createElement("div"),o=e.style;o.width="50px",o.height="50px",o.overflow="scroll",o.direction="rtl";var n=document.createElement("div"),r=n.style;return r.width="100px",r.height="100px",e.appendChild(n),document.body.appendChild(e),e.scrollLeft>0?h="positive-descending":(e.scrollLeft=1,h=0===e.scrollLeft?"negative":"positive-ascending"),document.body.removeChild(e),h}return h}var m=function(t){var e=t.columnIndex;return t.data,t.rowIndex+":"+e};function v(t){var e,o=t.getColumnOffset,s=t.getColumnStartIndexForOffset,d=t.getColumnStopIndexForStartIndex,h=t.getColumnWidth,v=t.getEstimatedTotalHeight,S=t.getEstimatedTotalWidth,w=t.getOffsetForColumnAndAlignment,I=t.getOffsetForRowAndAlignment,_=t.getRowHeight,y=t.getRowOffset,C=t.getRowStartIndexForOffset,x=t.getRowStopIndexForStartIndex,M=t.initInstanceProps,R=t.shouldResetStyleCacheOnItemSizeChange,b=t.validateProps;return(e=function(t){function e(e){var n;return(n=t.call(this,e)||this)._instanceProps=M(n.props,(0,r.A)(n)),n._resetIsScrollingTimeoutId=null,n._outerRef=void 0,n.state={instance:(0,r.A)(n),isScrolling:!1,horizontalScrollDirection:"forward",scrollLeft:"number"==typeof n.props.initialScrollLeft?n.props.initialScrollLeft:0,scrollTop:"number"==typeof n.props.initialScrollTop?n.props.initialScrollTop:0,scrollUpdateWasRequested:!1,verticalScrollDirection:"forward"},n._callOnItemsRendered=void 0,n._callOnItemsRendered=(0,l.A)((function(t,e,o,r,i,l,a,s){return n.props.onItemsRendered({overscanColumnStartIndex:t,overscanColumnStopIndex:e,overscanRowStartIndex:o,overscanRowStopIndex:r,visibleColumnStartIndex:i,visibleColumnStopIndex:l,visibleRowStartIndex:a,visibleRowStopIndex:s})})),n._callOnScroll=void 0,n._callOnScroll=(0,l.A)((function(t,e,o,r,i){return n.props.onScroll({horizontalScrollDirection:o,scrollLeft:t,scrollTop:e,verticalScrollDirection:r,scrollUpdateWasRequested:i})})),n._getItemStyle=void 0,n._getItemStyle=function(t,e){var r,i=n.props,l=i.columnWidth,a=i.direction,s=i.rowHeight,c=n._getItemStyleCache(R&&l,R&&a,R&&s),u=t+":"+e;if(c.hasOwnProperty(u))r=c[u];else{var d=o(n.props,e,n._instanceProps),f="rtl"===a;c[u]=r={position:"absolute",left:f?void 0:d,right:f?d:void 0,top:y(n.props,t,n._instanceProps),height:_(n.props,t,n._instanceProps),width:h(n.props,e,n._instanceProps)}}return r},n._getItemStyleCache=void 0,n._getItemStyleCache=(0,l.A)((function(t,e,o){return{}})),n._onScroll=function(t){var e=t.currentTarget,o=e.clientHeight,r=e.clientWidth,i=e.scrollLeft,l=e.scrollTop,a=e.scrollHeight,s=e.scrollWidth;n.setState((function(t){if(t.scrollLeft===i&&t.scrollTop===l)return null;var e=n.props.direction,c=i;if("rtl"===e)switch(p()){case"negative":c=-i;break;case"positive-descending":c=s-r-i}c=Math.max(0,Math.min(c,s-r));var u=Math.max(0,Math.min(l,a-o));return{isScrolling:!0,horizontalScrollDirection:t.scrollLeft<i?"forward":"backward",scrollLeft:c,scrollTop:u,verticalScrollDirection:t.scrollTop<l?"forward":"backward",scrollUpdateWasRequested:!1}}),n._resetIsScrollingDebounced)},n._outerRefSetter=function(t){var e=n.props.outerRef;n._outerRef=t,"function"==typeof e?e(t):null!=e&&"object"==typeof e&&e.hasOwnProperty("current")&&(e.current=t)},n._resetIsScrollingDebounced=function(){null!==n._resetIsScrollingTimeoutId&&c(n._resetIsScrollingTimeoutId),n._resetIsScrollingTimeoutId=u(n._resetIsScrolling,150)},n._resetIsScrolling=function(){n._resetIsScrollingTimeoutId=null,n.setState({isScrolling:!1},(function(){n._getItemStyleCache(-1)}))},n}(0,i.A)(e,t),e.getDerivedStateFromProps=function(t,e){return g(t,e),b(t),null};var T=e.prototype;return T.scrollTo=function(t){var e=t.scrollLeft,o=t.scrollTop;void 0!==e&&(e=Math.max(0,e)),void 0!==o&&(o=Math.max(0,o)),this.setState((function(t){return void 0===e&&(e=t.scrollLeft),void 0===o&&(o=t.scrollTop),t.scrollLeft===e&&t.scrollTop===o?null:{horizontalScrollDirection:t.scrollLeft<e?"forward":"backward",scrollLeft:e,scrollTop:o,scrollUpdateWasRequested:!0,verticalScrollDirection:t.scrollTop<o?"forward":"backward"}}),this._resetIsScrollingDebounced)},T.scrollToItem=function(t){var e=t.align,o=void 0===e?"auto":e,n=t.columnIndex,r=t.rowIndex,i=this.props,l=i.columnCount,a=i.height,s=i.rowCount,c=i.width,u=this.state,d=u.scrollLeft,h=u.scrollTop,p=f();void 0!==n&&(n=Math.max(0,Math.min(n,l-1))),void 0!==r&&(r=Math.max(0,Math.min(r,s-1)));var m=v(this.props,this._instanceProps),g=S(this.props,this._instanceProps)>c?p:0,_=m>a?p:0;this.scrollTo({scrollLeft:void 0!==n?w(this.props,n,o,d,this._instanceProps,_):d,scrollTop:void 0!==r?I(this.props,r,o,h,this._instanceProps,g):h})},T.componentDidMount=function(){var t=this.props,e=t.initialScrollLeft,o=t.initialScrollTop;if(null!=this._outerRef){var n=this._outerRef;"number"==typeof e&&(n.scrollLeft=e),"number"==typeof o&&(n.scrollTop=o)}this._callPropsCallbacks()},T.componentDidUpdate=function(){var t=this.props.direction,e=this.state,o=e.scrollLeft,n=e.scrollTop;if(e.scrollUpdateWasRequested&&null!=this._outerRef){var r=this._outerRef;if("rtl"===t)switch(p()){case"negative":r.scrollLeft=-o;break;case"positive-ascending":r.scrollLeft=o;break;default:var i=r.clientWidth,l=r.scrollWidth;r.scrollLeft=l-i-o}else r.scrollLeft=Math.max(0,o);r.scrollTop=Math.max(0,n)}this._callPropsCallbacks()},T.componentWillUnmount=function(){null!==this._resetIsScrollingTimeoutId&&c(this._resetIsScrollingTimeoutId)},T.render=function(){var t=this.props,e=t.children,o=t.className,r=t.columnCount,i=t.direction,l=t.height,s=t.innerRef,c=t.innerElementType,u=t.innerTagName,d=t.itemData,f=t.itemKey,h=void 0===f?m:f,p=t.outerElementType,g=t.outerTagName,w=t.rowCount,I=t.style,_=t.useIsScrolling,y=t.width,C=this.state.isScrolling,x=this._getHorizontalRangeToRender(),M=x[0],R=x[1],b=this._getVerticalRangeToRender(),T=b[0],O=b[1],P=[];if(r>0&&w)for(var z=T;z<=O;z++)for(var L=M;L<=R;L++)P.push((0,a.createElement)(e,{columnIndex:L,data:d,isScrolling:_?C:void 0,key:h({columnIndex:L,data:d,rowIndex:z}),rowIndex:z,style:this._getItemStyle(z,L)}));var W=v(this.props,this._instanceProps),E=S(this.props,this._instanceProps);return(0,a.createElement)(p||g||"div",{className:o,onScroll:this._onScroll,ref:this._outerRefSetter,style:(0,n.A)({position:"relative",height:l,width:y,overflow:"auto",WebkitOverflowScrolling:"touch",willChange:"transform",direction:i},I)},(0,a.createElement)(c||u||"div",{children:P,ref:s,style:{height:W,pointerEvents:C?"none":void 0,width:E}}))},T._callPropsCallbacks=function(){var t=this.props,e=t.columnCount,o=t.onItemsRendered,n=t.onScroll,r=t.rowCount;if("function"==typeof o&&e>0&&r>0){var i=this._getHorizontalRangeToRender(),l=i[0],a=i[1],s=i[2],c=i[3],u=this._getVerticalRangeToRender(),d=u[0],f=u[1],h=u[2],p=u[3];this._callOnItemsRendered(l,a,d,f,s,c,h,p)}if("function"==typeof n){var m=this.state,v=m.horizontalScrollDirection,g=m.scrollLeft,S=m.scrollTop,w=m.scrollUpdateWasRequested,I=m.verticalScrollDirection;this._callOnScroll(g,S,v,I,w)}},T._getHorizontalRangeToRender=function(){var t=this.props,e=t.columnCount,o=t.overscanColumnCount,n=t.overscanColumnsCount,r=t.overscanCount,i=t.rowCount,l=this.state,a=l.horizontalScrollDirection,c=l.isScrolling,u=l.scrollLeft,f=o||n||r||1;if(0===e||0===i)return[0,0,0,0];var h=s(this.props,u,this._instanceProps),p=d(this.props,h,u,this._instanceProps),m=c&&"backward"!==a?1:Math.max(1,f),v=c&&"forward"!==a?1:Math.max(1,f);return[Math.max(0,h-m),Math.max(0,Math.min(e-1,p+v)),h,p]},T._getVerticalRangeToRender=function(){var t=this.props,e=t.columnCount,o=t.overscanCount,n=t.overscanRowCount,r=t.overscanRowsCount,i=t.rowCount,l=this.state,a=l.isScrolling,s=l.verticalScrollDirection,c=l.scrollTop,u=n||r||o||1;if(0===e||0===i)return[0,0,0,0];var d=C(this.props,c,this._instanceProps),f=x(this.props,d,c,this._instanceProps),h=a&&"backward"!==s?1:Math.max(1,u),p=a&&"forward"!==s?1:Math.max(1,u);return[Math.max(0,d-h),Math.max(0,Math.min(i-1,f+p)),d,f]},e}(a.PureComponent)).defaultProps={direction:"ltr",itemData:void 0,useIsScrolling:!1},e}var g=function(t,e){t.children,t.direction,t.height,t.innerTagName,t.outerTagName,t.overscanColumnsCount,t.overscanCount,t.overscanRowsCount,t.width,e.instance},S=function(t,e){var o=t.rowCount,n=e.rowMetadataMap,r=e.estimatedRowHeight,i=e.lastMeasuredRowIndex,l=0;if(i>=o&&(i=o-1),i>=0){var a=n[i];l=a.offset+a.size}return l+(o-i-1)*r},w=function(t,e){var o=t.columnCount,n=e.columnMetadataMap,r=e.estimatedColumnWidth,i=e.lastMeasuredColumnIndex,l=0;if(i>=o&&(i=o-1),i>=0){var a=n[i];l=a.offset+a.size}return l+(o-i-1)*r},I=function(t,e,o,n){var r,i,l;if("column"===t?(r=n.columnMetadataMap,i=e.columnWidth,l=n.lastMeasuredColumnIndex):(r=n.rowMetadataMap,i=e.rowHeight,l=n.lastMeasuredRowIndex),o>l){var a=0;if(l>=0){var s=r[l];a=s.offset+s.size}for(var c=l+1;c<=o;c++){var u=i(c);r[c]={offset:a,size:u},a+=u}"column"===t?n.lastMeasuredColumnIndex=o:n.lastMeasuredRowIndex=o}return r[o]},_=function(t,e,o,n){var r,i;return"column"===t?(r=o.columnMetadataMap,i=o.lastMeasuredColumnIndex):(r=o.rowMetadataMap,i=o.lastMeasuredRowIndex),(i>0?r[i].offset:0)>=n?y(t,e,o,i,0,n):C(t,e,o,Math.max(0,i),n)},y=function(t,e,o,n,r,i){for(;r<=n;){var l=r+Math.floor((n-r)/2),a=I(t,e,l,o).offset;if(a===i)return l;a<i?r=l+1:a>i&&(n=l-1)}return r>0?r-1:0},C=function(t,e,o,n,r){for(var i="column"===t?e.columnCount:e.rowCount,l=1;n<i&&I(t,e,n,o).offset<r;)n+=l,l*=2;return y(t,e,o,Math.min(n,i-1),Math.floor(n/2),r)},x=function(t,e,o,n,r,i,l){var a="column"===t?e.width:e.height,s=I(t,e,o,i),c="column"===t?w(e,i):S(e,i),u=Math.max(0,Math.min(c-a,s.offset)),d=Math.max(0,s.offset-a+l+s.size);switch("smart"===n&&(n=r>=d-a&&r<=u+a?"auto":"center"),n){case"start":return u;case"end":return d;case"center":return Math.round(d+(u-d)/2);default:return r>=d&&r<=u?r:d>u||r<d?d:u}},M=v({getColumnOffset:function(t,e,o){return I("column",t,e,o).offset},getColumnStartIndexForOffset:function(t,e,o){return _("column",t,o,e)},getColumnStopIndexForStartIndex:function(t,e,o,n){for(var r=t.columnCount,i=t.width,l=I("column",t,e,n),a=o+i,s=l.offset+l.size,c=e;c<r-1&&s<a;)c++,s+=I("column",t,c,n).size;return c},getColumnWidth:function(t,e,o){return o.columnMetadataMap[e].size},getEstimatedTotalHeight:S,getEstimatedTotalWidth:w,getOffsetForColumnAndAlignment:function(t,e,o,n,r,i){return x("column",t,e,o,n,r,i)},getOffsetForRowAndAlignment:function(t,e,o,n,r,i){return x("row",t,e,o,n,r,i)},getRowOffset:function(t,e,o){return I("row",t,e,o).offset},getRowHeight:function(t,e,o){return o.rowMetadataMap[e].size},getRowStartIndexForOffset:function(t,e,o){return _("row",t,o,e)},getRowStopIndexForStartIndex:function(t,e,o,n){for(var r=t.rowCount,i=t.height,l=I("row",t,e,n),a=o+i,s=l.offset+l.size,c=e;c<r-1&&s<a;)c++,s+=I("row",t,c,n).size;return c},initInstanceProps:function(t,e){var o=t,n={columnMetadataMap:{},estimatedColumnWidth:o.estimatedColumnWidth||50,estimatedRowHeight:o.estimatedRowHeight||50,lastMeasuredColumnIndex:-1,lastMeasuredRowIndex:-1,rowMetadataMap:{}};return e.resetAfterColumnIndex=function(t,o){void 0===o&&(o=!0),e.resetAfterIndices({columnIndex:t,shouldForceUpdate:o})},e.resetAfterRowIndex=function(t,o){void 0===o&&(o=!0),e.resetAfterIndices({rowIndex:t,shouldForceUpdate:o})},e.resetAfterIndices=function(t){var o=t.columnIndex,r=t.rowIndex,i=t.shouldForceUpdate,l=void 0===i||i;"number"==typeof o&&(n.lastMeasuredColumnIndex=Math.min(n.lastMeasuredColumnIndex,o-1)),"number"==typeof r&&(n.lastMeasuredRowIndex=Math.min(n.lastMeasuredRowIndex,r-1)),e._getItemStyleCache(-1),l&&e.forceUpdate()},n},shouldResetStyleCacheOnItemSizeChange:!1,validateProps:function(t){t.columnWidth,t.rowHeight}}),R=function(t,e){return t};function b(t){var e,o=t.getItemOffset,s=t.getEstimatedTotalSize,d=t.getItemSize,h=t.getOffsetForIndexAndAlignment,m=t.getStartIndexForOffset,v=t.getStopIndexForStartIndex,g=t.initInstanceProps,S=t.shouldResetStyleCacheOnItemSizeChange,w=t.validateProps;return e=function(t){function e(e){var n;return(n=t.call(this,e)||this)._instanceProps=g(n.props,(0,r.A)(n)),n._outerRef=void 0,n._resetIsScrollingTimeoutId=null,n.state={instance:(0,r.A)(n),isScrolling:!1,scrollDirection:"forward",scrollOffset:"number"==typeof n.props.initialScrollOffset?n.props.initialScrollOffset:0,scrollUpdateWasRequested:!1},n._callOnItemsRendered=void 0,n._callOnItemsRendered=(0,l.A)((function(t,e,o,r){return n.props.onItemsRendered({overscanStartIndex:t,overscanStopIndex:e,visibleStartIndex:o,visibleStopIndex:r})})),n._callOnScroll=void 0,n._callOnScroll=(0,l.A)((function(t,e,o){return n.props.onScroll({scrollDirection:t,scrollOffset:e,scrollUpdateWasRequested:o})})),n._getItemStyle=void 0,n._getItemStyle=function(t){var e,r=n.props,i=r.direction,l=r.itemSize,a=r.layout,s=n._getItemStyleCache(S&&l,S&&a,S&&i);if(s.hasOwnProperty(t))e=s[t];else{var c=o(n.props,t,n._instanceProps),u=d(n.props,t,n._instanceProps),f="horizontal"===i||"horizontal"===a,h="rtl"===i,p=f?c:0;s[t]=e={position:"absolute",left:h?void 0:p,right:h?p:void 0,top:f?0:c,height:f?"100%":u,width:f?u:"100%"}}return e},n._getItemStyleCache=void 0,n._getItemStyleCache=(0,l.A)((function(t,e,o){return{}})),n._onScrollHorizontal=function(t){var e=t.currentTarget,o=e.clientWidth,r=e.scrollLeft,i=e.scrollWidth;n.setState((function(t){if(t.scrollOffset===r)return null;var e=n.props.direction,l=r;if("rtl"===e)switch(p()){case"negative":l=-r;break;case"positive-descending":l=i-o-r}return l=Math.max(0,Math.min(l,i-o)),{isScrolling:!0,scrollDirection:t.scrollOffset<l?"forward":"backward",scrollOffset:l,scrollUpdateWasRequested:!1}}),n._resetIsScrollingDebounced)},n._onScrollVertical=function(t){var e=t.currentTarget,o=e.clientHeight,r=e.scrollHeight,i=e.scrollTop;n.setState((function(t){if(t.scrollOffset===i)return null;var e=Math.max(0,Math.min(i,r-o));return{isScrolling:!0,scrollDirection:t.scrollOffset<e?"forward":"backward",scrollOffset:e,scrollUpdateWasRequested:!1}}),n._resetIsScrollingDebounced)},n._outerRefSetter=function(t){var e=n.props.outerRef;n._outerRef=t,"function"==typeof e?e(t):null!=e&&"object"==typeof e&&e.hasOwnProperty("current")&&(e.current=t)},n._resetIsScrollingDebounced=function(){null!==n._resetIsScrollingTimeoutId&&c(n._resetIsScrollingTimeoutId),n._resetIsScrollingTimeoutId=u(n._resetIsScrolling,150)},n._resetIsScrolling=function(){n._resetIsScrollingTimeoutId=null,n.setState({isScrolling:!1},(function(){n._getItemStyleCache(-1,null)}))},n}(0,i.A)(e,t),e.getDerivedStateFromProps=function(t,e){return T(t,e),w(t),null};var I=e.prototype;return I.scrollTo=function(t){t=Math.max(0,t),this.setState((function(e){return e.scrollOffset===t?null:{scrollDirection:e.scrollOffset<t?"forward":"backward",scrollOffset:t,scrollUpdateWasRequested:!0}}),this._resetIsScrollingDebounced)},I.scrollToItem=function(t,e){void 0===e&&(e="auto");var o=this.props,n=o.itemCount,r=o.layout,i=this.state.scrollOffset;t=Math.max(0,Math.min(t,n-1));var l=0;if(this._outerRef){var a=this._outerRef;l="vertical"===r?a.scrollWidth>a.clientWidth?f():0:a.scrollHeight>a.clientHeight?f():0}this.scrollTo(h(this.props,t,e,i,this._instanceProps,l))},I.componentDidMount=function(){var t=this.props,e=t.direction,o=t.initialScrollOffset,n=t.layout;if("number"==typeof o&&null!=this._outerRef){var r=this._outerRef;"horizontal"===e||"horizontal"===n?r.scrollLeft=o:r.scrollTop=o}this._callPropsCallbacks()},I.componentDidUpdate=function(){var t=this.props,e=t.direction,o=t.layout,n=this.state,r=n.scrollOffset;if(n.scrollUpdateWasRequested&&null!=this._outerRef){var i=this._outerRef;if("horizontal"===e||"horizontal"===o)if("rtl"===e)switch(p()){case"negative":i.scrollLeft=-r;break;case"positive-ascending":i.scrollLeft=r;break;default:var l=i.clientWidth,a=i.scrollWidth;i.scrollLeft=a-l-r}else i.scrollLeft=r;else i.scrollTop=r}this._callPropsCallbacks()},I.componentWillUnmount=function(){null!==this._resetIsScrollingTimeoutId&&c(this._resetIsScrollingTimeoutId)},I.render=function(){var t=this.props,e=t.children,o=t.className,r=t.direction,i=t.height,l=t.innerRef,c=t.innerElementType,u=t.innerTagName,d=t.itemCount,f=t.itemData,h=t.itemKey,p=void 0===h?R:h,m=t.layout,v=t.outerElementType,g=t.outerTagName,S=t.style,w=t.useIsScrolling,I=t.width,_=this.state.isScrolling,y="horizontal"===r||"horizontal"===m,C=y?this._onScrollHorizontal:this._onScrollVertical,x=this._getRangeToRender(),M=x[0],b=x[1],T=[];if(d>0)for(var O=M;O<=b;O++)T.push((0,a.createElement)(e,{data:f,key:p(O,f),index:O,isScrolling:w?_:void 0,style:this._getItemStyle(O)}));var P=s(this.props,this._instanceProps);return(0,a.createElement)(v||g||"div",{className:o,onScroll:C,ref:this._outerRefSetter,style:(0,n.A)({position:"relative",height:i,width:I,overflow:"auto",WebkitOverflowScrolling:"touch",willChange:"transform",direction:r},S)},(0,a.createElement)(c||u||"div",{children:T,ref:l,style:{height:y?"100%":P,pointerEvents:_?"none":void 0,width:y?P:"100%"}}))},I._callPropsCallbacks=function(){if("function"==typeof this.props.onItemsRendered&&this.props.itemCount>0){var t=this._getRangeToRender(),e=t[0],o=t[1],n=t[2],r=t[3];this._callOnItemsRendered(e,o,n,r)}if("function"==typeof this.props.onScroll){var i=this.state,l=i.scrollDirection,a=i.scrollOffset,s=i.scrollUpdateWasRequested;this._callOnScroll(l,a,s)}},I._getRangeToRender=function(){var t=this.props,e=t.itemCount,o=t.overscanCount,n=this.state,r=n.isScrolling,i=n.scrollDirection,l=n.scrollOffset;if(0===e)return[0,0,0,0];var a=m(this.props,l,this._instanceProps),s=v(this.props,a,l,this._instanceProps),c=r&&"backward"!==i?1:Math.max(1,o),u=r&&"forward"!==i?1:Math.max(1,o);return[Math.max(0,a-c),Math.max(0,Math.min(e-1,s+u)),a,s]},e}(a.PureComponent),e.defaultProps={direction:"ltr",itemData:void 0,layout:"vertical",overscanCount:2,useIsScrolling:!1},e}var T=function(t,e){t.children,t.direction,t.height,t.layout,t.innerTagName,t.outerTagName,t.width,e.instance},O=b({getItemOffset:function(t,e){return e*t.itemSize},getItemSize:function(t,e){return t.itemSize},getEstimatedTotalSize:function(t){var e=t.itemCount;return t.itemSize*e},getOffsetForIndexAndAlignment:function(t,e,o,n,r,i){var l=t.direction,a=t.height,s=t.itemCount,c=t.itemSize,u=t.layout,d=t.width,f="horizontal"===l||"horizontal"===u?d:a,h=Math.max(0,s*c-f),p=Math.min(h,e*c),m=Math.max(0,e*c-f+c+i);switch("smart"===o&&(o=n>=m-f&&n<=p+f?"auto":"center"),o){case"start":return p;case"end":return m;case"center":var v=Math.round(m+(p-m)/2);return v<Math.ceil(f/2)?0:v>h+Math.floor(f/2)?h:v;default:return n>=m&&n<=p?n:n<m?m:p}},getStartIndexForOffset:function(t,e){var o=t.itemCount,n=t.itemSize;return Math.max(0,Math.min(o-1,Math.floor(e/n)))},getStopIndexForStartIndex:function(t,e,o){var n=t.direction,r=t.height,i=t.itemCount,l=t.itemSize,a=t.layout,s=t.width,c=e*l,u="horizontal"===n||"horizontal"===a?s:r,d=Math.ceil((u+o-c)/l);return Math.max(0,Math.min(i-1,e+d-1))},initInstanceProps:function(t){},shouldResetStyleCacheOnItemSizeChange:!0,validateProps:function(t){t.itemSize}})}}]);
//# sourceMappingURL=81c6582c0320a2c8ba9a.chunk.js.map