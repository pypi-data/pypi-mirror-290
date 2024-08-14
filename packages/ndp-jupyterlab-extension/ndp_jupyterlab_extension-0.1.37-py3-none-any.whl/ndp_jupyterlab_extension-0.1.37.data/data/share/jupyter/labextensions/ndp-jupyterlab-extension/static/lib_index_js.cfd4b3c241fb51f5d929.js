"use strict";
(self["webpackChunkndp_jupyterlab_extension"] = self["webpackChunkndp_jupyterlab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/buttons.js":
/*!************************!*\
  !*** ./lib/buttons.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createButton: () => (/* binding */ createButton),
/* harmony export */   createDownloadButton: () => (/* binding */ createDownloadButton),
/* harmony export */   createDownloadSelectedResourcesButton: () => (/* binding */ createDownloadSelectedResourcesButton),
/* harmony export */   createFileManagerButton: () => (/* binding */ createFileManagerButton),
/* harmony export */   createGetWorkspacesDataButton: () => (/* binding */ createGetWorkspacesDataButton),
/* harmony export */   createGitExtensionButton: () => (/* binding */ createGitExtensionButton),
/* harmony export */   createInstallButton: () => (/* binding */ createInstallButton)
/* harmony export */ });
function createButton(text, className, onClickHandler) {
    const button = document.createElement('button');
    button.textContent = text;
    button.className = className;
    button.addEventListener('click', onClickHandler);
    return button;
}
function createFileManagerButton(widget) {
    return createButton('File Manager', 'ndp-button', widget._onGoToFileManagerButtonClick.bind(widget));
}
function createGitExtensionButton(widget) {
    return createButton('GIT Extension', 'ndp-button', widget._onGoToGitExtensionButtonClick.bind(widget));
}
function createDownloadButton(widget) {
    return createButton('Download All Resources', 'ndp-button', widget._onButtonDownloadClick.bind(widget));
}
function createInstallButton(widget) {
    return createButton('Install requirements.txt', 'ndp-button', widget._onButtonInstallClick.bind(widget));
}
function createGetWorkspacesDataButton(widget) {
    return createButton('Refresh', 'ndp-button', widget._onButtonGetWorkspacesDataClick.bind(widget));
}
function createDownloadSelectedResourcesButton(widget) {
    return createButton('Download Selected Resources', 'ndp-button', widget._onButtonDownloadSelectedResourcesClick.bind(widget));
}


/***/ }),

/***/ "./lib/checkboxes.js":
/*!***************************!*\
  !*** ./lib/checkboxes.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getSelectedResourcesLinks: () => (/* binding */ getSelectedResourcesLinks),
/* harmony export */   populateCheckboxes: () => (/* binding */ populateCheckboxes)
/* harmony export */ });
function populateCheckboxes(widget, datasetResources) {
    console.log(datasetResources);
    // Clear any existing checkboxes
    widget.checkboxContainer.innerHTML = '';
    // datasetResources is list of dicts
    datasetResources.forEach(resource => {
        const checkboxWrapper = document.createElement('div');
        checkboxWrapper.className = 'checkbox-wrapper';
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = resource.name;
        checkbox.value = resource.name;
        const label = document.createElement('label');
        label.htmlFor = resource.name;
        label.textContent = resource.name;
        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(label);
        widget.checkboxContainer.appendChild(checkboxWrapper);
    });
}
function getSelectedResourceLink(widget, datasetResources) {
    const selectedLinks = {};
    // Iterate over all checkboxes in the container
    const checkboxes = widget.checkboxContainer.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        const inputElement = checkbox;
        if (inputElement.checked) {
            const resource = datasetResources.find(res => res.name === inputElement.value);
            if (resource) {
                selectedLinks[resource.name] = resource.url;
            }
        }
    });
    return selectedLinks;
}
function getSelectedResourcesLinks(widget) {
    const selectedDatasetName = widget.dropdownDatasets.value;
    const selectedWorkspaceName = widget.dropdownWorkspaces.value;
    const selectedWorkspace = widget.workspaces.find(workspace => workspace.workspace_name === selectedWorkspaceName);
    const selectedDataset = selectedWorkspace === null || selectedWorkspace === void 0 ? void 0 : selectedWorkspace.datasets.find(dataset => dataset.dataset_name === selectedDatasetName);
    if (selectedDataset) {
        return getSelectedResourceLink(widget, selectedDataset.dataset_resources);
    }
    return [];
}


/***/ }),

/***/ "./lib/dropdowns.js":
/*!**************************!*\
  !*** ./lib/dropdowns.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createDropdownDatasets: () => (/* binding */ createDropdownDatasets),
