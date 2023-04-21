const fs = require('fs');

const instructions = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split(' '));

function* run(instructions) {
    let X = 1;
    for (let [instr, arg] of instructions) {
        if (instr === 'noop') {
            yield X;
        } else if (instr === 'addx') {
            yield X;
            X += parseInt(arg);
            yield X;
        }
    }
}

let i = 2;
let sum = 0;
const cpu = run(instructions);
for (let step = cpu.next(); !step.done; step = cpu.next()) {
    if ((i - 20) % 40 === 0 && i < 260) {
        sum += i * step.value;
    }
    ++i;
}
console.log(sum);
