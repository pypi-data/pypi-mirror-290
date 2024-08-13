import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  MainAreaWidget
} from '@jupyterlab/apputils';

// import {
//   IFileBrowserFactory
// } from '@jupyterlab/filebrowser';

import {
  Widget
} from '@lumino/widgets';



import { ISettingRegistry } from '@jupyterlab/settingregistry';

import {requestAPI, requestAPIWithParams} from './handler';

/**
 * Initialization data for the jupS3 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupS3:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settingRegistry: ISettingRegistry | null) => {
    console.log('JupyterLab extension jupS3 is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('jupS3 settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for jupS3.', reason);
        });
    }

    requestAPI<any>('get-example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The jupS3 server extension appears to be missing.\n${reason}`
        );
      });



    const content = new S3BrowserWidget();
        // @ts-ignore
    const widget = new MainAreaWidget({ content });
    widget.title.label = 'AURIN Data Browser';
    app.shell.add(widget, 'left');

  }
};


class S3BrowserWidget extends Widget {
  constructor() {
    super();
    this.addClass('jp-S3BrowserWidget');
    this.id = 's3-browser-widget';
    this.title.label = 'S3 Browser';
    this.title.closable = true;

    this.node.innerHTML = `
      <div>
        <img src="https://aurin.org.au/wp-content/uploads/2016/12/AURIN-ORG-AU-1.jpg" 
            width="214.4" 
            height="100" 
        />
        <h2 style="text-align:center;">AURIN Data</h2>
        <hr>
        <p style="font-style:italic;text-decoration:underline;">Right click any data file to save it to your home directory on the server:</p>
        <hr>
        <ul id="s3-contents"></ul>
        <ul id="s3-contents" class="jp-DirListing-content"></ul>
        <hr>
      </div>
    `;

     requestAPI<any>('get-bucket-contents')
      .then(data => {
        const ul = this.node.querySelector('#s3-contents') as HTMLUListElement;
      data.data.forEach((item: string) => {
        const li = document.createElement('li');
        li.classList.add('jp-DirListing-item');
        li.addEventListener('contextmenu', this.handleRightClick.bind(this));
        li.textContent = item;
        ul.appendChild(li);
      });
      })
      .catch(reason => {
        console.error(
          `Error getting S3 bucket contents.\n${reason}`
        );
      });

  }



  handleRightClick(event: MouseEvent) {
    event.preventDefault();
    const target = event.target as HTMLElement;
    if (target && target.tagName === 'LI') {
      console.log('Right-clicked item text:', target.textContent);
    }
    const contextMenu = this.createContextMenu(target.textContent);

    document.body.appendChild(contextMenu);
    contextMenu.style.top = `${event.clientY}px`;
    contextMenu.style.left = `${event.clientX}px`;

    const removeContextMenu = () => {
      document.body.removeChild(contextMenu);
      document.removeEventListener('click', removeContextMenu);
    };

    document.addEventListener('click', removeContextMenu);
  }

  createContextMenu(textContent: string | null): HTMLUListElement {

    const menu = document.createElement('ul');
    menu.classList.add('context-menu');
    const menuItem = document.createElement('li');
    menuItem.textContent = 'Checkout to your home directory';
    menuItem.addEventListener('click', (e) => {
      console.log('clicked:', textContent);
      const params = { file: textContent || '' }; // Example parameter

      requestAPIWithParams<any>('create-or-append-to-file', {}, params)
        .then(data => {
          console.log(data);
        })
        .catch(reason => {
          console.error(
            `The jupS3 server extension appears to be missing.\n${reason}`
          );
      });

    });

    menu.appendChild(menuItem);
    return menu;
  }

}
export default plugin;
