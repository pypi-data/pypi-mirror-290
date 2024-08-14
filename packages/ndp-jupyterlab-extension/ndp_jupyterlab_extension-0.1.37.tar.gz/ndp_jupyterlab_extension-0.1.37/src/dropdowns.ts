import { NDPWidget } from './widget';
import { populateCheckboxes } from './checkboxes';

interface Resource {
  name: string;
  url: string;
}
interface Dataset {
  dataset_name: string;
  dataset_resources: Array<Resource>;
}

interface GitHubLink {
  url: string;
}

interface Workspace {
  workspace_name: string;
  datasets: [Dataset];
  github_links: Array<GitHubLink>;
}

export function createDropdownWorkspaces() {
  const dropdownWorkspaces = document.createElement('select');
  dropdownWorkspaces.id = 'dropdown-workspaces';
  dropdownWorkspaces.className = 'ndp-dropdown';
  dropdownWorkspaces.ariaPlaceholder = '1';
  return dropdownWorkspaces;
}

export function updateWorkspacesDropdown(widget: NDPWidget) {
  widget.dropdownWorkspaces.innerHTML = '';
  const sortedWorkspaces = widget.workspaces.sort((a, b) =>
    a.workspace_name.localeCompare(b.workspace_name)
  );

  sortedWorkspaces.forEach((workspace: Workspace) => {
    const option = document.createElement('option');
    option.value = workspace.workspace_name;
    option.textContent = workspace.workspace_name;
    widget.dropdownWorkspaces.appendChild(option);
    // Populate the second dropdown if the selected workspace is found
    updateDatasetsDropdown(widget);
    // Populate the third dropdown if the selected workspace is found
    updateGitLinksDropdown(widget);
  });
}

export function createDropdownDatasets() {
  const dropdownDatasets = document.createElement('select');
  dropdownDatasets.className = 'ndp-dropdown';
  dropdownDatasets.id = 'dropdown-datasets';
  return dropdownDatasets;
}

export function createDropdownGitLinks() {
  const dropdownGitLinks = document.createElement('select');
  dropdownGitLinks.className = 'ndp-dropdown';
  dropdownGitLinks.id = 'dropdown-git-links';
  return dropdownGitLinks;
}

export function updateDatasetsDropdown(widget: NDPWidget) {
  // Get the selected option value
  const selectedWorkspaceName = widget.dropdownWorkspaces.value;
  // Find the selected workspace
  const selectedWorkspace = widget.workspaces.find(
    workspace => workspace.workspace_name === selectedWorkspaceName
  );
  if (selectedWorkspace) {
    // Clear the second dropdown options
    widget.dropdownDatasets.innerHTML = '';
    // Sort alphabetically
    const sortedDatasets = selectedWorkspace.datasets.sort((a, b) =>
      a.dataset_name.localeCompare(b.dataset_name)
    );
    sortedDatasets.forEach((dataset: Dataset) => {
      const option = document.createElement('option');
      option.value = dataset.dataset_name;
      option.textContent = dataset.dataset_name;
      widget.dropdownDatasets.appendChild(option);
    });

    // Populate checkboxes with the first dataset's resources
    if (sortedDatasets.length > 0) {
      populateCheckboxes(widget, sortedDatasets[0].dataset_resources);
    }
    // if no datasets selected, no checkboxes should be shown
    else {
      widget.checkboxContainer.innerHTML = '';
    }
  }
}

export function updateGitLinksDropdown(widget: NDPWidget) {
  // Get the selected option value
  const selectedWorkspaceName = widget.dropdownWorkspaces.value;
  // Find the selected workspace
  const selectedWorkspace = widget.workspaces.find(
    workspace => workspace.workspace_name === selectedWorkspaceName
  );
  let gitHubLinks;
  if (selectedWorkspace) {
    // Clear the second dropdown options
    widget.dropdownGitLinks.innerHTML = '';
    // Sort alphabetically
    // const sortedDatasets = selectedWorkspace.github_links.sort((a, b) =>
    //   a.localeCompare(b)
    // );
    gitHubLinks = selectedWorkspace.github_links;
    gitHubLinks.forEach((githubLink: GitHubLink) => {
      const option = document.createElement('option');
      option.value = githubLink.url;
      option.textContent = githubLink.url;
      widget.dropdownGitLinks.appendChild(option);
    });
  }
}
