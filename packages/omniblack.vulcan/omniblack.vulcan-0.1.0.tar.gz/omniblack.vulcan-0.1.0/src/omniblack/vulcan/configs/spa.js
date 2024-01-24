import url from '@rollup/plugin-url';

import { merge } from '#src/mergeRollup.js';
import { getFileNames } from '#src/configs/base.js';
import { getDeps } from '#src/configs/utils.js';
import { style } from '#src/styles.js';

import { html } from '@omniblack/rollup-plugin-html-template';
import { build_colors } from '@omniblack/mithril/build_colors.js';


export async function createSpaConfig(app, { dev, reload_port }) {
    const deps = getDeps(app, dev);
    const { assetFileNames } = getFileNames(app, { dev, reload_port });

    const plugins = [
        build_colors(),
        style({
            rootDir: app.src_dir,
        }),
        html({
            templatePath: await app.resolveModule(app.config.template_path),
            templateParameters: app.config.template_parameters,
            publicPath: app.config.public_path + '/',
        }),
        url({
            publicPath: app.config.public_path + '/',
            fileName: assetFileNames,
        }),
    ];

    const rollupConfig = {
        plugins,
    };

    const appType = app.config.type;
    const isLib = appType === 'lib';
    if (deps.has('svelte') && (!isLib || dev)) {
        const svelteOptions = await svelte(app, dev);
        merge(rollupConfig, svelteOptions);
    }

    return rollupConfig;
}


async function svelte(app, dev) {
    const svelteModule = await import('rollup-plugin-svelte');
    const sveltePlugin = svelteModule.default;


    return {
        beforePlugins: [
            sveltePlugin({
                emitCss: true,
                compilerOptions: {
                    dev,
                },
            }),
        ],
    };
}
