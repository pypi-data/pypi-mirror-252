/* eslint-env node */
import { fileURLToPath } from 'node:url';
import { watch, VERSION as ROLLUP_VERSION } from 'rollup';
import ms from 'pretty-ms';
import { bold, underline, green, blue } from 'colorette';
import signale from 'signale-logger';

import { App } from '#src/findApps.js';
import { createConfig } from '#src/createConfig.js';
import { log } from '#src/logger.js';

import { Path } from '@omniblack/pathlib';
import { collapseWhitespace } from '@omniblack/utils';
// This is a polyfill it modifies the global Object
// eslint-disable-next-line import/no-unassigned-import
import '@omniblack/utils/polyfill';


/* eslint-disable n/no-process-env */
const {
    CONFIG_PATH,
    JS_PATH,
    PKG_PATH,
    RELOAD_PORT,
} = process.env;
/* eslint-enable n/no-process-env */

async function main() {
    const app = await App.create({
        configPath: new Path(CONFIG_PATH),
        path: new Path(PKG_PATH),
        jsPath: new Path(JS_PATH),
    });

    const options = {
        reload_port: RELOAD_PORT,
        dev: true,
        log,
    };

    const config = await createConfig(app, options);

    const watcher = watch(config);

    watcher.on('event', async (event) => {
        if (event.code === 'START') {
            log.start(underline(`Started rollup: ${blue(ROLLUP_VERSION)}`));
        } else if (event.code === 'ERROR') {
            log.error('Build error Occurred.');
            log.error(event.error);
            const props = Object.assign({}, event.error);
            delete props.stack;

            // Use the root logger so we don't get a timestamp or scope
            // this make the props look connected to the previous message
            signale.log(props);
        } else if (event.code === 'BUNDLE_START') {
            const input = app.relative(event.input);
            const output = event.output.map(app.relative).join(', ');
            log.pending(
                collapseWhitespace(
                    `${green('Bundling')} ${bold(input)}
                ${green('->')} ${bold(output)}`,
                ),
            );
        } else if (event.code === 'BUNDLE_END') {
            const outputs = event.output.map(app.relative).join(', ');

            const msg = collapseWhitespace(
                `${green('Created')} ${bold(outputs)}
            ${green('in')} ${bold(ms(event.duration))}`,
            );
            log.success(msg);
            await event.result.close();
        } else if (event.code === 'END') {
            log.wait('waiting for changes');
        }
    });
}

const __name__ = fileURLToPath(import.meta.url);
const __main__ = process.argv[1];

if (__name__ === __main__) {
    main();
}
