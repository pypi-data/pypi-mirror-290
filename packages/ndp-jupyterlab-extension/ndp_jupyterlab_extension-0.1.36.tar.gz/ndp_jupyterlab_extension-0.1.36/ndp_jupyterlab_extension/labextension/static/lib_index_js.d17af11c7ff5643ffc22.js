"use strict";
(self["webpackChunkndp_jupyterlab_extension"] = self["webpackChunkndp_jupyterlab_extension"] || []).push([["lib_index_js"],{

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
/* harmony export */   NDPWidget: () => (/* binding */ NDPWidget),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_ndp_landing_image_png__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/ndp-landing-image.png */ "./style/ndp-landing-image.png");
/* harmony import */ var _style_ndp_logo_png__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/ndp_logo.png */ "./style/ndp_logo.png");



// import '../styles/styles.css'; // Import the CSS file
// interface Workspace {
//   workspace_name: string;
//   datasets: string[];
// }
class NDPWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    // private workspaces: Workspace[] = [];
    constructor(defaultBrowser, commands) {
        super();
        this.commands = commands;
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
        const settingsWidget = this.createSettingsWidget();
        settingsWidget.title.label = 'Settings';
        tabPanel.addWidget(homeWidget);
        tabPanel.addWidget(settingsWidget);
        tabPanel.id = 'tab-panel';
        tabPanel.tabBar.currentIndex = 1;
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
        // Create a button element to go to the file manager
        const buttonFileManager = document.createElement('button');
        buttonFileManager.textContent = 'File Manager';
        buttonFileManager.className = 'ndp-button';
        buttonFileManager.addEventListener('click', this._onGoToFileManagerButtonClick.bind(this));
        this.dropdownWorkspaces = document.createElement('select');
        this.dropdownWorkspaces.id = 'dropdown-workspaces';
        this.dropdownWorkspaces.className = 'ndp-dropdown'; // Apply CSS class
        this.dropdownDatasets = document.createElement('select');
        this.dropdownDatasets.id = 'dropdown-datasets';
        this.dropdownDatasets.className = 'ndp-dropdown'; // Apply CSS class
        // Initialize the spinner element
        this.spinner = document.createElement('div');
        this.spinnerContainer.className = 'spinner-container';
        this.spinner.className = 'spinner';
        this.spinner.style.display = 'none'; // Hide spinner initially
        this.pathDisplayContainer.className = 'path-display-container';
        this.pathDisplayTitle.className = 'path-display-title';
        this.pathDisplayTitle.textContent = 'Current Folder:';
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
    createSettingsWidget() {
        const settingsContainer = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        settingsContainer.addClass('ndp-tab-content');
        settingsContainer.node.textContent = 'Settings content goes here.';
        return settingsContainer;
    }
    /**
     * Callback on click on the go to file manager button
     */
    _onGoToFileManagerButtonClick(event) {
        this.commands.execute('filebrowser:activate');
    }
    /**
     * Update the path display element
     */
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
// Register the plugin with JupyterLab
const extension = {
    id: 'ndp-extension',
    autoStart: true,
    activate: (app, browser) => {
        console.log('NDP extension activated');
        const widget = new NDPWidget(browser, app.commands);
        app.shell.add(widget, 'left', { rank: 1000 });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


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
//# sourceMappingURL=lib_index_js.d17af11c7ff5643ffc22.js.map