/* harmony export */   createDropdownWorkspaces: () => (/* binding */ createDropdownWorkspaces),
/* harmony export */   updateDatasetsDropdown: () => (/* binding */ updateDatasetsDropdown),
/* harmony export */   updateWorkspacesDropdown: () => (/* binding */ updateWorkspacesDropdown)
/* harmony export */ });
/* harmony import */ var _checkboxes__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./checkboxes */ "./lib/checkboxes.js");

function createDropdownWorkspaces() {
    const dropdownWorkspaces = document.createElement('select');
    dropdownWorkspaces.id = 'dropdown-workspaces';
    dropdownWorkspaces.className = 'ndp-dropdown';
    dropdownWorkspaces.ariaPlaceholder = '1';
    return dropdownWorkspaces;
}
function updateWorkspacesDropdown(widget) {
    widget.dropdownWorkspaces.innerHTML = '';
    const sortedWorkspaces = widget.workspaces.sort((a, b) => a.workspace_name.localeCompare(b.workspace_name));
    sortedWorkspaces.forEach((workspace) => {
        const option = document.createElement('option');
        option.value = workspace.workspace_name;
        option.textContent = workspace.workspace_name;
        widget.dropdownWorkspaces.appendChild(option);
        // Populate the second dropdown if the selected workspace is found
        updateDatasetsDropdown(widget);
    });
}
function createDropdownDatasets() {
    const dropdownDatasets = document.createElement('select');
    dropdownDatasets.className = 'ndp-dropdown';
    dropdownDatasets.id = 'dropdown-datasets';
    return dropdownDatasets;
}
function updateDatasetsDropdown(widget) {
    // Get the selected option value
    const selectedWorkspaceName = widget.dropdownWorkspaces.value;
    // Find the selected workspace
    const selectedWorkspace = widget.workspaces.find(workspace => workspace.workspace_name === selectedWorkspaceName);
    if (selectedWorkspace) {
        // Clear the second dropdown options
        widget.dropdownDatasets.innerHTML = '';
        // Sort alphabetically
        const sortedDatasets = selectedWorkspace.datasets.sort((a, b) => a.dataset_name.localeCompare(b.dataset_name));
        sortedDatasets.forEach((dataset) => {
            const option = document.createElement('option');
            option.value = dataset.dataset_name;
            option.textContent = dataset.dataset_name;
            widget.dropdownDatasets.appendChild(option);
        });
        // Populate checkboxes with the first dataset's resources
        if (sortedDatasets.length > 0) {
            (0,_checkboxes__WEBPACK_IMPORTED_MODULE_0__.populateCheckboxes)(widget, sortedDatasets[0].dataset_resources);
        }
        // if no datasets selected, no checkboxes should be shown
        else {
            widget.checkboxContainer.innerHTML = '';
        }
    }
}


