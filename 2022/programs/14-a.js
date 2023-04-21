const fs = require('fs');
const BLANK = '.';

const paths = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split(' -> ')
        .filter((c) => c !== '')
        .map((p) => p.split(',').filter((n) => n !== '').map((n) => parseInt(n, 10))));

const maxCol = Math.max(...paths.flatMap((path) => path.flatMap(([col, ]) => col))) + 2;
const minCol = Math.min(...paths.flatMap((path) => path.flatMap(([col, ]) => col))) - 1;
const maxRow = Math.max(...paths.flatMap((path) => path.flatMap(([ , row]) => row))) + 2;
const board = [...Array(maxRow).keys()].map(() => [...Array(maxCol).keys()].map(() => BLANK));
board[0][500] = '+';

function printBoard() {
    for (let row = 0; row < maxRow; ++row) {
        console.log(board[row].slice(minCol, maxCol).join(''));
    }
}

function drawRocksBetween([col1, row1], [col2, row2]) {
    let [col, row] = [col1, row1];
    board[row][col] = '#';
    while (col !== col2 || row !== row2) {
        col += (col2 - col) / (Math.abs(col2 - col) || 1);
        row += (row2 - row) / (Math.abs(row2 - row) || 1);
        board[row][col] = '#';
    }
}
paths.forEach((path) => {
    for (let i = 1; i < path.length; ++i) {
        drawRocksBetween(path[i - 1], path[i]);
    }
});

// returns row that it settles on. If Infinity, it'll continue forever
function addSand() {
    let [row, col] = [0, 500];
    while (row < maxRow - 1) {
        if (board[row + 1][col] === BLANK) {
            row += 1;
        } else if (board[row + 1][col - 1] === BLANK) {
            [row, col] = [row + 1, col - 1];
        } else if (board[row + 1][col + 1] === BLANK) {
            [row, col] = [row + 1, col + 1];
        } else {
            board[row][col] = 'o';
            return row;
        }
    }
    return Infinity;
}
let numSandParticles = 0;
while (addSand() !== Infinity) {
    ++numSandParticles;
}
// printBoard();
console.log(numSandParticles);
