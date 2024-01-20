(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[4917],{39986:function(e,n,t){"use strict";t.r(n),t.d(n,{default:function(){return R}});var r=t(34896),i=t(83125),o=t(79894),s=t.n(o),a=t(6848),c=t(51471),u=t(60709),l=t(17165),d=t(90849),f=t(55732),h=t(97865),p=t(34707),m=t.n(p),g=t(70409),x=t(21084),v=t(5008),j=t(29549),y=t(98784),O=t.n(y),w=t(86677),b=t(27378),C=t(78624),_=t(2458),P=t(53333),S=t(44845),k=t(24753),E=t(27808),Z=t(33167),L=t(93246),N=t(24246);function z(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function D(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?z(Object(t),!0).forEach((function(n){(0,d.Z)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):z(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var M=function(e){var n,t=e.data,i=(0,g.pm)(),o=(0,x.qY)(),s=(0,b.useState)(null!==(n=t.regulations)&&void 0!==n?n:[]),a=s[0],c=s[1],d=(0,b.useState)(""),p=d[0],y=d[1],z=(0,l.WA)(),M=(0,h.Z)(z,2),R=M[0],q=M[1].isLoading,F=(0,b.useMemo)((function(){var e,n,r=null!==(e=null===(n=t.regulations)||void 0===n?void 0:n.filter((function(e){return function(e,n){var t;return null===(t=e.name)||void 0===t?void 0:t.toLocaleLowerCase().includes(n.toLocaleLowerCase())}(e,p)})))&&void 0!==e?e:[];return(0,L.F7)(r)}),[t.regulations,p]),T=!O().isEqual(a,t.regulations),W=(0,w.useRouter)(),X=function(){W.push(u.r5).then((function(){i.closeAll()}))},Y=function(){var e=(0,f.Z)(m().mark((function e(){var n;return m().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,R({regulations:a.map((function(e){return{id:e.id,selected:e.selected}})),locations:[]});case 2:n=e.sent,(0,Z.isErrorResult)(n)?i((0,k.Vo)((0,C.e$)(n.error))):i((0,k.t5)((0,N.jsxs)(r.xv,{children:["Fides has automatically associated the relevant locations with your regulation choices.",(0,N.jsx)(E.Z,{onClick:X,children:"View locations here."})]})));case 4:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return(0,N.jsxs)(r.gC,{alignItems:"start",spacing:4,children:[(0,N.jsx)(r.xu,{maxWidth:"510px",width:"100%",children:(0,N.jsx)(S.Z,{onChange:y,placeholder:"Search",search:p,onClear:function(){return y("")},"data-testid":"search-bar"})}),(0,N.jsx)(r.MI,{columns:{base:1,md:2,xl:3},spacing:6,width:"100%",children:Object.entries(F).map((function(e){var n=(0,h.Z)(e,2),t=n[0],r=n[1],i=a.filter((function(e){return r.find((function(n){return n.id===e.id}))&&e.selected})).map((function(e){return e.id}));return(0,N.jsx)(P.Z,{title:t,items:r,selected:i,onChange:function(e){!function(e){var n=a.map((function(n){var t=e.find((function(e){return e.id===n.id}));return null!==t&&void 0!==t?t:n}));c(n)}(r.map((function(n){return e.includes(n.id)?D(D({},n),{},{selected:!0}):D(D({},n),{},{selected:!1})})))},numSelected:i.length,indeterminate:[]},t)}))}),(0,N.jsx)(_.Z,{isOpen:o.isOpen,onClose:o.onClose,onConfirm:function(){Y(),o.onClose()},title:"Location updates",message:"Modifications in your regulation settings may also affect your location settings to simplify management. You can override any Fides-initiated changes directly in the location settings.",isCentered:!0,icon:(0,N.jsx)(v.aN,{color:"orange"})}),T?(0,N.jsx)(j.zx,{colorScheme:"primary",size:"sm",onClick:o.onOpen,isLoading:q,"data-testid":"save-btn",children:"Save"}):null]})},R=function(){var e=(0,l.QM)().isLoading,n=(0,a.C)(l.P8);return(0,N.jsx)(c.Z,{title:"Regulations",children:(0,N.jsxs)(r.xu,{"data-testid":"location-management",children:[(0,N.jsx)(r.X6,{marginBottom:2,fontSize:"2xl",children:"Regulations"}),(0,N.jsxs)(r.xu,{children:[(0,N.jsxs)(r.xv,{marginBottom:4,fontSize:"sm",maxWidth:"600px",children:["Select the regulations that apply to your organizations compliance requirements. The selections you make here will automatically update your location selections."," ",(0,N.jsx)(r.xv,{color:"complimentary.500",children:(0,N.jsx)(s(),{href:u.r5,passHref:!0,children:"You can view your location settings here."})})]}),(0,N.jsx)(r.xu,{children:e?(0,N.jsx)(i.$,{}):(0,N.jsx)(M,{data:n})})]})]})})}},180:function(e,n,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/management/regulations",function(){return t(39986)}])}},function(e){e.O(0,[8033,7751,530,4400,9774,2888,179],(function(){return n=180,e(e.s=n);var n}));var n=e.O();_N_E=n}]);