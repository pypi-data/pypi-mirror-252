(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9060],{62709:function(e,n,t){"use strict";t.d(n,{r:function(){return l}});var r=t(77751),o=t(32393),i=t(14007),a=t(27378);function s(){return s=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},s.apply(this,arguments)}var c=["spacing","children"],l=(0,o.Gp)((function(e,n){var t=(0,o.jC)("Switch",e),l=(0,o.Lr)(e),u=l.spacing,d=void 0===u?"0.5rem":u,p=l.children,f=function(e,n){if(null==e)return{};var t,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}(l,c),h=(0,r.O)(f),g=h.state,m=h.getInputProps,v=h.getCheckboxProps,b=h.getRootProps,x=h.getLabelProps,j=a.useMemo((function(){return s({display:"inline-block",position:"relative",verticalAlign:"middle",lineHeight:0},t.container)}),[t.container]),y=a.useMemo((function(){return s({display:"inline-flex",flexShrink:0,justifyContent:"flex-start",boxSizing:"content-box",cursor:"pointer"},t.track)}),[t.track]),w=a.useMemo((function(){return s({userSelect:"none",marginStart:d},t.label)}),[d,t.label]);return a.createElement(o.m$.label,s({},b(),{className:(0,i.cx)("chakra-switch",e.className),__css:j}),a.createElement("input",s({className:"chakra-switch__input"},m({},n))),a.createElement(o.m$.span,s({},v(),{className:"chakra-switch__track",__css:y}),a.createElement(o.m$.span,{__css:t.thumb,className:"chakra-switch__thumb","data-checked":(0,i.PB)(g.isChecked),"data-hover":(0,i.PB)(g.isHovered)})),p&&a.createElement(o.m$.span,s({className:"chakra-switch__label"},x(),{__css:w}),p))}));i.Ts&&(l.displayName="Switch")},9992:function(e,n,t){"use strict";t.d(n,{u:function(){return j}});var r=t(21893),o=t(25175),i=t(32393),a=t(14007),s=t(30867),c=t(72707),l=t(27092),u=t(27378),d=t(21084),p=t(16962),f=t(49031);function h(){return h=Object.assign||function(e){for(var n=1;n<arguments.length;n++){var t=arguments[n];for(var r in t)Object.prototype.hasOwnProperty.call(t,r)&&(e[r]=t[r])}return e},h.apply(this,arguments)}function g(e,n){if(null==e)return{};var t,r,o={},i=Object.keys(e);for(r=0;r<i.length;r++)t=i[r],n.indexOf(t)>=0||(o[t]=e[t]);return o}var m={exit:{scale:.85,opacity:0,transition:{opacity:{duration:.15,easings:"easeInOut"},scale:{duration:.2,easings:"easeInOut"}}},enter:{scale:1,opacity:1,transition:{opacity:{easings:"easeOut",duration:.2},scale:{duration:.2,ease:[.175,.885,.4,1.1]}}}},v=["openDelay","closeDelay","closeOnClick","closeOnMouseDown","closeOnEsc","onOpen","onClose","placement","id","isOpen","defaultIsOpen","arrowSize","arrowShadowColor","arrowPadding","modifiers","isDisabled","gutter","offset","direction"];var b=["children","label","shouldWrapChildren","aria-label","hasArrow","bg","portalProps","background","backgroundColor","bgColor"],x=(0,i.m$)(c.E.div),j=(0,i.Gp)((function(e,n){var t,c,j=(0,i.mq)("Tooltip",e),y=(0,i.Lr)(e),w=(0,i.Fg)(),O=y.children,C=y.label,k=y.shouldWrapChildren,P=y["aria-label"],S=y.hasArrow,E=y.bg,_=y.portalProps,T=y.background,z=y.backgroundColor,Z=y.bgColor,D=g(y,b),M=null!=(t=null!=(c=null!=T?T:z)?c:E)?t:Z;M&&(j.bg=M,j[r.j.arrowBg.var]=(0,a.K1)(w,"colors",M));var I,N=function(e){void 0===e&&(e={});var n=e,t=n.openDelay,o=void 0===t?0:t,i=n.closeDelay,s=void 0===i?0:i,c=n.closeOnClick,l=void 0===c||c,m=n.closeOnMouseDown,b=n.closeOnEsc,x=void 0===b||b,j=n.onOpen,y=n.onClose,w=n.placement,O=n.id,C=n.isOpen,k=n.defaultIsOpen,P=n.arrowSize,S=void 0===P?10:P,E=n.arrowShadowColor,_=n.arrowPadding,T=n.modifiers,z=n.isDisabled,Z=n.gutter,D=n.offset,M=n.direction,I=g(n,v),N=(0,d.qY)({isOpen:C,defaultIsOpen:k,onOpen:j,onClose:y}),A=N.isOpen,L=N.onOpen,F=N.onClose,$=(0,r.D)({enabled:A,placement:w,arrowPadding:_,modifiers:T,gutter:Z,offset:D,direction:M}),B=$.referenceRef,R=$.getPopperProps,X=$.getArrowInnerProps,W=$.getArrowProps,q=(0,d.Me)(O,"tooltip"),G=u.useRef(null),Y=u.useRef(),H=u.useRef(),Q=u.useCallback((function(){z||(Y.current=window.setTimeout(L,o))}),[z,L,o]),V=u.useCallback((function(){Y.current&&clearTimeout(Y.current),H.current=window.setTimeout(F,s)}),[s,F]),K=u.useCallback((function(){l&&V()}),[l,V]),U=u.useCallback((function(){m&&V()}),[m,V]),J=u.useCallback((function(e){A&&"Escape"===e.key&&V()}),[A,V]);(0,p.b)("keydown",x?J:void 0),u.useEffect((function(){return function(){clearTimeout(Y.current),clearTimeout(H.current)}}),[]),(0,p.b)("mouseleave",V,(function(){return G.current}));var ee=u.useCallback((function(e,n){return void 0===e&&(e={}),void 0===n&&(n=null),h({},e,{ref:(0,f.lq)(G,n,B),onMouseEnter:(0,a.v0)(e.onMouseEnter,Q),onClick:(0,a.v0)(e.onClick,K),onMouseDown:(0,a.v0)(e.onMouseDown,U),onFocus:(0,a.v0)(e.onFocus,Q),onBlur:(0,a.v0)(e.onBlur,V),"aria-describedby":A?q:void 0})}),[Q,V,U,A,q,K,B]),ne=u.useCallback((function(e,n){var t;return void 0===e&&(e={}),void 0===n&&(n=null),R(h({},e,{style:h({},e.style,(t={},t[r.j.arrowSize.var]=S?(0,a.px)(S):void 0,t[r.j.arrowShadowColor.var]=E,t))}),n)}),[R,S,E]),te=u.useCallback((function(e,n){return void 0===e&&(e={}),void 0===n&&(n=null),h({ref:n},I,e,{id:q,role:"tooltip",style:h({},e.style,{position:"relative",transformOrigin:r.j.transformOrigin.varRef})})}),[I,q]);return{isOpen:A,show:Q,hide:V,getTriggerProps:ee,getTooltipProps:te,getTooltipPositionerProps:ne,getArrowProps:W,getArrowInnerProps:X}}(h({},D,{direction:w.direction}));if((0,a.HD)(O)||k)I=u.createElement(i.m$.span,h({tabIndex:0},N.getTriggerProps()),O);else{var A=u.Children.only(O);I=u.cloneElement(A,N.getTriggerProps(A.props,A.ref))}var L=!!P,F=N.getTooltipProps({},n),$=L?(0,a.CE)(F,["role","id"]):F,B=(0,a.ei)(F,["role","id"]);return C?u.createElement(u.Fragment,null,I,u.createElement(l.M,null,N.isOpen&&u.createElement(o.h_,_,u.createElement(i.m$.div,h({},N.getTooltipPositionerProps(),{__css:{zIndex:j.zIndex,pointerEvents:"none"}}),u.createElement(x,h({variants:m},$,{initial:"exit",animate:"enter",exit:"exit",__css:j}),C,L&&u.createElement(s.TX,B,P),S&&u.createElement(i.m$.div,{"data-popper-arrow":!0,className:"chakra-tooltip__arrow-wrapper"},u.createElement(i.m$.div,{"data-popper-arrow-inner":!0,className:"chakra-tooltip__arrow",__css:{bg:j.bg}}))))))):u.createElement(u.Fragment,null,O)}));a.Ts&&(j.displayName="Tooltip")},38687:function(e,n,t){"use strict";var r=t(90849),o=t(31099),i=t(9992),a=t(5008),s=t(24246);function c(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?c(Object(t),!0).forEach((function(n){(0,r.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):c(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}n.Z=function(e){var n=(0,o.Z)({},e);return(0,s.jsx)(i.u,l(l({placement:"right"},n),{},{children:(0,s.jsx)(a.UO,{color:"gray.400"})}))}},24263:function(e,n,t){"use strict";t.r(n),t.d(n,{default:function(){return W}});var r=t(34896),o=t(83125),i=t(6848),a=t(51471),s=t(55732),c=t(97865),l=t(34707),u=t.n(l),d=t(70409),p=t(21084),f=t(5008),h=t(29549),g=t(98784),m=t.n(g),v=t(86677),b=t(27378),x=t(78624),j=t(2458),y=t(44845),w=t(24753),O=t(33167),C=t(60709),k=t(27808),P=t(90849),S=t(73679),E=t(53333),_=t(62709),T=t(92975),z=t(38687),Z=t(24246),D=function(e){var n=e.id,t=e.isChecked,o=e.onChange;return(0,Z.jsxs)(r.kC,{alignItems:"center",gap:"8px",children:[(0,Z.jsx)(_.r,{isChecked:t,size:"sm",onChange:o,colorScheme:"complimentary",id:n,"data-testid":"regulated-toggle"}),(0,Z.jsx)(T.lX,{fontSize:"sm",m:0,htmlFor:n,children:"Regulated"}),(0,Z.jsx)(z.Z,{label:"Toggle on to see only locations in this region with privacy regulations supported by Fides"})]})},M=t(60530),I=t(77751),N=t(62332),A=t(93246),L=function(e){var n=e.groups,t=e.locations,o=e.isOpen,i=e.onClose,a=e.selected,s=e.onChange,l=(0,b.useState)(a),u=l[0],d=l[1],p=(0,b.useState)(!1),f=p[0],g=p[1],m=(0,b.useMemo)((function(){var e=f?t.filter((function(e){var n;return null===(n=e.regulation)||void 0===n?void 0:n.length})):t;return{locationsByGroup:(0,A.VT)(e),filteredLocations:e}}),[t,f]),v=m.filteredLocations,x=m.locationsByGroup,j=(0,E.Q)({items:v,selected:u,onChange:d}),y=j.allSelected,w=j.handleToggleAll,O=j.handleToggleSelection,C=u.filter((function(e){return!Object.keys(x).includes(e)})).length,k=t[0].continent,P=Object.keys(x),S=!(1===P.length&&"Other"===P[0]);return(0,Z.jsxs)(M.u_,{size:"2xl",isOpen:o,onClose:i,isCentered:!0,children:[(0,Z.jsx)(M.ZA,{}),(0,Z.jsxs)(M.hz,{"data-testid":"subgroup-modal",children:[(0,Z.jsx)(M.xB,{fontSize:"lg",fontWeight:"semibold",pt:5,paddingInline:6,pb:5,backgroundColor:"gray.50",borderTopRadius:"md",borderBottom:"1px solid",borderColor:"gray.200",children:"Select locations"}),(0,Z.jsxs)(M.fe,{p:6,maxHeight:"70vh",overflowY:"auto",children:[(0,Z.jsxs)(r.kC,{justifyContent:"space-between",mb:4,children:[(0,Z.jsxs)(r.xu,{children:[(0,Z.jsx)(I.XZ,{colorScheme:"complimentary",size:"md",isChecked:y,onChange:w,mr:3,"data-testid":"select-all",children:(0,Z.jsx)(r.xv,{fontWeight:"semibold",fontSize:"md",children:k})}),(0,Z.jsxs)(r.Ct,{colorScheme:"purple",variant:"solid",width:"fit-content","data-testid":"num-selected-badge",children:[C," selected"]})]}),(0,Z.jsx)(D,{id:"".concat(k,"-modal-regulated"),isChecked:f,onChange:function(){return g(!f)}})]}),S?(0,Z.jsx)(N.UQ,{allowToggle:!0,allowMultiple:!0,children:Object.entries(x).map((function(e){var t=(0,c.Z)(e,2),o=t[0],i=t[1],a=n.find((function(e){return o===e.id})),s=a?a.name:o;return(0,Z.jsxs)(N.Qd,{"data-testid":"".concat(s,"-accordion"),children:[(0,Z.jsx)("h2",{children:(0,Z.jsxs)(N.KF,{children:[(0,Z.jsx)(r.xu,{as:"span",flex:"1",textAlign:"left",fontWeight:"semibold",fontSize:"sm",children:s}),(0,Z.jsx)(N.XE,{})]})}),(0,Z.jsx)(N.Hk,{pb:4,children:(0,Z.jsx)(r.MI,{columns:3,spacing:6,children:i.map((function(e){return(0,Z.jsx)(I.XZ,{size:"sm",colorScheme:"complimentary",isChecked:u.includes(e.id),onChange:function(){return O(e.id)},"data-testid":"".concat(e.name,"-checkbox"),children:e.name},e.id)}))})})]},o)}))}):(0,Z.jsx)(r.MI,{columns:3,spacing:6,paddingInline:4,children:v.map((function(e){return(0,Z.jsx)(I.XZ,{size:"sm",colorScheme:"complimentary",isChecked:u.includes(e.id),onChange:function(){return O(e.id)},"data-testid":"".concat(e.name,"-checkbox"),children:e.name},e.id)}))})]}),(0,Z.jsx)(M.mz,{justifyContent:"center",children:(0,Z.jsxs)(h.hE,{size:"sm",display:"flex",justifyContent:"space-between",width:"100%",children:[(0,Z.jsx)(h.zx,{flexGrow:1,variant:"outline",mr:3,onClick:i,children:"Cancel"}),(0,Z.jsx)(h.zx,{flexGrow:1,colorScheme:"primary",onClick:function(){var e=new Set(u);Object.entries(x).forEach((function(n){var t=(0,c.Z)(n,2),r=t[0];t[1].every((function(e){return u.includes(e.id)}))?e.add(r):e.delete(r)})),s(Array.from(e)),i()},"data-testid":"apply-btn",children:"Apply"})]})})]})]})};function F(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function $(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?F(Object(t),!0).forEach((function(n){(0,P.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):F(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var B=function(e){var n=e.title,t=e.groups,r=e.locations,o=e.selected,i=e.onChange,a=e.search,s=(0,p.qY)(),c=(0,b.useState)(!1),l=c[0],u=c[1],d=!(null===a||void 0===a||!a.length),f=t.length>0,h=r;t.length&&(h=t),d&&(h=[].concat((0,S.Z)(r),(0,S.Z)(t)).sort((function(e,n){return e.name.localeCompare(n.name)})));var g=l?h.filter((function(e){return(0,A.$q)(e,r)})):h,m=a?g.filter((function(e){return function(e,n){var t;return null===(t=e.name)||void 0===t?void 0:t.toLocaleLowerCase().includes(n.toLocaleLowerCase())}(e,a)})):g,v=t.filter((function(e){return"checked"===(0,A.ji)({group:e,selected:o,locations:r})})).map((function(e){return e.id})),x=t.filter((function(e){return"indeterminate"===(0,A.ji)({group:e,selected:o,locations:r})})).map((function(e){return e.id})),j=f?[].concat((0,S.Z)(v),(0,S.Z)(o)):o,y=o.length,w=function(e){var n=r.map((function(n){return e.includes(n.id)?$($({},n),{},{selected:!0}):$($({},n),{},{selected:!1})}));i(n)};return 0===m.length&&a?null:(0,Z.jsxs)(Z.Fragment,{children:[(0,Z.jsx)(E.Z,{title:n,items:m,selected:j,indeterminate:f?x:[],onChange:function(e){var n=new Set(e),o=new Set(j);e.forEach((function(e){o.has(e)||t.find((function(n){return n.id===e}))&&r.filter((function(n){var t;return null===(t=n.belongs_to)||void 0===t?void 0:t.includes(e)})).forEach((function(e){n.add(e.id)}))})),o.forEach((function(e){n.has(e)||t.find((function(n){return n.id===e}))&&r.filter((function(n){var t;return null===(t=n.belongs_to)||void 0===t?void 0:t.includes(e)})).forEach((function(e){n.delete(e.id)}))})),w(Array.from(n))},onViewMore:function(){s.onOpen()},numSelected:y,toggle:(0,Z.jsx)(D,{id:"".concat(n,"-regulated"),isChecked:l,onChange:function(){return u(!l)}})}),(0,Z.jsx)(L,{groups:t,locations:r,isOpen:s.isOpen,onClose:s.onClose,selected:o,onChange:w},"subgroup-modal-selected-".concat(j.length))]})},R=t(17165),X=function(e){var n,t=e.data,o=(0,d.pm)(),i=(0,p.qY)(),a=(0,b.useState)(null!==(n=t.locations)&&void 0!==n?n:[]),l=a[0],g=a[1],P=(0,b.useState)(""),S=P[0],E=P[1],_=(0,R.WA)(),T=(0,c.Z)(_,2),z=T[0],D=T[1].isLoading,M=(0,b.useMemo)((function(){return(0,A.Il)(t.locations||[],t.location_groups||[])}),[t]),I=!m().isEqual(l,t.locations),N=(0,v.useRouter)(),L=function(){N.push(C.vY).then((function(){o.closeAll()}))},F=function(){var e=(0,s.Z)(u().mark((function e(){var n;return u().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,z({locations:l.map((function(e){return{id:e.id,selected:e.selected}})),regulations:[]});case 2:n=e.sent,(0,O.isErrorResult)(n)?o((0,w.Vo)((0,x.e$)(n.error))):o((0,w.t5)((0,Z.jsxs)(r.xv,{children:["Fides has automatically associated the relevant regulations with your location choices."," ",(0,Z.jsx)(k.Z,{onClick:L,children:"View regulations here."})]})));case 4:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),$=function(e){var n=l.map((function(n){var t=e.find((function(e){return e.id===n.id}));return null!==t&&void 0!==t?t:n}));g(n)};return(0,Z.jsxs)(r.gC,{alignItems:"start",spacing:4,children:[(0,Z.jsx)(r.xu,{maxWidth:"510px",width:"100%",children:(0,Z.jsx)(y.Z,{onChange:E,placeholder:"Search",search:S,onClear:function(){return E("")},"data-testid":"search-bar"})}),(0,Z.jsx)(r.MI,{columns:{base:1,md:2,xl:3},spacing:6,width:"100%",children:Object.entries(M).map((function(e){var n=(0,c.Z)(e,2),t=n[0],r=n[1];return(0,Z.jsx)(B,{title:t,groups:r.locationGroups,locations:r.locations,selected:l.filter((function(e){return r.locations.find((function(n){return n.id===e.id}))&&e.selected})).map((function(e){return e.id})),onChange:$,search:S},t)}))}),(0,Z.jsx)(j.Z,{isOpen:i.isOpen,onClose:i.onClose,onConfirm:function(){F(),i.onClose()},title:"Regulation updates",message:"Modifications in your location settings may also affect your regulation settings to simplify management. You can override any Fides-initiated changes directly in the regulation settings.",isCentered:!0,icon:(0,Z.jsx)(f.aN,{color:"orange"})}),I?(0,Z.jsx)(h.zx,{colorScheme:"primary",size:"sm",onClick:i.onOpen,isLoading:D,"data-testid":"save-btn",children:"Save"}):null]})},W=function(){var e=(0,R.QM)().isLoading,n=(0,i.C)(R.P8);return(0,Z.jsx)(a.Z,{title:"Locations",children:(0,Z.jsxs)(r.xu,{"data-testid":"location-management",children:[(0,Z.jsx)(r.X6,{marginBottom:2,fontSize:"2xl",children:"Locations"}),(0,Z.jsxs)(r.xu,{children:[(0,Z.jsx)(r.xv,{marginBottom:4,fontSize:"sm",maxWidth:"720px",children:"Select the locations that you operate in and Fides will make sure that you are automatically presented with the relevant regulatory guidelines and global frameworks for your locations."}),(0,Z.jsx)(r.xu,{children:e?(0,Z.jsx)(o.$,{}):(0,Z.jsx)(X,{data:n})})]})]})})}},55478:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/management/locations",function(){return t(24263)}])}},function(e){e.O(0,[8033,7751,530,4400,9774,2888,179],(function(){return n=55478,e(e.s=n);var n}));var n=e.O();_N_E=n}]);