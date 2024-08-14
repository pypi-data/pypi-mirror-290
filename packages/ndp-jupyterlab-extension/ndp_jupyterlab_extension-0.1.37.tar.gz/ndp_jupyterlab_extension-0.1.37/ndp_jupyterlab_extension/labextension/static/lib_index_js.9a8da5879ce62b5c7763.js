"use strict";
(self["webpackChunkndp_jupyterlab_extension"] = self["webpackChunkndp_jupyterlab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'ndp-jupyterlab-extension', // API Namespace
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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");



/**
 * Initialization data for the main menu example.
 */
const extension = {
    id: '@jupyterlab-examples/main-menu:plugin',
    description: 'Minimal JupyterLab example adding a menu.',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IDefaultFileBrowser, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, defaultBrowser, labShell) => {
        const { commands } = app;
        const widget = new _widget__WEBPACK_IMPORTED_MODULE_2__.NDPWidget(defaultBrowser, commands);
        labShell.add(widget, 'left');
        app.restored.then(() => {
            labShell.activateById(widget.id);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createElementWithClass: () => (/* binding */ createElementWithClass)
/* harmony export */ });
function createElementWithClass(tag, className) {
    const element = document.createElement(tag);
    element.className = className;
    return element;
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NDPWidget: () => (/* binding */ NDPWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _workspaceUtils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./workspaceUtils */ "./lib/workspaceUtils.js");




class NDPWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(defaultBrowser, commands) {
        super();
        this.commands = commands;
        this.workspaces = [];
        this.fileBrowser = defaultBrowser;
        this.addClass('jp-example-view');
        this.id = 'ndp-widget';
        this.title.label = 'NDP';
        this.title.closable = true;
        const ndpLink = this.createNDPLogo();
        defaultBrowser.model.pathChanged.connect((sender, args) => {
            const currentPath = this.fileBrowser.model.path;
            this.updatePathDisplay(currentPath);
        });
        const buttonFileManager = this.createButton('File Manager', this._onGoToFileManagerButtonClick.bind(this));
        const buttonGitExtension = this.createButton('GIT Extension', this._onGoToGitExtensionButtonClick.bind(this));
        const buttonDownload = this.createButton('Download Selected Dataset', this._onButtonDownloadClick.bind(this));
        const buttonInstall = this.createButton('Install requirements.txt', this._onButtonInstallClick.bind(this));
        const buttonGetWorkspacesData = this.createButton('Refresh', this._onButtonGetWorkspacesDataClick.bind(this));
        this.dropdownWorkspaces = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('select', 'ndp-dropdown');
        this.dropdownDatasets = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('select', 'ndp-dropdown');
        this.spinnerContainer = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'spinner-container');
        this.spinner = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'spinner');
        this.spinner.style.display = 'none';
        this.pathDisplayContainer = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'path-display-container');
        this.pathDisplayTitle = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'path-display-title');
        this.pathDisplayTitle.textContent = 'Current Folder:';
        this.pathDisplay = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'path-display-path');
        this.spinnerContainer.appendChild(this.spinner);
        this.pathDisplayContainer.addEventListener('click', this._onGoToFileManagerButtonClick.bind(this));
        this.updatePathDisplay();
        const container = this.createContainer([
            this.createHeader('Utilities'),
            buttonFileManager,
            buttonGitExtension,
            buttonInstall,
            this.createHeader('My Current Workspace'),
            this.dropdownWorkspaces,
            buttonGetWorkspacesData,
            this.createHeader('Items in the Current Workspace'),
            this.dropdownDatasets,
            buttonDownload
        ]);
        this.node.appendChild(ndpLink);
        this.node.appendChild(container);
        this.node.appendChild(this.spinnerContainer);
        this.pathDisplayContainer.appendChild(this.pathDisplayTitle);
        this.pathDisplayContainer.appendChild(this.pathDisplay);
        this.node.appendChild(this.pathDisplayContainer);
        this._getWorkspacesData();
        this.dropdownWorkspaces.addEventListener('change', () => {
            this.updateDatasetsDropdown();
        });
    }
    createNDPLogo() {
        const ndpMapImg = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('img', 'ndp-logo-map');
        ndpMapImg.src = '../style/ndp-landing-image.png';
        const ndpLettersImg = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('img', 'ndp-logo');
        ndpLettersImg.src = '../style/ndp_logo.png';
        const ndpLink = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('a', '');
        ndpLink.href = 'https://ndp-test.sdsc.edu';
        ndpLink.target = '_blank';
        ndpLink.appendChild(ndpMapImg);
        ndpLink.appendChild(ndpLettersImg);
        return ndpLink;
    }
    createButton(text, onClick) {
        const button = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('button', 'ndp-button');
        button.textContent = text;
        button.addEventListener('click', onClick);
        return button;
    }
    createHeader(text) {
        const header = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'headers');
        header.textContent = text;
        return header;
    }
    createContainer(elements) {
        const container = (0,_utils__WEBPACK_IMPORTED_MODULE_1__.createElementWithClass)('div', 'ndp-button-container');
        elements.forEach(element => container.appendChild(element));
        return container;
    }
    _onGoToFileManagerButtonClick(event) {
        this.commands.execute('filebrowser:activate');
    }
    _onGoToGitExtensionButtonClick(event) {
        this.commands.execute('git:ui');
    }
    async _onButtonDownloadClick(event) {
        this.spinner.style.display = 'block';
        const currentPath = this.fileBrowser.model.path;
        const selectedDataset = this.dropdownDatasets.value;
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('download_datasets', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath, dataset: selectedDataset })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none';
        }
    }
    async _onButtonInstallClick(event) {
        this.spinner.style.display = 'block';
        const currentPath = this.fileBrowser.model.path;
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('install_requirements', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none';
        }
    }
    async _getWorkspacesData() {
        try {
            this.workspaces = await (0,_workspaceUtils__WEBPACK_IMPORTED_MODULE_3__.fetchWorkspaces)();
            this.updateWorkspacesDropdown();
        }
        catch (error) {
            console.error('Error fetching workspaces:', error);
        }
    }
    async _onButtonGetWorkspacesDataClick(event) {
        this.spinner.style.display = 'block';
        try {
            await this._getWorkspacesData();
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none';
        }
    }
    updateWorkspacesDropdown() {
        this.dropdownWorkspaces.innerHTML = '';
        const sortedWorkspaces = this.workspaces.sort((a, b) => a.workspace_name.localeCompare(b.workspace_name));
        sortedWorkspaces.forEach(workspace => {
            const option = document.createElement('option');
            option.value = workspace.workspace_name;
            option.textContent = workspace.workspace_name;
            this.dropdownWorkspaces.appendChild(option);
        });
        this.updateDatasetsDropdown();
    }
    updateDatasetsDropdown() {
        const selectedWorkspaceName = this.dropdownWorkspaces.value;
        const selectedWorkspace = this.workspaces.find(workspace => workspace.workspace_name === selectedWorkspaceName);
        if (selectedWorkspace) {
            this.dropdownDatasets.innerHTML = '';
            const sortedDatasets = selectedWorkspace.datasets.sort((a, b) => a.localeCompare(b));
            sortedDatasets.forEach(dataset => {
                const option = document.createElement('option');
                option.value = dataset;
                option.textContent = dataset;
                this.dropdownDatasets.appendChild(option);
            });
        }
    }
    updatePathDisplay(path) {
        const currentPath = path || this.fileBrowser.model.path;
        this.pathDisplay.textContent =
            currentPath === '' ? 'root/' : `root/${currentPath}`;
    }
}


/***/ }),

/***/ "./lib/workspaceUtils.js":
/*!*******************************!*\
  !*** ./lib/workspaceUtils.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   fetchWorkspaces: () => (/* binding */ fetchWorkspaces)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");

async function fetchWorkspaces() {
    try {
        const workspaces = await (0,_handler__WEBPACK_IMPORTED_MODULE_0__.requestAPI)('get_workspaces_data', {
            method: 'GET'
        });
        return workspaces;
    }
    catch (error) {
        console.error('Error fetching workspaces:', error);
        throw error;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.9a8da5879ce62b5c7763.js.map