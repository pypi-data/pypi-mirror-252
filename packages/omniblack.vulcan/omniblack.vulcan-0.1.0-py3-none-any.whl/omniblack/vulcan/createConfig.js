import { inspect } from 'node:util';
import { loadConfigFile } from 'rollup/loadConfigFile';
import { merge } from './mergeRollup.js';

import { createBaseConfig } from './configs/base.js';
import { createDevConfig } from './configs/dev.js';
import { createSpaConfig } from './configs/spa.js';
import { createLibConfig } from './configs/lib.js';

const possibleConfigs = ['mjs', 'js', 'cjs']
    .map((ext) => `rollup.config.${ext}`);

const notFoundErrors = new Set([
    'ERR_MODULE_NOT_FOUND',
    'UNRESOLVED_ENTRY',
    'MODULE_NOT_FOUND',
]);

export async function createConfig(app, options) {
    const config = await createBaseConfig(app, options);

    if (app.config.type === 'lib') {
        merge(config, await createLibConfig(app, options));
    } else if (app.config.type === 'spa') {
        merge(config, await createSpaConfig(app, options));
    }

    if (options.dev) {
        merge(config, await createDevConfig(app, options));
    }


    for (const configPath of possibleConfigs) {
        try {
            const fullPath = app.path.join(configPath);

            const {default: userConfig} = await import(String(fullPath));

            merge(config, userConfig);
        } catch (err) {
            if (!notFoundErrors.has(err.code)) {
                throw err;
            }
        }
    }

    const { beforePlugins = [] } = config;
    config.plugins = beforePlugins.concat(config.plugins ?? []);

    delete config.beforePlugins;

    return config;
}
