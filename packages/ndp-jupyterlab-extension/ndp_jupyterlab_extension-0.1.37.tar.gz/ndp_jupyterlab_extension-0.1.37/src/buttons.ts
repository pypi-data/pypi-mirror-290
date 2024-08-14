// buttons.ts
import { NDPWidget } from './widget';

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
  return createButton(
    'Clone Repository',
    'ndp-button',
    widget._onCloneGitRepoButtonClick.bind(widget)
  );
}
