(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7062],{58772:function(e,t,n){"use strict";var o=n(90331);function s(){}function l(){}l.resetWarningCache=s,e.exports=function(){function e(e,t,n,s,l,a){if(a!==o){var r=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw r.name="Invariant Violation",r}}function t(){return e}e.isRequired=e;var n={array:e,bigint:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:l,resetWarningCache:s};return n.PropTypes=n,n}},23615:function(e,t,n){e.exports=n(58772)()},90331:function(e){"use strict";e.exports="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED"},37062:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return R}});var o=n(27378),s=n(23615),l=n.n(s),a=n(35315),r=n.n(a);const{string:i,array:c,object:u,number:p,bool:d,oneOfType:y,any:h,func:m}=l(),f={id:i,className:i,style:y([i,u]),elements:y([c,h]),stylesheet:y([c,h]),layout:y([u,h]),pan:y([u,h]),zoom:p,panningEnabled:d,userPanningEnabled:d,minZoom:p,maxZoom:p,zoomingEnabled:d,userZoomingEnabled:d,boxSelectionEnabled:d,autoungrabify:d,autolock:d,autounselectify:d,get:m,toJson:m,diff:m,forEach:m,cy:m,headless:d,styleEnabled:d,hideEdgesOnViewport:d,textureOnViewport:d,motionBlur:d,motionBlurOpacity:p,wheelSensitivity:p,pixelRatio:y([i,u])},b=(e,t)=>{if(((e,t)=>null==e||null==t)(e,t)&&(null!=e||null!=t))return!0;if(e===t)return!1;if("object"!=typeof e||"object"!=typeof t)return e!==t;const n=Object.keys(e),o=Object.keys(t),s=n=>e[n]!==t[n];return n.length!==o.length||!(!n.some(s)&&!o.some(s))},g=(e,t)=>null!=e?e[t]:null,E={diff:b,get:g,toJson:e=>e,forEach:(e,t)=>e.forEach(t),elements:[{data:{id:"a",label:"Example node A"}},{data:{id:"b",label:"Example node B"}},{data:{id:"e",source:"a",target:"b"}}],stylesheet:[{selector:"node",style:{label:"data(label)"}}],zoom:1,pan:{x:0,y:0}},O=(e,t,n,o)=>n(g(e,o),g(t,o)),x=(e,t,n,o,s)=>{e[t](s(o))},w=(e,t,n,o)=>{const s=o(n);null!=s&&e.layout(s).run()},_=(e,t,n,o)=>{const s=e.style();null!=s&&s.fromJson(o(n)).update()},k=(e,t,n,o,s,l,a)=>{const r=[],i=e.collection(),c=[],u={},p={},d=e=>s(s(e,"data"),"id");l(n,(e=>{const t=d(e);p[t]=e})),null!=t&&l(t,(t=>{const n=d(t);u[n]=t,(e=>null!=p[e])(n)||i.merge(e.getElementById(n))})),l(n,(e=>{const t=d(e),n=(e=>u[e])(t);(e=>null!=u[e])(t)?c.push({ele1:n,ele2:e}):r.push(o(e))})),i.length>0&&e.remove(i),r.length>0&&e.add(r),c.forEach((({ele1:t,ele2:n})=>C(e,t,n,o,s,a)))},C=(e,t,n,o,s,l)=>{const a=s(s(n,"data"),"id"),r=e.getElementById(a),i={};["data","position","selected","selectable","locked","grabbable","classes"].forEach((e=>{const a=s(n,e);l(a,s(t,e))&&(i[e]=o(a))}));const c=s(n,"scratch");l(c,s(t,"scratch"))&&r.scratch(o(c)),Object.keys(i).length>0&&r.json(i)};class R extends o.Component{static get propTypes(){return f}static get defaultProps(){return E}static normalizeElements(e){if(null!=e.length)return e;{let{nodes:t,edges:n}=e;return null==t&&(t=[]),null==n&&(n=[]),t.concat(n)}}constructor(e){super(e),this.displayName="CytoscapeComponent",this.containerRef=o.createRef()}componentDidMount(){const e=this.containerRef.current,{global:t,headless:n,styleEnabled:o,hideEdgesOnViewport:s,textureOnViewport:l,motionBlur:a,motionBlurOpacity:i,wheelSensitivity:c,pixelRatio:u}=this.props,p=this._cy=new(r())({container:e,headless:n,styleEnabled:o,hideEdgesOnViewport:s,textureOnViewport:l,motionBlur:a,motionBlurOpacity:i,wheelSensitivity:c,pixelRatio:u});t&&(window[t]=p),this.updateCytoscape(null,this.props)}updateCytoscape(e,t){const n=this._cy,{diff:o,toJson:s,get:l,forEach:a}=t;((e,t,n,o,s,l,a)=>{e.batch((()=>{(o===b||O(t,n,o,"elements"))&&k(e,g(t,"elements"),g(n,"elements"),s,l,a,o),O(t,n,o,"stylesheet")&&_(e,g(t,"stylesheet"),g(n,"stylesheet"),s),["zoom","minZoom","maxZoom","zoomingEnabled","userZoomingEnabled","pan","panningEnabled","userPanningEnabled","boxSelectionEnabled","autoungrabify","autolock","autounselectify"].forEach((l=>{O(t,n,o,l)&&x(e,l,g(t,l),g(n,l),s)}))})),O(t,n,o,"layout")&&w(e,g(t,"layout"),g(n,"layout"),s)})(n,e,t,o,s,l,a),null!=t.cy&&t.cy(n)}componentDidUpdate(e){this.updateCytoscape(e,this.props)}componentWillUnmount(){this._cy.destroy()}render(){const{id:e,className:t,style:n}=this.props;return o.createElement("div",{ref:this.containerRef,id:e,className:t,style:n})}}}}]);