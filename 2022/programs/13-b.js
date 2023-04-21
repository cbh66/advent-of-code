const fs = require('fs');
const RIGHT = -1;
const WRONG = 1;
const UNDETERMINED = 0;
const DIVIDERS = [ [[2]], [[6]] ];

const pairs = fs.readFileSync(0)
    .toString()
    .split('\n\n')
    .filter((l) => l !== '')
    .map((l) => l.split('\n').filter((c) => c !== '').map(JSON.parse));
const packets = [...DIVIDERS, ...pairs.flat()];

const compare = (left, right) => {
    if (typeof left === 'number' && typeof right === 'number') {
        if (left < right) {
            return RIGHT;
        } else if (right < left) {
            return WRONG;
        }
        return UNDETERMINED;
    }
    if (typeof left === 'number') {
        left = [left];
    }
    if (typeof right === 'number') {
        right = [right];
    }
    for (let i = 0; i < left.length && i < right.length; ++i) {
        const result = compare(left[i], right[i]);
        if (result !== UNDETERMINED) return result;
    }
    if (left.length < right.length) {
        return RIGHT;
    } else if (right.length < left.length) {
        return WRONG;
    }
    return UNDETERMINED;
}

packets.sort(compare);
console.log((packets.indexOf(DIVIDERS[0]) + 1) * (packets.indexOf(DIVIDERS[1]) + 1));
