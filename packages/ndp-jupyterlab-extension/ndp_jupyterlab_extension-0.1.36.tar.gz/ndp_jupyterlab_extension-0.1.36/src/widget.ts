// widget.ts
import { Widget } from '@lumino/widgets';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import ndp_map_path from '../style/ndp-landing-image.png';
import ndp_letters_path from '../style/ndp_logo.png';
import { requestAPI } from './handler';
import { JupyterFrontEnd } from '@jupyterlab/application';
import {
  createDropdownWorkspaces,
  createDropdownDatasets,
  updateWorkspacesDropdown,
  updateDatasetsDropdown
} from './dropdowns';
import {
  createFileManagerButton,
  createGitExtensionButton,
  createDownloadButton,
  createInstallButton,
  createGetWorkspacesDataButton,
  createDownloadSelectedResourcesButton, createGitCloneButton
} from './buttons';
import { getSelectedResourcesLinks, populateCheckboxes } from './checkboxes';
// import { createCheckboxes } from './checkboxes';

interface Resource {
  name: string;
  url: string;
}
interface Dataset {
  dataset_name: string;
  dataset_resources: Array<Resource>;
}
interface Workspace {
  workspace_name: string;
  datasets: [Dataset];
}

export class NDPWidget extends Widget {
  private spinner: HTMLElement;
  public dropdownWorkspaces: HTMLSelectElement;
  public dropdownDatasets: HTMLSelectElement;
  fileBrowser: IDefaultFileBrowser;
  private pathDisplay: HTMLDivElement;
  private spinnerContainer: HTMLDivElement;
  private pathDisplayTitle;
  private pathDisplayContainer: HTMLDivElement;
  public workspaces: Workspace[] = [];
  checkboxContainer: HTMLDivElement;

