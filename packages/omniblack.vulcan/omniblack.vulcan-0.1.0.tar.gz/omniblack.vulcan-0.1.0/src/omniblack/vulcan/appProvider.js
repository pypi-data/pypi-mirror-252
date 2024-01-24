/* eslint-env node */
import { loadFile } from './files.js';

export function configProvider(app) {
    const name = '@omniblack/vulcan/current_config';

    return {
        name: '@omniblack/vulcan/config_provider',
        resolveId(source) {
            if (source === name) {
                return name;
            }
        },
        async load(id) {
            if (id === name) {
                if (this.meta.watchMode) {
                    this.addWatchFile(String(app.configPath));
                }

                const config = await loadFile(app.configPath);
                const configStr = JSON.stringify(config);
                return `export default ${configStr}`;
            }
        },
    };
}
