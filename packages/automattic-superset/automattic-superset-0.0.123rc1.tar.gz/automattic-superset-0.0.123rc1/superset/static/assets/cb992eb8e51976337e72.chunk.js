"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2892],{42892:(t,n,e)=>{e.r(n),e.d(n,{default:()=>E});var r=e(7240),o=e(96453),a=e(5556),s=e.n(a),i=e(24143),c=e.n(i),u=e(86914),l=e(71918);var d=e(32142),p=e(53682),f=e(94963),h=e(75107);const y={data:s().arrayOf(s().shape({source:s().string,target:s().string,value:s().number})),width:s().number,height:s().number,colorScheme:s().string},g=(0,d.gV)(p.A.FLOAT);function m(t,n){const{data:e,width:r,height:o,colorScheme:a,sliceId:s}=n,i=c().select(t);i.classed("superset-legacy-chart-sankey",!0);const d=r-5-5,p=o-5-5;i.selectAll("*").remove();const y=i.append("div").attr("class","sankey-tooltip").style("opacity",0),m=i.append("svg").attr("width",d+5+5).attr("height",p+5+5).append("g").attr("transform","translate(5,5)"),v=f.getScale(a),k=function(){var t={},n=24,e=8,r=[1,1],o=[],a=[];function s(){function t(t,n){return t.source.y-n.source.y}function n(t,n){return t.target.y-n.target.y}o.forEach((function(e){e.sourceLinks.sort(n),e.targetLinks.sort(t)})),o.forEach((function(t){var n=0,e=0;t.sourceLinks.forEach((function(t){t.sy=n,n+=t.dy})),t.targetLinks.forEach((function(t){t.ty=e,e+=t.dy}))}))}function i(t){return t.y+t.dy/2}function c(t){return t.value}return t.nodeWidth=function(e){return arguments.length?(n=+e,t):n},t.nodePadding=function(n){return arguments.length?(e=+n,t):e},t.nodes=function(n){return arguments.length?(o=n,t):o},t.links=function(n){return arguments.length?(a=n,t):a},t.size=function(n){return arguments.length?(r=n,t):r},t.layout=function(d){return o.forEach((function(t){t.sourceLinks=[],t.targetLinks=[]})),a.forEach((function(t){var n=t.source,e=t.target;"number"==typeof n&&(n=t.source=o[t.source]),"number"==typeof e&&(e=t.target=o[t.target]),n.sourceLinks.push(t),e.targetLinks.push(t)})),o.forEach((function(t){t.value=Math.max((0,u.sum)(t.sourceLinks,c),(0,u.sum)(t.targetLinks,c))})),function(){for(var t,e,a=o,s=0;a.length;)t=[],a.forEach((function(e){e.x=s,e.dx=n,e.sourceLinks.forEach((function(n){t.indexOf(n.target)<0&&t.push(n.target)}))})),a=t,++s;(function(t){o.forEach((function(n){n.sourceLinks.length||(n.x=t-1)}))})(s),e=(r[0]-n)/(s-1),o.forEach((function(t){t.x*=e}))}(),function(t){var n,s=(0,l.$I)().key((function(t){return t.x})).sortKeys(u.ascending).entries(o).map((function(t){return t.values}));n=(0,u.min)(s,(function(t){return(r[1]-(t.length-1)*e)/(0,u.sum)(t,c)})),s.forEach((function(t){t.forEach((function(t,e){t.y=e,t.dy=t.value*n}))})),a.forEach((function(t){t.dy=t.value*n})),h();for(var d=1;t>0;--t)f(d*=.99),h(),p(d),h();function p(t){function n(t){return i(t.source)*t.value}s.forEach((function(e){e.forEach((function(e){if(e.targetLinks.length){var r=(0,u.sum)(e.targetLinks,n)/(0,u.sum)(e.targetLinks,c);e.y+=(r-i(e))*t}}))}))}function f(t){function n(t){return i(t.target)*t.value}s.slice().reverse().forEach((function(e){e.forEach((function(e){if(e.sourceLinks.length){var r=(0,u.sum)(e.sourceLinks,n)/(0,u.sum)(e.sourceLinks,c);e.y+=(r-i(e))*t}}))}))}function h(){s.forEach((function(t){var n,o,a,s=0,i=t.length;for(t.sort(y),a=0;a<i;++a)(o=s-(n=t[a]).y)>0&&(n.y+=o),s=n.y+n.dy+e;if((o=s-e-r[1])>0)for(s=n.y-=o,a=i-2;a>=0;--a)(o=(n=t[a]).y+n.dy+e-s)>0&&(n.y-=o),s=n.y}))}function y(t,n){return t.y-n.y}}(d),s(),t},t.relayout=function(){return s(),t},t.link=function(){var t=.5;function n(n){var e,r,o=n.source.x+n.source.dx,a=n.target.x,s=(e=+(e=o),r=+(r=a),function(t){return e*(1-t)+r*t}),i=s(t),c=s(1-t),u=n.source.y+n.sy+n.dy/2,l=n.target.y+n.ty+n.dy/2;return"M"+o+","+u+"C"+i+","+u+" "+c+","+l+" "+a+","+l}return n.curvature=function(e){return arguments.length?(t=+e,n):t},n},t}().nodeWidth(15).nodePadding(10).size([d,p]),x=k.link();let L={};const E=e.map((t=>{const n={...t};return n.source=L[n.source]||(L[n.source]={name:n.source}),n.target=L[n.target]||(L[n.target]={name:n.target}),n.value=Number(n.value),n}));function $(t){y.html((()=>function(t){let n;if(t.sourceLinks)n=`${t.name} Value: <span class='emph'>${g(t.value)}</span>`;else{const e=g(t.value),r=c().round(t.value/t.source.value*100,1),o=c().round(t.value/t.target.value*100,1);n=["<div class=''>Path Value: <span class='emph'>",e,"</span></div>","<div class='percents'>","<span class='emph'>",Number.isFinite(r)?r:"100","%</span> of ",t.source.name,"<br/>",`<span class='emph'>${Number.isFinite(o)?o:"--"}%</span> of `,t.target.name,"</div>"].join("")}return n}(t))).transition().duration(200);const{height:n,width:e}=y.node().getBoundingClientRect();y.style("left",`${Math.min(c().event.offsetX+10,r-e)}px`).style("top",`${Math.min(c().event.offsetY+10,o-n)}px`).style("position","absolute").style("opacity",.95)}function b(){y.transition().duration(100).style("opacity",0)}L=c().values(L),k.nodes(L).links(E).layout(32);const N=m.append("g").selectAll(".link").data(E).enter().append("path").attr("class","link").attr("d",x).style("stroke-width",(t=>Math.max(1,t.dy))).sort(((t,n)=>n.dy-t.dy)).on("mouseover",$).on("mouseout",b);function w(){var t;const n=null!=(t=i.selectAll(".node")[0])?t:[],e=(0,h.HC)(n);n.forEach((t=>{const n=t.getElementsByTagName("text")[0];n&&(e.includes(t)?n.classList.add("opacity-0"):n.classList.remove("opacity-0"))}))}const C=m.append("g").selectAll(".node").data(L).enter().append("g").attr("class","node").attr("transform",(t=>`translate(${t.x},${t.y})`)).call(c().behavior.drag().origin((t=>t)).on("dragstart",(function(){this.parentNode.append(this)})).on("drag",(function(t){c().select(this).attr("transform",`translate(${t.x},${t.y=Math.max(0,Math.min(o-t.dy,c().event.y))})`),k.relayout(),N.attr("d",x)})).on("dragend",w));C.append("rect").attr("height",(t=>t.dy>5?t.dy:5)).attr("width",k.nodeWidth()).style("fill",(t=>{const n=t.name||"N/A";return t.color=v(n,s,a),t.color})).style("stroke",(t=>c().rgb(t.color).darker(2))).on("mouseover",$).on("mouseout",b),C.append("text").attr("x",-6).attr("y",(t=>t.dy/2)).attr("dy",".35em").attr("text-anchor","end").attr("transform",null).text((t=>t.name)).attr("class","opacity-0").filter((t=>t.x<d/2)).attr("x",6+k.nodeWidth()).attr("text-anchor","start"),w()}m.displayName="Sankey",m.propTypes=y;const v=m;var k=e(2445);const x=(0,r.A)(v),L=({className:t,...n})=>(0,k.Y)("div",{className:t,children:(0,k.Y)(x,{...n})});L.propTypes={className:s().string.isRequired};const E=(0,o.I4)(L)`
  ${({theme:t})=>`\n    .superset-legacy-chart-sankey {\n      .node {\n        rect {\n          cursor: move;\n          fill-opacity: ${t.opacity.heavy};\n          shape-rendering: crispEdges;\n        }\n        text {\n          pointer-events: none;\n          text-shadow: 0 1px 0 ${t.colors.grayscale.light5};\n          font-size: ${t.typography.sizes.s}px;\n        }\n      }\n      .link {\n        fill: none;\n        stroke: ${t.colors.grayscale.dark2};\n        stroke-opacity: ${t.opacity.light};\n        &:hover {\n          stroke-opacity: ${t.opacity.mediumLight};\n        }\n      }\n      .opacity-0 {\n        opacity: 0;\n      }\n    }\n    .sankey-tooltip {\n      position: absolute;\n      width: auto;\n      background: ${t.colors.grayscale.light2};\n      padding: ${3*t.gridUnit}px;\n      font-size: ${t.typography.sizes.s}px;\n      color: ${t.colors.grayscale.dark2};\n      border: 1px solid ${t.colors.grayscale.light5};\n      text-align: center;\n      pointer-events: none;\n    }\n  `}
`},7240:(t,n,e)=>{e.d(n,{A:()=>a});var r=e(96540),o=e(2445);function a(t,n){class e extends r.Component{constructor(t){super(t),this.container=void 0,this.setContainerRef=this.setContainerRef.bind(this)}componentDidMount(){this.execute()}componentDidUpdate(){this.execute()}componentWillUnmount(){this.container=void 0,null!=n&&n.componentWillUnmount&&n.componentWillUnmount.bind(this)()}setContainerRef(t){this.container=t}execute(){this.container&&t(this.container,this.props)}render(){const{id:t,className:n}=this.props;return(0,o.Y)("div",{ref:this.setContainerRef,id:t,className:n})}}const a=e;return t.displayName&&(a.displayName=t.displayName),t.propTypes&&(a.propTypes={...a.propTypes,...t.propTypes}),t.defaultProps&&(a.defaultProps=t.defaultProps),e}}}]);
//# sourceMappingURL=cb992eb8e51976337e72.chunk.js.map