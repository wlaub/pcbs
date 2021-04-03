import sys
import time, math

import struct
import threading

import serial

from matplotlib import pyplot as plt
from matplotlib import animation as anim

"""
Notes: looks like I get about 160 KSPS to share with all ADCs.
3x ADCs can run at about 50 KSPS, which meets requirements but is a little
disappointing.

A single-channel high-speed mode might be an option, though this requires
multiple antialiasing filters and maybe implies using two pins per channel
for the two different bandwidths
"""

class Packet():
    def __init__(self, data):
        self.flag = data[0]
        self.data = data[1:]

class Receiver():
    chunk_size = 1024*8
    read_size = 1024

    def __init__(self, port, fig, ax):
        self.fig = fig
        self.ax = ax

        self.ser = serial.Serial(port, timeout=1)
        self.buff = b''
        self.rawdata = []
        self.packets = []

        self.receive_exit = threading.Event()
        self.timings = []
        
        self.prev_time = time.time()

    def shutdown(self):
        self.receive_exit.set()

    def receive(self):
        while not self.receive_exit.is_set():
            self.buff += self.ser.read(self.read_size)
            if len(self.buff) >= self.chunk_size*2:
                self.chunk = self.buff
                self.buff = b''

        self.ser.close()
       
    def parse_rawdata(self):

        raw = self.rawdata

        def find_next_index(raw):
            for idx, val in enumerate(raw):
                if val & 0x8000 != 0:
                    return idx
            return -1 


        #discard any partial packets
        if raw[0] & 0x8000 == 0:
            next_idx = find_next_index(raw)
            print(f'Discarding {next_idx} shorts of junk')
            raw = raw[next_idx:]

        time_accum = 0
        sample_count = 0

        while True:
            next_idx = find_next_index(raw[1:])+1
            if next_idx == 0: break

            packet_data, raw = raw[:next_idx], raw[next_idx:]

            pack = Packet(packet_data)
            time_accum += (pack.flag&0x7fff)
            self.packets.append(pack)
            sample_count += 1

        return sample_count,time_accum

        self.rawdata = raw

    def plot(self, frame, *fargs):
        size = 128

        bufflen = len(self.buff)

        if bufflen < self.chunk_size: return

        delta_time = time.time()-self.prev_time
        print(f'Rate: {(bufflen/delta_time)/1e6:.3f} MBps ({bufflen/1e3:.3f} kBytes, {delta_time*1000:.3f}) ms')
        self.prev_time = time.time()

        chunk = self.buff[-self.chunk_size:]
        self.buff = b''

        ndata = struct.unpack('H'*int(self.chunk_size/2), chunk)
#        self.rawdata.extend(ndata)
        self.rawdata = ndata
        count, delta = self.parse_rawdata()
        print(f'Rate: {1e6*count/delta}, Samples: {count}, delta: {delta}')

        if len(self.packets) < size: return
        self.ax.clear()
        xvals = list(range(size))

        packets = self.packets[-size:]
        
 
        for i in range(1):
            yvals = [x.data[i] for x in packets]
            self.ax.plot(xvals, yvals, linewidth = 1)


fig, ax = plt.subplots(1,1)



port = sys.argv[1]           
rec = Receiver(port, fig, ax)

receive_thread = threading.Thread(target=rec.receive)

ani = anim.FuncAnimation(fig, rec.plot, interval=20)

receive_thread.start()
try:
    plt.show()
#    while True:
#        print(f'Received {len(rec.packets)} packets')
#        time.sleep(1)
except KeyboardInterrupt: pass

print(f'Shutting down...')

rec.shutdown()

print(f'waiting for receiver to wrap up...')

receive_thread.join()

print(f'Finished.')

