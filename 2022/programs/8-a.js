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

function isVisible(grid, { x, y }) {
    return (Math.max(...gridInclusiveRange(grid, { x: [0, x - 1], y: [y, y] })) < grid[x][y]) ||
        (Math.max(...gridInclusiveRange(grid, { x: [x + 1], y: [y, y] })) < grid[x][y]) ||
        (Math.max(...gridInclusiveRange(grid, { x: [x, x], y: [0, y - 1] })) < grid[x][y]) ||
        (Math.max(...gridInclusiveRange(grid, { x: [x, x], y: [y + 1] })) < grid[x][y]);
}

let count = 0;
for (let x = 0; x < grid.length; ++x) {
    for (let y = 0; y < grid[x].length; ++y) {
        if (isVisible(grid, { x, y })) {
            ++count;
        }
    }
}
console.log(count);
