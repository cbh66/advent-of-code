const fs = require('fs');

const instructions = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split(' '));

function* run(instructions) {
    let X = 1;
    yield X;
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

const cpu = run(instructions);
let step = cpu.next();
let current_row = ''
while (!step.done) {
    current_row += (step.value - 1 <= current_row.length && current_row.length <= step.value + 1)
        ? '#' : ' ';
    if (current_row.length === 40) {
        console.log(current_row);
        current_row = '';
    }
    step = cpu.next();
}
