#!/usr/bin/python3

import sys
from operator import mul
from functools import reduce

class Packet:
    def __init__(self, version, typeId, contents):
        self.version = version
        self.typeId = typeId
        self.contents = contents # num for literals, array of children for operators

    def value(self):
        if self.typeId == 0: # sum
            return sum(c.value() for c in self.contents)
        elif self.typeId == 1: # product
            return reduce(mul, [c.value() for c in self.contents], 1)
        elif self.typeId == 2: # min
            return min([c.value() for c in self.contents])
        elif self.typeId == 3: # max
            return max([c.value() for c in self.contents])
        elif self.typeId == 4: # literal
            return self.contents
        elif self.typeId == 5: # gt
            return 1 if self.contents[0].value() > self.contents[1].value() else 0
        elif self.typeId == 6: # lt
            return 1 if self.contents[0].value() < self.contents[1].value() else 0
        elif self.typeId == 7: # eq
            return 1 if self.contents[0].value() == self.contents[1].value() else 0
        else:
            raise Exception(f'Unknown operator type ID {self.typeId}')

def parse_next_packet(input):
    version = int(input[:3], 2)
    typeId = int(input[3:6], 2)
    remainder = input[6:]
    if typeId == 4:
        value_str = ''
        while True:
            block = remainder[:5]
            remainder = remainder[5:]
            value_str += block[1:]
            if block[0] == '0':
                break
            if len(remainder) == 0:
                raise Exception(f'Malformed literal, {value_str}')
        # print(f'Found literal with value {int(value_str, 2)}')
        return (Packet(version, 4, contents=int(value_str, 2)), remainder)
    else:
        lengthTypeId = int(remainder[0])
        subPackets = []
        if lengthTypeId == 0:
            subPacketLength = int(remainder[1:16], 2)
            contentsEnd = 16 + subPacketLength
            contents = remainder[16:contentsEnd]
            remainder = remainder[contentsEnd:]
            while len(contents) > 0:
                subPacket, contents = parse_next_packet(contents)
                subPackets.append(subPacket)
        else:
            numSubPackets = int(remainder[1:12], 2)
            remainder = remainder[12:]
            for _ in range(numSubPackets):
                subPacket, remainder = parse_next_packet(remainder)
                subPackets.append(subPacket)
        # print(f'Found operator with {len(subPackets)} children')
        return (Packet(version, typeId, contents=subPackets), remainder)

def main(input):
    num_bits = len(input) * 4
    binary_str = f'{int(input, 16):0>{num_bits}b}'
    packet, remainder = parse_next_packet(binary_str)
    # print(remainder)
    print(packet.value())

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()][0])
