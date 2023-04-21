const fs = require('fs');

const lines = fs.readFileSync(0)
    .toString()
    .split('\n')
    .filter((l) => l !== '')
    .map((l) => l.split(' '));

function newDir(parent) {
    return {
        type: 'dir',
        contents: {
            '..': parent,
        },
    };
}
const rootDir = newDir();
let currentDir = rootDir;

let i = 0;
while (i < lines.length) {
    const [start, command, arg] = lines[i];
    if (start !== '$') {
        throw new Error(`Unexpected line start at ${i}: "${start}"`);
    }
    if (command === 'cd') {
        if (arg === '/') {
            currentDir = rootDir;
        } else {
            currentDir = currentDir.contents[arg];
        }
        ++i;
    } else if (command === 'ls') {
        ++i;
        while (i < lines.length && lines[i][0] !== '$') {
            const [description, name] = lines[i]
            if (description === 'dir' && currentDir.contents[name] === undefined) {
                currentDir.contents[name] = newDir(currentDir);

            } else {
                const size = parseInt(description);
                currentDir.contents[name] = {
                    type: 'file',
                    size,
                };
            }
            ++i;
        }
    }
}


function calculateDirSizes(ref) {
    if (ref.type === 'file') {
        return ref.size;
    }
    const size = Object.entries(ref.contents)
        .filter(([childName]) => (childName !== '..'))
        .map(([, childRef]) => calculateDirSizes(childRef))
        .reduce((a, b) => a + b);
    ref.size = size;
    return size;
}
calculateDirSizes(rootDir);

function dirSizesAbove(threshold, ref) {
    if (ref.type === 'file') {
        return [];
    }
    let dirs = Object.entries(ref.contents)
        .filter(([childName, _]) => (childName !== '..'))
        .map(([childName, childRef]) => {
            console.log(childName);
            return dirSizesAbove(threshold, childRef);
        })
        .reduce((a, b) => [...a, ...b], []);
    if (ref.size >= threshold) {
        dirs = [...dirs, ref.size];
    }
    return dirs;
}
const unusedSpace = 70000000 - rootDir.size;
const minToDelete = 30000000 - unusedSpace;
console.log(Math.min(...dirSizesAbove(minToDelete, rootDir)));


// function pprint(name, ref, indent) {
//     if (ref.type === 'file') {
//         console.log(`${indent}- ${name} (file, size=${ref.size})`);
//     } else {
//         console.log(`${indent}- ${name} (dir size=${ref.size})`);
//         Object.entries(ref.contents).forEach(([childName, childRef]) => {
//             if (childName !== '..') {
//                 pprint(childName, childRef, indent + '  ');
//             }
//         });
//     }
// }

// pprint('/', rootDir, '');
