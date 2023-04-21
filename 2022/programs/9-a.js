const fs = require('fs');

const instructions = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split(' '));

const add = ([x, y], [dx, dy]) => [x + dx, y + dy];
const difference = ([ax, ay], [bx, by]) => [ax - bx, ay - by];

class Rope {
    head = [0, 0];
    tail = [0, 0];

    move = (dir) => {
        this.head = add(this.head, dir);
        const [dx, dy] = difference(this.head, this.tail);
        if (Math.abs(dx) > 1 || Math.abs(dy) > 1) {
            this.tail = add(this.tail, [
                Math.max(-1, Math.min(dx, 1)),
                Math.max(-1, Math.min(dy, 1)),
            ]);
        }
    };
}

const rope = new Rope();
const trail = new Set(['0,0']);

for (let [dir, amt] of instructions) {
    amt = parseInt(amt);
    for (let i = 0; i < amt; ++i) {
        switch (dir) {
            case 'U': rope.move([0, -1]); break;
            case 'D': rope.move([0, 1]); break;
            case 'L': rope.move([-1, 0]); break;
            case 'R': rope.move([1, 0]); break;
        }
        const [newX, newY] = rope.tail;
        trail.add(`${newX},${newY}`);
    }
}
console.log(trail.size);
