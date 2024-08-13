"use strict";(self.webpackChunk_jupyter_docprovider_extension=self.webpackChunk_jupyter_docprovider_extension||[]).push([[544],{544:(e,o,t)=>{t.r(o),t.d(o,{default:()=>x});var r,i=t(974),n=t(607),a=t(586),s=t(141),l=t(881),c=t(31),d=t(765),u=t(605),v=t(697),p=t(744);!function(e){e.openPath="filebrowser:open-path"}(r||(r={}));const g={id:"@jupyter/docprovider-extension:drive",description:"The default collaborative drive provider",provides:p.ICollaborativeDrive,requires:[u.ITranslator],optional:[p.IGlobalAwareness],activate:(e,o,t)=>{const r=o.load("jupyter_collaboration"),i=new p.YDrive(e.serviceManager.user,r,t);return e.serviceManager.contents.addDrive(i),i}},h={id:"@jupyter/docprovider-extension:yfile",description:"Plugin to register the shared model factory for the content type 'file'",autoStart:!0,requires:[p.ICollaborativeDrive],optional:[],activate:(e,o)=>{o.sharedModelFactory.registerDocumentFactory("file",(()=>new v.YFile))}},w={id:"@jupyter/docprovider-extension:ynotebook",description:"Plugin to register the shared model factory for the content type 'notebook'",autoStart:!0,requires:[p.ICollaborativeDrive],optional:[d.ISettingRegistry],activate:(e,o,t)=>{let r=!0;t&&t.load("@jupyterlab/notebook-extension:tracker").then((e=>{const o=e=>{var o;const t=null==e?void 0:e.get("experimentalEnableDocumentWideUndoRedo").composite;r=null===(o=!t)||void 0===o||o};o(e),e.changed.connect((e=>o(e)))})),o.sharedModelFactory.registerDocumentFactory("notebook",(()=>new v.YNotebook({disableDocumentWideUndoRedo:r})))}},y={id:"@jupyter/docprovider-extension:defaultFileBrowser",description:"The default file browser factory provider",provides:a.IDefaultFileBrowser,requires:[p.ICollaborativeDrive,a.IFileBrowserFactory],optional:[i.IRouter,i.JupyterFrontEnd.ITreeResolver,i.ILabShell,d.ISettingRegistry],activate:async(e,o,t,r,i,n)=>{const{commands:a}=e;e.serviceManager.contents.addDrive(o);const s=t.createFileBrowser("filebrowser",{auto:!1,restore:!1,driveName:o.name});return f.restoreBrowser(s,a,r,i,n),s}},b={id:"@jupyter/docprovider-extension:logger",description:"A logging plugin for debugging purposes.",autoStart:!0,optional:[l.ILoggerRegistry,s.IEditorTracker,c.INotebookTracker,u.ITranslator],activate:(e,o,t,r,i)=>{const a=(null!=i?i:u.nullTranslator).load("jupyter_collaboration"),s="https://schema.jupyter.org/jupyter_collaboration/session/v1";if(!o)return void e.serviceManager.events.stream.connect(((e,o)=>{var t,r;o.schema_id===s&&(console.debug(`[${o.room}(${o.path})] ${null!==(t=o.action)&&void 0!==t?t:""}: ${null!==(r=o.msg)&&void 0!==r?r:""}`),"WARNING"===o.level&&(0,n.showDialog)({title:a.__("Warning"),body:a.__(`Two collaborative sessions are accessing the file ${o.path} simultaneously.\n                \nOpening the same file using different views simultaneously is not supported. Please, close one view; otherwise, you might lose some of your progress.`),buttons:[n.Dialog.okButton()]}))}));const l=new Map,c=(e,t)=>{const r=o.getLogger(t.context.path);l.set(t.context.localPath,r),t.disposed.connect((e=>{l.delete(e.context.localPath)}))};t&&t.widgetAdded.connect(c),r&&r.widgetAdded.connect(c),(async()=>{var o,t;const{events:r}=e.serviceManager;for await(const e of r.stream)if(e.schema_id===s){const r=l.get(e.path);null==r||r.log({type:"text",level:e.level.toLowerCase(),data:`[${e.room}] ${null!==(o=e.action)&&void 0!==o?o:""}: ${null!==(t=e.msg)&&void 0!==t?t:""}`}),"WARNING"===e.level&&(0,n.showDialog)({title:a.__("Warning"),body:a.__("Two collaborative sessions are accessing the file %1 simultaneously.\n                \nOpening a document with multiple views simultaneously is not supported. Please close one view; otherwise, you might lose some of your progress.",e.path),buttons:[n.Dialog.warnButton({label:a.__("Ok")})]})}})()}};var f;!function(e){e.restoreBrowser=async function(e,o,t,i,n){const a="jp-mod-restoring";if(e.addClass(a),!t)return await e.model.restore(e.id),await e.model.refresh(),void e.removeClass(a);const s=async()=>{t.routed.disconnect(s);const l=await(null==i?void 0:i.paths);(null==l?void 0:l.file)||(null==l?void 0:l.browser)?(await e.model.restore(e.id,!1),l.file&&await o.execute(r.openPath,{path:l.file,dontShowBrowser:!0}),l.browser&&await o.execute(r.openPath,{path:l.browser,dontShowBrowser:!0})):(await e.model.restore(e.id),await e.model.refresh()),e.removeClass(a),(null==n?void 0:n.isEmpty("main"))&&o.execute("launcher:create")};t.routed.connect(s)}}(f||(f={}));var m=t(74);const x=[g,h,w,y,b,{id:"@jupyter/docprovider-extension:notebook-cell-executor",description:"Add notebook cell executor that uses REST API instead of kernel protocol over WebSocket.",autoStart:!0,provides:c.INotebookCellExecutor,activate:e=>"true"===m.PageConfig.getOption("serverSideExecution")?new p.NotebookCellServerExecutor({serverSettings:e.serviceManager.serverSettings}):Object.freeze({runCell:c.runCell})}]}}]);