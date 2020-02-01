import struct
import sys

raw = open(sys.argv[1], 'rb').read()

template = """
unsigned char buffer[{length}] = {{
{data}
}};

"""

result = template.format(
    length = len(raw), 
    data = ', '.join([f'0x{x:02x}' for x in raw])
    )

open("lookup_table.h", 'w').write(result)

