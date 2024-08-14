// buttons.ts
import { NDPWidget } from './widget';
import { showDialog, Dialog } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';

export function createButton(
  text: string,
  className: string,
  onClickHandler: (event: Event) => void
) {
  const button = document.createElement('button');
  button.textContent = text;
  button.className = className;
  button.addEventListener('click', onClickHandler);
  return button;
}

export function createFileManagerButton(widget: NDPWidget) {
  return createButton(
    'File Manager',
    'ndp-button',
    widget._onGoToFileManagerButtonClick.bind(widget)
  );
}

export function createGitExtensionButton(widget: NDPWidget) {
  return createButton(
    'GIT Extension',
    'ndp-button',
    widget._onGoToGitExtensionButtonClick.bind(widget)
  );
}

export function createDownloadButton(widget: NDPWidget) {
  return createButton(
    'Download All Resources',
    'ndp-button',
    widget._onButtonDownloadClick.bind(widget)
  );
}

export function createInstallButton(widget: NDPWidget) {
  return createButton(
    'Install requirements.txt',
    'ndp-button',
    widget._onButtonInstallClick.bind(widget)
  );
}

export function createGetWorkspacesDataButton(widget: NDPWidget) {
  return createButton(
    'Refresh',
    'ndp-button',
    widget._onButtonGetWorkspacesDataClick.bind(widget)
  );
}

export function createDownloadSelectedResourcesButton(widget: NDPWidget) {
  return createButton(
    'Download Selected Resources',
    'ndp-button',
    widget._onButtonDownloadSelectedResourcesClick.bind(widget)
  );
}

export function createGitCloneButton(widget: NDPWidget) {
  return createButton('Clone Repository', 'ndp-button', async () => {
    const repoUrl = 'https://github.com/your-repo-url.git'; // Replace with the desired repo URL

    // Create a custom input widget for the dialog
    const body = new Widget();
    const input = document.createElement('input');
    input.value = repoUrl;
    input.style.width = '100%';
    body.node.appendChild(input);

    // Open a custom dialog with the input field
    const result = await showDialog({
      title: 'Clone a Repository',
      body,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Clone' })]
    });

    if (result.button.accept) {
      const clonedRepoUrl = input.value;
      if (clonedRepoUrl) {
        // Execute the clone command with the provided URL
        await widget.commands.execute('git:clone', { path: widget.fileBrowser.model.path, url: clonedRepoUrl });
      }
    }
  });
}
