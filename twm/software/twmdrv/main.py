import serial
import struct
import time

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

with serial.Serial('/dev/ttyACM0', 115200) as ser:
    for offset in range(30):
        start_time = time.time()
        data = make_colors(offset, 0,0,0,255)
        raw = compose(0, data)
        ser.write(raw)

        data = make_colors(offset, 0,0,0,255)
        raw = compose(1, data)
        ser.write(raw)



        time.sleep(.1)
