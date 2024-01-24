import XRegExp from 'xregexp';
import { merge } from '#src/mergeRollup.js';
import { createSpaConfig } from '#src/configs/spa.js';
import { getDeps } from '#src/configs/utils.js';

export async function createLibConfig(app, options) {
    const config = {
        preserveEntrySignatures: 'strict',
    };
    const deps = getDeps(app, options.dev);

    const spaLib = options.dev && deps.has('svelte');

    if (!spaLib) {
        const allDeps = getDeps(app, options.dev, {
            includePeer: true,
            includeOptional: true,
        });

        const re = XRegExp.tag();
        const depRegexps = Array.from(allDeps).map(
            (dep) => re`^${dep}(?:\/.+)*$`,
        );

        if (depRegexps.length > 0) {
            const depRegex = XRegExp.union(depRegexps, 'u');

            config.external = (dep) => XRegExp.test(dep, depRegex);
        }
    }

    if (spaLib) {
        merge(config, await createSpaConfig(app, options));
    }
    return config;
}

