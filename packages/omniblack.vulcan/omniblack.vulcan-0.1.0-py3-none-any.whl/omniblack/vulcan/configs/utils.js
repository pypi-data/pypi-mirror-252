class Set extends globalThis.Set {
    extend(iterable) {
        for (const item of iterable) {
            this.add(item);
        }
    }
}

export function getDeps(app, dev, options = {}) {
    const {
        includePeer = false,
        includeDev = false,
        includeOptional = false,
    } = options;

    const prodDeps = Object.keys(app.manifest.dependencies ?? {});
    const deps = new Set(prodDeps);

    if (dev || includeDev) {
        const devDeps = Object.keys(app.manifest.devDependencies ?? {});
        deps.extend(devDeps);
    }

    if (includePeer) {
        const peerDeps = Object.keys(app.manifest.peerDependencies ?? {});
        deps.extend(peerDeps);
    }

    if (includeOptional) {
        const optionalDeps = Object.keys(
            app.manifest.optionalDependencies ?? {},
        );
        deps.extend(optionalDeps);
    }

    return deps;
}

const allowedConditions = {
    'spa': [
        'import',
        'default',
    ],
    'lib': [
        'import',
        'default',
    ],
    'app': [
        'import',
        'default',
    ],
};


export function getConditions(app, dev) {
    const conditions = allowedConditions[app.config.type];

    if (dev) {
        conditions.push('development');
    } else {
        conditions.push('production');
    }

    const environments = getEnvs(app);

    conditions.push(...environments);

    return conditions;
}

export function getEntryConditions(app, dev) {
    const conditions = getConditions(app, dev);

    return conditions;
}

export function getEnvs(app) {
    if (Object.hasOwn(app.config, 'environments')) {
        return new Set(app.config.environments);
    }

    return new Set();
}
