const fs = require('fs');

const grid = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split('').map((c) => parseInt(c, 10)));

function* gridInclusiveRange(grid, { x: [startX, endX], y: [startY, endY] }) {
    for (let x = startX; x <= (endX ?? grid.length + 1); ++x) {
        for (let y = startY; y <= (endY ?? grid[x].length + 1); ++y) {
            if (0 <= x && x < grid.length && 0 <= y && y < grid[x].length) {
                yield grid[x][y];
            }
        }
    }
}

function orderedRange(grid, { x: [startX, endX], y: [startY, endY] }) {
    const xReversed = (endX !== undefined && endX < startX);
    const yReversed = (endY !== undefined && endY < startY);
    const xRange = (xReversed) ? [endX, startX] : [startX, endX];
    const yRange = (yReversed) ? [endY, startY] : [startY, endY];
    let range = [...gridInclusiveRange(grid, { x: xRange, y: yRange })];
    if (xReversed || yReversed) {
        range.reverse();
    }
    return range;
}

function keepUntil(arr, predicate) {
    let newArr = [];
    let i = 0;
    while (i < arr.length && !predicate(arr[i])) {
        newArr.push(arr[i]);
        ++i;
    }
    if (i < arr.length) {
        newArr.push(arr[i]);
    }
    return newArr;
}

function scenicScore(grid, { x, y }) {
    const predicate = (value) => value >= grid[x][y];
    const up = keepUntil(orderedRange(grid, { x: [x - 1, -1], y: [y, y] }), predicate).length;
    const left = keepUntil(orderedRange(grid, { x: [x, x], y: [y - 1, -1] }), predicate).length;
    const down = keepUntil(orderedRange(grid, { x: [x + 1], y: [y, y] }), predicate).length;
    const right = keepUntil(orderedRange(grid, { x: [x, x], y: [y + 1] }), predicate).length;
    return up * left * down * right;
}

let maxScore = 0;
for (let x = 0; x < grid.length; ++x) {
    for (let y = 0; y < grid[x].length; ++y) {
        const score = scenicScore(grid, { x, y });
        maxScore = Math.max(score, maxScore);
    }
}
console.log(maxScore);
