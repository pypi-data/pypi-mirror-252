/* eslint-env node */
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
import replace from '@rollup/plugin-replace';
import json from '@rollup/plugin-json';
import yaml from '@rollup/plugin-yaml';
import toml from '@fbraem/rollup-plugin-toml';
import { imports } from 'resolve.exports';

import { configProvider } from '#src/appProvider.js';
import {
    getEnvs,
    getConditions,
    getEntryConditions,
} from '#src/configs/utils.js';

// eslint-disable-next-line n/no-process-env
const ENV = JSON.stringify(process.env.NODE_ENV);

export async function createBaseConfig(app, options) {
    const input = getInput(app, options);
    const conditions = Array.from(getConditions(app, options.dev));
    const envs = getEnvs(app);
    const isNodeOnly = envs.has('node') && !envs.has('browser');

    return {
        output: {
            format: 'es',
            dir: String(app.resolvePath(app.config.output_dir ?? 'build')),
            ...getFileNames(app, options),
            sourcemap: app.config.sourcemap ?? true,
            sourcemapExcludeSources: app.config.sourcemapExcludeSources
                ?? false,
        },
        input: String(app.resolvePath(input)),
        beforePlugins: [
            replace({
                preventAssignment: true,
                values: {
                    // process env is required by at lot of npm modules
                    // We should offer other env options eventually
                    'process.env.NODE_ENV': ENV,
                },
            }),
        ],
        plugins: [
            json({ namedExports: false, preferConst: true }),
            yaml(),
            toml(),
            configProvider(app),
            resolve({
                browser: envs.has('browser'),
                preferBuiltins: isNodeOnly,
                exportConditions: conditions,
            }),
            commonjs(),
        ],
        watch: {
            clearScreen: false,
        },
    };
}



function getInput(app, { dev }) {
    const conditions = getEntryConditions(app, dev);

    const { manifest } = app;
    return imports(manifest, '#vulcan-dev-entry', { conditions });
}


export function getFileNames(app, options) {
    const isLib = app.config.type === 'lib';

    if (!isLib) {
        return {
            assetFileNames: 'assets/[name]-[hash][extname]',
            chunkFileNames: '[name]-[hash].js',
            entryFileNames: '[name]-[hash].js',
        };
    } else {
        return {
            assetFileNames: 'assets/[name][extname]',
            chunkFileNames: '[name].js',
            entryFileNames: '[name].js',
        };
    }
}
