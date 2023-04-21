#!/usr/bin/python3
import sys
DECRYPTION_KEY = 811589153

def mix(items, source_index):
    item = items.pop(source_index)
    target_index = (source_index + item['val']) % len(items)
    items.insert(target_index, item)

def main(inputs):
    inputs = [input * DECRYPTION_KEY for input in inputs]
    inputs = [{ 'original_index': i, 'val': inputs[i] } for i in range(len(inputs))]
    for iteration in range(10):
        for i in range(len(inputs)):
            item_index = next(index for (index, val) in enumerate(inputs) if val['original_index'] == i)
            mix(inputs, item_index)
    zero_index = next(index for (index, val) in enumerate(inputs) if val['val'] == 0)
    print(sum(inputs[(zero_index + increment) % len(inputs)]['val'] for increment in [1000, 2000, 3000]))

if __name__ == "__main__":
    main([int(line.strip()) for line in sys.stdin.readlines()])
