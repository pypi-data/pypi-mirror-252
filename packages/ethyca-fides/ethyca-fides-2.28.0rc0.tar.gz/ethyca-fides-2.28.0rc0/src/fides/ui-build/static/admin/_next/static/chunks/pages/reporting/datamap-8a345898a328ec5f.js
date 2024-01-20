(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9196],{62709:function(e,t,n){"use strict";n.d(t,{r:function(){return u}});var r=n(77751),a=n(32393),i=n(14007),s=n(27378);function o(){return o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},o.apply(this,arguments)}var c=["spacing","children"],u=(0,a.Gp)((function(e,t){var n=(0,a.jC)("Switch",e),u=(0,a.Lr)(e),l=u.spacing,d=void 0===l?"0.5rem":l,f=u.children,p=function(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(u,c),_=(0,r.O)(p),g=_.state,x=_.getInputProps,h=_.getCheckboxProps,S=_.getRootProps,E=_.getLabelProps,T=s.useMemo((function(){return o({display:"inline-block",position:"relative",verticalAlign:"middle",lineHeight:0},n.container)}),[n.container]),O=s.useMemo((function(){return o({display:"inline-flex",flexShrink:0,justifyContent:"flex-start",boxSizing:"content-box",cursor:"pointer"},n.track)}),[n.track]),m=s.useMemo((function(){return o({userSelect:"none",marginStart:d},n.label)}),[d,n.label]);return s.createElement(a.m$.label,o({},S(),{className:(0,i.cx)("chakra-switch",e.className),__css:T}),s.createElement("input",o({className:"chakra-switch__input"},x({},t))),s.createElement(a.m$.span,o({},h(),{className:"chakra-switch__track",__css:O}),s.createElement(a.m$.span,{__css:n.thumb,className:"chakra-switch__thumb","data-checked":(0,i.PB)(g.isChecked),"data-hover":(0,i.PB)(g.isHovered)})),f&&s.createElement(a.m$.span,o({className:"chakra-switch__label"},E(),{__css:m}),f))}));i.Ts&&(u.displayName="Switch")},9992:function(e,t,n){"use strict";n.d(t,{u:function(){return T}});var r=n(21893),a=n(25175),i=n(32393),s=n(14007),o=n(30867),c=n(72707),u=n(27092),l=n(27378),d=n(21084),f=n(16962),p=n(49031);function _(){return _=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},_.apply(this,arguments)}function g(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}var x={exit:{scale:.85,opacity:0,transition:{opacity:{duration:.15,easings:"easeInOut"},scale:{duration:.2,easings:"easeInOut"}}},enter:{scale:1,opacity:1,transition:{opacity:{easings:"easeOut",duration:.2},scale:{duration:.2,ease:[.175,.885,.4,1.1]}}}},h=["openDelay","closeDelay","closeOnClick","closeOnMouseDown","closeOnEsc","onOpen","onClose","placement","id","isOpen","defaultIsOpen","arrowSize","arrowShadowColor","arrowPadding","modifiers","isDisabled","gutter","offset","direction"];var S=["children","label","shouldWrapChildren","aria-label","hasArrow","bg","portalProps","background","backgroundColor","bgColor"],E=(0,i.m$)(c.E.div),T=(0,i.Gp)((function(e,t){var n,c,T=(0,i.mq)("Tooltip",e),O=(0,i.Lr)(e),m=(0,i.Fg)(),A=O.children,v=O.label,j=O.shouldWrapChildren,R=O["aria-label"],C=O.hasArrow,b=O.bg,y=O.portalProps,D=O.background,I=O.backgroundColor,P=O.bgColor,w=g(O,S),k=null!=(n=null!=(c=null!=D?D:I)?c:b)?n:P;k&&(T.bg=k,T[r.j.arrowBg.var]=(0,s.K1)(m,"colors",k));var N,G=function(e){void 0===e&&(e={});var t=e,n=t.openDelay,a=void 0===n?0:n,i=t.closeDelay,o=void 0===i?0:i,c=t.closeOnClick,u=void 0===c||c,x=t.closeOnMouseDown,S=t.closeOnEsc,E=void 0===S||S,T=t.onOpen,O=t.onClose,m=t.placement,A=t.id,v=t.isOpen,j=t.defaultIsOpen,R=t.arrowSize,C=void 0===R?10:R,b=t.arrowShadowColor,y=t.arrowPadding,D=t.modifiers,I=t.isDisabled,P=t.gutter,w=t.offset,k=t.direction,N=g(t,h),G=(0,d.qY)({isOpen:v,defaultIsOpen:j,onOpen:T,onClose:O}),L=G.isOpen,M=G.onOpen,U=G.onClose,Y=(0,r.D)({enabled:L,placement:m,arrowPadding:y,modifiers:D,gutter:P,offset:w,direction:k}),F=Y.referenceRef,V=Y.getPopperProps,z=Y.getArrowInnerProps,H=Y.getArrowProps,B=(0,d.Me)(A,"tooltip"),W=l.useRef(null),X=l.useRef(),K=l.useRef(),Z=l.useCallback((function(){I||(X.current=window.setTimeout(M,a))}),[I,M,a]),q=l.useCallback((function(){X.current&&clearTimeout(X.current),K.current=window.setTimeout(U,o)}),[o,U]),$=l.useCallback((function(){u&&q()}),[u,q]),J=l.useCallback((function(){x&&q()}),[x,q]),Q=l.useCallback((function(e){L&&"Escape"===e.key&&q()}),[L,q]);(0,f.b)("keydown",E?Q:void 0),l.useEffect((function(){return function(){clearTimeout(X.current),clearTimeout(K.current)}}),[]),(0,f.b)("mouseleave",q,(function(){return W.current}));var ee=l.useCallback((function(e,t){return void 0===e&&(e={}),void 0===t&&(t=null),_({},e,{ref:(0,p.lq)(W,t,F),onMouseEnter:(0,s.v0)(e.onMouseEnter,Z),onClick:(0,s.v0)(e.onClick,$),onMouseDown:(0,s.v0)(e.onMouseDown,J),onFocus:(0,s.v0)(e.onFocus,Z),onBlur:(0,s.v0)(e.onBlur,q),"aria-describedby":L?B:void 0})}),[Z,q,J,L,B,$,F]),te=l.useCallback((function(e,t){var n;return void 0===e&&(e={}),void 0===t&&(t=null),V(_({},e,{style:_({},e.style,(n={},n[r.j.arrowSize.var]=C?(0,s.px)(C):void 0,n[r.j.arrowShadowColor.var]=b,n))}),t)}),[V,C,b]),ne=l.useCallback((function(e,t){return void 0===e&&(e={}),void 0===t&&(t=null),_({ref:t},N,e,{id:B,role:"tooltip",style:_({},e.style,{position:"relative",transformOrigin:r.j.transformOrigin.varRef})})}),[N,B]);return{isOpen:L,show:Z,hide:q,getTriggerProps:ee,getTooltipProps:ne,getTooltipPositionerProps:te,getArrowProps:H,getArrowInnerProps:z}}(_({},w,{direction:m.direction}));if((0,s.HD)(A)||j)N=l.createElement(i.m$.span,_({tabIndex:0},G.getTriggerProps()),A);else{var L=l.Children.only(A);N=l.cloneElement(L,G.getTriggerProps(L.props,L.ref))}var M=!!R,U=G.getTooltipProps({},t),Y=M?(0,s.CE)(U,["role","id"]):U,F=(0,s.ei)(U,["role","id"]);return v?l.createElement(l.Fragment,null,N,l.createElement(u.M,null,G.isOpen&&l.createElement(a.h_,y,l.createElement(i.m$.div,_({},G.getTooltipPositionerProps(),{__css:{zIndex:T.zIndex,pointerEvents:"none"}}),l.createElement(E,_({variants:x},Y,{initial:"exit",animate:"enter",exit:"exit",__css:T}),v,M&&l.createElement(o.TX,F,R),C&&l.createElement(i.m$.div,{"data-popper-arrow":!0,className:"chakra-tooltip__arrow-wrapper"},l.createElement(i.m$.div,{"data-popper-arrow-inner":!0,className:"chakra-tooltip__arrow",__css:{bg:T.bg}}))))))):l.createElement(l.Fragment,null,A)}));s.Ts&&(T.displayName="Tooltip")},68512:function(e,t,n){"use strict";var r=n(90849),a=n(34896),i=n(88038),s=n.n(i),o=(n(27378),n(24246));function c(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function u(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?c(Object(n),!0).forEach((function(t){(0,r.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):c(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}t.Z=function(e){var t=e.children,n=e.title,r=e.mainProps;return(0,o.jsxs)(a.kC,{"data-testid":n,direction:"column",height:"calc(100vh - 48px)",width:"calc(100vw - 200px)",children:[(0,o.jsxs)(s(),{children:[(0,o.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,o.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,o.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,o.jsx)(a.kC,u(u({pt:6,as:"main",overflow:"auto",direction:"column",flex:1,minWidth:0},r),{},{children:t}))]})}},62905:function(e,t,n){"use strict";n.d(t,{Dd:function(){return h},Oy:function(){return x},XK:function(){return p},bH:function(){return g}});var r=n(90849),a=n(77751),i=n(34896),s=n(62332),o=n(29549),c=n(60530),u=n(27378),l=n(24246);function d(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function f(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?d(Object(n),!0).forEach((function(t){(0,r.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):d(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var p=function(e,t){var n=e.filter((function(e){return e.isChecked}));return n.length>0?"".concat(t,"=").concat(n.map((function(e){return e.value})).join("&".concat(t,"="))):void 0},_=function(e){var t=e.value,n=e.displayText,r=e.isChecked,s=e.onCheckboxChange;return(0,l.jsx)(a.XZ,{value:t,height:"20px",mb:"25px",isChecked:r,onChange:function(e){var n=e.target;s(t,n.checked)},_focusWithin:{bg:"gray.100"},colorScheme:"complimentary",children:(0,l.jsx)(i.xv,{fontSize:"sm",lineHeight:5,textOverflow:"ellipsis",overflow:"hidden",children:n})},t)},g=function(e){var t=e.options,n=e.header,r=e.onCheckboxChange,a=e.columns,c=void 0===a?3:a,d=e.numDefaultOptions,p=void 0===d?15:d,g=(0,u.useState)(!1),x=g[0],h=g[1],S=x?t:t.slice(0,p),E=t.length>p;return(0,l.jsxs)(s.Qd,{border:"0px",padding:"12px 8px 8px 12px",children:[(0,l.jsx)(i.X6,{height:"56px",children:(0,l.jsxs)(s.KF,{height:"100%",children:[(0,l.jsx)(i.xu,{flex:"1",alignItems:"center",justifyContent:"center",textAlign:"left",fontWeight:600,children:n}),(0,l.jsx)(s.XE,{})]})}),(0,l.jsxs)(s.Hk,{id:"panel-".concat(n),children:[(0,l.jsx)(i.MI,{columns:c,children:S.map((function(e){return(0,l.jsx)(_,f(f({},e),{},{onCheckboxChange:r}),e.value)}))}),!x&&E?(0,l.jsx)(o.zx,{size:"sm",variant:"ghost",onClick:function(){h(!0)},children:"View more"}):null,x&&E?(0,l.jsx)(o.zx,{size:"sm",variant:"ghost",onClick:function(){h(!1)},children:"View less"}):null]})]})},x=function(e){var t=e.heading,n=e.children;return(0,l.jsxs)(i.xu,{padding:"12px 8px 8px 12px",maxHeight:600,children:[t?(0,l.jsx)(i.X6,{size:"md",lineHeight:6,fontWeight:"bold",mb:2,children:t}):null,n]})},h=function(e){var t=e.isOpen,n=e.onClose,r=e.children,a=e.resetFilters;return(0,l.jsxs)(c.u_,{isOpen:t,onClose:n,isCentered:!0,size:"2xl",children:[(0,l.jsx)(c.ZA,{}),(0,l.jsxs)(c.hz,{children:[(0,l.jsx)(c.xB,{children:"Filters"}),(0,l.jsx)(c.ol,{}),(0,l.jsx)(i.iz,{}),(0,l.jsx)(c.fe,{maxH:"85vh",padding:"0px",overflowX:"auto",style:{scrollbarGutter:"stable"},children:r}),(0,l.jsx)(c.mz,{children:(0,l.jsxs)(i.xu,{display:"flex",justifyContent:"space-between",width:"100%",children:[(0,l.jsx)(o.zx,{variant:"outline",size:"sm",mr:3,onClick:a,flexGrow:1,children:"Reset filters"}),(0,l.jsx)(o.zx,{colorScheme:"primary",size:"sm",onClick:n,flexGrow:1,children:"Done"})]})})]})]})}},44409:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return G}});var r=n(27378),a=n(68512),i=n(90849),s=n(21084),o=n(34896),c=n(29470),u=n(29549),l=n(73452),d=n(92222),f=n(59003),p=n(25803),_=n(62905),g=n(61561),x=n(62332),h=n(6848),S=n(47134),E=n(75846),T=n(10612),O=n(24246);function m(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function A(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?m(Object(n),!0).forEach((function(t){(0,i.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):m(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var v=function(e){var t=e.isOpen,n=e.onClose,r=e.resetFilters,a=e.dataUseOptions,i=e.onDataUseChange,s=e.dataCategoriesOptions,o=e.onDataCategoriesChange,c=e.dataSubjectOptions,u=e.onDataSubjectChange;return(0,O.jsx)(_.Dd,{isOpen:t,onClose:n,resetFilters:r,children:(0,O.jsxs)(x.UQ,{width:"100%",allowToggle:!0,children:[(0,O.jsx)(_.bH,{options:a,onCheckboxChange:i,header:"Data uses"}),(0,O.jsx)(_.bH,{options:s,onCheckboxChange:o,header:"Data categories"}),(0,O.jsx)(_.bH,{options:c,onCheckboxChange:u,header:"Data subjects"})]})})},j=n(44047),R=n(43978);function C(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function b(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?C(Object(n),!0).forEach((function(t){(0,i.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):C(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var y,D=(0,d.Cl)(),I={items:[],total:0,page:1,size:25,pages:1};!function(e){e.SYSTEM_NAME="system_name",e.DATA_USE="data_use",e.DATA_CATEGORY="data_categories",e.DATA_SUBJECT="data_subjects",e.LEGAL_NAME="legal_name",e.DPO="dpo",e.LEGAL_BASIS_FOR_PROCESSING="legal_basis_for_processing",e.ADMINISTRATING_DEPARTMENT="adminstrating_department",e.COOKIE_MAX_AGE_SECONDS="cookie_max_age_seconds",e.PRIVACY_POLICY="privacy_policy",e.LEGAL_ADDRESS="legal_address",e.COOKIE_REFRESH="cookie_refresh",e.DATA_SECURITY_PRACTICES="data_security_practices",e.DATA_SHARED_WITH_THIRD_PARTIES="DATA_SHARED_WITH_THIRD_PARTIES",e.DATA_STEWARDS="data_stewards",e.DECLARATION_NAME="declaration_name",e.DESCRIPTION="description",e.DOES_INTERNATIONAL_TRANSFERS="does_international_transfers",e.DPA_LOCATION="dpa_location",e.EGRESS="egress",e.EXEMPT_FROM_PRIVACY_REGULATIONS="exempt_from_privacy_regulations",e.FEATURES="features",e.FIDES_KEY="fides_key",e.FLEXIBLE_LEGAL_BASIS_FOR_PROCESSING="flexible_legal_basis_for_processing",e.IMPACT_ASSESSMENT_LOCATION="impact_assessment_location",e.INGRESS="ingress",e.JOINT_CONTROLLER_INFO="joint_controller_info",e.LEGAL_BASIS_FOR_PROFILING="legal_basis_for_profiling",e.LEGAL_BASIS_FOR_TRANSFERS="legal_basis_for_transfers",e.LEGITIMATE_INTEREST_DISCLOSURE_URL="legitimate_interest_disclosure_url",e.LINK_TO_PROCESSOR_CONTRACT="link_to_processor_contract",e.PROCESSES_PERSONAL_DATA="processes_personal_data",e.REASON_FOR_EXEMPTION="reason_for_exemption",e.REQUIRES_DATA_PROTECTION_ASSESSMENTS="requires_data_protection_assessments",e.RESPONSIBILITY="responsibility",e.RETENTION_PERIOD="retention_period",e.SHARED_CATEGORIES="shared_categories",e.SPECIAL_CATEGORY_LEGAL_BASIS="special_category_legal_basis",e.SYSTEM_DEPENDENCIES="system_dependencies",e.THIRD_COUNTRY_SAFEGUARDS="third_country_safeguards",e.THIRD_PARTIES="third_parties",e.USES_COOKIES="uses_cookies",e.USES_NON_COOKIE_ACCESS="uses_non_cookie_access",e.USES_PROFILING="uses_profiling"}(y||(y={}));var P=function(e){var t=[];switch(e){case R.fI.SYSTEM_DATA_USE:t=[y.SYSTEM_NAME];break;case R.fI.DATA_USE_SYSTEM:t=[y.DATA_USE];break;case R.fI.DATA_CATEGORY_SYSTEM:t=[y.DATA_CATEGORY];break;default:t=[y.SYSTEM_NAME]}return t},w=function(e){var t=[];return R.fI.SYSTEM_DATA_USE===e&&(t=[y.SYSTEM_NAME,y.DATA_USE,y.DATA_CATEGORY,y.DATA_SUBJECT]),R.fI.DATA_USE_SYSTEM===e&&(t=[y.DATA_USE,y.SYSTEM_NAME,y.DATA_CATEGORY,y.DATA_SUBJECT]),R.fI.DATA_CATEGORY_SYSTEM===e&&(t=[y.DATA_CATEGORY,y.SYSTEM_NAME,y.DATA_USE,y.DATA_SUBJECT]),t},k=function(e){var t=[];return R.fI.SYSTEM_DATA_USE===e&&(t=[y.SYSTEM_NAME,y.DATA_USE]),R.fI.DATA_USE_SYSTEM===e&&(t=[y.DATA_USE,y.SYSTEM_NAME]),R.fI.DATA_CATEGORY_SYSTEM===e&&(t=[y.DATA_CATEGORY,y.SYSTEM_NAME]),t},N=function(){var e=(0,j.x8)().isLoading,t=(0,p.oi)(),n=t.PAGE_SIZES,a=t.pageSize,i=t.setPageSize,x=t.onPreviousPageClick,m=t.isPreviousPageDisabled,C=t.onNextPageClick,N=t.isNextPageDisabled,G=t.startRange,L=t.endRange,M=t.pageIndex,U=t.setTotalPages,Y=t.resetPageIndexToDefault,F=function(){var e=(0,s.qY)(),t=e.isOpen,n=e.onClose,a=e.onOpen;(0,E.fd)();var i=(0,h.C)(E.U3);(0,S.te)();var o=(0,h.C)(S.ZL);(0,T.MO)();var c=(0,h.C)(T.qb),u=(0,r.useState)([]),l=u[0],d=u[1],f=(0,r.useState)([]),p=f[0],_=f[1],g=(0,r.useState)([]),x=g[0],O=g[1];(0,r.useEffect)((function(){0===l.length&&d(i.map((function(e){return{value:e.fides_key,displayText:e.name||e.fides_key,isChecked:!1}})))}),[i,l,d]),(0,r.useEffect)((function(){0===p.length&&_(c.map((function(e){return{value:e.fides_key,displayText:e.name||e.fides_key,isChecked:!1}})))}),[c,p,_]),(0,r.useEffect)((function(){0===x.length&&O(o.map((function(e){return{value:e.fides_key,displayText:e.name||e.fides_key,isChecked:!1}})))}),[o,x,O]);var m=function(e,t,n,r){r(n.map((function(n){return n.value===e?A(A({},n),{},{isChecked:t}):n})))};return{isOpen:t,onClose:n,onOpen:a,resetFilters:function(){d((function(e){return e.map((function(e){return A(A({},e),{},{isChecked:!1})}))})),_((function(e){return e.map((function(e){return A(A({},e),{},{isChecked:!1})}))})),O((function(e){return e.map((function(e){return A(A({},e),{},{isChecked:!1})}))}))},dataUseOptions:l,onDataUseChange:function(e,t){m(e,t,l,d)},dataCategoriesOptions:p,onDataCategoriesChange:function(e,t){m(e,t,p,_)},dataSubjectOptions:x,onDataSubjectChange:function(e,t){m(e,t,x,O)}}}(),V=F.isOpen,z=F.onClose,H=F.onOpen,B=F.resetFilters,W=F.dataUseOptions,X=F.onDataUseChange,K=F.dataCategoriesOptions,Z=F.onDataCategoriesChange,q=F.dataSubjectOptions,$=F.onDataSubjectChange,J=(0,r.useMemo)((function(){return(0,_.XK)(W,"data_uses")}),[W]),Q=(0,r.useMemo)((function(){return(0,_.XK)(K,"data_categories")}),[K]),ee=(0,r.useMemo)((function(){return(0,_.XK)(q,"data_subjects")}),[q]),te=(0,r.useState)(!1),ne=te[0],re=te[1],ae=(0,r.useState)(""),ie=ae[0],se=ae[1],oe=(0,r.useState)(R.fI.SYSTEM_DATA_USE),ce=oe[0],ue=oe[1],le=function(e){ue(e),re(!0),Y()},de=(0,g.tH)({pageIndex:M,pageSize:a,groupBy:ce,search:ie,dataUses:J,dataSubjects:ee,dataCategories:Q}),fe=de.data,pe=de.isLoading,_e=de.isFetching,ge=(0,r.useMemo)((function(){var e=fe||I;return ne&&re(!1),b(b({},e),{},{grouping:P(ce),columnOrder:w(ce)})}),[fe]),xe=ge.items,he=ge.total,Se=ge.pages,Ee=ge.grouping,Te=ge.columnOrder;(0,r.useEffect)((function(){U(Se)}),[Se,U]);var Oe="270px",me=(0,r.useMemo)((function(){return[D.accessor((function(e){return e.system_name}),{enableGrouping:!0,id:y.SYSTEM_NAME,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"System"},e))},meta:{width:Oe,minWidth:Oe,displayText:"System"}}),D.accessor((function(e){return e.data_uses}),{id:y.DATA_USE,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"data uses",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data use"},e))},meta:{width:Oe,minWidth:Oe,displayText:"Data use"}}),D.accessor((function(e){return e.data_categories}),{id:y.DATA_CATEGORY,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"data categories",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data categories"},e))},meta:{width:Oe,displayText:"Data categories"}}),D.accessor((function(e){return e.data_subjects}),{id:y.DATA_SUBJECT,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"data subjects",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data subject"},e))},meta:{width:Oe,displayText:"Data subject"}}),D.accessor((function(e){return e.legal_name}),{id:y.LEGAL_NAME,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legal name"},e))},meta:{width:Oe,displayText:"Legal name"}}),D.accessor((function(e){return e.dpo}),{id:y.DPO,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data privacy officer"},e))},meta:{width:Oe,displayText:"Data privacy officer"}}),D.accessor((function(e){return e.legal_basis_for_processing}),{id:y.LEGAL_BASIS_FOR_PROCESSING,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legal basis for processing"},e))},meta:{width:Oe,displayText:"Legal basis for processing"}}),D.accessor((function(e){return e.administrating_department}),{id:y.ADMINISTRATING_DEPARTMENT,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Administrating department"},e))},meta:{width:Oe,displayText:"Administrating department"}}),D.accessor((function(e){return e.cookie_max_age_seconds}),{id:y.COOKIE_MAX_AGE_SECONDS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Cookie max age seconds"},e))},meta:{width:Oe,displayText:"Cookie max age seconds"}}),D.accessor((function(e){return e.privacy_policy}),{id:y.PRIVACY_POLICY,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Privacy policy"},e))},meta:{width:Oe,displayText:"Privacy policy"}}),D.accessor((function(e){return e.legal_address}),{id:y.LEGAL_ADDRESS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legal address"},e))},meta:{width:Oe,displayText:"Legal address"}}),D.accessor((function(e){return e.cookie_refresh}),{id:y.COOKIE_REFRESH,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,{value:"Cookie refresh",table:e.table,header:e.header,column:e.column})},meta:{width:Oe,displayText:"Cookie refresh"}}),D.accessor((function(e){return e.data_security_practices}),{id:y.DATA_SECURITY_PRACTICES,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data security practices"},e))},meta:{width:Oe,displayText:"Data security practices"}}),D.accessor((function(e){return e.data_shared_with_third_parties}),{id:y.DATA_SHARED_WITH_THIRD_PARTIES,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data shared with third parties"},e))},meta:{width:Oe,displayText:"Data shared with third parties"}}),D.accessor((function(e){return e.data_stewards}),{id:y.DATA_STEWARDS,cell:function(e){return(0,O.jsx)(p.WP,{expand:!1,suffix:"data stewards",value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Data stewards"},e))},meta:{width:Oe,displayText:"Data stewards"}}),D.accessor((function(e){return e.declaration_name}),{id:y.DECLARATION_NAME,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Declaration name"},e))},meta:{width:Oe,displayText:"Declaration name"}}),D.accessor((function(e){return e.does_international_transfers}),{id:y.DOES_INTERNATIONAL_TRANSFERS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Does internation transfers"},e))},meta:{width:Oe,displayText:"Does internation transfers"}}),D.accessor((function(e){return e.dpa_location}),{id:y.DPA_LOCATION,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"DPA Location"},e))},meta:{width:Oe,displayText:"DPA Location"}}),D.accessor((function(e){return e.egress}),{id:y.EGRESS,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"egress",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Egress"},e))},meta:{width:Oe,displayText:"Egress"}}),D.accessor((function(e){return e.exempt_from_privacy_regulations}),{id:y.EXEMPT_FROM_PRIVACY_REGULATIONS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Exempt from privacy regulations"},e))},meta:{width:Oe,displayText:"Exempt from privacy regulations"}}),D.accessor((function(e){return e.features}),{id:y.FEATURES,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"features",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Features"},e))},meta:{width:Oe,displayText:"Features"}}),D.accessor((function(e){return e.fides_key}),{id:y.FIDES_KEY,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Fides key"},e))},meta:{width:Oe,displayText:"Fides key"}}),D.accessor((function(e){return e.flexible_legal_basis_for_processing}),{id:y.FLEXIBLE_LEGAL_BASIS_FOR_PROCESSING,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Flexible legal basis for processing"},e))},meta:{width:Oe,displayText:"Flexible legal basis for processing"}}),D.accessor((function(e){return e.impact_assessment_location}),{id:y.IMPACT_ASSESSMENT_LOCATION,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Impact assessment location"},e))},meta:{width:Oe,displayText:"Impact assessment location"}}),D.accessor((function(e){return e.ingress}),{id:y.INGRESS,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"ingress",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Ingress"},e))},meta:{width:Oe,displayText:"Ingress"}}),D.accessor((function(e){return e.joint_controller_info}),{id:y.JOINT_CONTROLLER_INFO,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Joint controller info"},e))},meta:{width:Oe,displayText:"Joint controller info"}}),D.accessor((function(e){return e.legal_basis_for_profiling}),{id:y.LEGAL_BASIS_FOR_PROFILING,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"profiles",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legal basis for profiling"},e))},meta:{width:Oe,displayText:"Legal basis for profiling"}}),D.accessor((function(e){return e.legal_basis_for_transfers}),{id:y.LEGAL_BASIS_FOR_TRANSFERS,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"transfers",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legal basis for transfers"},e))},meta:{width:Oe,displayText:"Legal basis for transfers"}}),D.accessor((function(e){return e.legitimate_interest_disclosure_url}),{id:y.LEGITIMATE_INTEREST_DISCLOSURE_URL,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Legitimate interest disclosure url"},e))},meta:{width:Oe,displayText:"Legitimate interest disclosure url"}}),D.accessor((function(e){return e.link_to_processor_contract}),{id:y.LINK_TO_PROCESSOR_CONTRACT,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Link to processor contract"},e))},meta:{width:Oe,displayText:"Link to processor contract"}}),D.accessor((function(e){return e.processes_personal_data}),{id:y.PROCESSES_PERSONAL_DATA,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Processes personal data"},e))},meta:{width:Oe,displayText:"Processes personal data"}}),D.accessor((function(e){return e.reason_for_exemption}),{id:y.REASON_FOR_EXEMPTION,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Reason for excemption"},e))},meta:{width:Oe,displayText:"Reason for excemption"}}),D.accessor((function(e){return e.requires_data_protection_assessments}),{id:y.REQUIRES_DATA_PROTECTION_ASSESSMENTS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Requires data protection assessments"},e))},meta:{width:Oe,displayText:"Requires data protection assessments"}}),D.accessor((function(e){return e.responsibility}),{id:y.RESPONSIBILITY,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"responsibilitlies",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Responsibility"},e))},meta:{width:Oe,displayText:"Responsibility"}}),D.accessor((function(e){return e.retention_period}),{id:y.RETENTION_PERIOD,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Retention period"},e))},meta:{width:Oe,displayText:"Retention period"}}),D.accessor((function(e){return e.shared_categories}),{id:y.SHARED_CATEGORIES,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"shared categories",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Shared categories"},e))},meta:{width:Oe,displayText:"Shared categories"}}),D.accessor((function(e){return e.special_category_legal_basis}),{id:y.SPECIAL_CATEGORY_LEGAL_BASIS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Special category legal basis"},e))},meta:{width:Oe,displayText:"Special category legal basis"}}),D.accessor((function(e){return e.system_dependencies}),{id:y.SYSTEM_DEPENDENCIES,cell:function(e){return(0,O.jsx)(p.WP,{suffix:"dependencies",expand:!1,value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"System dependencies"},e))},meta:{width:Oe,displayText:"System dependencies"}}),D.accessor((function(e){return e.third_country_safeguards}),{id:y.THIRD_COUNTRY_SAFEGUARDS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Third country safeguards"},e))},meta:{width:Oe,displayText:"Third country safeguards"}}),D.accessor((function(e){return e.third_parties}),{id:y.THIRD_PARTIES,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Third parties"},e))},meta:{width:Oe,displayText:"Third parties"}}),D.accessor((function(e){return e.uses_cookies}),{id:y.USES_COOKIES,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Uses cookies"},e))},meta:{width:Oe,displayText:"Uses cookies"}}),D.accessor((function(e){return e.uses_non_cookie_access}),{id:y.USES_NON_COOKIE_ACCESS,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Uses non cookie access"},e))},meta:{width:Oe,displayText:"Uses non cookie access"}}),D.accessor((function(e){return e.uses_profiling}),{id:y.USES_PROFILING,cell:function(e){return(0,O.jsx)(p.G3,{value:e.getValue()})},header:function(e){return(0,O.jsx)(p.Rr,b({value:"Uses profiling"},e))},meta:{width:Oe,displayText:"Uses profiling"}})]}),[]),Ae=(0,s.qY)(),ve=Ae.isOpen,je=Ae.onOpen,Re=Ae.onClose,Ce=(0,f.b7)({getCoreRowModel:(0,d.sC)(),getGroupedRowModel:(0,d.qe)(),getExpandedRowModel:(0,d.rV)(),columns:me,manualPagination:!0,data:xe,initialState:{columnOrder:Te},state:{expanded:!0,grouping:Ee}}),be=function(){switch(ce){case R.fI.SYSTEM_DATA_USE:return"system";case R.fI.DATA_USE_SYSTEM:return"data use";case R.fI.DATA_CATEGORY_SYSTEM:return"data category";default:return"system"}};return pe||e?(0,O.jsx)(p.I4,{rowHeight:36,numRows:15}):(0,O.jsxs)(o.kC,{flex:1,direction:"column",overflow:"auto",children:[(0,O.jsx)(o.X6,{mb:8,fontSize:"2xl",fontWeight:"semibold",children:"Data Map Report"}),(0,O.jsx)(v,{isOpen:V,onClose:z,resetFilters:B,dataUseOptions:W,onDataUseChange:X,dataCategoriesOptions:K,onDataCategoriesChange:Z,dataSubjectOptions:q,onDataSubjectChange:$}),(0,O.jsx)(p.F1,{isOpen:ve,onClose:Re,headerText:"Data Map Settings",prefixColumns:k(ce),tableInstance:Ce}),(0,O.jsxs)(p.Q$,{children:[(0,O.jsx)(p.HO,{globalFilter:ie,setGlobalFilter:function(e){Y(),se(e)},placeholder:"System name, Fides key, or ID"}),(0,O.jsxs)(o.kC,{alignItems:"center",children:[(0,O.jsxs)(c.v2,{children:[(0,O.jsxs)(c.j2,{as:u.zx,size:"xs",variant:"outline",mr:2,rightIcon:(0,O.jsx)(l.v4,{}),spinnerPlacement:"end",isLoading:ne,loadingText:"Group by ".concat(be()),children:["Group by ",be()]}),(0,O.jsxs)(c.qy,{zIndex:11,children:[(0,O.jsx)(c.ii,{onClick:function(){le(R.fI.SYSTEM_DATA_USE)},isChecked:R.fI.SYSTEM_DATA_USE===ce,value:R.fI.SYSTEM_DATA_USE,children:"System"}),(0,O.jsx)(c.ii,{onClick:function(){le(R.fI.DATA_USE_SYSTEM)},isChecked:R.fI.DATA_USE_SYSTEM===ce,value:R.fI.DATA_USE_SYSTEM,children:"Data use"})]})]}),(0,O.jsx)(u.zx,{"data-testid":"filter-multiple-systems-btn",size:"xs",variant:"outline",onClick:je,mr:2,children:"Edit columns"}),(0,O.jsx)(u.zx,{"data-testid":"filter-multiple-systems-btn",size:"xs",variant:"outline",onClick:H,children:"Filter"})]})]}),(0,O.jsx)(p.ZK,{tableInstance:Ce}),(0,O.jsx)(p.s8,{totalRows:he,pageSizes:n,setPageSize:i,onPreviousPageClick:x,isPreviousPageDisabled:m||_e,onNextPageClick:C,isNextPageDisabled:N||_e,startRange:G,endRange:L})]})},G=function(){return(0,O.jsx)(a.Z,{title:"Datamap Report",mainProps:{padding:"40px",paddingRight:"48px"},children:(0,O.jsx)(N,{})})}},86548:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/reporting/datamap",function(){return n(44409)}])},30808:function(e,t,n){"use strict";function r(e,t){if(null==e)return{};var n,r,a={},i=Object.keys(e);for(r=0;r<i.length;r++)n=i[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}n.d(t,{Z:function(){return r}})},6983:function(e,t,n){"use strict";function r(e,t){return r=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},r(e,t)}n.d(t,{Z:function(){return r}})}},function(e){e.O(0,[7751,530,3452,3216,7453,5803,9774,2888,179],(function(){return t=86548,e(e.s=t);var t}));var t=e.O();_N_E=t}]);