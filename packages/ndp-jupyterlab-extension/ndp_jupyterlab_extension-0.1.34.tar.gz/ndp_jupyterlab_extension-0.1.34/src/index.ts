import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { NDPWidget } from './widget';

/**
 * Initialization data for the main menu example.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: '@jupyterlab-examples/main-menu:plugin',
  description: 'Minimal JupyterLab example adding a menu.',
  autoStart: true,
  requires: [IDefaultFileBrowser, ILabShell],
  activate: (
    app: JupyterFrontEnd,
    defaultBrowser: IDefaultFileBrowser,
    labShell: ILabShell
  ) => {
    const { commands } = app;
    const widget = new NDPWidget(defaultBrowser, commands);
    labShell.add(widget, 'left');
    app.restored.then(() => {
      labShell.activateById(widget.id);
    });
  }
};

export default extension;
