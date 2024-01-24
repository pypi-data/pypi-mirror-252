/* eslint-env node */
import { fileURLToPath } from 'node:url';
import { rollup } from 'rollup';

import signale from 'signale-logger';

import { createConfig } from './createConfig.js';
import { App } from './findApps.js';
import { Path } from '@omniblack/pathlib';

// This is a polyfill it modifies the global Object
// eslint-disable-next-line import/no-unassigned-import
import '@omniblack/utils/polyfill';

const log = signale.scope('Rollup');
log.config({
    displayTimestamp: true,
    displayLabel: true,
    formatTime: 'LTS',
});

async function main() {
    // eslint-disable-next-line n/no-process-env
    const { CONFIG_PATH, JS_PATH, PKG_PATH } = process.env;

    const app = await App.create({
        configPath: new Path(CONFIG_PATH),
        path: new Path(PKG_PATH),
        jsPath: new Path(JS_PATH),
    });

    const options = {
        dev: false,
        log,
    };

    const config = await createConfig(app, options);

    const { output: outputOptions, ...inputOptions } = config;

    const bundle = await rollup(inputOptions);

    await bundle.write(outputOptions);
    await bundle.close();
}

const __file__ = fileURLToPath(import.meta.url);

if (process.argv[1] === __file__) {
    main();
}
