import{r as d,j as e,d2 as F,v as s,F as P,R as v,w as E,aN as L,d3 as R,d4 as S,d5 as a,d6 as w,d7 as z,b as A,d8 as j}from"./vendor-BMWfu6zp.js";import{S as C,j as k,Z as $,U as _,t as I,a4 as O}from"./vendor-arizeai-Sj74jm5V.js";import{b2 as T,d as D,R as N,b3 as G,b4 as M}from"./components-BC3-LP_a.js";import{L as U,E as B,h as q,M as J,a as m,D as K,d as W,b as H,e as V,P as Y,c as Z,T as Q,p as X,f as u,g as ee,i as re,j as g,k as ae,l as h,m as x,n as oe,o as te,q as ne,r as se,s as le,A as ie}from"./pages--n2933VW.js";import"./vendor-three-DwGkEfCM.js";import"./vendor-codemirror-DO3VqEcD.js";import"./vendor-recharts-BGN0SxgJ.js";(function(){const n=document.createElement("link").relList;if(n&&n.supports&&n.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))c(o);new MutationObserver(o=>{for(const t of o)if(t.type==="childList")for(const l of t.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&c(l)}).observe(document,{childList:!0,subtree:!0});function i(o){const t={};return o.integrity&&(t.integrity=o.integrity),o.referrerPolicy&&(t.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?t.credentials="include":o.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(o){if(o.ep)return;o.ep=!0;const t=i(o);fetch(o.href,t)}})();const b="arize-phoenix-feature-flags",p={__CLEAR__:!0};function ce(){const r=localStorage.getItem(b);if(!r)return p;try{const n=JSON.parse(r);return Object.assign({},p,n)}catch{return p}}const f=d.createContext(null);function de(){const r=v.useContext(f);if(r===null)throw new Error("useFeatureFlags must be used within a FeatureFlagsProvider");return r}function pe(r){const[n,i]=d.useState(ce()),c=o=>{localStorage.setItem(b,JSON.stringify(o)),i(o)};return e(f.Provider,{value:{featureFlags:n,setFeatureFlags:c},children:e(me,{children:r.children})})}function me(r){const{children:n}=r,{featureFlags:i,setFeatureFlags:c}=de(),[o,t]=d.useState(!1);return F("ctrl+shift+f",()=>t(!0)),s(P,{children:[n,e(_,{type:"modal",isDismissable:!0,onDismiss:()=>t(!1),children:o&&e(C,{title:"Feature Flags",children:e(k,{height:"size-1000",padding:"size-100",children:Object.keys(i).map(l=>e($,{isSelected:i[l],onChange:y=>c({...i,[l]:y}),children:l},l))})})})]})}function ue(){return e(L,{styles:r=>E`
        body {
          background-color: var(--ac-global-color-grey-75);
          color: var(--ac-global-text-color-900);
          font-family: "Roboto";
          font-size: ${r.typography.sizes.medium.fontSize}px;
          margin: 0;
          #root,
          #root > div[data-overlay-container="true"],
          #root > div[data-overlay-container="true"] > .ac-theme {
            height: 100vh;
          }
        }

        /* Remove list styling */
        ul {
          display: block;
          list-style-type: none;
          margin-block-start: none;
          margin-block-end: 0;
          padding-inline-start: 0;
          margin-block-start: 0;
        }

        /* A reset style for buttons */
        .button--reset {
          background: none;
          border: none;
          padding: 0;
        }
        /* this css class is added to html via modernizr @see modernizr.js */
        .no-hiddenscroll {
          /* Works on Firefox */
          * {
            scrollbar-width: thin;
            scrollbar-color: var(--ac-global-color-grey-300)
              var(--ac-global-color-grey-400);
          }

          /* Works on Chrome, Edge, and Safari */
          *::-webkit-scrollbar {
            width: 14px;
          }

          *::-webkit-scrollbar-track {
            background: var(--ac-global-color-grey-100);
          }

          *::-webkit-scrollbar-thumb {
            background-color: var(--ac-global-color-grey-75);
            border-radius: 8px;
            border: 1px solid var(--ac-global-color-grey-300);
          }
        }

        :root {
          --px-blue-color: ${r.colors.arizeBlue};

          --px-flex-gap-sm: ${r.spacing.margin4}px;
          --px-flex-gap-sm: ${r.spacing.margin8}px;

          --px-section-background-color: ${r.colors.gray500};

          /* An item is a typically something in a list */
          --px-item-background-color: ${r.colors.gray800};
          --px-item-border-color: ${r.colors.gray600};

          --px-spacing-sm: ${r.spacing.padding4}px;
          --px-spacing-med: ${r.spacing.padding8}px;
          --px-spacing-lg: ${r.spacing.padding16}px;

          --px-border-radius-med: ${r.borderRadius.medium}px;

          --px-font-size-sm: ${r.typography.sizes.small.fontSize}px;
          --px-font-size-med: ${r.typography.sizes.medium.fontSize}px;
          --px-font-size-lg: ${r.typography.sizes.large.fontSize}px;

          --px-gradient-bar-height: 8px;

          --px-nav-collapsed-width: 45px;
          --px-nav-expanded-width: 200px;
        }

        .ac-theme--dark {
          --px-primary-color: #9efcfd;
          --px-primary-color--transparent: rgb(158, 252, 253, 0.2);
          --px-reference-color: #baa1f9;
          --px-reference-color--transparent: #baa1f982;
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
        .ac-theme--light {
          --px-primary-color: #00add0;
          --px-primary-color--transparent: rgba(0, 173, 208, 0.2);
          --px-reference-color: #4500d9;
          --px-reference-color--transparent: rgba(69, 0, 217, 0.2);
          --px-corpus-color: #92969c;
          --px-corpus-color--transparent: #92969c63;
        }
      `})}const ge=R(S(s(a,{path:"/",element:e(U,{}),errorElement:e(B,{}),children:[e(a,{index:!0,loader:q}),s(a,{path:"/model",handle:{crumb:()=>"model"},element:e(J,{}),children:[e(a,{index:!0,element:e(m,{})}),e(a,{element:e(m,{}),children:e(a,{path:"dimensions",children:e(a,{path:":dimensionId",element:e(K,{}),loader:W})})}),e(a,{path:"embeddings",children:e(a,{path:":embeddingDimensionId",element:e(H,{}),loader:V,handle:{crumb:r=>r.embedding.name}})})]}),s(a,{path:"/projects",handle:{crumb:()=>"projects"},element:e(Y,{}),children:[e(a,{index:!0,element:e(Z,{})}),s(a,{path:":projectId",element:e(Q,{}),loader:X,handle:{crumb:r=>r.project.name},children:[e(a,{index:!0,element:e(u,{})}),e(a,{element:e(u,{}),children:e(a,{path:"traces/:traceId",element:e(ee,{})})})]})]}),s(a,{path:"/datasets",handle:{crumb:()=>"datasets"},children:[e(a,{index:!0,element:e(re,{})}),s(a,{path:":datasetId",loader:g,handle:{crumb:r=>r.dataset.name},children:[s(a,{element:e(ae,{}),loader:g,children:[e(a,{index:!0,element:e(h,{}),loader:x}),e(a,{path:"experiments",element:e(h,{}),loader:x}),e(a,{path:"examples",element:e(oe,{}),loader:te,children:e(a,{path:":exampleId",element:e(ne,{})})})]}),e(a,{path:"compare",handle:{crumb:()=>"compare"},loader:se,element:e(le,{})})]})]}),e(a,{path:"/apis",element:e(ie,{}),handle:{crumb:()=>"APIs"}})]})),{basename:window.Config.basename});function he(){return e(w,{router:ge})}function xe(){return e(T,{children:e(be,{})})}function be(){const{theme:r}=D();return e(O,{theme:r,children:e(z,{theme:I,children:s(A.RelayEnvironmentProvider,{environment:N,children:[e(ue,{}),e(pe,{children:e(G,{children:e(d.Suspense,{children:e(M,{children:e(he,{})})})})})]})})})}const fe=document.getElementById("root"),ye=j.createRoot(fe);ye.render(e(xe,{}));
