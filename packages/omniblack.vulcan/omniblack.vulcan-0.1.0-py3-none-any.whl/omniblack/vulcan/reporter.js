/* eslint-env node */
import { createWriteStream, closeSync } from 'node:fs';

const RECORD_SEPARATOR = '\u001E';

let ipc_stream;

function send(arg) {
    ipc_stream?.write(JSON.stringify(arg) + RECORD_SEPARATOR);
}

class Process {
    constructor() {
        this.__state = 'success';
        this.__progress = 0;
    }

    set state(newState) {
        this.__state = newState;
        send({
            type: 'update',
            state: newState,
        });
    }

    get state() {
        return this.__state;
    }


    set progress(newProgress) {
        this.__progress = newProgress;
        send({
            type: 'update',
            progress: newProgress,
        });
    }

    get progress() {
        return this.__progress;
    }
}

const endedStates = new Set(['success', 'error']);

// eslint-disable-next-line n/no-process-env
const IPC_FD = Number.parseInt(process.env.IPC_FD);

if (!Number.isNaN(IPC_FD)) {
    ipc_stream = createWriteStream('', {
        fd: IPC_FD,
    });

    process.on('exit', () => {
        ipc_stream.end();
        closeSync(IPC_FD);
    });
}


export function reporter({ log }) {
    const process_proxy = new Process();

    let loadedModules = 0;
    function updateProgress(plugin) {
        if (endedStates.has(process_proxy.state)) {
            process_proxy.progress = 0;
            return;
        }

        let totalModules = 0;
        // eslint-disable-next-line no-unused-vars
        for (const module of plugin.getModuleIds()) {
            totalModules += 1;
        }

        const new_progress = (loadedModules / totalModules) * 100;
        if (Number.isNaN(new_progress)) {
            process_proxy.progress = 0;
        } else {
            process_proxy.progress = new_progress;
        }
    }

    return {
        name: '@omniblack/vulcan reporter',
        options(options) {
            options.onwarn = onwarn;
            return options;
        },
        buildStart() {
            loadedModules = 0;
            process_proxy.state = 'running';
            updateProgress(this);
            return null;
        },
        load() {
            updateProgress(this);
            return null;
        },
        moduleParsed() {
            loadedModules += 1;
            updateProgress(this);
            return null;
        },
        buildEnd(error) {
            if (error) {
                process_proxy.state = 'error';
                send({
                    type: 'error',
                    error,
                });
            } else {
                process_proxy.state = 'success';
            }


            updateProgress(this);
            return null;
        },
    };

    function onwarn({ loc, frame, message }) {
        if (loc) {
            log.warn(`${loc.file} (${loc.line}:${loc.column}) ${message}`);
            if (frame) {
                log.warn(frame);
            }
        } else {
            log.warn(message);
        }
    }
}

