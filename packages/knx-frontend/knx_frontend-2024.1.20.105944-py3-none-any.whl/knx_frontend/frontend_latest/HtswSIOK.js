/*! For license information please see HtswSIOK.js.LICENSE.txt */
export const id=171;export const ids=[171];export const modules={8336:(e,r,t)=>{var i=t(309),a=t(8144),o=t(4243);(0,i.Z)([(0,o.Mo)("ha-card")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        box-shadow: var(--ha-card-box-shadow, none);
        box-sizing: border-box;
        border-radius: var(--ha-card-border-radius, 12px);
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([raised]) {
        border: none;
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return a.dy`
      ${this.header?a.dy`<h1 class="card-header">${this.header}</h1>`:a.Ld}
      <slot></slot>
    `}}]}}),a.oi)},7006:(e,r,t)=>{var i=t(309),a=t(4541),o=t(7838),s=t(879),c=t(8144),n=t(4243);(0,i.Z)([(0,n.Mo)("ha-circular-progress")],(function(e,r){class t extends r{constructor(...r){super(...r),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"alt",value(){return"Loading"}},{kind:"field",decorators:[(0,n.Cb)()],key:"size",value(){return"medium"}},{kind:"set",key:"density",value:function(e){}},{kind:"get",key:"density",value:function(){switch(this.size){case"tiny":return-8;case"small":return-5;case"medium":default:return 0;case"large":return 5}}},{kind:"set",key:"indeterminate",value:function(e){}},{kind:"get",key:"indeterminate",value:function(){return this.active}},{kind:"get",static:!0,key:"styles",value:function(){return[(0,a.Z)((0,o.Z)(t),"styles",this),c.iv`
        :host {
          overflow: hidden;
        }
      `]}}]}}),s.D)},4776:(e,r,t)=>{t.r(r);var i=t(309),a=t(8144),o=t(4243),s=(t(7006),t(3358),t(3957),t(9950));(0,i.Z)([(0,o.Mo)("hass-loading-screen")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,attribute:"no-toolbar"})],key:"noToolbar",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"rootnav",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)()],key:"message",value:void 0},{kind:"method",key:"render",value:function(){var e;return a.dy`
      ${this.noToolbar?"":a.dy`<div class="toolbar">
            ${this.rootnav||null!==(e=history.state)&&void 0!==e&&e.root?a.dy`
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:a.dy`
                  <ha-icon-button-arrow-prev
                    .hass=${this.hass}
                    @click=${this._handleBack}
                  ></ha-icon-button-arrow-prev>
                `}
          </div>`}
      <div class="content">
        <ha-circular-progress active></ha-circular-progress>
        ${this.message?a.dy`<div id="loading-text">${this.message}</div>`:a.Ld}
      </div>
    `}},{kind:"method",key:"_handleBack",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[s.Qx,a.iv`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-menu-button,
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          height: calc(100% - var(--header-height));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        #loading-text {
          max-width: 350px;
          margin-top: 16px;
        }
      `]}}]}}),a.oi)},879:(e,r,t)=>{t.d(r,{D:()=>u});var i=t(7480),a=t(4243),o=t(8103),s=t(8144),c=t(3448),n=t(153),d=t(6538);class l extends s.oi{constructor(){super(...arguments),this.indeterminate=!1,this.progress=0,this.density=0,this.closed=!1}open(){this.closed=!1}close(){this.closed=!0}render(){const e={"mdc-circular-progress--closed":this.closed,"mdc-circular-progress--indeterminate":this.indeterminate},r=48+4*this.density,t={width:`${r}px`,height:`${r}px`};return s.dy`
      <div
        class="mdc-circular-progress ${(0,c.$)(e)}"
        style="${(0,d.V)(t)}"
        role="progressbar"
        aria-label="${(0,n.o)(this.ariaLabel)}"
        aria-valuemin="0"
        aria-valuemax="1"
        aria-valuenow="${(0,n.o)(this.indeterminate?void 0:this.progress)}">
        ${this.renderDeterminateContainer()}
        ${this.renderIndeterminateContainer()}
      </div>`}renderDeterminateContainer(){const e=48+4*this.density,r=e/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,i=6.2831852*t,a=(1-this.progress)*i,o=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return s.dy`
      <div class="mdc-circular-progress__determinate-container">
        <svg class="mdc-circular-progress__determinate-circle-graphic"
             viewBox="0 0 ${e} ${e}">
          <circle class="mdc-circular-progress__determinate-track"
                  cx="${r}" cy="${r}" r="${t}"
                  stroke-width="${o}"></circle>
          <circle class="mdc-circular-progress__determinate-circle"
                  cx="${r}" cy="${r}" r="${t}"
                  stroke-dasharray="${6.2831852*t}"
                  stroke-dashoffset="${a}"
                  stroke-width="${o}"></circle>
        </svg>
      </div>`}renderIndeterminateContainer(){return s.dy`
      <div class="mdc-circular-progress__indeterminate-container">
        <div class="mdc-circular-progress__spinner-layer">
          ${this.renderIndeterminateSpinnerLayer()}
        </div>
      </div>`}renderIndeterminateSpinnerLayer(){const e=48+4*this.density,r=e/2,t=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,i=6.2831852*t,a=.5*i,o=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return s.dy`
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${e} ${e}">
            <circle cx="${r}" cy="${r}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${a}"
                    stroke-width="${o}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__gap-patch">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${e} ${e}">
            <circle cx="${r}" cy="${r}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${a}"
                    stroke-width="${.8*o}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${e} ${e}">
            <circle cx="${r}" cy="${r}" r="${t}"
                    stroke-dasharray="${i}"
                    stroke-dashoffset="${a}"
                    stroke-width="${o}"></circle>
          </svg>
        </div>`}update(e){super.update(e),e.has("progress")&&(this.progress>1&&(this.progress=1),this.progress<0&&(this.progress=0))}}(0,i.gn)([(0,a.Cb)({type:Boolean,reflect:!0})],l.prototype,"indeterminate",void 0),(0,i.gn)([(0,a.Cb)({type:Number,reflect:!0})],l.prototype,"progress",void 0),(0,i.gn)([(0,a.Cb)({type:Number,reflect:!0})],l.prototype,"density",void 0),(0,i.gn)([(0,a.Cb)({type:Boolean,reflect:!0})],l.prototype,"closed",void 0),(0,i.gn)([o.L,(0,a.Cb)({type:String,attribute:"aria-label"})],l.prototype,"ariaLabel",void 0);const p=s.iv`.mdc-circular-progress__determinate-circle,.mdc-circular-progress__indeterminate-circle-graphic{stroke:#6200ee;stroke:var(--mdc-theme-primary, #6200ee)}.mdc-circular-progress__determinate-track{stroke:transparent}@keyframes mdc-circular-progress-container-rotate{to{transform:rotate(360deg)}}@keyframes mdc-circular-progress-spinner-layer-rotate{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes mdc-circular-progress-color-1-fade-in-out{from{opacity:.99}25%{opacity:.99}26%{opacity:0}89%{opacity:0}90%{opacity:.99}to{opacity:.99}}@keyframes mdc-circular-progress-color-2-fade-in-out{from{opacity:0}15%{opacity:0}25%{opacity:.99}50%{opacity:.99}51%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-3-fade-in-out{from{opacity:0}40%{opacity:0}50%{opacity:.99}75%{opacity:.99}76%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-4-fade-in-out{from{opacity:0}65%{opacity:0}75%{opacity:.99}90%{opacity:.99}to{opacity:0}}@keyframes mdc-circular-progress-left-spin{from{transform:rotate(265deg)}50%{transform:rotate(130deg)}to{transform:rotate(265deg)}}@keyframes mdc-circular-progress-right-spin{from{transform:rotate(-265deg)}50%{transform:rotate(-130deg)}to{transform:rotate(-265deg)}}.mdc-circular-progress{display:inline-flex;position:relative;direction:ltr;line-height:0;transition:opacity 250ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-circular-progress__determinate-container,.mdc-circular-progress__indeterminate-circle-graphic,.mdc-circular-progress__indeterminate-container,.mdc-circular-progress__spinner-layer{position:absolute;width:100%;height:100%}.mdc-circular-progress__determinate-container{transform:rotate(-90deg)}.mdc-circular-progress__indeterminate-container{font-size:0;letter-spacing:0;white-space:nowrap;opacity:0}.mdc-circular-progress__determinate-circle-graphic,.mdc-circular-progress__indeterminate-circle-graphic{fill:transparent}.mdc-circular-progress__determinate-circle{transition:stroke-dashoffset 500ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-circular-progress__gap-patch{position:absolute;top:0;left:47.5%;box-sizing:border-box;width:5%;height:100%;overflow:hidden}.mdc-circular-progress__gap-patch .mdc-circular-progress__indeterminate-circle-graphic{left:-900%;width:2000%;transform:rotate(180deg)}.mdc-circular-progress__circle-clipper{display:inline-flex;position:relative;width:50%;height:100%;overflow:hidden}.mdc-circular-progress__circle-clipper .mdc-circular-progress__indeterminate-circle-graphic{width:200%}.mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{left:-100%}.mdc-circular-progress--indeterminate .mdc-circular-progress__determinate-container{opacity:0}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{opacity:1}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{animation:mdc-circular-progress-container-rotate 1568.2352941176ms linear infinite}.mdc-circular-progress--indeterminate .mdc-circular-progress__spinner-layer{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-1{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-1-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-2{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-2-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-3{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-3-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-4{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-4-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--closed{opacity:0}:host{display:inline-flex}.mdc-circular-progress__determinate-track{stroke:transparent;stroke:var(--mdc-circular-progress-track-color, transparent)}`;let u=class extends l{};u.styles=[p],u=(0,i.gn)([(0,a.Mo)("mwc-circular-progress")],u)},7171:(e,r,t)=>{t.r(r),t.d(r,{KNXProjectView:()=>$});var i=t(309),a=t(8144),o=t(4243),s=t(4516),c=(t(4776),t(657),t(8336),t(6291),t(2828),t(4541)),n=t(7838),d=t(3448),l=t(8394),p=t(6133);const u=new p.r("knx-project-tree-view");(0,i.Z)([(0,o.Mo)("knx-project-tree-view")],(function(e,r){class t extends r{constructor(...r){super(...r),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"multiselect",value(){return!1}},{kind:"field",decorators:[(0,o.SB)()],key:"_selectableRanges",value(){return{}}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,n.Z)(t.prototype),"connectedCallback",this).call(this);const e=r=>{Object.entries(r).forEach((([r,t])=>{t.group_addresses.length>0&&(this._selectableRanges[r]={selected:!1,groupAddresses:t.group_addresses}),e(t.group_ranges)}))};e(this.data.group_ranges),u.debug("ranges",this._selectableRanges)}},{kind:"method",key:"render",value:function(){return a.dy`<div class="ha-tree-view">${this._recurseData(this.data.group_ranges)}</div>`}},{kind:"method",key:"_recurseData",value:function(e,r=0){const t=Object.entries(e).map((([e,t])=>{const i=Object.keys(t.group_ranges).length>0;if(!(i||t.group_addresses.length>0))return a.Ld;const o=e in this._selectableRanges,s=!!o&&this._selectableRanges[e].selected,c={"range-item":!0,"root-range":0===r,"sub-range":r>0,selectable:o,"selected-range":s,"non-selected-range":o&&!s},n=a.dy`<div
        class=${(0,d.$)(c)}
        toggle-range=${o?e:a.Ld}
        @click=${o?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:a.Ld}
      >
        <span class="range-key">${e}</span>
        <span class="range-text">${t.name}</span>
      </div>`;if(i){const e={"root-group":0===r,"sub-group":0!==r};return a.dy`<div class=${(0,d.$)(e)}>
          ${n} ${this._recurseData(t.group_ranges,r+1)}
        </div>`}return a.dy`${n}`}));return a.dy`${t}`}},{kind:"method",key:"_selectionChangedMulti",value:function(e){const r=e.target.getAttribute("toggle-range");this._selectableRanges[r].selected=!this._selectableRanges[r].selected,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionChangedSingle",value:function(e){const r=e.target.getAttribute("toggle-range"),t=this._selectableRanges[r].selected;Object.values(this._selectableRanges).forEach((e=>{e.selected=!1})),this._selectableRanges[r].selected=!t,this._selectionUpdate(),this.requestUpdate()}},{kind:"method",key:"_selectionUpdate",value:function(){const e=Object.values(this._selectableRanges).reduce(((e,r)=>r.selected?e.concat(r.groupAddresses):e),[]);u.debug("selection changed",e),(0,l.B)(this,"knx-group-range-selection-changed",{groupAddresses:e})}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      :host {
        margin: 0;
        height: 100%;
        overflow-y: scroll;
        overflow-x: hidden;
        background-color: var(--card-background-color);
      }

      .ha-tree-view {
        cursor: default;
      }

      .root-group {
        margin-bottom: 8px;
      }

      .root-group > * {
        padding-top: 5px;
        padding-bottom: 5px;
      }

      .range-item {
        display: block;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        font-size: 0.875rem;
      }

      .range-item > * {
        vertical-align: middle;
        pointer-events: none;
      }

      .range-key {
        color: var(--text-primary-color);
        font-size: 0.75rem;
        font-weight: 700;
        background-color: var(--label-badge-grey);
        border-radius: 4px;
        padding: 1px 4px;
        margin-right: 2px;
      }

      .root-range {
        padding-left: 8px;
        font-weight: 500;
        background-color: var(--secondary-background-color);

        & .range-key {
          color: var(--primary-text-color);
          background-color: var(--card-background-color);
        }
      }

      .sub-range {
        padding-left: 13px;
      }

      .selectable {
        cursor: pointer;
      }

      .selectable:hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }

      .selected-range {
        background-color: rgba(var(--rgb-primary-color), 0.12);

        & .range-key {
          background-color: var(--primary-color);
        }
      }

      .selected-range:hover {
        background-color: rgba(var(--rgb-primary-color), 0.07);
      }

      .non-selected-range {
        background-color: var(--card-background-color);
      }
    `}}]}}),a.oi);const g=/^[v^~<>=]*?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,h=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const r=e.match(g);if(!r)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return r.shift(),r},m=e=>"*"===e||"x"===e||"X"===e,b=e=>{const r=parseInt(e,10);return isNaN(r)?e:r},v=(e,r)=>{if(m(e)||m(r))return 0;const[t,i]=((e,r)=>typeof e!=typeof r?[String(e),String(r)]:[e,r])(b(e),b(r));return t>i?1:t<i?-1:0},y=(e,r)=>{for(let t=0;t<Math.max(e.length,r.length);t++){const i=v(e[t]||"0",r[t]||"0");if(0!==i)return i}return 0},k=(e,r,t)=>{x(t);const i=((e,r)=>{const t=h(e),i=h(r),a=t.pop(),o=i.pop(),s=y(t,i);return 0!==s?s:a&&o?y(a.split("."),o.split(".")):a||o?a?-1:1:0})(e,r);return f[t].includes(i)},f={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1],"!=":[-1,1]},_=Object.keys(f),x=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===_.indexOf(e))throw new Error(`Invalid operator, expected one of ${_.join("|")}`)},w=new p.r("knx-project-view");let $=(0,i.Z)([(0,o.Mo)("knx-project-view")],(function(e,r){return{F:class extends r{constructor(...r){super(...r),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"rangeSelectorHidden",value(){return!0}},{kind:"field",decorators:[(0,o.SB)()],key:"_visibleGroupAddresses",value(){return[]}},{kind:"field",decorators:[(0,o.SB)()],key:"_groupRangeAvailable",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){this.knx.project?this._isGroupRangeAvailable():this.knx.loadProject().then((()=>{this._isGroupRangeAvailable(),this.requestUpdate()}))}},{kind:"method",key:"_isGroupRangeAvailable",value:function(){var e,r;const t=null!==(e=null===(r=this.knx.project)||void 0===r?void 0:r.knxproject.info.xknxproject_version)&&void 0!==e?e:"0.0.0";w.debug("project version: "+t),this._groupRangeAvailable=k(t,"3.3.0",">=")}},{kind:"field",key:"_columns",value(){return(0,s.Z)(((e,r)=>{const t="100px",i="82px";return{address:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_address"),width:t},name:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_name"),width:e?"calc(100% - 82px - 100px)":"calc(50% - 82px)"},description:{filterable:!0,sortable:!0,hidden:e,title:this.knx.localize("project_view_table_description"),width:"calc(50% - 100px)"},dpt:{sortable:!0,filterable:!0,title:this.knx.localize("project_view_table_dpt"),width:i,template:e=>e.dpt?a.dy`<span style="display:inline-block;width:24px;text-align:right;"
                  >${e.dpt.main}</span
                >${e.dpt.sub?"."+e.dpt.sub.toString().padStart(3,"0"):""} `:""}}}))}},{kind:"method",key:"_getRows",value:function(e){return e.length?Object.entries(this.knx.project.knxproject.group_addresses).reduce(((r,[t,i])=>(e.includes(t)&&r.push(i),r)),[]):Object.values(this.knx.project.knxproject.group_addresses)}},{kind:"method",key:"_visibleAddressesChanged",value:function(e){this._visibleGroupAddresses=e.detail.groupAddresses}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.knx.project)return a.dy` <hass-loading-screen></hass-loading-screen> `;const e=this._getRows(this._visibleGroupAddresses);return a.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
      >
        ${this.knx.project.project_loaded?a.dy`${this.narrow&&this._groupRangeAvailable?a.dy`<ha-icon-button
                    slot="toolbar-icon"
                    .label=${this.hass.localize("ui.components.related-filter-menu.filter")}
                    .path=${"M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z"}
                    @click=${this._toggleRangeSelector}
                  ></ha-icon-button>`:a.Ld}
              <div class="sections">
                ${this._groupRangeAvailable?a.dy`
                      <knx-project-tree-view
                        .data=${this.knx.project.knxproject}
                        @knx-group-range-selection-changed=${this._visibleAddressesChanged}
                      ></knx-project-tree-view>
                    `:a.Ld}
                <ha-data-table
                  class="ga-table"
                  .hass=${this.hass}
                  .columns=${this._columns(this.narrow,this.hass.language)}
                  .data=${e}
                  .hasFab=${!1}
                  .searchLabel=${this.hass.localize("ui.components.data-table.search")}
                  .clickable=${!1}
                ></ha-data-table>
              </div>`:a.dy` <ha-card .header=${this.knx.localize("attention")}>
              <div class="card-content">
                <p>${this.knx.localize("project_view_upload")}</p>
              </div>
            </ha-card>`}
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_toggleRangeSelector",value:function(){this.rangeSelectorHidden=!this.rangeSelectorHidden}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      hass-loading-screen {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
      }
      .sections {
        display: flex;
        flex-direction: row;
        height: 100%;
      }

      :host([narrow]) knx-project-tree-view {
        position: absolute;
        max-width: calc(100% - 60px); /* 100% -> max 871px before not narrow */
        z-index: 1;
        right: 0;
        transition: 0.5s;
        border-left: 1px solid var(--divider-color);
      }

      :host([narrow][rangeSelectorHidden]) knx-project-tree-view {
        width: 0;
      }

      :host(:not([narrow])) knx-project-tree-view {
        max-width: 255px; /* min 616px - 816px for tree-view + ga-table (depending on side menu) */
      }

      .ga-table {
        flex: 1;
      }
    `}}]}}),a.oi)}};
//# sourceMappingURL=HtswSIOK.js.map