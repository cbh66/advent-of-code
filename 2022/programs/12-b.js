const fs = require('fs');

const chars = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split('').filter((c) => c !== ''));

let startX, startY, endX, endY;
for (let x = 0; x < chars.length; ++x) {
    for (let y = 0; y < chars[x].length; ++y) {
        if (chars[x][y] === 'S') {
            startX = x;
            startY = y;
            chars[x][y] = 'a';
        } else if (chars[x][y] === 'E') {
            endX = x;
            endY = y;
            chars[x][y] = 'z';
        }
    }
}
const heights = chars.map((l) => l.map((c) => c.charCodeAt(0) - 'a'.charCodeAt(0)));

const shortestPathFrom = (startX, startY) => {
    const shortestPaths = heights.map((l) => l.map(() => Infinity));

    const isInBounds = (x, y) => (0 <= x && x < heights.length && 0 <= y && y < heights[x].length);

    const findShortestPaths = (x, y, lengthSoFar) => {
        if (!isInBounds(x, y)) return;
        if (shortestPaths[x][y] <= lengthSoFar) return;
        shortestPaths[x][y] = lengthSoFar;
        for (let [nextX, nextY] of [[x - 1, y], [x, y - 1], [x + 1, y], [x, y + 1]]) {
            if (!isInBounds(nextX, nextY)) continue;
            if (heights[nextX][nextY] > heights[x][y] + 1) continue;
            findShortestPaths(nextX, nextY, lengthSoFar + 1);
        }
    }

    findShortestPaths(startX, startY, 0);
    return shortestPaths[endX][endY];
}

let minLength = Infinity;
for (let x = 0; x < heights.length; ++x) {
    for (let y = 0; y < heights[x].length; ++y) {
        if (heights[x][y] === 0) {
            minLength = Math.min(minLength, shortestPathFrom(x, y));
        }
    }
}
console.log(minLength);
