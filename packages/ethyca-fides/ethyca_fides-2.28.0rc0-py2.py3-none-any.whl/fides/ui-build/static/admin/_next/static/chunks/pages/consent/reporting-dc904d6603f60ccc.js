(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3422],{51471:function(e,t,n){"use strict";n.d(t,{Z:function(){return y}});var r=n(90849),o=n(34896),i=n(88038),a=n.n(i),s=n(86677),u=(n(27378),n(90768)),c=n(51365),d=n(29549),l=n(60709),f=n(24246),p=function(){var e=(0,s.useRouter)();return(0,f.jsx)(o.xu,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,f.jsxs)(o.xu,{children:[(0,f.jsxs)(o.Kq,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,f.jsx)(o.xv,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,f.jsx)(d.zx,{size:"sm",variant:"outline",onClick:function(){e.push(l.fz)},children:"Configure"})]}),(0,f.jsxs)(o.xv,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})};function g(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function m(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?g(Object(n),!0).forEach((function(t){(0,r.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):g(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var y=function(e){var t=e.children,n=e.title,r=e.mainProps,i=(0,u.hz)(),d=(0,s.useRouter)(),l="/privacy-requests"===d.pathname||"/datastore-connection"===d.pathname,g=!(i.flags.privacyRequestsConfiguration&&l),y=(0,c.JE)(void 0,{skip:g}).data,b=(0,c.PW)(void 0,{skip:g}).data,v=i.flags.privacyRequestsConfiguration&&(!y||!b)&&l;return(0,f.jsxs)(o.kC,{"data-testid":n,direction:"column",height:"calc(100vh - 48px)",children:[(0,f.jsxs)(a(),{children:[(0,f.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,f.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,f.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,f.jsxs)(o.kC,m(m({as:"main",direction:"column",py:6,px:10,flex:1,minWidth:0,overflow:"auto"},r),{},{children:[v?(0,f.jsx)(p,{}):null,t]}))]})}},78624:function(e,t,n){"use strict";n.d(t,{D4:function(){return i.D4},MM:function(){return p},Ot:function(){return c},c6:function(){return l},cj:function(){return m},e$:function(){return s},fn:function(){return u},iC:function(){return g},nU:function(){return f},tB:function(){return d}});var r,o=n(90849),i=n(60041),a="An unexpected error occurred. Please try again.",s=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:a;if((0,i.Bw)(e)){if((0,i.hE)(e.data))return e.data.detail;if((0,i.cz)(e.data)){var n,r=null===(n=e.data.detail)||void 0===n?void 0:n[0];return"".concat(null===r||void 0===r?void 0:r.msg,": ").concat(null===r||void 0===r?void 0:r.loc)}if(409===e.status&&(0,i.Dy)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")");if(404===e.status&&(0,i.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function u(e){return"object"===typeof e&&null!=e&&"status"in e}function c(e){return"object"===typeof e&&null!=e&&"data"in e&&"string"===typeof e.data.detail}function d(e){return"object"===typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}var l,f=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:a};if((0,i.oK)(e))return{status:e.originalStatus,message:e.data};if((0,i.Bw)(e)){var n=e.status;return{status:n,message:s(e,t.message)}}return t},p=function(e){return Object.entries(e).map((function(e){return{value:e[1],label:e[1]}}))};!function(e){e.GVL="gvl",e.AC="gacp"}(l||(l={}));var g=(r={},(0,o.Z)(r,l.GVL,{label:"GVL",fullName:"Global Vendor List"}),(0,o.Z)(r,l.AC,{label:"AC",fullName:"Google Additional Consent List"}),r),m=function(e){return e.split(".")[0]===l.AC?l.AC:l.GVL}},61856:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return j}});var r=n(34896),o=n(27378),i=n(51471),a=n(55732),s=n(97865),u=n(34707),c=n.n(u),d=n(70409),l=n(32751),f=n(29549),p=n(78624),g=n(90849);function m(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function y(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?m(Object(n),!0).forEach((function(t){(0,g.Z)(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):m(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}var b=n(28703).u.injectEndpoints({endpoints:function(e){return{downloadReport:e.query({query:function(e){var t=y(y({},function(e){var t,n,r=e.startDate,o=e.endDate;return r&&(t=new Date(r)).setUTCHours(0,0,0),o&&(n=new Date(o)).setUTCHours(0,0,0),y(y({},t?{created_gt:t.toISOString()}:{}),n?{created_lt:n.toISOString()}:{})}({startDate:e.startDate,endDate:e.endDate})),{},{download_csv:"true"});return{url:"plus/consent_reporting",params:t,responseHandler:"content-type"}},providesTags:["Consent Reporting"]})}}}).useLazyDownloadReportQuery,v=n(24246),h=function(){var e=(0,o.useState)(""),t=e[0],n=e[1],i=(0,o.useState)(""),u=i[0],g=i[1],m=(0,d.pm)(),y=b(),h=(0,s.Z)(y,2),j=h[0],x=h[1].isLoading,w=function(){var e=(0,a.Z)(c().mark((function e(){var n,r,o,i;return c().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,j({startDate:t,endDate:u});case 2:(n=e.sent).isError?(r=(0,p.e$)(n.error,"A problem occurred while generating your consent report.  Please try again."),m({status:"error",description:r})):(o=document.createElement("a"),i=new Blob([n.data],{type:"text/csv"}),o.href=window.URL.createObjectURL(i),o.download="consent-reports.csv",o.click());case 4:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return(0,v.jsxs)(r.Ug,{gap:4,maxWidth:"720px","data-testid":"consent-reporting",children:[(0,v.jsxs)(l.BZ,{size:"sm",flex:1,children:[(0,v.jsx)(l.Ui,{borderRadius:"md",children:"From"}),(0,v.jsx)(l.II,{type:"date",name:"From",value:t,max:u||void 0,onChange:function(e){return n(e.target.value)},borderRadius:"md","data-testid":"input-from-date"})]}),(0,v.jsxs)(l.BZ,{size:"sm",flex:1,children:[(0,v.jsx)(l.Ui,{borderRadius:"md",children:"To"}),(0,v.jsx)(l.II,{type:"date",name:"To",value:u,min:t||void 0,onChange:function(e){return g(e.target.value)},borderRadius:"md","data-testid":"input-to-date"})]}),(0,v.jsx)(f.zx,{onClick:w,isLoading:x,colorScheme:"primary",size:"sm","data-testid":"download-btn",children:"Download report"})]})},j=function(){return(0,v.jsxs)(i.Z,{title:"Configure consent",children:[(0,v.jsx)(r.xu,{mb:4,children:(0,v.jsx)(r.X6,{fontSize:"2xl",fontWeight:"semibold",mb:2,"data-testid":"header",children:"Configure consent"})}),(0,v.jsx)(r.xv,{fontSize:"sm",mb:8,width:{base:"100%",lg:"50%"},children:'Download a CSV containing a report of consent preferences made by users on your sites. Select a date range below and click "Download report". Depending on the number of records in the date range you select, it may take several minutes to prepare the file after you click "Download report".'}),(0,v.jsx)(r.xu,{"data-testid":"consent",children:(0,v.jsx)(h,{})})]})}},60041:function(e,t,n){"use strict";n.d(t,{Bw:function(){return a},D4:function(){return o},Dy:function(){return u},XD:function(){return c},cz:function(){return d},hE:function(){return s},oK:function(){return i}});var r=n(76649),o=function(e){return"error"in e},i=function(e){return(0,r.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status},a=function(e){return(0,r.Ln)({status:"number",data:{}},e)},s=function(e){return(0,r.Ln)({detail:"string"},e)},u=function(e){return(0,r.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e)},c=function(e){return(0,r.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e)},d=function(e){return(0,r.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)}},15806:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/consent/reporting",function(){return n(61856)}])}},function(e){e.O(0,[9774,2888,179],(function(){return t=15806,e(e.s=t);var t}));var t=e.O();_N_E=t}]);