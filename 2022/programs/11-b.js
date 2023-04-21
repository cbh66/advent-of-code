const fs = require('fs');

const monkees = fs.readFileSync(0)
    .toString()
    .split('\n\n')
    .filter((s) => s !== '')
    .map((s) => s.split('\n').filter((l) => l !== ''))
    .map((s) => {
        let items = s[1].split('Starting items: ')[1].split(', ').map((i) => parseInt(i, 10));
        let numInspections = 0;
        const [, formula] = s[2].split('new = ');
        const [, divisibility] = s[3] .split('divisible by ');
        const [, trueTarget] = s[4].split('true: throw to monkey ');
        const [, falseTarget] = s[5].split('false: throw to monkey ');
        return { 
            takeTurn: (lcm) => {
                const results = items.map((i) => {
                    i = eval(formula.replaceAll('old', i.toString(10))) % lcm;
                    if (i % parseInt(divisibility, 10) === 0) {
                        return { item: i, target: parseInt(trueTarget, 10) };
                    } else {
                        return { item: i, target: parseInt(falseTarget, 10) };
                    }
                });
                items = [];
                numInspections += results.length;
                return results;
            },
            acceptItem: (newItem) => {
                items.push(newItem);
            },
            numInspections: () => numInspections,
            divisibility: parseInt(divisibility, 10),
         };
    });

const lcm = monkees.map((m) => m.divisibility).reduce((a, b) => a * b);
for (let round = 0; round < 10000; ++round) {
    for (let i = 0; i < monkees.length; ++i) {
        const results = monkees[i].takeTurn(lcm);
        results.forEach(({ item, target }) => monkees[target].acceptItem(item));
    }
}
const inspections = monkees.map((m) => m.numInspections()).sort((a, b) => b - a);
console.log(inspections[0] * inspections[1]);
