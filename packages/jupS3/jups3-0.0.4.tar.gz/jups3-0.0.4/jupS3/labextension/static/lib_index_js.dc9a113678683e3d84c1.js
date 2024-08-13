"use strict";
(self["webpackChunkjupS3"] = self["webpackChunkjupS3"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI),
/* harmony export */   requestAPIWithParams: () => (/* binding */ requestAPIWithParams)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupS3', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
async function requestAPIWithParams(endPoint = '', init = {}, params = {}) {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    let requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupS3', // API Namespace
    endPoint);
    // Add query parameters to the URL
    const urlParams = new URLSearchParams(params).toString();
    if (urlParams) {
        requestUrl += `?${urlParams}`;
    }
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");

// import {
//   IFileBrowserFactory
// } from '@jupyterlab/filebrowser';



/**
 * Initialization data for the jupS3 extension.
 */
const plugin = {
    id: 'jupS3:plugin',
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate: (app, settingRegistry) => {
        console.log('JupyterLab extension jupS3 is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupS3 settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupS3.', reason);
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('get-example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The jupS3 server extension appears to be missing.\n${reason}`);
        });
        const content = new S3BrowserWidget();
        // @ts-ignore
        const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
        widget.title.label = 'AURIN Data Browser';
        app.shell.add(widget, 'left');
    }
};
class S3BrowserWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super();
        this.addClass('jp-S3BrowserWidget');
        this.id = 's3-browser-widget';
        this.title.label = 'S3 Browser';
        this.title.closable = true;
        this.node.innerHTML = `
      <div>
        <img src="https://aurin.org.au/wp-content/uploads/2016/12/AURIN-ORG-AU-1.jpg" 
            width="214.4" 
            height="100" 
        />
        <h2 style="text-align:center;">AURIN Data</h2>
        <hr>
        <p style="font-style:italic;text-decoration:underline;">Right click any data file to save it to your home directory on the server:</p>
        <hr>
        <ul id="s3-contents"></ul>
        <ul id="s3-contents" class="jp-DirListing-content"></ul>
        <hr>
      </div>
    `;
        (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('get-bucket-contents')
            .then(data => {
            const ul = this.node.querySelector('#s3-contents');
            data.data.forEach((item) => {
                const li = document.createElement('li');
                li.classList.add('jp-DirListing-item');
                li.addEventListener('contextmenu', this.handleRightClick.bind(this));
                li.textContent = item;
                ul.appendChild(li);
            });
        })
            .catch(reason => {
            console.error(`Error getting S3 bucket contents.\n${reason}`);
        });
    }
    handleRightClick(event) {
        event.preventDefault();
        const target = event.target;
        if (target && target.tagName === 'LI') {
            console.log('Right-clicked item text:', target.textContent);
        }
        const contextMenu = this.createContextMenu(target.textContent);
        document.body.appendChild(contextMenu);
        contextMenu.style.top = `${event.clientY}px`;
        contextMenu.style.left = `${event.clientX}px`;
        const removeContextMenu = () => {
            document.body.removeChild(contextMenu);
            document.removeEventListener('click', removeContextMenu);
        };
        document.addEventListener('click', removeContextMenu);
    }
    createContextMenu(textContent) {
        const menu = document.createElement('ul');
        menu.classList.add('context-menu');
        const menuItem = document.createElement('li');
        menuItem.textContent = 'Checkout to your home directory';
        menuItem.addEventListener('click', (e) => {
            console.log('clicked:', textContent);
            const params = { file: textContent || '' }; // Example parameter
            (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPIWithParams)('create-or-append-to-file', {}, params)
                .then(data => {
                console.log(data);
            })
                .catch(reason => {
                console.error(`The jupS3 server extension appears to be missing.\n${reason}`);
            });
        });
        menu.appendChild(menuItem);
        return menu;
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.dc9a113678683e3d84c1.js.map