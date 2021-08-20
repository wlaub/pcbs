import struct
import sys

raw = open(sys.argv[1], 'rb').read()

template = """
unsigned char buffer[{length}] = {{
{data}
}};

unsigned short length_map[8192] = {{
{lenmap}
}};
"""

lengths = []
for i in range(4096):
    addr = struct.unpack('I', raw[i*4:i*4+4])[0]
    actual_size = struct.unpack('H', raw[addr-2:addr])[0]
    lengths.append(actual_size)

lenset = sorted(list(set(lengths)))

lenmap = []
for i, actual_size in enumerate(lengths):
    setidx = lenset.index(actual_size)
    next_size = lenset[min(setidx+1, len(lenset)-1)]
    prev_size = lenset[max(setidx-1, 0)]
    lenmap.append(prev_size)
    lenmap.append(next_size)

result = template.format(
    length = len(raw), 
    data = ', '.join([f'0x{x:02x}' for x in raw]),
    lenmap = ', '.join([f'0x{x:04x}' for x in lenmap]),
    )

#print(result)
open("lookup_table.h", 'w').write(result)

