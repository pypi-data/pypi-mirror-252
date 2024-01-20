(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8538],{51471:function(e,r,t){"use strict";t.d(r,{Z:function(){return b}});var n=t(90849),s=t(34896),i=t(88038),a=t.n(i),o=t(86677),c=(t(27378),t(90768)),u=t(51365),l=t(29549),d=t(60709),f=t(24246),p=function(){var e=(0,o.useRouter)();return(0,f.jsx)(s.xu,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,f.jsxs)(s.xu,{children:[(0,f.jsxs)(s.Kq,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,f.jsx)(s.xv,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,f.jsx)(l.zx,{size:"sm",variant:"outline",onClick:function(){e.push(d.fz)},children:"Configure"})]}),(0,f.jsxs)(s.xv,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})};function h(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function x(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?h(Object(t),!0).forEach((function(r){(0,n.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):h(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}var b=function(e){var r=e.children,t=e.title,n=e.mainProps,i=(0,c.hz)(),l=(0,o.useRouter)(),d="/privacy-requests"===l.pathname||"/datastore-connection"===l.pathname,h=!(i.flags.privacyRequestsConfiguration&&d),b=(0,u.JE)(void 0,{skip:h}).data,j=(0,u.PW)(void 0,{skip:h}).data,m=i.flags.privacyRequestsConfiguration&&(!b||!j)&&d;return(0,f.jsxs)(s.kC,{"data-testid":t,direction:"column",height:"calc(100vh - 48px)",children:[(0,f.jsxs)(a(),{children:[(0,f.jsxs)("title",{children:["Fides Admin UI - ",t]}),(0,f.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,f.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,f.jsxs)(s.kC,x(x({as:"main",direction:"column",py:6,px:10,flex:1,minWidth:0,overflow:"auto"},n),{},{children:[m?(0,f.jsx)(p,{}):null,r]}))]})}},9408:function(e,r,t){"use strict";t.d(r,{HK:function(){return i},VY:function(){return n.V}});var n=t(36653),s=t(78624),i=function(){var e=(0,n.V)().errorAlert;return{handleError:function(r){var t="An unexpected error occurred. Please try again.";(0,s.Ot)(r)?t=r.data.detail:(0,s.tB)(r)&&(t=r.data.detail[0].msg),e(t)}}};t(27378)},36653:function(e,r,t){"use strict";t.d(r,{V:function(){return d}});var n=t(90849),s=t(70409),i=t(23286),a=t(34896),o=t(93235),c=t(24246);function u(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function l(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?u(Object(t),!0).forEach((function(r){(0,n.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):u(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}var d=function(){var e=(0,s.pm)();return{errorAlert:function(r,t,n){var s=l(l({},n),{},{position:(null===n||void 0===n?void 0:n.position)||"top",render:function(e){var n=e.onClose;return(0,c.jsxs)(i.bZ,{alignItems:"normal",status:"error",children:[(0,c.jsx)(i.zM,{}),(0,c.jsxs)(a.xu,{children:[t&&(0,c.jsx)(i.Cd,{children:t}),(0,c.jsx)(i.X,{children:r})]}),(0,c.jsx)(o.P,{onClick:n,position:"relative",right:0,size:"sm",top:-1})]})}});null!==n&&void 0!==n&&n.id&&e.isActive(n.id)?e.update(n.id,s):e(s)},successAlert:function(r,t,n){var s=l(l({},n),{},{position:(null===n||void 0===n?void 0:n.position)||"top",render:function(e){var n=e.onClose;return(0,c.jsxs)(i.bZ,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,c.jsx)(i.zM,{}),(0,c.jsxs)(a.xu,{children:[t&&(0,c.jsx)(i.Cd,{children:t}),(0,c.jsx)(i.X,{children:r})]}),(0,c.jsx)(o.P,{onClick:n,position:"relative",right:0,size:"sm",top:-1})]})}});null!==n&&void 0!==n&&n.id&&e.isActive(n.id)?e.update(n.id,s):e(s)}}}},2458:function(e,r,t){"use strict";var n=t(90849),s=t(60530),i=t(34896),a=t(29549),o=t(24246);function c(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function u(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?c(Object(t),!0).forEach((function(r){(0,n.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):c(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}r.Z=function(e){var r=e.isOpen,t=e.onClose,n=e.onConfirm,c=e.onCancel,l=e.title,d=e.message,f=e.cancelButtonText,p=e.cancelButtonThemingProps,h=e.continueButtonText,x=e.continueButtonThemingProps,b=e.isLoading,j=e.returnFocusOnClose,m=e.isCentered,y=e.testId,g=void 0===y?"confirmation-modal":y,v=e.icon;return(0,o.jsxs)(s.u_,{isOpen:r,onClose:t,size:"lg",returnFocusOnClose:null===j||void 0===j||j,isCentered:m,children:[(0,o.jsx)(s.ZA,{}),(0,o.jsxs)(s.hz,{textAlign:"center",p:6,"data-testid":g,children:[v?(0,o.jsx)(i.M5,{mb:2,children:v}):null,l?(0,o.jsx)(s.xB,{fontWeight:"medium",pb:0,children:l}):null,d?(0,o.jsx)(s.fe,{children:d}):null,(0,o.jsx)(s.mz,{children:(0,o.jsxs)(i.MI,{columns:2,width:"100%",children:[(0,o.jsx)(a.zx,u(u({variant:"outline",mr:3,onClick:function(){c&&c(),t()},"data-testid":"cancel-btn",isDisabled:b},p),{},{children:f||"Cancel"})),(0,o.jsx)(a.zx,u(u({colorScheme:"primary",onClick:n,"data-testid":"continue-btn",isLoading:b},x),{},{children:h||"Continue"}))]})})]})]})}},56069:function(e,r,t){"use strict";var n=t(90849),s=t(90089),i=t(34896),a=t(29549),o=t(73452),c=t(79894),u=t.n(c),l=t(24246),d=["backPath"];function f(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function p(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?f(Object(t),!0).forEach((function(r){(0,n.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):f(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}r.Z=function(e){var r=e.backPath,t=(0,s.Z)(e,d);return(0,l.jsxs)(i.kC,p(p({alignItems:"center",mt:-4,mb:3},t),{},{children:[(0,l.jsx)(u(),{href:r,passHref:!0,children:(0,l.jsx)(a.hU,{"aria-label":"Back",icon:(0,l.jsx)(o.Rp,{}),mr:2,size:"xs",variant:"outline"})}),(0,l.jsx)(u(),{href:r,passHref:!0,children:(0,l.jsx)(i.xv,{as:"a",fontSize:"sm",fontWeight:"500",children:"Back"})})]}))}},24753:function(e,r,t){"use strict";t.d(r,{MA:function(){return l},Vo:function(){return f},t5:function(){return d}});var n=t(90849),s=t(34896),i=t(24246);function a(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function o(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?a(Object(t),!0).forEach((function(r){(0,n.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}var c=function(e){var r=e.children;return(0,i.jsxs)(s.xv,{"data-testid":"toast-success-msg",children:[(0,i.jsx)("strong",{children:"Success:"})," ",r]})},u=function(e){var r=e.children;return(0,i.jsxs)(s.xv,{"data-testid":"toast-error-msg",children:[(0,i.jsx)("strong",{children:"Error:"})," ",r]})},l={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},d=function(e){var r=(0,i.jsx)(c,{children:e});return o(o({},l),{description:r})},f=function(e){var r=(0,i.jsx)(u,{children:e});return o(o({},l),{description:r,status:"error"})}},40695:function(e,r,t){"use strict";var n=t(21295),s=t(34896),i=t(30794),a=t(5008),o=(t(27378),t(24246));r.Z=function(e){var r=e.isEmptyState,t=e.yamlError;return(0,o.jsx)(n.Rg,{in:!0,children:(0,o.jsxs)(s.xu,{w:"fit-content",bg:"white",p:3,borderRadius:3,children:[(0,o.jsxs)(s.Ug,{children:[(0,o.jsx)(s.X6,{as:"h5",color:"gray.700",size:"xs",children:"YAML"}),(0,o.jsx)(i.Vp,{colorScheme:"red",size:"sm",variant:"solid",children:"Error"})]}),(0,o.jsx)(s.xu,{bg:"red.50",border:"1px solid",borderColor:"red.300",color:"red.300",mt:"16px",borderRadius:"6px",children:(0,o.jsxs)(s.Ug,{alignItems:"flex-start",margin:["14px","17px","14px","17px"],children:[(0,o.jsx)(a.f9,{}),r&&(0,o.jsxs)(s.xu,{children:[(0,o.jsx)(s.X6,{as:"h5",color:"red.500",fontWeight:"semibold",size:"xs",children:"Error message:"}),(0,o.jsx)(s.xv,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:"Yaml system is required"})]}),t&&(0,o.jsxs)(s.xu,{children:[(0,o.jsx)(s.X6,{as:"h5",color:"red.500",fontWeight:"semibold",size:"xs",children:"Error message:"}),(0,o.jsx)(s.xv,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:t.message}),(0,o.jsx)(s.xv,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:t.reason}),(0,o.jsxs)(s.xv,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:["Ln ",(0,o.jsx)("b",{children:t.mark.line}),", Col"," ",(0,o.jsx)("b",{children:t.mark.column}),", Pos"," ",(0,o.jsx)("b",{children:t.mark.position})]})]})]})})]})})}},16473:function(e,r,t){"use strict";t.d(r,{F:function(){return a},M:function(){return i}});var n=t(76649),s=t(65218),i=t.n(s)()((function(){return t.e(7088).then(t.bind(t,57088)).then((function(e){return e.default}))}),{ssr:!1,loadableGenerated:{webpack:function(){return[57088]}}}),a=function(e){return(0,n.Ln)({name:"string"},e)&&"YAMLException"===e.name}},34129:function(e,r,t){"use strict";t.r(r),t.d(r,{default:function(){return F}});var n=t(34896),s=t(29549),i=t(27378),a=t(51471),o=t(56069),c=t(60709),u=t(90849),l=t(55732),d=t(97865),f=t(34707),p=t.n(f),h=t(70409),x=t(34090),b=t(86677),j=t(60245),m=t(68301),y=t(90768),g=t(43139),v=t(78624),O=t(2458),w=t(24753),P=t(41609),C=t(44047),k=t(43978),z=t(66334),S=t(24246);function D(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function E(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?D(Object(t),!0).forEach((function(r){(0,u.Z)(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):D(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}var Z=function(e){return!("system_type"in e)},_={url:"",classify:!1,classifyConfirmed:!1},A=m.Ry().shape({url:m.Z_().required().label("Database URL"),classify:m.O7(),classifyConfirmed:m.O7().when(["url","classify"],{is:function(e,r){return e&&r},then:m.O7().equals([!0])})}),L=function(){var e=(0,z.pR)(),r=(0,d.Z)(e,2),t=r[0],i=r[1].isLoading,a=(0,z.IR)(),o=(0,d.Z)(a,2),c=o[0],u=o[1].isLoading,f=(0,C.Du)(),m=(0,d.Z)(f,2),D=m[0],L=m[1].isLoading,R=i||u||L,M=(0,h.pm)(),V=(0,b.useRouter)(),Y=(0,y.hz)(),T=(0,j.I0)(),B=function(){var e=(0,l.Z)(p().mark((function e(r){var n,s,i;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,t({organization_key:P.Av,generate:{config:{connection_string:r.url},target:k.GC.DB,type:k.j.DATASETS}});case 2:if(!("error"in(s=e.sent))){e.next=5;break}return e.abrupt("return",{error:(0,v.e$)(s.error)});case 5:if((i=(null!==(n=s.data.generate_results)&&void 0!==n?n:[]).filter(Z))&&i.length>0){e.next=8;break}return e.abrupt("return",{error:"Unable to generate a dataset with this connection."});case 8:return e.abrupt("return",{datasets:i});case 9:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}(),F=function(){var e=(0,l.Z)(p().mark((function e(r){var t;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,c(r);case 2:if(!("error"in(t=e.sent))){e.next=5;break}return e.abrupt("return",{error:(0,v.e$)(t.error)});case 5:return e.abrupt("return",{dataset:t.data});case 6:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}(),I=function(){var e=(0,l.Z)(p().mark((function e(r){var t,n,s;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t=r.values,n=r.datasets,e.next=3,D({dataset_schemas:n.map((function(e){var r=e.name;return{fides_key:e.fides_key,name:r}})),schema_config:{organization_key:P.Av,generate:{config:{connection_string:t.url},target:k.GC.DB,type:k.j.DATASETS}}});case 3:if(!("error"in(s=e.sent))){e.next=6;break}return e.abrupt("return",{error:(0,v.e$)(s.error)});case 6:return e.abrupt("return",{classifyInstances:s.data.classify_instances});case 7:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}(),W=function(){var e=(0,l.Z)(p().mark((function e(r){var t,n,s,i,a;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,B(r);case 2:if(!("error"in(n=e.sent))){e.next=6;break}return M((0,w.Vo)(n.error)),e.abrupt("return");case 6:return e.next=8,Promise.all(n.datasets.map((function(e){return F(e)})));case 8:if(s=e.sent,!("error"in(i=null!==(t=s.find((function(e){return"error"in e})))&&void 0!==t?t:s[0]))){e.next=13;break}return M((0,w.Vo)(i.error)),e.abrupt("return");case 13:if(r.classify){e.next=17;break}return M((0,w.t5)("Generated ".concat(i.dataset.name," dataset"))),V.push("/dataset/".concat(i.dataset.fides_key)),e.abrupt("return");case 17:return e.next=19,I({values:r,datasets:n.datasets});case 19:if(!("error"in(a=e.sent))){e.next=23;break}return M((0,w.Vo)(a.error)),e.abrupt("return");case 23:M((0,w.t5)("Generate and classify are now in progress")),T((0,z.Zl)(i.dataset.fides_key)),V.push("/dataset");case 26:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}();return(0,S.jsx)(x.J9,{initialValues:E(E({},_),{},{classify:Y.plus}),validationSchema:A,onSubmit:W,validateOnChange:!1,validateOnBlur:!1,children:function(e){var r=e.isSubmitting,t=e.errors,i=e.values,a=e.submitForm,o=e.resetForm,c=e.setFieldValue;return(0,S.jsxs)(x.l0,{children:[(0,S.jsxs)(n.gC,{spacing:8,align:"left",children:[(0,S.jsx)(n.xv,{size:"sm",color:"gray.700",children:"Connect to a database using the connection URL. You may have received this URL from a colleague or your Ethyca developer support engineer."}),(0,S.jsx)(n.xu,{children:(0,S.jsx)(g.j0,{name:"url",label:"Database URL"})}),Y.plus?(0,S.jsx)(g.w8,{name:"classify",label:"Classify dataset",tooltip:"Use Fides Classify to suggest labels based on your data."}):null,(0,S.jsx)(n.xu,{children:(0,S.jsx)(s.zx,{size:"sm",colorScheme:"primary",type:"submit",isLoading:r||R,isDisabled:r||R,"data-testid":"create-dataset-btn",children:"Generate dataset"})})]}),(0,S.jsx)(O.Z,{title:"Generate and classify this dataset",message:"You have chosen to generate and classify this dataset. This process may take several minutes. In the meantime you can continue using Fides. You will receive a notification when the process is complete.",isOpen:void 0!==t.classifyConfirmed,onClose:function(){o({values:E(E({},i),{},{classifyConfirmed:!1})})},onConfirm:function(){c("classifyConfirmed",!0),setTimeout((function(){a()}),0)}})]})}})},R=t(66527),M=t(9408),V=t(16473),Y=t(40695);function T(e){return"object"===typeof e&&null!=e&&"dataset"in e&&Array.isArray(e.dataset)}var B=function(){var e=(0,z.IR)(),r=(0,d.Z)(e,1)[0],t=(0,i.useState)(!0),a=t[0],o=t[1],c=(0,i.useState)(!1),u=c[0],f=c[1],x=(0,i.useState)(!1),j=x[0],m=x[1],y=(0,i.useRef)(null),g=(0,b.useRouter)(),O=(0,h.pm)(),P=(0,M.VY)().errorAlert,C=(0,i.useState)(void 0),k=C[0],D=C[1],E=function(){var e=(0,l.Z)(p().mark((function e(t){var n,s;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return T(t)?(s=(0,d.Z)(t.dataset,1),n=s[0]):n=t,e.abrupt("return",r(n));case 2:case"end":return e.stop()}}),e)})));return function(r){return e.apply(this,arguments)}}(),Z=function(){var e=(0,l.Z)(p().mark((function e(){var r,t,n;return p().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return f(!0),r=y.current.getValue(),t=R.ZP.load(r,{json:!0}),e.next=5,E(t);case 5:n=e.sent,(0,v.D4)(n)?O((0,w.Vo)((0,v.e$)(n.error))):"data"in n&&(s=n.data,O((0,w.t5)("Successfully loaded new dataset YAML")),(0,z.Zl)(s.fides_key),g.push("/dataset/".concat(s.fides_key))),f(!1);case 8:case"end":return e.stop()}var s}),e)})));return function(){return e.apply(this,arguments)}}();return(0,S.jsxs)(n.kC,{gap:"97px",children:[(0,S.jsxs)(n.xu,{w:"75%",children:[(0,S.jsx)(n.xu,{color:"gray.700",fontSize:"14px",mb:4,children:"Get started creating your first dataset by pasting your dataset yaml below! You may have received this yaml from a colleague or your Ethyca developer support engineer."}),(0,S.jsxs)(n.gC,{align:"stretch",children:[(0,S.jsx)(n.iz,{color:"gray.100"}),(0,S.jsx)(V.M,{defaultLanguage:"yaml",height:"calc(100vh - 515px)",onChange:function(e){try{m(!0),function(e){R.ZP.load(e,{json:!0}),D(void 0)}(e),o(!(e&&""!==e.trim()))}catch(r){(0,V.F)(r)?D(r):P("Could not parse the supplied YAML")}},onMount:function(e){y.current=e,y.current.focus()},options:{fontFamily:"Menlo",fontSize:13,minimap:{enabled:!0}},theme:"light"}),(0,S.jsx)(n.iz,{color:"gray.100"}),(0,S.jsx)(s.hE,{mt:"24px !important",size:"sm",spacing:"8px",variant:"outline",children:(0,S.jsx)(s.zx,{bg:"primary.800",color:"white",isDisabled:a||!!k||u,isLoading:u,loadingText:"Saving Yaml system",onClick:Z,size:"sm",variant:"solid",type:"submit",_active:{bg:"primary.500"},_hover:{bg:"primary.400"},children:"Create dataset"})})]})]}),(0,S.jsx)(n.xu,{children:j&&(a||k)&&(0,S.jsx)(Y.Z,{isEmptyState:a,yamlError:k})})]})},F=function(){var e=(0,i.useState)(null),r=e[0],t=e[1];return(0,S.jsxs)(a.Z,{title:"Datasets",children:[(0,S.jsx)(o.Z,{backPath:c.$m}),(0,S.jsx)(n.X6,{mb:2,fontSize:"2xl",fontWeight:"semibold",children:"Datasets"}),(0,S.jsxs)(n.Kq,{spacing:8,children:[(0,S.jsx)(n.xu,{w:{base:"100%",lg:"50%"},children:(0,S.jsx)(n.xv,{children:"Create a dataset using YAML or connect to a database."})}),(0,S.jsxs)(n.xu,{children:[(0,S.jsx)(s.zx,{size:"sm",mr:2,variant:"outline",onClick:function(){return t("yaml")},isActive:"yaml"===r,"data-testid":"upload-yaml-btn",children:"Upload a new dataset YAML"}),(0,S.jsx)(s.zx,{size:"sm",mr:2,variant:"outline",onClick:function(){return t("database")},isActive:"database"===r,"data-testid":"connect-db-btn",children:"Connect to a database"})]}),"database"===r&&(0,S.jsx)(n.xu,{w:{base:"100%",lg:"50%"},children:(0,S.jsx)(L,{})}),"yaml"===r&&(0,S.jsx)(n.xu,{w:{base:"100%"},children:(0,S.jsx)(B,{})})]})]})}},73846:function(e,r,t){(window.__NEXT_P=window.__NEXT_P||[]).push(["/dataset/new",function(){return t(34129)}])}},function(e){e.O(0,[7751,6432,530,3452,3453,8301,7068,6557,9774,2888,179],(function(){return r=73846,e(e.s=r);var r}));var r=e.O();_N_E=r}]);