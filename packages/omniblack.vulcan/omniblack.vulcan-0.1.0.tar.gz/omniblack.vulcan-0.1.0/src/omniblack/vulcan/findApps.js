import { inspect } from 'node:util';
import { pathToFileURL, fileURLToPath } from 'node:url';

import { defaultsDeep } from 'lodash-es';

import autoBind from 'auto-bind';

import { loadFile } from './files.js';

import { Path } from '@omniblack/pathlib';

const configDefault = {
    output_dir: 'build',
};


export class Package {
    constructor({
        config,
        configPath,
        js,
        jsPath,
        path,
        rootDir,
    }) {
        this.path = path;
        this.src_dir = path.join('src');

        this.config = defaultsDeep(config, configDefault);
        this.configPath = configPath;
        this.configUrl = pathToFileURL(String(configPath));

        this.manifest = js;
        this.manifestPath = jsPath;
        this.manifestUrl = pathToFileURL(String(jsPath));


        autoBind(this);
    }

    static async create({ configPath, jsPath, path }) {
        const js = await loadFile(jsPath);
        const config = await loadFile(configPath);

        return new this({ configPath, jsPath, path, js, config });
    }

    /*
     * Return the file imported from context of the app
     */
    async import(path) {
        const file = await this.resolveModule(path);

        return await import(file);
    }

    /*
     * Promises to return the resolved absolute path to specified file or
     *     module. This will look into node_modules, but can not resolve to
     *     a directory.
     */
    async resolveModule(module) {
        const resolvedUrl = await import.meta.resolve(
            module,
            String(this.configUrl),
        );
        return fileURLToPath(resolvedUrl);
    }

    /*
     * Return a resolved path using the app directory as the source.
     *     This will not search node_modules, but can resolve a directory.
     */
    resolvePath(...paths) {
        return this.path.resolve(...paths);
    }

    relative(path) {
        path = new Path(path);
        return path.relativeTo(this.path);
    }

    [inspect.custom](_depth, _options) {
        return Object.fromEntries(Object.entries(this)
            .filter(
                ([key]) => !key.startsWith('__') && key !== inspect.custom,
            ),
        );
    }

    get procEnv() {
        return {
            NAME: this.manifest.name,
            VERSION: this.manifest.version,
            PKG_PATH: this.path,
            MANIFEST: String(this.manifestPath),
        };
    }
}

export { Package as App };
