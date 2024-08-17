import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { requestAPI } from './handler';

/**
 * Initialization data for the pergamon_theme_server extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pergamon_theme_server:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension pergamon_theme_server is activated!!!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('pergamon_theme_server settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for pergamon_theme_server.', reason);
        });
    }

    requestAPI<any>('customcss')
      .then(data => {
        var head = document.head || document.getElementsByTagName('head')[0],
        style = document.createElement('style');

        head.appendChild(style);

        style.type = 'text/css';
        style.appendChild(document.createTextNode(data));

        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The pergamon_theme_server server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
