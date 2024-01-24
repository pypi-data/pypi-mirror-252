import signale from 'signale-logger';

export const log = signale.scope('Rollup');

log.config({
    displayTimestamp: true,
    displayLabel: false,
    formatTime: 'LTS',
});
