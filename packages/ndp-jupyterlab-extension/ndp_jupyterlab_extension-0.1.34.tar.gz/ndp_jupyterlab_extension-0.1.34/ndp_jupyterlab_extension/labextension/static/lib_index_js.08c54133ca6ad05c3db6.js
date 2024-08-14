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
/* harmony import */ var _style_ndp_landing_image_png__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/ndp-landing-image.png */ "./style/ndp-landing-image.png");
/* harmony import */ var _style_ndp_logo_png__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/ndp_logo.png */ "./style/ndp_logo.png");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");




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
        // Initialize the properties
        this.spinnerContainer = document.createElement('div');
        this.pathDisplayContainer = document.createElement('div');
        this.pathDisplayTitle = document.createElement('div');
        this.pathDisplay = document.createElement('div');
        this.spinner = document.createElement('div');
        this.dropdownWorkspaces = document.createElement('select');
        this.dropdownDatasets = document.createElement('select');
        // Create the TabPanel
        const tabPanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.TabPanel();
        tabPanel.addClass('ndp-tab-panel');
        const homeWidget = this.createHomeWidget();
        homeWidget.title.label = 'Home';
        // const settingsWidget = this.createSettingsWidget();
        tabPanel.addWidget(homeWidget);
        // tabPanel.addWidget(settingsWidget);
        // tabPanel.tabBar.addTab({ title: { label: 'Home' } });
        // tabPanel.tabBar.addTab({ title: { label: 'Settings' } });
        tabPanel.id = 'tab-panel';
        tabPanel.tabBar.currentIndex = 0;
        this.node.appendChild(tabPanel.node);
    }
    createHomeWidget() {
        const homeContainer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        homeContainer.addClass('ndp-tab-content');
        // Create an image element for the map
        const ndpMapImg = document.createElement('img');
        ndpMapImg.src = _style_ndp_landing_image_png__WEBPACK_IMPORTED_MODULE_1__;
        ndpMapImg.className = 'ndp-logo-map';
        // Create an image element for the NDP letters
        const ndpLettersImg = document.createElement('img');
        ndpLettersImg.src = _style_ndp_logo_png__WEBPACK_IMPORTED_MODULE_2__;
        ndpLettersImg.className = 'ndp-logo';
        // Create an anchor element
        const ndpLink = document.createElement('a');
        ndpLink.href = 'https://ndp-test.sdsc.edu';
        ndpLink.target = '_blank'; // to open the link in a new tab
        ndpLink.appendChild(ndpMapImg);
        ndpLink.appendChild(ndpLettersImg);
        // Create a Show Path button element
        this.fileBrowser.model.pathChanged.connect((sender, args) => {
            const currentPath = this.fileBrowser.model.path;
            this.updatePathDisplay(currentPath);
        });
        // Create a button element to go to the file manager
        const buttonFileManager = document.createElement('button');
        buttonFileManager.textContent = 'File Manager';
        buttonFileManager.className = 'ndp-button';
        buttonFileManager.addEventListener('click', this._onGoToFileManagerButtonClick.bind(this));
        // Create a button element to go to the GIT Extension
        const buttonGitExtension = document.createElement('button');
        buttonGitExtension.textContent = 'GIT Extension';
        buttonGitExtension.className = 'ndp-button';
        buttonGitExtension.addEventListener('click', this._onGoToGitExtensionButtonClick.bind(this));
        // Create a Download button element
        const buttonDownload = document.createElement('button');
        buttonDownload.textContent = 'Download Dummy Dataset';
        buttonDownload.className = 'ndp-button';
        buttonDownload.addEventListener('click', this._onButtonDownloadClick.bind(this));
        // Create an Unzip button element
        const buttonUnZip = document.createElement('button');
        buttonUnZip.textContent = 'Extract .zip Files';
        buttonUnZip.className = 'ndp-button';
        buttonUnZip.addEventListener('click', this._onButtonUnzipClick.bind(this));
        // Create an Install Requirements button element
        const buttonInstall = document.createElement('button');
        buttonInstall.textContent = 'Install requirements.txt';
        buttonInstall.className = 'ndp-button';
        buttonInstall.addEventListener('click', this._onButtonInstallClick.bind(this));
        // Create an Get Workspaces Data button element
        const buttonGetWorkspacesData = document.createElement('button');
        buttonGetWorkspacesData.textContent = 'Get My Workspaces';
        buttonGetWorkspacesData.className = 'ndp-button';
        buttonGetWorkspacesData.addEventListener('click', this._onButtonGetWorkspacesDataClick.bind(this));
        this.dropdownWorkspaces = document.createElement('select');
        this.dropdownWorkspaces.id = 'dropdown-workspaces';
        this.dropdownDatasets = document.createElement('select');
        this.dropdownDatasets.id = 'dropdown-datasets';
        // Create a spinner element
        this.spinnerContainer = document.createElement('div');
        this.spinner = document.createElement('div');
        this.spinnerContainer.className = 'spinner-container';
        this.spinner.className = 'spinner';
        this.spinner.style.display = 'none'; // Hide spinner initially
        this.pathDisplayContainer = document.createElement('div');
        this.pathDisplayContainer.className = 'path-display-container';
        this.pathDisplayTitle = document.createElement('div');
        this.pathDisplayTitle.className = 'path-display-title';
        this.pathDisplayTitle.textContent = 'Current Folder:';
        this.pathDisplay = document.createElement('div');
        this.pathDisplay.className = 'path-display-path';
        this.spinnerContainer.appendChild(this.spinner);
        this.pathDisplayContainer.addEventListener('click', this._onGoToFileManagerButtonClick.bind(this));
        // Display the current path
        this.updatePathDisplay();
        // Create a div to center the button and spinner
        const container = document.createElement('div');
        container.className = 'ndp-button-container';
        container.appendChild(buttonFileManager);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(buttonGitExtension);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(buttonDownload);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(buttonUnZip);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(buttonInstall);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(buttonGetWorkspacesData);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(this.dropdownWorkspaces);
        container.appendChild(document.createElement('br')); // Add break line
        container.appendChild(this.dropdownDatasets);
        this.pathDisplayContainer.appendChild(this.pathDisplayTitle);
        this.pathDisplayContainer.appendChild(this.pathDisplay);
        homeContainer.node.appendChild(ndpLink);
        homeContainer.node.appendChild(container);
        homeContainer.node.appendChild(this.spinnerContainer);
        homeContainer.node.appendChild(this.pathDisplayContainer);
        return homeContainer;
    }
    // private createSettingsWidget(): Widget {
    //   const settingsContainer = new Widget();
    //   settingsContainer.addClass('ndp-tab-content');
    //   settingsContainer.node.textContent = 'Settings content goes here.';
    //   return settingsContainer;
    // }
    /**
     * Callback on click on the go to file manager button
     */
    _onGoToFileManagerButtonClick(event) {
        this.commands.execute('filebrowser:activate');
    }
    /**
     * Callback on click on the go to GIT Extension button
     */
    _onGoToGitExtensionButtonClick(event) {
        this.commands.execute('git:ui');
    }
    /**
     * Callback on click on the widget buttons
     */
    async _onButtonDownloadClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        // Get value from datasets dropdown
        const selectedDataset = this.dropdownDatasets.value;
        console.log('Making request to JupyterLab API');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('download_datasets', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath, dataset: selectedDataset })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _onButtonUnzipClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        console.log('Making request to JupyterLab API');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('unzip', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _onButtonInstallClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        console.log('Making request to JupyterLab API');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('install_requirements', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _onButtonGetWorkspacesDataClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        // const currentPath = this.fileBrowser.model.path;
        console.log('Making request to JupyterLab API: Workspaces');
        try {
            this.workspaces = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('get_workspaces_data', {
                method: 'GET'
            });
            console.log(this.workspaces);
            this.dropdownWorkspaces.innerHTML = '';
            // Populate the dropdown with new options
            this.workspaces.forEach((workspace) => {
                const option = document.createElement('option');
                option.value = workspace.workspace_name;
                option.textContent = workspace.workspace_name;
                this.dropdownWorkspaces.appendChild(option);
                // Populate the second dropdown if the selected workspace is found
                this.updateDatasetsDropdown();
            });
            // Add event listener to the first dropdown
            this.dropdownWorkspaces.addEventListener('change', () => {
                this.updateDatasetsDropdown();
            });
        }
        catch (reason) {
            console.error(`The ndp_jupyterlab_extension server extension appears to be missing.\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    updateDatasetsDropdown() {
        // Get the selected option value
        const selectedWorkspaceName = this.dropdownWorkspaces.value;
        // Find the selected workspace
        const selectedWorkspace = this.workspaces.find(workspace => workspace.workspace_name === selectedWorkspaceName);
        if (selectedWorkspace) {
            // Clear the second dropdown options
            this.dropdownDatasets.innerHTML = '';
            selectedWorkspace.datasets.forEach((dataset) => {
                const option = document.createElement('option');
                option.value = dataset;
                option.textContent = dataset;
                this.dropdownDatasets.appendChild(option);
            });
        }
    }
    /**
     * Update the path display element
     */
    updatePathDisplay(path) {
        const currentPath = path || this.fileBrowser.model.path;
        // console.log(currentPath);
        if (currentPath === '') {
            this.pathDisplay.textContent = 'root/';
        }
        else {
            this.pathDisplay.textContent = `root/${currentPath}`;
        }
    }
}


/***/ }),

/***/ "./style/ndp-landing-image.png":
/*!*************************************!*\
  !*** ./style/ndp-landing-image.png ***!
  \*************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "eb6ed1b8570cdd09e208.png";

/***/ }),

/***/ "./style/ndp_logo.png":
/*!****************************!*\
  !*** ./style/ndp_logo.png ***!
  \****************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "75ca306c12e316e98388.png";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.08c54133ca6ad05c3db6.js.map