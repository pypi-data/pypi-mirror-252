(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4242],{44845:function(e,t,n){"use strict";var s=n(90849),r=n(90089),i=n(32751),o=n(5008),a=n(29549),c=n(24246),l=["search","onChange","withIcon","onClear","placeholder"];function d(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);t&&(s=s.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,s)}return n}function u(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?d(Object(n),!0).forEach((function(t){(0,s.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):d(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}t.Z=function(e){var t=e.search,n=e.onChange,s=e.withIcon,d=e.onClear,f=e.placeholder,h=(0,r.Z)(e,l);return(0,c.jsxs)(i.BZ,{size:"sm",minWidth:"308px",children:[s?(0,c.jsx)(i.Z8,{pointerEvents:"none",children:(0,c.jsx)(o.PT,{color:"gray.300",w:"17px",h:"17px"})}):null,(0,c.jsx)(i.II,u({autoComplete:"off",type:"search",minWidth:200,size:"sm",borderRadius:"md",value:t,name:"search",onChange:function(e){return n(e.target.value)},placeholder:f||""},h)),d?(0,c.jsx)(i.xH,{children:(0,c.jsx)(a.zx,{borderLeftRadius:0,height:"95%",right:"14px",flexShrink:0,fontWeight:"light",size:"sm",onClick:d,children:"Clear"})}):null]})}},88486:function(e,t,n){"use strict";n.d(t,{Gt:function(){return f},eB:function(){return h},oI:function(){return u}});var s=n(34090),r=n(27378),i=n(6848),o=n(30691),a=n(2458),c=n(24246),l=(0,r.createRef)(),d=(0,r.createRef)(),u=function(){var e=(0,i.T)(),t=(0,i.C)(o.DB),n=(0,r.useCallback)((function(){d.current=void 0,l.current=void 0}),[]),s=(0,r.useCallback)((function(){e((0,o.Mr)()),d.current&&(d.current(!0),n())}),[e,n]),a=(0,r.useCallback)((function(){e((0,o.Mr)()),d.current&&(d.current(!1),n())}),[e,n]);return{attemptAction:(0,r.useCallback)((function(){return t?(e((0,o.h7)()),l.current||(l.current=new Promise((function(e){d.current=e}))),l.current):Promise.resolve(!0)}),[t,e]),onConfirm:s,onClose:a}},f=function(e){var t=e.id,n=e.name,a=(0,s.u6)().dirty,c=(0,i.T)();return(0,r.useEffect)((function(){return c((0,o.Zu)({id:t,name:n})),function(){c((0,o.dz)({id:t}))}}),[c,t,n]),(0,r.useEffect)((function(){c((0,o.$p)({id:t,isDirty:a}))}),[a,c,t]),null},h=function(){var e=u(),t=e.onConfirm,n=e.onClose,s=(0,i.C)(o.uv);return(0,c.jsx)(a.Z,{isOpen:s,onClose:n,onConfirm:t,isCentered:!0,title:"Unsaved Changes",message:"You have unsaved changes"})}},89348:function(e,t,n){"use strict";n.d(t,{q:function(){return H}});var s=n(62332),r=n(27378),i=n(90849),o=n(55732),a=n(97865),c=n(34707),l=n.n(c),d=n(70409),u=n(21084),f=n(34896),h=n(30794),m=n(29549),x=n(78624),y=n(88486),g=n(55232),p=n(40240),j=n(96156),v=n(34090),b=n(24246),C=function(e){var t=e.systems,n=e.dataFlows,s=e.onDataFlowSystemChange,r=(0,v.u6)().setFieldValue,i=n.map((function(e){return e.fides_key}));return(0,b.jsxs)(p.iA,{size:"sm","data-testid":"assign-systems-delete-table",children:[(0,b.jsx)(p.hr,{children:(0,b.jsxs)(p.Tr,{children:[(0,b.jsx)(p.Th,{children:"System"}),(0,b.jsx)(p.Th,{})]})}),(0,b.jsx)(p.p3,{children:t.filter((function(e){return i.includes(e.fides_key)})).map((function(e){return(0,b.jsxs)(p.Tr,{_hover:{bg:"gray.50"},"data-testid":"row-".concat(e.fides_key),children:[(0,b.jsx)(p.Td,{children:(0,b.jsx)(f.xv,{fontSize:"xs",lineHeight:4,fontWeight:"medium",children:e.name})}),(0,b.jsx)(p.Td,{textAlign:"end",children:(0,b.jsx)(m.hU,{background:"gray.50","aria-label":"Unassign data flow from system",icon:(0,b.jsx)(j.l,{}),variant:"outline",size:"sm",onClick:function(){return function(e){var t=n.filter((function(t){return t.fides_key!==e.fides_key}));r("dataFlowSystems",t),s(t)}(e)},"data-testid":"unassign-btn"})})]},e.fides_key)}))})]})},w=n(60530),k=n(92975),S=n(62709),O=n(44845),_=n(13861),z=n(73679),D=function(e){var t=e.allSystems,n=e.dataFlowSystems,s=e.onChange,r=e.flowType,i=(0,v.u6)().setFieldValue,o=function(e){if(!!n.find((function(t){return t.fides_key===e.fides_key}))){var t=n.filter((function(t){return t.fides_key!==e.fides_key}));i("dataFlowSystems",t),s(t)}else{var r=[].concat((0,z.Z)(n),[{fides_key:e.fides_key,type:"system"}]);i("dataFlowSystems",r),s(r)}};return(0,b.jsx)(f.xu,{overflowY:"auto",maxHeight:"300px",children:(0,b.jsxs)(p.iA,{size:"sm","data-testid":"assign-systems-table",maxHeight:"50vh",overflowY:"scroll",children:[(0,b.jsx)(p.hr,{position:"sticky",top:0,background:"white",zIndex:1,children:(0,b.jsxs)(p.Tr,{children:[(0,b.jsx)(p.Th,{children:"System"}),(0,b.jsxs)(p.Th,{textAlign:"right",children:["Set as ",r]})]})}),(0,b.jsx)(p.p3,{children:t.map((function(e){var t=!!n.find((function(t){return t.fides_key===e.fides_key}));return(0,b.jsxs)(p.Tr,{_hover:{bg:"gray.50"},"data-testid":"row-".concat(e.fides_key),children:[(0,b.jsx)(p.Td,{children:(0,b.jsx)(f.xv,{fontSize:"xs",lineHeight:4,fontWeight:"medium",children:e.name})}),(0,b.jsx)(p.Td,{textAlign:"right",children:(0,b.jsx)(S.r,{isChecked:t,onChange:function(){return o(e)},"data-testid":"assign-switch"})})]},e.fides_key)}))})]})})},F=function(e){var t=e.currentSystem,n=e.systems,s=e.isOpen,i=e.onClose,a=e.dataFlowSystems,c=e.onDataFlowSystemChange,d=e.flowType,u=(0,v.u6)().setFieldValue,h=(0,r.useState)(""),x=h[0],y=h[1],g=(0,r.useState)(a),p=g[0],j=g[1],C=function(){var e=(0,o.Z)(l().mark((function e(){return l().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:c(p),i();case 2:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),z=0===n.length,F=(0,r.useMemo)((function(){return n?n.filter((function(e){return e.fides_key!==t.fides_key})).filter((function(e){return(0,_.R)(e,x)})):[]}),[n,t.fides_key,x]),T=(0,r.useMemo)((function(){var e=new Set(p.map((function(e){return e.fides_key})));return F.every((function(t){return e.has(t.fides_key)}))}),[F,p]);return(0,b.jsxs)(w.u_,{isOpen:s,onClose:i,size:"2xl",isCentered:!0,children:[(0,b.jsx)(w.ZA,{}),(0,b.jsxs)(w.hz,{p:8,"data-testid":"confirmation-modal",children:[(0,b.jsxs)(w.xB,{fontWeight:"medium",display:"flex",justifyContent:"space-between",alignItems:"center",children:[(0,b.jsxs)(f.xv,{fontSize:"2xl",lineHeight:8,fontWeight:"semibold",children:["Configure ",d.toLocaleLowerCase()," systems"]}),(0,b.jsxs)(f.Ct,{bg:"green.500",color:"white",px:1,children:["Assigned to ",p.length," systems"]})]}),(0,b.jsx)(w.fe,{"data-testid":"assign-systems-modal-body",children:z?(0,b.jsx)(f.xv,{children:"No systems found"}):(0,b.jsxs)(f.Kq,{spacing:4,children:[(0,b.jsxs)(f.kC,{justifyContent:"space-between",children:[(0,b.jsx)(f.xv,{fontSize:"sm",flexGrow:1,fontWeight:"medium",children:"Add or remove destination systems from your data map"}),(0,b.jsx)(f.xu,{children:(0,b.jsxs)(k.NI,{display:"flex",alignItems:"center",children:[(0,b.jsx)(k.lX,{fontSize:"sm",htmlFor:"assign-all-systems",mb:"0",children:"Assign all systems"}),(0,b.jsx)(S.r,{size:"sm",id:"assign-all-systems",isChecked:T,onChange:function(e){if(e.target.checked&&n){var t=F.map((function(e){return{fides_key:e.fides_key,type:"system"}}));u("dataFlowSystems",t),j(t)}else j([])},"data-testid":"assign-all-systems-toggle"})]})})]}),(0,b.jsx)(O.Z,{search:x,onChange:y,placeholder:"Search for systems","data-testid":"system-search",withIcon:!0}),(0,b.jsx)(D,{flowType:d,allSystems:F,dataFlowSystems:p,onChange:j})]})}),(0,b.jsx)(w.mz,{justifyContent:"flex-start",children:(0,b.jsxs)(m.hE,{size:"sm",children:[(0,b.jsx)(m.zx,{variant:"outline",mr:2,onClick:i,"data-testid":"cancel-btn",children:"Cancel"}),z?null:(0,b.jsx)(m.zx,{colorScheme:"primary",onClick:C,"data-testid":"confirm-btn",children:"Confirm"})]})})]})]})},T=n(24753),L=n(6848),Z=n(48466),P=n(51860);function I(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);t&&(s=s.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,s)}return n}function E(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?I(Object(n),!0).forEach((function(t){(0,i.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):I(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var W={dataFlowSystems:[]},A=function(e){var t=e.system,n=e.isIngress,i=e.isSystemTab,c=(0,d.pm)(),p=n?"Source":"Destination",j="".concat(p,"s"),w=(0,u.qY)(),k=(0,Z.qQ)(),S=(0,a.Z)(k,1)[0];(0,Z.K3)();var O=(0,L.C)(P.cS),_=(0,r.useMemo)((function(){var e=n?t.ingress:t.egress;e||(e=[]);var s=O?O.map((function(e){return e.fides_key})):[];return e.filter((function(e){return s.includes(e.fides_key)}))}),[n,t,O]),z=(0,r.useState)(_),D=z[0],I=z[1];(0,r.useEffect)((function(){I(_)}),[_]);var A=function(){var e=(0,o.Z)(l().mark((function e(s,r){var i,o,a,d;return l().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return i=s.dataFlowSystems,o=r.resetForm,a=E(E({},t),{},{ingress:n?i:t.ingress,egress:n?t.egress:i}),e.next=5,S(a);case 5:d=e.sent,(0,x.D4)(d)?c((0,T.Vo)("Failed to update data flows")):c((0,T.t5)("".concat(j," updated"))),o({values:{dataFlowSystems:i}});case 8:case"end":return e.stop()}}),e)})));return function(t,n){return e.apply(this,arguments)}}();return(0,b.jsxs)(s.Qd,{children:[(0,b.jsx)(s.KF,{height:"68px",paddingLeft:i?6:2,"data-testid":"data-flow-button-".concat(p),children:(0,b.jsxs)(f.kC,{alignItems:"center",justifyContent:"start",flex:1,textAlign:"left",children:[(0,b.jsx)(f.xv,{fontSize:"sm",lineHeight:5,fontWeight:"semibold",mr:2,children:j}),(0,b.jsx)(h.Vp,{ml:2,backgroundColor:"primary.400",borderRadius:"6px",color:"white",children:D.length}),(0,b.jsx)(f.LZ,{}),(0,b.jsx)(s.XE,{})]})}),(0,b.jsx)(s.Hk,{backgroundColor:"gray.50",padding:6,"data-testid":"data-flow-panel-".concat(p),children:(0,b.jsx)(f.Kq,{borderRadius:"md",backgroundColor:"gray.50","aria-selected":"true",spacing:4,"data-testid":"selected",children:(0,b.jsx)(v.J9,{initialValues:W,onSubmit:A,children:function(e){var n=e.isSubmitting,s=e.dirty,r=e.resetForm;return(0,b.jsxs)(v.l0,{children:[(0,b.jsx)(y.Gt,{id:"".concat(t.fides_key,":").concat(p),name:"".concat(p," Data Flow")}),(0,b.jsx)(m.zx,{colorScheme:"primary",size:"xs",width:"fit-content",onClick:w.onOpen,"data-testid":"assign-systems-btn",rightIcon:(0,b.jsx)(g.A5,{}),marginBottom:4,children:"Configure ".concat(j.toLocaleLowerCase())}),(0,b.jsx)(C,{systems:O,dataFlows:D,onDataFlowSystemChange:I}),(0,b.jsxs)(m.hE,{marginTop:6,children:[(0,b.jsx)(m.zx,{size:"sm",variant:"outline",disabled:!s&&D===_,onClick:function(){I(_),r({values:{dataFlowSystems:_}})},children:"Cancel"}),(0,b.jsx)(m.zx,{size:"sm",colorScheme:"primary",type:"submit",isLoading:n,disabled:!s&&D===_,"data-testid":"save-btn",children:"Save"})]}),w.isOpen?(0,b.jsx)(F,{currentSystem:t,systems:O,isOpen:w.isOpen,onClose:w.onClose,dataFlowSystems:D,onDataFlowSystemChange:I,flowType:p}):null]})}})})})]})},H=function(e){var t=e.system,n=e.isSystemTab;return(0,b.jsxs)(s.UQ,{allowToggle:!0,"data-testid":"data-flow-accordion",children:[(0,b.jsx)(A,{system:t,isIngress:!0,isSystemTab:n}),(0,b.jsx)(A,{system:t,isSystemTab:n})]})}},29073:function(e,t,n){"use strict";var s=n(34896),r=n(73452),i=n(24246);t.Z=function(e){var t=e.title,n=e.description,o=e.button;return(0,i.jsxs)(s.Ug,{backgroundColor:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",py:4,px:6,"data-testid":"empty-state",children:[(0,i.jsx)(r.ii,{alignSelf:"start",color:"blue.400",mt:.5}),(0,i.jsxs)(s.xu,{flexGrow:1,children:[(0,i.jsx)(s.xv,{fontWeight:"bold",fontSize:"sm",mb:1,children:t}),(0,i.jsx)(s.xv,{fontSize:"sm",color:"gray.600",lineHeight:"5",children:n})]}),o]})}},13861:function(e,t,n){"use strict";n.d(t,{R:function(){return F},Z:function(){return T}});var s=n(34896),r=n(27378),i=n(14007),o=n(33571),a=n.n(o),c=n(24246),l=function(e){var t=e.columns,n=e.items,r=e.renderItem,o=(0,i.yo)(n,t);return(0,c.jsx)(s.xu,{children:o.map((function(e,n,i){var o=i.length;return(0,c.jsx)(s.xu,{className:a()["grid-row"],borderBottomWidth:o>1&&n===o-1&&e.length===t?"0.5px":void 0,children:(0,c.jsx)(s.MI,{columns:t,children:e.map((function(e){return(0,c.jsx)(s.xu,{className:a()["grid-item"],children:r(e)},JSON.stringify(e))}))})},JSON.stringify(e))}))})},d=n(44845),u=n(55732),f=n(97865),h=n(34707),m=n.n(h),x=n(21084),y=n(70409),g=n(29470),p=n(29549),j=n(5008),v=n(79894),b=n.n(v),C=n(86677),w=n(6848),k=n(2458),S=n(60709),O=n(78624),_=n(24753),z=n(51860),D=function(e){var t=e.system,n=(0,x.qY)(),r=n.isOpen,i=n.onOpen,o=n.onClose,a=(0,y.pm)(),l=(0,w.T)(),d=(0,C.useRouter)(),h=(0,z.DW)(),v=(0,f.Z)(h,1)[0],D=function(){var e=(0,u.Z)(m().mark((function e(){var n;return m().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,v(t.fides_key);case 2:n=e.sent,(0,O.D4)(n)?a((0,_.Vo)((0,O.e$)(n.error))):a((0,_.t5)("Successfully deleted system")),o();case 5:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}(),F=""===t.name||null==t.name?t.fides_key:t.name;return(0,c.jsxs)(s.xu,{display:"flex","data-testid":"system-".concat(t.fides_key),children:[(0,c.jsx)(b(),{href:"".concat(S.So,"/configure/").concat(t.fides_key),passHref:!0,children:(0,c.jsxs)(s.xu,{flexGrow:1,p:4,"data-testid":"system-box",_hover:{cursor:"pointer"},children:[(0,c.jsx)(s.X6,{as:"h2",fontSize:"16px",mb:2,children:F}),(0,c.jsx)(s.xu,{color:"gray.600",fontSize:"14px",children:(0,c.jsx)(s.xv,{children:t.description})})]})}),(0,c.jsxs)(g.v2,{children:[(0,c.jsx)(g.j2,{as:p.hU,icon:(0,c.jsx)(j.nX,{}),"aria-label":"more actions",variant:"unstyled",size:"sm","data-testid":"more-btn",m:1}),(0,c.jsxs)(g.qy,{children:[(0,c.jsx)(g.sN,{onClick:function(){l((0,z.db)(t)),d.push("".concat(S.So,"/configure/").concat(t.fides_key))},"data-testid":"edit-btn",children:"Edit"}),(0,c.jsx)(g.sN,{onClick:i,"data-testid":"delete-btn",children:"Delete"})]})]}),(0,c.jsx)(k.Z,{isOpen:r,onClose:o,onConfirm:D,title:"Delete ".concat(F),message:(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)(s.xv,{children:["You are about to permanently delete the system"," ",(0,c.jsx)(s.xv,{color:"complimentary.500",as:"span",fontWeight:"bold",children:F}),"."]}),(0,c.jsx)(s.xv,{children:"Are you sure you would like to continue?"})]})})]})},F=function(e,t){var n,s;return(null===(n=e.name)||void 0===n?void 0:n.toLocaleLowerCase().includes(t.toLocaleLowerCase()))||(null===(s=e.description)||void 0===s?void 0:s.toLocaleLowerCase().includes(t.toLocaleLowerCase()))},T=function(e){var t=e.systems,n=(0,r.useState)(""),i=n[0],o=n[1],a=(0,r.useMemo)((function(){return t?t.filter((function(e){return F(e,i)})):[]}),[t,i]);return t&&t.length?(0,c.jsxs)(s.xu,{"data-testid":"system-management",children:[(0,c.jsx)(s.xu,{mb:4,"data-testid":"system-filters",children:(0,c.jsx)(d.Z,{search:i,onChange:o,maxWidth:"30vw",placeholder:"Search system name or description","data-testid":"system-search",withIcon:!0})}),(0,c.jsx)(l,{columns:3,items:a,renderItem:function(e){return(0,c.jsx)(D,{system:e})}})]}):(0,c.jsx)("div",{"data-testid":"empty-state",children:"No systems registered."})}},40397:function(e,t,n){"use strict";n.d(t,{f:function(){return c}});var s=n(6848),r=n(47134),i=n(75846),o=n(45128),a=n(75523),c=function(e){var t=e.includeDatasets,n=e.includeDisabled,c=(0,a.MO)().isLoading,l=(0,r.te)().isLoading,d=(0,i.fd)().isLoading,u=(0,o.LH)({onlyUnlinkedDatasets:!1},{skip:!t}).isLoading,f=(0,s.C)(a.qb),h=(0,s.C)(a.Bd),m=(0,s.C)(r.ZL),x=(0,s.C)(r.H7),y=(0,s.C)(i.U3),g=(0,s.C)(i.jp),p=(0,s.C)(o.Q4);return{allDataCategories:n?f:h,allDataSubjects:n?m:x,allDataUses:n?y:g,allDatasets:t?p:void 0,isLoading:c||l||d||u}}},33167:function(e,t,n){"use strict";n.d(t,{isAPIError:function(){return s.Bw},isErrorResult:function(){return s.D4}});var s=n(60041)},33571:function(e){e.exports={"grid-row":"BorderGrid_grid-row__gzSVf","grid-item":"BorderGrid_grid-item__7gUTW"}}}]);