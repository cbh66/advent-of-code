#!/usr/bin/python3

import sys

class Packet:
    def __init__(self, version, children, value):
        self.version = version
        self.children = children
        self.value = value

    def __repr__(self):
        ver = self.version
        cld = len(self.children) if self.children else 'None'
        val = self.value if self.value else 'None' 
        return f'ver={ver}, cld={cld}, val={val}'

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
        return (Packet(version, children=[], value=int(value_str, 2)), remainder)
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
        return (Packet(version, subPackets, value=None), remainder)

def version_sums(packet):
    return packet.version + sum(version_sums(c) for c in packet.children)

def main(input):
    num_bits = len(input) * 4
    binary_str = f'{int(input, 16):0>{num_bits}b}'
    packet, remainder = parse_next_packet(binary_str)
    # print(remainder)
    print(version_sums(packet))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()][0])
