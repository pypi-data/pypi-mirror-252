import del from 'rollup-plugin-delete';

import { reporter } from '#src/reporter.js';

export async function createDevConfig(app, { port, log }) {
    return {
        plugins: [
            del({
                targets: [String(app.resolvePath(
                    app.config.output_dir ?? 'build',
                ))],
                hook: 'generateBundle',
            }),
            reporter({ log }),
        ],
    };
}