/***/ }),

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
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _dropdowns__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./dropdowns */ "./lib/dropdowns.js");
/* harmony import */ var _buttons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./buttons */ "./lib/buttons.js");
/* harmony import */ var _checkboxes__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./checkboxes */ "./lib/checkboxes.js");
// widget.ts







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
        defaultBrowser.model.pathChanged.connect((sender, args) => {
            const currentPath = this.fileBrowser.model.path;
            this.updatePathDisplay(currentPath);
        });
        // Use imported functions to create dropdowns
        this.dropdownWorkspaces = (0,_dropdowns__WEBPACK_IMPORTED_MODULE_3__.createDropdownWorkspaces)();
        this.dropdownDatasets = (0,_dropdowns__WEBPACK_IMPORTED_MODULE_3__.createDropdownDatasets)();
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
        // Adding headers
        const headerUtilities = document.createElement('div');
        headerUtilities.textContent = 'Utilities';
        headerUtilities.className = 'headers';
        headerUtilities.style.paddingTop = '0px';
        const headerActions = document.createElement('div');
        headerActions.textContent = 'Actions for Current Folder';
        headerActions.className = 'headers';
        const headerWorkspace = document.createElement('div');
        headerWorkspace.textContent = 'My Workspaces';
        headerWorkspace.className = 'headers';
        const headerDatasets = document.createElement('div');
        headerDatasets.textContent = 'Datasets';
        headerDatasets.className = 'headers';
        const headerCheckboxes = document.createElement('div');
        headerCheckboxes.textContent = 'Dataset Resources';
        headerCheckboxes.className = 'headers';
        container.appendChild(headerUtilities);
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createFileManagerButton)(this));
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createGitExtensionButton)(this));
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createInstallButton)(this));
        container.appendChild(headerWorkspace);
        container.appendChild(this.dropdownWorkspaces);
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createGetWorkspacesDataButton)(this));
        container.appendChild(headerDatasets);
        container.appendChild(this.dropdownDatasets);
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createDownloadButton)(this));
        // Create a div for the checkboxes and append it to the container
        this.checkboxContainer = document.createElement('div');
        this.checkboxContainer.className = 'checkbox-container';
        container.appendChild(headerCheckboxes);
        container.appendChild(this.checkboxContainer);
        container.appendChild((0,_buttons__WEBPACK_IMPORTED_MODULE_4__.createDownloadSelectedResourcesButton)(this));
        // Append the elements to the widget's DOM node
        this.node.appendChild(ndpLink);
        this.node.appendChild(container);
        this.node.appendChild(this.spinnerContainer);
        this.pathDisplayContainer.appendChild(this.pathDisplayTitle);
        this.pathDisplayContainer.appendChild(this.pathDisplay);
        this.node.appendChild(this.pathDisplayContainer);
        this._getWorkspacesData();
        // Add event listener to the namespaces dropdown
        this.dropdownWorkspaces.addEventListener('change', () => {
            (0,_dropdowns__WEBPACK_IMPORTED_MODULE_3__.updateDatasetsDropdown)(this);
        });
        // Add event listener to the datasets dropdown
        this.dropdownDatasets.addEventListener('change', () => {
            const selectedDatasetName = this.dropdownDatasets.value;
            const selectedWorkspaceName = this.dropdownWorkspaces.value;
            const selectedWorkspace = this.workspaces.find(workspace => workspace.workspace_name === selectedWorkspaceName);
            const selectedDataset = selectedWorkspace === null || selectedWorkspace === void 0 ? void 0 : selectedWorkspace.datasets.find(dataset => dataset.dataset_name === selectedDatasetName);
            // if dataset is selected, update resouces checkboxes
            if (selectedDataset) {
                console.log('Selected Dataset');
                (0,_checkboxes__WEBPACK_IMPORTED_MODULE_5__.populateCheckboxes)(this, selectedDataset.dataset_resources);
            }
        });
    }
    // end of constructor
    _onGoToFileManagerButtonClick(event) {
        this.commands.execute('filebrowser:activate');
    }
    _onGoToGitExtensionButtonClick(event) {
        this.commands.execute('git:clone');
    }
    async _onButtonDownloadClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        // Get value from datasets dropdown
        const selectedDataset = this.dropdownDatasets.value;
        console.log('Making request to JupyterLab API: Download');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('download_datasets', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath, dataset: selectedDataset })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`Server Extension Error\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _onButtonInstallClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        console.log('Making request to JupyterLab API: Install');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('install_requirements', {
                method: 'POST',
                body: JSON.stringify({ path: currentPath })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`Server Extension Error\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _getWorkspacesData() {
        console.log('Making request to JupyterLab API: Workspaces');
        try {
            this.workspaces = await (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('get_workspaces_data', {
                method: 'GET'
            });
            console.log(this.workspaces);
            (0,_dropdowns__WEBPACK_IMPORTED_MODULE_3__.updateWorkspacesDropdown)(this);
        }
        catch (error) {
            console.error('Error fetching workspaces:', error);
        }
    }
    async _onButtonGetWorkspacesDataClick(event) {
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        try {
            this._getWorkspacesData();
        }
        catch (reason) {
            console.error(`Server Extension Error\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    async _onButtonDownloadSelectedResourcesClick(event) {
        const resources = (0,_checkboxes__WEBPACK_IMPORTED_MODULE_5__.getSelectedResourcesLinks)(this);
        console.log();
        this.spinner.style.display = 'block'; // Show spinner
        // Get the current path from the file manager
        const currentPath = this.fileBrowser.model.path;
        // Get value from datasets dropdown
        const selectedDataset = this.dropdownDatasets.value;
        console.log('Making request to JupyterLab API: Download');
        try {
            const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('download_datasets', {
                method: 'POST',
                body: JSON.stringify({
                    path: currentPath,
                    dataset: selectedDataset,
                    resources: resources
                })
            });
            console.log(data);
        }
        catch (reason) {
            console.error(`Server Extension Error\n${reason}`);
        }
        finally {
            this.spinner.style.display = 'none'; // Hide spinner
        }
    }
    updatePathDisplay(path) {
        const currentPath = path || this.fileBrowser.model.path;
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
//# sourceMappingURL=lib_index_js.cfd4b3c241fb51f5d929.js.map