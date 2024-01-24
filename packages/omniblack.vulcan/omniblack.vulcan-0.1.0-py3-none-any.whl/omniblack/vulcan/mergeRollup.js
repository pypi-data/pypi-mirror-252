import { mergeWith } from 'lodash-es';


export function merge(...configs) {
    return mergeWith(...configs, (value, otherValue) => {
        if (Array.isArray(value)) {
            return value.concat(otherValue);
        }
    });
}
