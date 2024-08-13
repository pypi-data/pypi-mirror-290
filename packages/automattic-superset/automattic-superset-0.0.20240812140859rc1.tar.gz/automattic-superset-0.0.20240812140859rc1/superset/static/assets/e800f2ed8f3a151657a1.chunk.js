"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8209],{61816:(e,t,i)=>{i.d(t,{Q:()=>n,Y:()=>o});const n=[[255,255,178],[254,217,118],[254,178,76],[253,141,60],[240,59,32],[189,0,38]];function o(e,t=!1,i=Float32Array){let n;if(Number.isFinite(e[0]))n=new i(e);else{n=new i(4*e.length);let t=0;for(let i=0;i<e.length;i++){const o=e[i];n[t++]=o[0],n[t++]=o[1],n[t++]=o[2],n[t++]=Number.isFinite(o[3])?o[3]:255}}if(t)for(let e=0;e<n.length;e++)n[e]/=255;return n}},88514:(e,t,i)=>{i.d(t,{A:()=>o});const n={pickingSelectedColor:null,pickingHighlightColor:new Uint8Array([0,255,255,255]),pickingActive:!1,pickingAttribute:!1},o={inject:{"vs:DECKGL_FILTER_GL_POSITION":"\n    // for picking depth values\n    picking_setPickingAttribute(position.z / position.w);\n  ","vs:DECKGL_FILTER_COLOR":"\n  picking_setPickingColor(geometry.pickingColor);\n  ","fs:#decl":"\nuniform bool picking_uAttribute;\n  ","fs:DECKGL_FILTER_COLOR":{order:99,injection:"\n  // use highlight color if this fragment belongs to the selected object.\n  color = picking_filterHighlightColor(color);\n\n  // use picking color if rendering to picking FBO.\n  color = picking_filterPickingColor(color);\n    "}},name:"picking",vs:"uniform bool picking_uActive;\nuniform bool picking_uAttribute;\nuniform vec3 picking_uSelectedColor;\nuniform bool picking_uSelectedColorValid;\n\nout vec4 picking_vRGBcolor_Avalid;\n\nconst float COLOR_SCALE = 1. / 255.;\n\nbool picking_isColorValid(vec3 color) {\n  return dot(color, vec3(1.0)) > 0.001;\n}\n\nbool isVertexPicked(vec3 vertexColor) {\n  return\n    picking_uSelectedColorValid &&\n    !picking_isColorValid(abs(vertexColor - picking_uSelectedColor));\n}\n\nvoid picking_setPickingColor(vec3 pickingColor) {\n  if (picking_uActive) {\n    picking_vRGBcolor_Avalid.a = float(picking_isColorValid(pickingColor));\n\n    if (!picking_uAttribute) {\n      picking_vRGBcolor_Avalid.rgb = pickingColor * COLOR_SCALE;\n    }\n  } else {\n    picking_vRGBcolor_Avalid.a = float(isVertexPicked(pickingColor));\n  }\n}\n\nvoid picking_setPickingAttribute(float value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.r = value;\n  }\n}\nvoid picking_setPickingAttribute(vec2 value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.rg = value;\n  }\n}\nvoid picking_setPickingAttribute(vec3 value) {\n  if (picking_uAttribute) {\n    picking_vRGBcolor_Avalid.rgb = value;\n  }\n}\n",fs:"uniform bool picking_uActive;\nuniform vec3 picking_uSelectedColor;\nuniform vec4 picking_uHighlightColor;\n\nin vec4 picking_vRGBcolor_Avalid;\nvec4 picking_filterHighlightColor(vec4 color) {\n  if (picking_uActive) {\n    return color;\n  }\n  bool selected = bool(picking_vRGBcolor_Avalid.a);\n\n  if (selected) {\n    float highLightAlpha = picking_uHighlightColor.a;\n    float blendedAlpha = highLightAlpha + color.a * (1.0 - highLightAlpha);\n    float highLightRatio = highLightAlpha / blendedAlpha;\n\n    vec3 blendedRGB = mix(color.rgb, picking_uHighlightColor.rgb, highLightRatio);\n    return vec4(blendedRGB, blendedAlpha);\n  } else {\n    return color;\n  }\n}\nvec4 picking_filterPickingColor(vec4 color) {\n  if (picking_uActive) {\n    if (picking_vRGBcolor_Avalid.a == 0.0) {\n      discard;\n    }\n    return picking_vRGBcolor_Avalid;\n  }\n  return color;\n}\nvec4 picking_filterColor(vec4 color) {\n  vec4 highightColor = picking_filterHighlightColor(color);\n  return picking_filterPickingColor(highightColor);\n}\n\n",getUniforms:function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:n;const t={};if(void 0!==e.pickingSelectedColor)if(e.pickingSelectedColor){const i=e.pickingSelectedColor.slice(0,3);t.picking_uSelectedColorValid=1,t.picking_uSelectedColor=i}else t.picking_uSelectedColorValid=0;if(e.pickingHighlightColor){const i=Array.from(e.pickingHighlightColor,(e=>e/255));Number.isFinite(i[3])||(i[3]=1),t.picking_uHighlightColor=i}return void 0!==e.pickingActive&&(t.picking_uActive=Boolean(e.pickingActive),t.picking_uAttribute=Boolean(e.pickingAttribute)),t}}},70957:(e,t,i)=>{i.d(t,{S:()=>f});var n=i(2404),o=i.n(n),r=i(96540),a=i(92094),l=i(45722),s=i(83505),c=i(96453),g=i(58642),u=i(2445);const p=c.I4.div`
  ${({theme:e,top:t,left:i})=>`\n    position: absolute;\n    top: ${t}px;\n    left: ${i}px;\n    padding: ${2*e.gridUnit}px;\n    margin: ${2*e.gridUnit}px;\n    background: ${e.colors.grayscale.dark2};\n    color: ${e.colors.grayscale.light5};\n    maxWidth: 300px;\n    fontSize: ${e.typography.sizes.s}px;\n    zIndex: 9;\n    pointerEvents: none;\n  `}
