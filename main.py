import serial
from time import sleep

uno = serial.Serial(port="COM3", baudrate=115200)
print("Arduino UNO is connected.\n")
uno.write(("\n").encode())
res = uno.readline()
print("ready!\n")

import threading
import matplotlib.pyplot as plt
import sys

class Analog:
    def __init__(self):
        self.data = []
        self.index = 0
        pass

    def update(self):
        try:
            res = uno.readline()
            res = res.decode()[:len(res)-1]
            print("upper======================")
            print(res.replace("\n", ""))
            print("lower======================")
            self.data.append(float(res.replace("\n", "")))
            sleep(0.02)
        except Exception:
            pass

    def get_now_data(self, size):
        if len(self.data) < size:
            return [0]*(size-len(self.data))+self.data
        else:
            return [v for v in self.data][-size:]


analog = Analog()


class Updater(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stop = False

    def run(self):
        global analog
        while True:
            analog.update()
            sleep(0.000001)
            if self.stop:
                break


t1 = Updater("Thread 1: Updater")
t1.start()

fig = plt.figure()
ax = "None"

def exiter(_):
    t1.stop = True
    sys.exit()
    
while True:
    data = analog.get_now_data(30)
    if ax == "None":
        ax = fig.add_subplot(1, 1, 1)
    ax.plot(data)
    ax.set_ylim([-1.2, 1.2])
    plt.pause(0.01)
    fig.canvas.mpl_connect("close_event", exiter)
    ax.cla()
