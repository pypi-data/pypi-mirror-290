"use strict";(self.webpackChunk_jupyter_docprovider_extension=self.webpackChunk_jupyter_docprovider_extension||[]).push([[422],{734:(e,t,n)=>{n.d(t,{CW:()=>u,D7:()=>r,P1:()=>s,WD:()=>c,vZ:()=>a,wt:()=>o});const r=64,o=128,s=63,c=127,a=2147483647,u=4294967295},721:(e,t,n)=>{n.d(t,{$C:()=>l,t3:()=>b,cw:()=>p,bo:()=>i});var r=n(734);n(801);const o=Number.MAX_SAFE_INTEGER;Number.MIN_SAFE_INTEGER,r.vZ,r.CW,Number.isInteger,Number.isNaN,Number.parseInt;var s=n(554);const c=e=>new Error(e),a=c("Unexpected end of array"),u=c("Integer out of Range");class f{constructor(e){this.arr=e,this.pos=0}}const l=e=>new f(e),i=e=>((e,t)=>{const n=new Uint8Array(e.arr.buffer,e.pos+e.arr.byteOffset,t);return e.pos+=t,n})(e,p(e)),d=e=>e.arr[e.pos++],p=e=>{let t=0,n=1;const s=e.arr.length;for(;e.pos<s;){const s=e.arr[e.pos++];if(t+=(s&r.WD)*n,n*=128,s<r.wt)return t;if(t>o)throw u}throw a},b=s.tv?e=>s.tv.decode(i(e)):e=>{let t=p(e);if(0===t)return"";{let n=String.fromCodePoint(d(e));if(--t<100)for(;t--;)n+=String.fromCodePoint(d(e));else for(;t>0;){const r=t<1e4?t:1e4,o=e.arr.subarray(e.pos,e.pos+r);e.pos+=r,n+=String.fromCodePoint.apply(null,o),t-=r}return decodeURIComponent(escape(n))}}},214:(e,t,n)=>{n.d(t,{Bw:()=>u,Fo:()=>f,Gu:()=>h,Qj:()=>b,xv:()=>a,zd:()=>i});var r=n(801),o=n(734),s=n(554);class c{constructor(){this.cpos=0,this.cbuf=new Uint8Array(100),this.bufs=[]}}const a=()=>new c,u=e=>{let t=e.cpos;for(let n=0;n<e.bufs.length;n++)t+=e.bufs[n].length;return t},f=e=>{const t=new Uint8Array(u(e));let n=0;for(let r=0;r<e.bufs.length;r++){const o=e.bufs[r];t.set(o,n),n+=o.length}return t.set(new Uint8Array(e.cbuf.buffer,0,e.cpos),n),t},l=(e,t)=>{const n=e.cbuf.length;e.cpos===n&&(e.bufs.push(e.cbuf),e.cbuf=new Uint8Array(2*n),e.cpos=0),e.cbuf[e.cpos++]=t},i=(e,t)=>{for(;t>o.WD;)l(e,o.wt|o.WD&t),t=r.RI(t/128);l(e,o.WD&t)},d=new Uint8Array(3e4),p=d.length/3,b=s.db&&s.db.encodeInto?(e,t)=>{if(t.length<p){const n=s.db.encodeInto(t,d).written||0;i(e,n);for(let t=0;t<n;t++)l(e,d[t])}else h(e,s.Af(t))}:(e,t)=>{const n=unescape(encodeURIComponent(t)),r=n.length;i(e,r);for(let t=0;t<r;t++)l(e,n.codePointAt(t))},h=(e,t)=>{i(e,t.byteLength),((e,t)=>{const n=e.cbuf.length,o=e.cpos,s=r.jk(n-o,t.length),c=t.length-s;e.cbuf.set(t.subarray(0,s),o),e.cpos+=s,c>0&&(e.bufs.push(e.cbuf),e.cbuf=new Uint8Array(r.T9(2*n,c)),e.cbuf.set(t.subarray(s)),e.cpos=c)})(e,t)};new DataView(new ArrayBuffer(4))},801:(e,t,n)=>{n.d(t,{RI:()=>r,T9:()=>s,jk:()=>o,n7:()=>c,sj:()=>a});const r=Math.floor,o=(Math.ceil,Math.abs,Math.imul,Math.round,Math.log10,Math.log2,Math.log,Math.sqrt,(e,t)=>e<t?e:t),s=(e,t)=>e>t?e:t,c=(Number.isNaN,Math.pow),a=(Math.sign,e=>0!==e?e<0:1/e<0)},554:(e,t,n)=>{n.d(t,{Af:()=>u,QV:()=>r,db:()=>a,jN:()=>c,tv:()=>f});const r=String.fromCharCode,o=(String.fromCodePoint,r(65535),/^\s*/g),s=/([A-Z])/g,c=(e,t)=>(e=>e.replace(o,""))(e.replace(s,(e=>`${t}${(e=>e.toLowerCase())(e)}`))),a="undefined"!=typeof TextEncoder?new TextEncoder:null,u=a?e=>a.encode(e):e=>{const t=unescape(encodeURIComponent(e)),n=t.length,r=new Uint8Array(n);for(let e=0;e<n;e++)r[e]=t.codePointAt(e);return r};let f="undefined"==typeof TextDecoder?null:new TextDecoder("utf-8",{fatal:!0,ignoreBOM:!0});f&&1===f.decode(new Uint8Array).length&&(f=null)}}]);