`;function d(e){const{tooltip:t}=e;if(null==t)return null;const{x:i,y:n,content:o}=t,r="string"==typeof o?(0,g.nn)(o):o;return(0,u.Y)(p,{top:n,left:i,children:r})}const h=(0,r.memo)((0,r.forwardRef)(((e,t)=>{const[i,n]=(0,r.useState)(null),[c,g]=(0,r.useState)(null),[p,h]=(0,r.useState)(e.viewport),f=(0,s.Z)(e.viewport);(0,r.useImperativeHandle)(t,(()=>({setTooltip:n})),[]);const m=(0,r.useCallback)((()=>{if(c&&Date.now()-c>250){const t=e.setControlValue;t&&t("viewport",p),g(null)}}),[c,e.setControlValue,p]);(0,r.useEffect)((()=>{const e=setInterval(m,250);return clearInterval(e)}),[m]),(0,r.useEffect)((()=>{o()(e.viewport,f)||h(e.viewport)}),[f,e.viewport]);const v=(0,r.useCallback)((({viewState:e})=>{h(e),g(Date.now())}),[]),C=(0,r.useCallback)((()=>e.layers.some((e=>"function"==typeof e))?e.layers.map((e=>"function"==typeof e?e():e)):e.layers),[e.layers]),{children:x=null,height:_,width:A}=e;return(0,u.FD)(u.FK,{children:[(0,u.FD)("div",{style:{position:"relative",width:A,height:_},children:[(0,u.Y)(l.A,{controller:!0,width:A,height:_,layers:C(),viewState:p,glOptions:{preserveDrawingBuffer:!0},onViewStateChange:v,children:(0,u.Y)(a.b,{preserveDrawingBuffer:!0,mapStyle:e.mapStyle||"light",mapboxApiAccessToken:e.mapboxApiAccessToken})}),x]}),(0,u.Y)(d,{tooltip:i})]})}))),f=(0,c.I4)(h)`
  .deckgl-tooltip > div {
    overflow: hidden;
    text-overflow: ellipsis;
  }
