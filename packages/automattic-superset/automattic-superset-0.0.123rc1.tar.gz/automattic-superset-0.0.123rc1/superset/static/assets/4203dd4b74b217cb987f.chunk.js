"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4513],{74513:(e,t,a)=>{a.r(t),a.d(t,{default:()=>X});var s=a(7240),i=a(96453),o=a(5556),r=a.n(o),n=a(7350),l=a.n(n),c=a(20249),h=a.n(c),m=a(24143),p=a.n(m),d=a(95093),u=a.n(d),y=a(71111),x=a.n(y),g=a(7349),b=a(58928),f=a(94963),v=a(32142),k=a(95579),w=a(53682),A=a(13270),L=a(36673),C=a(40981),$=a(84338),M=a(17171);const T=r().oneOfType([r().number,r().oneOf(["auto"])]),N=r().oneOfType([r().string,r().shape({label:r().string})]),D=r().shape({r:r().number.isRequired,g:r().number.isRequired,b:r().number.isRequired}),E=r().shape({x:r().number,y:r().number}),O=r().shape({x:r().string,y:r().number}),S=r().shape({outliers:r().arrayOf(r().number),Q1:r().number,Q2:r().number,Q3:r().number,whisker_high:r().number,whisker_low:r().number}),F=r().shape({markerLabels:r().arrayOf(r().string),markerLineLabels:r().arrayOf(r().string),markerLines:r().arrayOf(r().number),markers:r().arrayOf(r().number),measures:r().arrayOf(r().number),rangeLabels:r().arrayOf(r().string),ranges:r().arrayOf(r().number)}),_=r().shape({annotationType:r().oneOf(Object.keys(C.ij)),color:r().string,hideLine:r().bool,name:r().string,opacity:r().string,show:r().bool,showMarkers:r().bool,sourceType:r().string,style:r().string,value:r().oneOfType([r().number,r().string]),width:r().number}),B=[{text:"No data",dy:"-.75em",class:"header"},{text:"Adjust filters or check the Datasource.",dy:".75em",class:"body"}],z=(0,g.mo)(b.M);x().utils.noData=function(e,t){const a=e.options().margin(),s=x().utils.availableHeight(null,t,a),i=x().utils.availableWidth(null,t,a),o=a.left+i/2,r=a.top+s/2;t.selectAll("g").remove();const n=t.selectAll(".nv-noData").data(B);n.enter().append("text").attr("class",(e=>`nvd3 nv-noData ${e.class}`)).attr("dy",(e=>e.dy)).style("text-anchor","middle"),n.attr("x",o).attr("y",r).text((e=>e.text))};const{getColor:I,getScale:R}=f,V=["line","area","compare","bar","time_pivot"],G={data:r().oneOfType([r().arrayOf(r().oneOfType([O,r().shape({key:r().string,values:r().arrayOf(O)}),r().shape({key:r().arrayOf(r().string),values:r().arrayOf(E)}),r().shape({classed:r().string,key:r().string,type:r().string,values:r().arrayOf(E),yAxis:r().number}),r().shape({label:r().string,values:r().arrayOf(S)}),r().shape({key:r().string,values:r().arrayOf(r().object)})])),F]),width:r().number,height:r().number,annotationData:r().object,annotationLayers:r().arrayOf(_),bottomMargin:T,colorScheme:r().string,comparisonType:r().string,contribution:r().bool,leftMargin:T,onError:r().func,showLegend:r().bool,showMarkers:r().bool,useRichTooltip:r().bool,vizType:r().oneOf(["area","bar","box_plot","bubble","bullet","compare","column","dist_bar","line","time_pivot","pie"]),xAxisFormat:r().string,numberFormat:r().string,xAxisLabel:r().string,xAxisShowMinMax:r().bool,xIsLogScale:r().bool,xTicksLayout:r().oneOf(["auto","staggered","45°"]),yAxisFormat:r().string,yAxisBounds:r().arrayOf(r().number),yAxisLabel:r().string,yAxisShowMinMax:r().bool,yIsLogScale:r().bool,orderBars:r().bool,isBarStacked:r().bool,showBarValue:r().bool,reduceXTicks:r().bool,showControls:r().bool,showBrush:r().oneOf([!0,"yes",!1,"no","auto"]),onBrushEnd:r().func,yAxis2Format:r().string,lineInterpolation:r().string,isDonut:r().bool,isPieLabelOutside:r().bool,pieLabelType:r().oneOf(["key","value","percent","key_value","key_percent","key_value_percent"]),showLabels:r().bool,areaStackedStyle:r().string,entity:r().string,maxBubbleSize:r().number,xField:N,yField:N,sizeField:N,baseColor:D},P=()=>{},U=(0,v.gV)();function W(e,t){const{data:a,width:s,height:i,annotationData:o,annotationLayers:r=[],areaStackedStyle:n,baseColor:c,bottomMargin:m,colorScheme:d,comparisonType:y,contribution:b,entity:f,isBarStacked:T,isDonut:N,isPieLabelOutside:D,leftMargin:E,lineInterpolation:O="linear",markerLabels:S,markerLines:F,markerLineLabels:_,markers:B,maxBubbleSize:G,onBrushEnd:W=P,onError:q=P,orderBars:H,pieLabelType:Y,rangeLabels:j,ranges:X,reduceXTicks:Q=!1,showBarValue:J,showBrush:K,showControls:Z,showLabels:ee,showLegend:te,showMarkers:ae,sizeField:se,useRichTooltip:ie,vizType:oe,xAxisFormat:re,numberFormat:ne,xAxisLabel:le,xAxisShowMinMax:ce=!1,xField:he,xIsLogScale:me,xTicksLayout:pe,yAxisFormat:de,yAxisBounds:ue,yAxisLabel:ye,yAxisShowMinMax:xe=!1,yAxis2ShowMinMax:ge=!1,yField:be,yIsLogScale:fe,sliceId:ve}=t,ke=null!==document.querySelector("#explorer-container"),we=e;we.innerHTML="";const Ae=r.filter((e=>e.show));let Le,Ce=we,$e=null;for(;Ce.parentElement;){if(Ce.parentElement.id.startsWith("chart-id-")){$e=Ce.parentElement.id;break}Ce=Ce.parentElement}let Me=s,Te="key";function Ne(e){return e.includes(oe)}we.style.width=`${s}px`,we.style.height=`${i}px`,$e?(0,M.G0)($e):(0,M.$v)(!0),x().addGraph((function(){const t=p().select(e);t.classed("superset-legacy-chart-nvd3",!0),t.classed(`superset-legacy-chart-nvd3-${h()(oe)}`,!0);let r=t.select("svg");r.empty()&&(r=t.append("svg"));const we="bullet"===oe?Math.min(i,50):i,Ce=Ne(V),De="staggered"===pe,Ee="auto"===pe&&Ne(["column","dist_bar"])||"45°"===pe?45:0;if(45===Ee&&(0,$.A)(K))return q((0,k.t)("You cannot use 45° tick layout along with the time range filter")),null;const Oe=(0,$.A)(K)||"auto"===K&&i>=480&&"45°"!==pe,Se=(0,v.gV)(ne);switch(oe){case"line":Oe?(Le=x().models.lineWithFocusChart(),De&&(Le.focus.margin({bottom:40}),Le.focusHeight(80)),Le.focus.xScale(p().time.scale.utc())):Le=x().models.lineChart(),Le.xScale(p().time.scale.utc()),Le.interpolate(O),Le.clipEdge(!1);break;case"time_pivot":Le=x().models.lineChart(),Le.xScale(p().time.scale.utc()),Le.interpolate(O);break;case"bar":Le=x().models.multiBarChart().showControls(Z).groupSpacing(.1),Q||(Me=(0,M.Vv)(a,T,s)),Le.width(Me),Le.xAxis.showMaxMin(!1),Le.stacked(T);break;case"dist_bar":Le=x().models.multiBarChart().showControls(Z).reduceXTicks(Q).groupSpacing(.1),Le.xAxis.showMaxMin(!1),Le.stacked(T),H&&a.forEach((e=>{const t=[...e.values];e.values=t.sort(((e,t)=>(0,M.k9)(e.x)<(0,M.k9)(t.x)?-1:1))})),Q||(Me=(0,M.Vv)(a,T,s)),Le.width(Me);break;case"pie":if(Le=x().models.pieChart(),Te="x",Le.valueFormat(Se),N&&Le.donut(!0),Le.showLabels(ee),Le.labelsOutside(D),Le.labelThreshold(.05),Le.cornerRadius(!0),["key","value","percent"].includes(Y))Le.labelType(Y);else if("key_value"===Y)Le.labelType((e=>`${e.data.x}: ${Se(e.data.y)}`));else{const e=p().sum(a,(e=>e.y)),t=(0,v.gV)(w.A.PERCENT_2_POINT);"key_percent"===Y?(Le.tooltip.valueFormatter((e=>t(e))),Le.labelType((a=>`${a.data.x}: ${t(a.data.y/e)}`))):(Le.tooltip.valueFormatter((a=>`${Se(a)} (${t(a/e)})`)),Le.labelType((a=>`${a.data.x}: ${Se(a.data.y)} (${t(a.data.y/e)})`)))}Le.margin({top:0});break;case"column":Le=x().models.multiBarChart().reduceXTicks(!1);break;case"compare":Le=x().models.cumulativeLineChart(),Le.xScale(p().time.scale.utc()),Le.useInteractiveGuideline(!0),Le.xAxis.showMaxMin(!1);break;case"bubble":Le=x().models.scatterChart(),Le.showDistX(!1),Le.showDistY(!1),Le.tooltip.contentGenerator((e=>(0,M.oh)({point:e.point,entity:f,xField:he,yField:be,sizeField:se,xFormatter:(0,M.wn)(re),yFormatter:(0,M.wn)(de),sizeFormatter:U}))),Le.pointRange([5,G**2]),Le.pointDomain([0,p().max(a,(e=>p().max(e.values,(e=>e.size))))]);break;case"area":Le=x().models.stackedAreaChart(),Le.showControls(Z),Le.style(n),Le.xScale(p().time.scale.utc());break;case"box_plot":Te="label",Le=x().models.boxPlotChart(),Le.x((e=>e.label)),Le.maxBoxWidth(75);break;case"bullet":Le=x().models.bulletChart(),a.rangeLabels=j,a.ranges=X,a.markerLabels=S,a.markerLines=F,a.markerLineLabels=_,a.markers=B;break;default:throw new Error(`Unrecognized visualization for nvd3${oe}`)}let Fe;Le.margin({left:0,bottom:0}),J&&((0,M.C$)(r,a,T,de),Le.dispatch.on("stateChange.drawBarValues",(()=>{(0,M.C$)(r,a,T,de)}))),Oe&&W!==P&&Le.focus&&Le.focus.dispatch.on("brush",(e=>{const t=(0,M.EF)(e.extent);t&&e.brush.on("brushend",(()=>{W(t)}))})),Le.xAxis&&Le.xAxis.staggerLabels&&Le.xAxis.staggerLabels(De),Le.xAxis&&Le.xAxis.rotateLabels&&Le.xAxis.rotateLabels(Ee),Le.x2Axis&&Le.x2Axis.staggerLabels&&Le.x2Axis.staggerLabels(De),Le.x2Axis&&Le.x2Axis.rotateLabels&&Le.x2Axis.rotateLabels(Ee),"showLegend"in Le&&void 0!==te&&(Me<340&&"pie"!==oe?Le.showLegend(!1):Le.showLegend(te)),fe&&Le.yScale(p().scale.log()),me&&Le.xScale(p().scale.log()),Ce?(Fe=(0,g.mo)(re),Le.interactiveLayer.tooltip.headerFormatter(z)):Fe=(0,M.wn)(re),Le.x2Axis&&Le.x2Axis.tickFormat&&Le.x2Axis.tickFormat(Fe),Le.xAxis&&Le.xAxis.tickFormat&&(Ne(["dist_bar","box_plot"])?Le.xAxis.tickFormat((e=>e.length>40?`${e.slice(0,Math.max(0,40))}…`:e)):Le.xAxis.tickFormat(Fe));let _e=(0,M.wn)(de);if(Le.yAxis&&Le.yAxis.tickFormat&&(!b&&"percentage"!==y||de&&de!==w.A.SMART_NUMBER&&de!==w.A.SMART_NUMBER_SIGNED||(_e=(0,v.gV)(w.A.PERCENT_1_POINT)),Le.yAxis.tickFormat(_e)),Le.y2Axis&&Le.y2Axis.tickFormat&&Le.y2Axis.tickFormat(_e),Le.yAxis&&Le.yAxis.ticks(5),Le.y2Axis&&Le.y2Axis.ticks(5),(0,M.dw)(Le.xAxis,ce),(0,M.dw)(Le.x2Axis,ce),(0,M.dw)(Le.yAxis,xe),(0,M.dw)(Le.y2Axis,ge||xe),"time_pivot"===oe){if(c){const{r:e,g:t,b:a}=c;Le.color((s=>{const i=s.rank>0?.5*s.perc:1;return`rgba(${e}, ${t}, ${a}, ${i})`}))}Le.useInteractiveGuideline(!0),Le.interactiveLayer.tooltip.contentGenerator((e=>(0,M.qY)(e,Fe,_e)))}else if("bullet"!==oe){const e=R(d);Le.color((t=>t.color||e((0,M.n0)(t[Te]),ve,d)))}Ne(["line","area","bar","dist_bar"])&&ie&&(Le.useInteractiveGuideline(!0),"line"===oe||"bar"===oe?Le.interactiveLayer.tooltip.contentGenerator((e=>(0,M.Au)(e,z,_e))):"dist_bar"===oe?Le.interactiveLayer.tooltip.contentGenerator((e=>(0,M.Jy)(e,_e))):Le.interactiveLayer.tooltip.contentGenerator((e=>(0,M.VA)(e,z,_e,Le)))),Ne(["compare"])&&Le.interactiveLayer.tooltip.contentGenerator((e=>(0,M.Jy)(e,_e))),Le.width(Me),Le.height(we),r.datum(a).transition().duration(500).attr("height",we).attr("width",Me).call(Le),fe&&Le.yAxis.tickFormat((e=>0!==e&&Math.log10(e)%1==0?_e(e):"")),Ee>0&&r.select(".nv-x.nv-axis > g").selectAll("g").selectAll("text").attr("dx",-6.5);const Be=()=>{if(Le.yDomain&&Array.isArray(ue)&&2===ue.length){const[e,t]=ue,s=(0,A.A)(e)&&!Number.isNaN(e),i=(0,A.A)(t)&&!Number.isNaN(t);if((s||i)&&"area"===oe&&"expand"===Le.style())Le.yDomain([0,1]);else if((s||i)&&"area"===oe&&"stream"===Le.style())Le.yDomain((0,M.gC)(a));else if(s&&i)Le.yDomain([e,t]),Le.clipEdge(!0);else if(s||i){let[o,r]=[0,1];"area"===oe||Ne(["bar","dist_bar"])&&Le.stacked()?[o,r]=(0,M.gC)(a):[o,r]=(0,M.B2)(a);const n=s?e:o,l=i?t:r;Le.yDomain([n,l]),Le.clipEdge(!0)}}};if(Be(),Le.dispatch&&Le.dispatch.stateChange&&Le.dispatch.on("stateChange.applyYAxisBounds",Be),ae&&(r.selectAll(".nv-point").style("stroke-opacity",1).style("fill-opacity",1),Le.dispatch.on("stateChange.showMarkers",(()=>{setTimeout((()=>{r.selectAll(".nv-point").style("stroke-opacity",1).style("fill-opacity",1)}),10)}))),void 0!==Le.yAxis||void 0!==Le.yAxis2){const t=Math.ceil(Math.min(s*(ke?.01:.03),30)),i=Le.margin();Le.xAxis&&(i.bottom=28);const n=(0,M.cm)(r,Le.yAxis2?"nv-y1":"nv-y"),c=(0,M.cm)(r,"nv-x");if(i.left=n+t,ye&&""!==ye&&(i.left+=25),J&&(i.top+=24),ce&&(i.right=Math.max(20,c/2)+t),45===Ee?(i.bottom=c*Math.sin(Math.PI*Ee/180)+t+30,i.right=c*Math.cos(Math.PI*Ee/180)+t):De&&(i.bottom=40),m&&"auto"!==m&&(i.bottom=parseInt(m,10)),E&&"auto"!==E&&(i.left=E),le&&""!==le&&Le.xAxis){i.bottom+=25;let e=0;i.bottom&&!Number.isNaN(i.bottom)&&(e=i.bottom-45),Le.xAxis.axisLabel(le).axisLabelDistance(e)}if(ye&&""!==ye&&Le.yAxis){let e=0;i.left&&!Number.isNaN(i.left)&&(e=i.left-70),Le.yAxis.axisLabel(ye).axisLabelDistance(e)}if(Ce&&o&&Ae.length>0){const e=Ae.filter((e=>e.annotationType===C.Ay.TIME_SERIES)).reduce(((e,t)=>e.concat((o[t.name]||[]).map((e=>{if(!e)return{};const a=Array.isArray(e.key)?`${t.name}, ${e.key.join(", ")}`:`${t.name}, ${e.key}`;return{...e,key:a,color:t.color,strokeWidth:t.width,classed:`${t.opacity} ${t.style} nv-timeseries-annotation-layer showMarkers${t.showMarkers} hideLine${t.hideLine}`}})))),[]);a.push(...e)}if($e&&(Le&&Le.interactiveLayer&&Le.interactiveLayer.tooltip&&Le.interactiveLayer.tooltip.classes([(0,M.Ir)($e)]),Le&&Le.tooltip&&Le.tooltip.classes([(0,M.Ir)($e)])),Le.margin(i),r.datum(a).transition().duration(500).attr("width",Me).attr("height",we).call(Le),window.addEventListener("scroll",l()((()=>(0,M.$v)(!1)),250)),Ce&&Ae.length>0){const t=Ae.filter((e=>e.annotationType===C.Ay.FORMULA));let s,i,n;if("bar"===oe?(i=p().min(a[0].values,(e=>e.x)),s=p().max(a[0].values,(e=>e.x)),n=p().scale.quantile().domain([i,s]).range(Le.xAxis.range())):(i=Le.xAxis.scale().domain()[0].valueOf(),s=Le.xAxis.scale().domain()[1].valueOf(),n=Le.xScale?Le.xScale():Le.xAxis.scale?Le.xAxis.scale():p().scale.linear()),n&&n.clamp&&n.clamp(!0),t.length>0){const e=[];if("bar"===oe){const t=a.reduce(((e,t)=>(t.values.forEach((t=>e.add(t.x))),e)),new Set);e.push(...t.values()),e.sort()}else{let t=Math.min(...a.map((e=>Math.min(...e.values.slice(1).map(((t,a)=>t.x-e.values[a].x))))));const o=(s-i)/(t||1);t=o<100?(s-i)/100:t,t=o>500?(s-i)/500:t,e.push(i);for(let a=i;a<s;a+=t)e.push(a);e.push(s)}const o=t.map((t=>{const{value:a}=t;return{key:t.name,values:e.map((e=>({x:e,y:(0,L.p)(a,e)}))),color:t.color,strokeWidth:t.width,classed:`${t.opacity} ${t.style}`}}));a.push(...o)}const l=Le.xAxis1?Le.xAxis1:Le.xAxis,c=Le.yAxis1?Le.yAxis1:Le.yAxis,h=l.scale().range()[1],m=c.scale().range()[0];o&&(Ae.filter((e=>e.annotationType===C.Ay.EVENT&&o&&o[e.name])).forEach(((t,a)=>{const s=(0,C.tH)(t),i=p().select(e).select(".nv-wrap").append("g").attr("class",`nv-event-annotation-layer-${a}`),r=s.color||I((0,M.n0)(s.name),d),l=(0,M.AN)({...s,annotationTipClass:`arrow-down nv-event-annotation-layer-${t.sourceType}`}),c=(o[s.name].records||[]).map((e=>{const t=new Date(u().utc(e[s.timeColumn]));return{...e,[s.timeColumn]:t}})).filter((e=>!Number.isNaN(e[s.timeColumn].getMilliseconds())));c.length>0&&i.selectAll("line").data(c).enter().append("line").attr({x1:e=>n(new Date(e[s.timeColumn])),y1:0,x2:e=>n(new Date(e[s.timeColumn])),y2:m}).attr("class",`${s.opacity} ${s.style}`).style("stroke",r).style("stroke-width",s.width).on("mouseover",l.show).on("mouseout",l.hide).call(l),Le.focus&&Le.focus.dispatch.on("onBrush.event-annotation",(()=>{i.selectAll("line").data(c).attr({x1:e=>n(new Date(e[s.timeColumn])),y1:0,x2:e=>n(new Date(e[s.timeColumn])),y2:m,opacity:e=>{const t=n(new Date(e[s.timeColumn]));return t>0&&t<h?1:0}})}))})),Ae.filter((e=>e.annotationType===C.Ay.INTERVAL&&o&&o[e.name])).forEach(((t,a)=>{const s=(0,C.tH)(t),i=p().select(e).select(".nv-wrap").append("g").attr("class",`nv-interval-annotation-layer-${a}`),r=s.color||I((0,M.n0)(s.name),d),l=(0,M.AN)(s),c=(o[s.name].records||[]).map((e=>{const t=new Date(u().utc(e[s.timeColumn])),a=new Date(u().utc(e[s.intervalEndColumn]));return{...e,[s.timeColumn]:t,[s.intervalEndColumn]:a}})).filter((e=>!Number.isNaN(e[s.timeColumn].getMilliseconds())&&!Number.isNaN(e[s.intervalEndColumn].getMilliseconds())));c.length>0&&i.selectAll("rect").data(c).enter().append("rect").attr({x:e=>Math.min(n(new Date(e[s.timeColumn])),n(new Date(e[s.intervalEndColumn]))),y:0,width:e=>Math.max(Math.abs(n(new Date(e[s.intervalEndColumn]))-n(new Date(e[s.timeColumn]))),1),height:m}).attr("class",`${s.opacity} ${s.style}`).style("stroke-width",s.width).style("stroke",r).style("fill",r).style("fill-opacity",.2).on("mouseover",l.show).on("mouseout",l.hide).call(l),Le.focus&&Le.focus.dispatch.on("onBrush.interval-annotation",(()=>{i.selectAll("rect").data(c).attr({x:e=>n(new Date(e[s.timeColumn])),width:e=>{const t=n(new Date(e[s.timeColumn]));return n(new Date(e[s.intervalEndColumn]))-t}})}))}))),r.datum(a).attr("height",we).attr("width",Me).call(Le),Le.dispatch.on("renderEnd.timeseries-annotation",(()=>{p().selectAll(".slice_container .nv-timeseries-annotation-layer.showMarkerstrue .nv-point").style("stroke-opacity",1).style("fill-opacity",1),p().selectAll(".slice_container .nv-timeseries-annotation-layer.hideLinetrue").style("stroke-width",0)}))}}return(0,M.OK)(Le),Le}))}W.displayName="NVD3",W.propTypes=G;const q=W;var H=a(2445);const Y=(0,s.A)(q,{componentWillUnmount:function(){const{id:e}=this.props;null!=e?(0,M.G0)(e):(0,M.$v)(!0)}}),j=({className:e,...t})=>(0,H.Y)("div",{className:e,children:(0,H.Y)(Y,{...t})});j.propTypes={className:r().string.isRequired};const X=(0,i.I4)(j)`
  .superset-legacy-chart-nvd3-dist-bar,
  .superset-legacy-chart-nvd3-bar {
    overflow-x: auto !important;
    svg {
      &.nvd3-svg {
        width: auto;
        font-size: ${({theme:e})=>e.typography.sizes.m};
      }
    }
  }
  .superset-legacy-chart-nvd3 {
    nv-x text {
      font-size: ${({theme:e})=>e.typography.sizes.m};
    }
    g.superset path {
      stroke-dasharray: 5, 5;
    }
    .nvtooltip tr.highlight td {
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      font-size: ${({theme:e})=>e.typography.sizes.m}px !important;
    }
    text.nv-axislabel {
      font-size: ${({theme:e})=>e.typography.sizes.m} !important;
    }
    g.solid path,
    line.solid {
      stroke-dasharray: unset;
    }
    g.dashed path,
    line.dashed {
      stroke-dasharray: 5, 5;
    }
    g.longDashed path,
    line.dotted {
      stroke-dasharray: 1, 1;
    }

    g.opacityLow path,
    line.opacityLow {
      stroke-opacity: 0.2;
    }

    g.opacityMedium path,
    line.opacityMedium {
      stroke-opacity: 0.5;
    }
    g.opacityHigh path,
    line.opacityHigh {
      stroke-opacity: 0.8;
    }
    g.time-shift-0 path,
    line.time-shift-0 {
      stroke-dasharray: 5, 5;
    }
    g.time-shift-1 path,
    line.time-shift-1 {
      stroke-dasharray: 1, 5;
    }
    g.time-shift-2 path,
    line.time-shift-3 {
      stroke-dasharray: 5, 1;
    }
    g.time-shift-3 path,
    line.time-shift-3 {
      stroke-dasharray: 5, 1;
    }
    g.time-shift-4 path,
    line.time-shift-4 {
      stroke-dasharray: 5, 10;
    }
    g.time-shift-5 path,
    line.time-shift-5 {
      stroke-dasharray: 0.9;
    }
    g.time-shift-6 path,
    line.time-shift-6 {
      stroke-dasharray: 15, 10, 5;
    }
    g.time-shift-7 path,
    line.time-shift-7 {
      stroke-dasharray: 15, 10, 5, 10;
    }
    g.time-shift-8 path,
    line.time-shift-8 {
      stroke-dasharray: 15, 10, 5, 10, 15;
    }
    g.time-shift-9 path,
    line.time-shift-9 {
      stroke-dasharray: 5, 5, 1, 5;
    }
    .nv-noData.body {
      font-size: ${({theme:e})=>e.typography.sizes.m};
      font-weight: ${({theme:e})=>e.typography.weights.normal};
    }
  }
  .superset-legacy-chart-nvd3-tr-highlight {
    border-top: 1px solid;
    border-bottom: 1px solid;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
  }
  .superset-legacy-chart-nvd3-tr-total {
    font-weight: ${({theme:e})=>e.typography.weights.bold};
  }
  .nvtooltip {
    .tooltip-header {
      white-space: nowrap;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
    }
    tbody tr:not(.tooltip-header) td:nth-of-type(2) {
      word-break: break-word;
    }
  }
  .d3-tip.nv-event-annotation-layer-table,
  .d3-tip.nv-event-annotation-layer-NATIVE {
    width: 200px;
    border-radius: 2px;
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    fill-opacity: 0.6;
    margin: ${({theme:e})=>2*e.gridUnit}px;
    padding: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.light5};
    &:after {
      content: '\\25BC';
      font-size: ${({theme:e})=>e.typography.sizes.m};
      color: ${({theme:e})=>e.colors.grayscale.base};
      position: absolute;
      bottom: -14px;
      left: 94px;
    }
  }
`},7240:(e,t,a)=>{a.d(t,{A:()=>o});var s=a(96540),i=a(2445);function o(e,t){class a extends s.Component{constructor(e){super(e),this.container=void 0,this.setContainerRef=this.setContainerRef.bind(this)}componentDidMount(){this.execute()}componentDidUpdate(){this.execute()}componentWillUnmount(){this.container=void 0,null!=t&&t.componentWillUnmount&&t.componentWillUnmount.bind(this)()}setContainerRef(e){this.container=e}execute(){this.container&&e(this.container,this.props)}render(){const{id:e,className:t}=this.props;return(0,i.Y)("div",{ref:this.setContainerRef,id:e,className:t})}}const o=a;return e.displayName&&(o.displayName=e.displayName),e.propTypes&&(o.propTypes={...o.propTypes,...e.propTypes}),e.defaultProps&&(o.defaultProps=e.defaultProps),a}}}]);
//# sourceMappingURL=4203dd4b74b217cb987f.chunk.js.map