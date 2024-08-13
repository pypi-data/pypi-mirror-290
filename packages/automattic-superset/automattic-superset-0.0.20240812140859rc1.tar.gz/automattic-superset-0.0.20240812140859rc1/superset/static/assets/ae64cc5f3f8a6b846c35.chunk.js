"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2865],{55246:(t,e,n)=>{n.r(e),n.d(e,{default:()=>x});var r=n(7240),s=n(96453),o=n(24143),a=n.n(o),i=n(5556),c=n.n(i),l=n(32142),p=n(69161),u=n(94963),d=n(31787);const h={data:c().arrayOf(c().shape({country_id:c().string,metric:c().number})),width:c().number,height:c().number,country:c().string,linearColorScheme:c().string,mapBaseUrl:c().string,numberFormat:c().string},y={};function g(t,e){const{data:n,width:r,height:s,country:o,linearColorScheme:i,numberFormat:c,colorScheme:h,sliceId:g}=e,m=t,f=(0,l.gV)(c),v=(0,p.A)().get(i).createLinearScale(function(t,e){let n,r;if(void 0===e)for(const e of t)null!=e&&(void 0===n?e>=e&&(n=r=e):(n>e&&(n=e),r<e&&(r=e)));else{let s=-1;for(let o of t)null!=(o=e(o,++s))&&(void 0===n?o>=o&&(n=r=o):(n>o&&(n=o),r<o&&(r=o)))}return[n,r]}(n,(t=>t.metric))),x=u.getScale(h),$={};n.forEach((t=>{$[t.country_id]=h?x(t.country_id,g):v(t.metric)}));const b=t=>$[t.properties.ISO]||"none",k=a().geo.path(),w=a().select(m);w.classed("superset-legacy-chart-country-map",!0),w.selectAll("*").remove(),m.style.height=`${s}px`,m.style.width=`${r}px`;const C=w.append("svg:svg").attr("width",r).attr("height",s).attr("preserveAspectRatio","xMidYMid meet"),N=C.append("rect").attr("class","background").attr("width",r).attr("height",s),A=C.append("g"),S=A.append("g").classed("map-layer",!0),T=A.append("g").classed("text-layer",!0).attr("transform",`translate(${r/2}, 45)`),_=T.append("text").classed("big-text",!0),z=T.append("text").classed("result-text",!0).attr("dy","1em");let M;const I=function(t){const e=t&&M!==t;let n,o,a;const i=r/2,c=s/2;if(e){const e=k.centroid(t);[n,o]=e,a=4,M=t}else n=i,o=c,a=1,M=null;A.transition().duration(750).attr("transform",`translate(${i},${c})scale(${a})translate(${-n},${-o})`),T.style("opacity",0).attr("transform",`translate(0,0)translate(${n},${e?o-5:45})`).transition().duration(750).style("opacity",1),_.transition().duration(750).style("font-size",e?6:16),z.transition().duration(750).style("font-size",e?16:24)};N.on("click",I);const R=function(t){let e=b(t);"none"!==e&&(e=a().rgb(e).darker().toString()),a().select(this).style("fill",e),function(t){let e="";t&&t.properties&&(e=t.properties.ID_2?t.properties.NAME_2:t.properties.NAME_1),_.text(e)}(t);const r=n.filter((e=>e.country_id===t.properties.ISO));var s;(s=r).length>0&&z.text(f(s[0].metric))},U=function(){a().select(this).style("fill",b),_.text(""),z.text("")};function Y(t){const{features:e}=t,n=a().geo.centroid(t),o=a().geo.mercator().scale(100).center(n).translate([r/2,s/2]);k.projection(o);const i=k.bounds(t),c=100*r/(i[1][0]-i[0][0]),l=100*s/(i[1][1]-i[0][1]),p=c<l?c:l;o.scale(p);const u=k.bounds(t);o.translate([r-(u[0][0]+u[1][0])/2,s-(u[0][1]+u[1][1])/2]),S.selectAll("path").data(e).enter().append("path").attr("d",k).attr("class","region").attr("vector-effect","non-scaling-stroke").style("fill",b).on("mouseenter",R).on("mouseout",U).on("click",I)}const D=y[o];if(D)Y(D);else{const e=d.Ay[o];a().json(e,((e,n)=>{if(e){var r;const e=(null==(r=d.JK.find((t=>t[0]===o)))?void 0:r[1])||o;a().select(t).html(`<div class="alert alert-danger">Could not load map data for ${e}</div>`)}else y[o]=n,Y(n)}))}}g.displayName="CountryMap",g.propTypes=h;const m=g;var f=n(2445);const v=(0,r.A)(m),x=(0,s.I4)((({className:t,...e})=>(0,f.Y)("div",{className:t,children:(0,f.Y)(v,{...e})})))`
  ${({theme:t})=>`\n    .superset-legacy-chart-country-map svg {\n      background-color: ${t.colors.grayscale.light5};\n    }\n\n    .superset-legacy-chart-country-map {\n      position: relative;\n    }\n\n    .superset-legacy-chart-country-map .background {\n      fill: ${t.colors.grayscale.light5};\n      pointer-events: all;\n    }\n\n    .superset-legacy-chart-country-map .map-layer {\n      fill: ${t.colors.grayscale.light5};\n      stroke: ${t.colors.grayscale.light1};\n    }\n\n    .superset-legacy-chart-country-map .effect-layer {\n      pointer-events: none;\n    }\n\n    .superset-legacy-chart-country-map .text-layer {\n      color: ${t.colors.grayscale.dark1};\n      text-anchor: middle;\n      pointer-events: none;\n    }\n\n    .superset-legacy-chart-country-map text.result-text {\n      font-weight: ${t.typography.weights.light};\n      font-size: ${t.typography.sizes.xl}px;\n    }\n\n    .superset-legacy-chart-country-map text.big-text {\n      font-weight: ${t.typography.weights.bold};\n      font-size: ${t.typography.sizes.l}px;\n    }\n\n    .superset-legacy-chart-country-map path.region {\n      cursor: pointer;\n      stroke: ${t.colors.grayscale.light2};\n    }\n  `}
`},7240:(t,e,n)=>{n.d(e,{A:()=>o});var r=n(96540),s=n(2445);function o(t,e){class n extends r.Component{constructor(t){super(t),this.container=void 0,this.setContainerRef=this.setContainerRef.bind(this)}componentDidMount(){this.execute()}componentDidUpdate(){this.execute()}componentWillUnmount(){this.container=void 0,null!=e&&e.componentWillUnmount&&e.componentWillUnmount.bind(this)()}setContainerRef(t){this.container=t}execute(){this.container&&t(this.container,this.props)}render(){const{id:t,className:e}=this.props;return(0,s.Y)("div",{ref:this.setContainerRef,id:t,className:e})}}const o=n;return t.displayName&&(o.displayName=t.displayName),t.propTypes&&(o.propTypes={...o.propTypes,...t.propTypes}),t.defaultProps&&(o.defaultProps=t.defaultProps),n}}}]);
//# sourceMappingURL=ae64cc5f3f8a6b846c35.chunk.js.map