`},32548:(e,t,i)=>{i.d(t,{A:()=>o});var n=i(2445);const o=({label:e,value:t})=>(0,n.FD)("div",{children:[e,(0,n.Y)("strong",{children:t})]})},28209:(e,t,i)=>{i.r(t),i.d(t,{default:()=>F,getLayer:()=>U});var n=i(63950),o=i.n(n),r=i(96540),a=i(64467),l=i(93261),s=i(527),c=i(67661),g=i(77325),u=i(38404),p=i(33023),d=i(82170),h=i(4679),f=i(88514),m=i(61816);const v=[0,0,0,0],C=[0,255,0,255],x=["minColor","maxColor","colorRange","colorDomain"],_={cellSizePixels:{value:100,min:1},cellMarginPixels:{value:2,min:0,max:5},colorDomain:null,colorRange:m.Q};class A extends h.A{constructor(...e){super(...e),(0,a.A)(this,"state",void 0)}static isSupported(e){return(0,g.QN)(e,[u.G.TEXTURE_FLOAT])}getShaders(){return{vs:"#define SHADER_NAME screen-grid-layer-vertex-shader\n#define RANGE_COUNT 6\n\nattribute vec3 positions;\nattribute vec3 instancePositions;\nattribute vec4 instanceCounts;\nattribute vec3 instancePickingColors;\n\nuniform float opacity;\nuniform vec3 cellScale;\nuniform vec4 minColor;\nuniform vec4 maxColor;\nuniform vec4 colorRange[RANGE_COUNT];\nuniform vec2 colorDomain;\nuniform bool shouldUseMinMax;\nuniform sampler2D maxTexture;\n\nvarying vec4 vColor;\nvarying float vSampleCount;\n\nvec4 quantizeScale(vec2 domain, vec4 range[RANGE_COUNT], float value) {\n  vec4 outColor = vec4(0., 0., 0., 0.);\n  if (value >= domain.x && value <= domain.y) {\n    float domainRange = domain.y - domain.x;\n    if (domainRange <= 0.) {\n      outColor = colorRange[0];\n    } else {\n      float rangeCount = float(RANGE_COUNT);\n      float rangeStep = domainRange / rangeCount;\n      float idx = floor((value - domain.x) / rangeStep);\n      idx = clamp(idx, 0., rangeCount - 1.);\n      int intIdx = int(idx);\n      outColor = colorRange[intIdx];\n    }\n  }\n  outColor = outColor / 255.;\n  return outColor;\n}\n\nvoid main(void) {\n  vSampleCount = instanceCounts.a;\n\n  float weight = instanceCounts.r;\n  float maxWeight = texture2D(maxTexture, vec2(0.5)).r;\n\n  float step = weight / maxWeight;\n  vec4 minMaxColor = mix(minColor, maxColor, step) / 255.;\n\n  vec2 domain = colorDomain;\n  float domainMaxValid = float(colorDomain.y != 0.);\n  domain.y = mix(maxWeight, colorDomain.y, domainMaxValid);\n  vec4 rangeColor = quantizeScale(domain, colorRange, weight);\n\n  float rangeMinMax = float(shouldUseMinMax);\n  vec4 color = mix(rangeColor, minMaxColor, rangeMinMax);\n  vColor = vec4(color.rgb, color.a * opacity);\n  picking_setPickingColor(instancePickingColors);\n\n  gl_Position = vec4(instancePositions + positions * cellScale, 1.);\n}\n",fs:"#define SHADER_NAME screen-grid-layer-fragment-shader\n\nprecision highp float;\n\nvarying vec4 vColor;\nvarying float vSampleCount;\n\nvoid main(void) {\n  if (vSampleCount <= 0.0) {\n    discard;\n  }\n  gl_FragColor = vColor;\n\n  DECKGL_FILTER_COLOR(gl_FragColor, geometry);\n}\n",modules:[f.A]}}initializeState(){const{gl:e}=this.context;this.getAttributeManager().addInstanced({instancePositions:{size:3,update:this.calculateInstancePositions},instanceCounts:{size:4,noAlloc:!0}}),this.setState({model:this._getModel(e)})}shouldUpdateState({changeFlags:e}){return e.somethingChanged}updateState(e){super.updateState(e);const{oldProps:t,props:i,changeFlags:n}=e,o=this.getAttributeManager();i.numInstances!==t.numInstances?o.invalidateAll():t.cellSizePixels!==i.cellSizePixels&&o.invalidate("instancePositions"),this._updateUniforms(t,i,n)}draw({uniforms:e}){const{parameters:t,maxTexture:i}=this.props,n=this.props.minColor||v,o=this.props.maxColor||C,r=this.props.colorDomain||[1,0],{model:a}=this.state;a.setUniforms(e).setUniforms({minColor:n,maxColor:o,maxTexture:i,colorDomain:r}).draw({parameters:{depthTest:!1,depthMask:!1,...t}})}calculateInstancePositions(e,{numInstances:t}){const{width:i,height:n}=this.context.viewport,{cellSizePixels:o}=this.props,r=Math.ceil(i/o),{value:a,size:l}=e;for(let e=0;e<t;e++){const t=e%r,s=Math.floor(e/r);a[e*l+0]=t*o/i*2-1,a[e*l+1]=1-s*o/n*2,a[e*l+2]=0}}_getModel(e){return new p.A(e,{...this.getShaders(),id:this.props.id,geometry:new d.A({drawMode:6,attributes:{positions:new Float32Array([0,0,0,1,0,0,1,1,0,0,1,0])}}),isInstanced:!0})}_shouldUseMinMax(){const{minColor:e,maxColor:t,colorDomain:i,colorRange:n}=this.props;return e||t?(l.A.deprecated("ScreenGridLayer props: minColor and maxColor","colorRange, colorDomain")(),!0):!i&&!n}_updateUniforms(e,t,i){const{model:n}=this.state;if(x.some((i=>e[i]!==t[i]))&&n.setUniforms({shouldUseMinMax:this._shouldUseMinMax()}),e.colorRange!==t.colorRange&&n.setUniforms({colorRange:(0,m.Y)(t.colorRange)}),e.cellMarginPixels!==t.cellMarginPixels||e.cellSizePixels!==t.cellSizePixels||i.viewportChanged){const{width:e,height:t}=this.context.viewport,{cellSizePixels:i,cellMarginPixels:o}=this.props,r=i>o?o:0,a=new Float32Array([(i-r)/e*2,-(i-r)/t*2,1]);n.setUniforms({cellScale:a})}}}(0,a.A)(A,"layerName","ScreenGridCellLayer"),(0,a.A)(A,"defaultProps",_);var k=i(56238),b=i(67667);const S={...A.defaultProps,getPosition:{type:"accessor",value:e=>e.position},getWeight:{type:"accessor",value:1},gpuAggregation:!0,aggregation:"SUM"},y="positions",w={data:{props:["cellSizePixels"]},weights:{props:["aggregation"],accessors:["getWeight"]}};class R extends k.A{constructor(...e){super(...e),(0,a.A)(this,"state",void 0)}initializeState(){const{gl:e}=this.context;if(!A.isSupported(e))return this.setState({supported:!1}),void l.A.error("ScreenGridLayer: ".concat(this.id," is not supported on this browser"))();super.initializeAggregationLayer({dimensions:w,getCellSize:e=>e.cellSizePixels});const t={count:{size:1,operation:c.Rn.SUM,needMax:!0,maxTexture:(0,b.mV)(e,{id:"".concat(this.id,"-max-texture")})}};this.setState({supported:!0,projectPoints:!0,weights:t,subLayerData:{attributes:{}},maxTexture:t.count.maxTexture,positionAttributeName:"positions",posOffset:[0,0],translation:[1,-1]}),this.getAttributeManager().add({[y]:{size:3,accessor:"getPosition",type:5130,fp64:this.use64bitPositions()},count:{size:3,accessor:"getWeight"}})}shouldUpdateState({changeFlags:e}){return this.state.supported&&e.somethingChanged}updateState(e){super.updateState(e)}renderLayers(){if(!this.state.supported)return[];const{maxTexture:e,numRow:t,numCol:i,weights:n}=this.state,{updateTriggers:o}=this.props,{aggregationBuffer:r}=n.count;return new(this.getSubLayerClass("cells",A))(this.props,this.getSubLayerProps({id:"cell-layer",updateTriggers:o}),{data:{attributes:{instanceCounts:r}},maxTexture:e,numInstances:t*i})}finalizeState(e){super.finalizeState(e);const{aggregationBuffer:t,maxBuffer:i,maxTexture:n}=this.state;null==t||t.delete(),null==i||i.delete(),null==n||n.delete()}getPickingInfo({info:e}){const{index:t}=e;if(t>=0){const{gpuGridAggregator:i,gpuAggregation:n,weights:o}=this.state,r=n?i.getData("count"):o.count;e.object=s.A.getAggregationData({pixelIndex:t,...r})}return e}updateResults({aggregationData:e,maxData:t}){const{count:i}=this.state.weights;i.aggregationData=e,i.aggregationBuffer.setData({data:e}),i.maxData=t,i.maxTexture.setImageData({data:t})}updateAggregationState(e){const t=e.props.cellSizePixels,i=e.oldProps.cellSizePixels!==t,{viewportChanged:n}=e.changeFlags;let o=e.props.gpuAggregation;this.state.gpuAggregation!==e.props.gpuAggregation&&o&&!s.A.isSupported(this.context.gl)&&(l.A.warn("GPU Grid Aggregation not supported, falling back to CPU")(),o=!1);const r=o!==this.state.gpuAggregation;this.setState({gpuAggregation:o});const a=this.isAttributeChanged(y),{dimensions:c}=this.state,{data:g,weights:u}=c,p=a||r||n||this.isAggregationDirty(e,{compareAll:o,dimension:g}),d=this.isAggregationDirty(e,{dimension:u});this.setState({aggregationDataDirty:p,aggregationWeightsDirty:d});const{viewport:h}=this.context;if(n||i){const{width:e,height:i}=h,n=Math.ceil(e/t),o=Math.ceil(i/t);this.allocateResources(o,n),this.setState({scaling:[e/2,-i/2,1],gridOffset:{xOffset:t,yOffset:t},width:e,height:i,numCol:n,numRow:o})}d&&this._updateAccessors(e),(p||d)&&this._resetResults()}_updateAccessors(e){const{getWeight:t,aggregation:i,data:n}=e.props,{count:o}=this.state.weights;o&&(o.getWeight=t,o.operation=c.Rn[i]),this.setState({getValue:(0,c.Mm)(i,t,{data:n})})}_resetResults(){const{count:e}=this.state.weights;e&&(e.aggregationData=null)}}(0,a.A)(R,"layerName","ScreenGridLayer"),(0,a.A)(R,"defaultProps",S);var P=i(95579),D=i(25564),M=i(41857),L=i(32548),T=i(95490),z=i(70957),G=i(2445);function E(e){var t,i,n;return(0,G.FD)("div",{className:"deckgl-tooltip",children:[(0,G.Y)(L.A,{label:(0,P.t)("Longitude and Latitude")+": ",value:`${null==e||null==(t=e.coordinate)?void 0:t[0]}, ${null==e||null==(i=e.coordinate)?void 0:i[1]}`}),(0,G.Y)(L.A,{label:(0,P.t)("Weight")+": ",value:`${null==(n=e.object)?void 0:n.cellWeight}`})]})}function U(e,t,i,n){const o=e,r=o.color_picker;let a=t.data.features.map((e=>({...e,color:[r.r,r.g,r.b,255*r.a]})));return o.js_data_mutator&&(a=(0,D.A)(o.js_data_mutator)(a)),new R({id:`screengrid-layer-${o.slice_id}`,data:a,cellSizePixels:o.grid_size,minColor:[r.r,r.g,r.b,0],maxColor:[r.r,r.g,r.b,255*r.a],outline:!1,getWeight:e=>e.weight||0,...(0,M.T)(o,n,E)})}const I=e=>{const t=(0,r.useRef)(),i=(0,r.useCallback)((()=>{const t=e.payload.data.features||[],{width:i,height:n,formData:o}=e;return o.autozoom?(0,T.A)(e.viewport,{width:i,height:n,points:(r=t,r.map((e=>e.position)))}):e.viewport;var r}),[e]),[n,a]=(0,r.useState)(e.payload.form_data),[l,s]=(0,r.useState)(i());(0,r.useEffect)((()=>{e.payload.form_data!==n&&(s(i()),a(e.payload.form_data))}),[i,e.payload.form_data,n]);const c=(0,r.useCallback)((e=>{const{current:i}=t;i&&i.setTooltip(e)}),[]),g=(0,r.useCallback)((()=>[U(e.formData,e.payload,o(),c)]),[e.formData,e.payload,c]),{formData:u,payload:p,setControlValue:d}=e;return(0,G.Y)("div",{children:(0,G.Y)(z.S,{ref:t,viewport:l,layers:g(),setControlValue:d,mapStyle:u.mapbox_style,mapboxApiAccessToken:p.data.mapboxApiKey,width:e.width,height:e.height})})},F=(0,r.memo)(I)},41857:(e,t,i)=>{i.d(t,{T:()=>r,g:()=>l});var n=i(86914),o=i(25564);function r(e,t,i,n){const r=e;let a,l,s=i;return r.js_tooltip&&(s=(0,o.A)(r.js_tooltip)),s&&(a=e=>(e.picked?t({content:s(e),x:e.x,y:e.y}):t(null),!0)),r.js_onclick_href?l=e=>{const t=(0,o.A)(r.js_onclick_href)(e);return window.open(t),!0}:r.table_filter&&void 0!==n&&(l=e=>(n(e.object[r.line_column]),!0)),{onClick:l,onHover:a,pickable:Boolean(a)}}const a={p1:.01,p5:.05,p95:.95,p99:.99};function l(e="sum",t=null){if("count"===e)return e=>e.length;let i;return i=e in a?(i,o)=>{let r;return r=t?i.sort(((e,i)=>n.ascending(t(e),t(i)))):i.sort(n.ascending),n.quantile(r,a[e],o)}:n[e],t?e=>i(e.map((e=>t(e)))):e=>i(e)}},49443:(e,t,i)=>{i.r(t),i.d(t,{hexToRGB:()=>o});var n=i(2117);function o(e,t=255){if(!e)return[0,0,0,t];const{r:i,g:o,b:r}=(0,n.Qh)(e);return[i,o,r,t]}},95490:(e,t,i)=>{i.d(t,{A:()=>s});var n=i(54982),o=i(86914);const r=[-90,90],a=[-180,180];function l([e,t],[i,n],o=.25){return e<t?[e,t]:[Math.max(i,e-o),Math.min(n,t+o)]}function s(e,{points:t,width:i,height:s,minExtent:c,maxZoom:g,offset:u,padding:p=20}){const{bearing:d,pitch:h}=e,f=function(e){const t=l((0,o.extent)(e,(e=>e[1])),r),i=l((0,o.extent)(e,(e=>e[0])),a);return[[i[0],t[0]],[i[1],t[1]]]}(t);try{return{...(0,n.Fe)({bounds:f,width:i,height:s,minExtent:c,maxZoom:g,offset:u,padding:p}),bearing:d,pitch:h}}catch(e){console.error("Could not fit viewport",e)}return e}},25564:(e,t,i)=>{i.d(t,{A:()=>c});var n=i(68961),o=i.n(n),r=i(4523),a=i(86914),l=i(49443);const s={console,_:r.Ay,colors:l,d3array:a};function c(e,t,i){const n={},r=`SAFE_EVAL_${Math.floor(1e6*Math.random())}`;n[r]={};const a=`${r}=${e}`,l={...s,...t};Object.keys(l).forEach((e=>{n[e]=l[e]}));try{return o().runInNewContext(a,n,i),n[r]}catch(e){return()=>e}}}}]);
//# sourceMappingURL=e800f2ed8f3a151657a1.chunk.js.map