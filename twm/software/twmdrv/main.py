import serial
import struct
import time
import sys

class Color:
    def __init__(self, r,g,b,w):
        self.r=r
        self.g=g
        self.b=b
        self.w=w

    def to_bytes(self):
        res = ''.join([f'{x:02x}' for x in [self.w, self.r, self.g, self.b]])
        return bytes(res, encoding='ascii')

def make_colors(pos, r, g, b, w):
    result = []
    for i in range(30):
        if i == pos:
            result.append(Color(r,g,b,w))
        else:
            result.append(Color(0,0,0,0))
    return result

def serialize_colors(data):
    return b''.join(x.to_bytes() for x in data)

def compose(idx, data):
    result = idx.to_bytes(1,byteorder='big')
    result += serialize_colors(data)
    result += b'\xff'*8
    return result

r,g,b,w = map(int, sys.argv[1:5])
c = Color(r,g,b,w)
k = Color(0,0,0,0)

data = [k]*30
for i in range(30):
    data[i] = c

hwdata=[
*([Color(0,0,0,0)]*1),
*([Color(0,0,0,128)]*7),
*([Color(0,0,0,0)]*7),
]

#sides = [k, Color(255,0,0,0), k]*5
#sides.append(sides[0])

sides = [k, k, Color(255,0,0,0), k, k]*3
sides[7] = Color(255,0,0,8)

with serial.Serial('/dev/ttyACM0', 115200) as ser:

    ser.write(compose(1, [k]*15))
    ser.write(compose(2, [k]*15))
    ser.write(compose(3, [k]*15))
    ser.write(compose(4, [k]*15))

    ser.write(compose(0, data))
#    for i in [1,2,3,4]:
#        ser.write(compose(i, sides))


#    ser.write(compose(1, data[:15]))
#    ser.write(compose(3, data[:15]))
#    ser.write(compose(1, hwdata))
#    ser.write(compose(1, [Color(0,0,0,255)]*15))
#    ser.write(compose(2, [Color(0,0,0,4)]*15))
#    ser.write(compose(3, [Color(0,0,0,0)]*15))
#    ser.write(compose(4, [Color(4,0,8,0)]*15))

   
