import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the jupyterlab-algorithm-style-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-algorithm-style-extension:plugin',
  description: 'jupyterlab-algorithm-style-extension',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-algorithm-style-extension is activated!');
  }
};

export default plugin;
