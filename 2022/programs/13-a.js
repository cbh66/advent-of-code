const fs = require('fs');
const RIGHT = 'right';
const WRONG = 'wrong';
const UNDETERMINED = 'undetermined';

const pairs = fs.readFileSync(0)
    .toString()
    .split('\n\n')
    .filter((l) => l !== '')
    .map((l) => l.split('\n').filter((c) => c !== '').map(JSON.parse));

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

let sum = 0;
let i = 1;
for (let [left, right] of pairs) {
    if (compare(left, right) === RIGHT) {
        sum += i;
    }
    ++i;
}
console.log(sum);
