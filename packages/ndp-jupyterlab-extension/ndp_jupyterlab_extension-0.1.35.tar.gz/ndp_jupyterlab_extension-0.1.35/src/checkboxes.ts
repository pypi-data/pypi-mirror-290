import { NDPWidget } from './widget';

interface Resource {
  name: string;
  url: string;
}

export function populateCheckboxes(
  widget: NDPWidget,
  datasetResources: Array<Resource>
) {
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

function getSelectedResourceLink(
  widget: NDPWidget,
  datasetResources: Array<Resource>
): object {
  const selectedLinks: { [key: string]: string } = {};

  // Iterate over all checkboxes in the container
  const checkboxes = widget.checkboxContainer.querySelectorAll(
    'input[type="checkbox"]'
  );
  checkboxes.forEach(checkbox => {
    const inputElement = checkbox as HTMLInputElement;
    if (inputElement.checked) {
      const resource = datasetResources.find(
        res => res.name === inputElement.value
      );
      if (resource) {
        selectedLinks[resource.name] = resource.url;
      }
    }
  });

  return selectedLinks;
}

export function getSelectedResourcesLinks(widget: NDPWidget): object {
  const selectedDatasetName = widget.dropdownDatasets.value;
  const selectedWorkspaceName = widget.dropdownWorkspaces.value;
  const selectedWorkspace = widget.workspaces.find(
    workspace => workspace.workspace_name === selectedWorkspaceName
  );
  const selectedDataset = selectedWorkspace?.datasets.find(
    dataset => dataset.dataset_name === selectedDatasetName
  );

  if (selectedDataset) {
    return getSelectedResourceLink(widget, selectedDataset.dataset_resources);
  }
  return [];
}
