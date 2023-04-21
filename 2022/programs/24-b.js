const fs = require('fs');

const grid = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '');


const start = [0, 1];
const destination = [grid.length - 1, grid[grid.length - 1].length - 2];

function direction(char) {
    switch (char) {
        case '<': return [0, -1];
        case '>': return [0, +1];
        case '^': return [-1, 0];
        case 'v': return [+1, 0];
    }
}

function move({ pos: [row, col], dir: [dr, dc] }) {
    return [row + dr, col + dc];
}

function isSame([r1, c1], [r2, c2]) {
    return r1 === r2 && c1 === c2;
}

function isInBounds([row, col]) {
    if (row < 0 || col < 0 || row >= grid.length || col >= grid[row].length) return false;
    if (grid[row][col] === '#') return false;
    return true;
}

function advanceBlizzards({ grid, blizzards }) {
    return blizzards.map(({ pos, dir }) => {
        let [newRow, newCol] = move({ pos, dir });
        while (!isInBounds([newRow, newCol])) {
            newRow = (newRow + grid.length) % grid.length;
            newCol = (newCol + grid[newRow].length) % grid[newRow].length;
            [newRow, newCol] = move({ pos: [newRow, newCol], dir });
        }
        return { pos: [newRow, newCol], dir };
    });
}

const initialBlizzards = [];
for (let row = 0; row < grid.length; ++row) {
    for (let col = 0; col < grid[row].length; ++col) {
        const char = grid[row][col];
        if (char !== '.' && char !== '#') {
            initialBlizzards.push({ dir: direction(char), pos: [row, col] });
        }
    }
}

function shortestPath({ start, destination, initialBlizzards }) {
    const queue = [{ pos: start, turnNum: 0, blizzards: initialBlizzards }];
    let alreadyAdded = new Set();
    while (queue.length > 0) {
        const { pos, turnNum, blizzards } = queue.shift();
        if (isSame(destination, pos)) {
            return { turnNum, blizzards };
        }
        const nextBlizzards = advanceBlizzards({ blizzards, grid });
        for (let dir of [[0, -1], [0, +1], [-1, 0], [+1, 0], [0, 0]]) {
            const nextAttempt = move({ pos, dir });
            if (!isInBounds(nextAttempt)) continue;
            const hiBblizzard = blizzards.some(({ pos: b }) => isSame(pos, b));
            if (hiBblizzard) continue;
            const key = `${turnNum}:${nextAttempt}`
            if (alreadyAdded.has(key)) continue;
            alreadyAdded.add(key);
            queue.push({ pos: nextAttempt, blizzards: nextBlizzards, turnNum: turnNum + 1 });
        }
    }
}
const firstLeg = shortestPath({ start, destination, initialBlizzards });
console.log(`First leg: length ${firstLeg.turnNum}`)
const secondLeg = shortestPath({ start: destination, destination: start, initialBlizzards: firstLeg.blizzards });
console.log(`Second leg: length ${secondLeg.turnNum}`);
const thirdLeg = shortestPath({ start, destination, initialBlizzards: secondLeg.blizzards });
console.log(`Final leg: length ${thirdLeg.turnNum}`);
console.log(`Sum: ${firstLeg + secondLeg + thirdLeg}`);
