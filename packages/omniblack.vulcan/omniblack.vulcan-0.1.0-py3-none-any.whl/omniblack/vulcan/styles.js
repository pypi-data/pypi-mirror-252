import { extname, basename } from 'node:path';
import { readFile } from 'node:fs/promises';
import postcss from 'postcss';
import atImport from 'postcss-import';
import { createFilter } from '@rollup/pluginutils';

async function postcssProcess(plugins, code, filePath) {
    const processor = postcss(plugins);
    const result = await processor.process(code, {from: filePath});

    return result.css;
}

export function style(opts={}) {
    const {
        plugins=[],
    } = opts;
    const filter = createFilter(
        opts.include ?? ['**/*.css'],
        opts.exclude,
    );

    function handle(id) {
        return filter(id);
    }

    let options;
    return {
        name: '@omniblack/style',
        async transform(code, id) {
            if (!handle(id)) {
                return null;
            }

            const boundResolve = this.resolve.bind(this);
            const addWatchFile = this.resolve.bind(this);


            const allPlugins = [
                atImport({
                    async resolve(cssId) {
                        const resolved = await boundResolve(cssId, id);
                        addWatchFile(resolved.id);
                        return resolved.id;
                    },
                }),
                ...plugins,
            ];

            this.emitFile({
                type: 'asset',
                name: basename(id),
                source: await postcssProcess(allPlugins, code, id),
            });

            return {code: '', moduleSideEffects: false};
        },
    };
}

