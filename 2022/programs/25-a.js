const fs = require('fs');

const allNums = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '');

const DIGIT_MAP = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
};

function fromSnafu(snafuNum) {
    if (snafuNum in DIGIT_MAP) {
        return DIGIT_MAP[snafuNum];
    }
    const digit = snafuNum.slice(-1);
    const rest = snafuNum.slice(0, -1);
    return DIGIT_MAP[digit] + (5 * fromSnafu(rest));
}

function toSnafu(num) {
    function toDigit(d) {
        for (const [snafuDigit, value] of Object.entries(DIGIT_MAP)) {
            if (d === value) {
                return snafuDigit;
            }
        }
    }
    let snafu = ''
    while (num !== 0) {
        snafu = toDigit(((num + 2) % 5) - 2) + snafu;
        num = Math.floor((num + 2) / 5);
    }
    return snafu;
}

const sum = allNums.map(fromSnafu).reduce((a, b) => a + b);
console.log(toSnafu(sum));
