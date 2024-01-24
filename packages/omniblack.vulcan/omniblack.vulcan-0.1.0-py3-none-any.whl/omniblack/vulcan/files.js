const typeRenames = {
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'json5': 'json5',
};

const loaders = {
    yaml,
    json5,
    json,
};

export async function loadFile(path) {
    const ext = path.suffix;

    const type = typeRenames[ext];

    const loader = loaders[type];

    return await loader(path);
}



async function json(path) {
    const str = await path.readFile();

    return JSON.parse(str);
}

async function yaml(path) {
    const yamlModule = await import('js-yaml');
    const yaml = yamlModule.default;

    const fileStr = await path.readFile();

    return yaml.load(fileStr);
}


async function json5(path) {
    const JSON5Module = await import('json5');
    const JSON5 = JSON5Module.default;

    const fileStr = await path.readFile();

    return JSON5.parse(fileStr);
}