  constructor(
    defaultBrowser: IDefaultFileBrowser,
    public commands: JupyterFrontEnd['commands']
  ) {
    super();
    this.fileBrowser = defaultBrowser;

    this.addClass('jp-example-view');
    this.id = 'ndp-widget';
    this.title.label = 'NDP';
    this.title.closable = true;

    // Create an image element for the map
    const ndpMapImg = document.createElement('img');
    ndpMapImg.src = ndp_map_path;
    ndpMapImg.className = 'ndp-logo-map';

    // Create an image element for the NDP letters
    const ndpLettersImg = document.createElement('img');
    ndpLettersImg.src = ndp_letters_path;
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
    this.dropdownWorkspaces = createDropdownWorkspaces();
    this.dropdownDatasets = createDropdownDatasets();

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
    this.pathDisplayContainer.addEventListener(
      'click',
      this._onGoToFileManagerButtonClick.bind(this)
    );

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
    container.appendChild(createFileManagerButton(this));
    container.appendChild(createGitExtensionButton(this));
    container.appendChild(createGitCloneButton(this));
    container.appendChild(createInstallButton(this));
    container.appendChild(headerWorkspace);
    container.appendChild(this.dropdownWorkspaces);
    container.appendChild(createGetWorkspacesDataButton(this));
    container.appendChild(headerDatasets);
    container.appendChild(this.dropdownDatasets);
    container.appendChild(createDownloadButton(this));

    // Create a div for the checkboxes and append it to the container
    this.checkboxContainer = document.createElement('div');
    this.checkboxContainer.className = 'checkbox-container';

    container.appendChild(headerCheckboxes);
    container.appendChild(this.checkboxContainer);
    container.appendChild(createDownloadSelectedResourcesButton(this));

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
      updateDatasetsDropdown(this);
    });

    // Add event listener to the datasets dropdown
    this.dropdownDatasets.addEventListener('change', () => {
      const selectedDatasetName = this.dropdownDatasets.value;
      const selectedWorkspaceName = this.dropdownWorkspaces.value;
      const selectedWorkspace = this.workspaces.find(
        workspace => workspace.workspace_name === selectedWorkspaceName
      );
      const selectedDataset = selectedWorkspace?.datasets.find(
        dataset => dataset.dataset_name === selectedDatasetName
      );
      // if dataset is selected, update resouces checkboxes
      if (selectedDataset) {
        console.log('Selected Dataset');
        populateCheckboxes(this, selectedDataset.dataset_resources);
      }
    });
  }
  // end of constructor
  _onGoToFileManagerButtonClick(event: Event): void {
    this.commands.execute('filebrowser:activate');
  }

  _onGoToGitExtensionButtonClick(event: Event): void {
    this.commands.execute('git:ui');
  }

  async _onButtonDownloadClick(event: Event): Promise<void> {
    this.spinner.style.display = 'block'; // Show spinner
    // Get the current path from the file manager
    const currentPath = this.fileBrowser.model.path;

    // Get value from datasets dropdown
    const selectedDataset = this.dropdownDatasets.value;

    console.log('Making request to JupyterLab API: Download');
    try {
      const data = await requestAPI<any>('download_datasets', {
        method: 'POST',
        body: JSON.stringify({ path: currentPath, dataset: selectedDataset })
      });
      console.log(data);
    } catch (reason) {
      console.error(`Server Extension Error\n${reason}`);
    } finally {
      this.spinner.style.display = 'none'; // Hide spinner
    }
  }

  async _onButtonInstallClick(event: Event): Promise<void> {
    this.spinner.style.display = 'block'; // Show spinner
    // Get the current path from the file manager
    const currentPath = this.fileBrowser.model.path;
    console.log('Making request to JupyterLab API: Install');
    try {
      const data = await requestAPI<any>('install_requirements', {
        method: 'POST',
        body: JSON.stringify({ path: currentPath })
      });
      console.log(data);
    } catch (reason) {
      console.error(`Server Extension Error\n${reason}`);
    } finally {
      this.spinner.style.display = 'none'; // Hide spinner
    }
  }

  private async _getWorkspacesData(): Promise<void> {
    console.log('Making request to JupyterLab API: Workspaces');
    try {
      this.workspaces = await requestAPI<Workspace[]>('get_workspaces_data', {
        method: 'GET'
      });
      console.log(this.workspaces);

      updateWorkspacesDropdown(this);
    } catch (error) {
      console.error('Error fetching workspaces:', error);
    }
  }

  async _onButtonGetWorkspacesDataClick(event: Event): Promise<void> {
    this.spinner.style.display = 'block'; // Show spinner
    // Get the current path from the file manager
    try {
      this._getWorkspacesData();
    } catch (reason) {
      console.error(`Server Extension Error\n${reason}`);
    } finally {
      this.spinner.style.display = 'none'; // Hide spinner
    }
  }

  async _onButtonDownloadSelectedResourcesClick(event: Event): Promise<void> {
    const resources = getSelectedResourcesLinks(this);
    console.log();
    this.spinner.style.display = 'block'; // Show spinner
    // Get the current path from the file manager
    const currentPath = this.fileBrowser.model.path;

    // Get value from datasets dropdown
    const selectedDataset = this.dropdownDatasets.value;

    console.log('Making request to JupyterLab API: Download');
    try {
      const data = await requestAPI<any>('download_datasets', {
        method: 'POST',
        body: JSON.stringify({
          path: currentPath,
          dataset: selectedDataset,
          resources: resources
        })
      });
      console.log(data);
    } catch (reason) {
      console.error(`Server Extension Error\n${reason}`);
    } finally {
      this.spinner.style.display = 'none'; // Hide spinner
    }
  }
  private updatePathDisplay(path?: string): void {
    const currentPath = path || this.fileBrowser.model.path;
    if (currentPath === '') {
      this.pathDisplay.textContent = 'root/';
    } else {
      this.pathDisplay.textContent = `root/${currentPath}`;
    }
  }
}
