import datetime

import serial
import matplotlib.pyplot as plt
import keyboard
import xlsxwriter

saveMode = False
width = 1
xOffset = 0

def export_current_fig():
    global x, y
    displayX = list(filter(lambda e: (x[-1] - width * 1000000) - xOffset < e < x[-1] - xOffset, x))
    displayY = list(y[x.index(displayX[0]) - 1: x.index(displayX[-1])])

    workbook = xlsxwriter.Workbook(f"{str(datetime.datetime.now()).replace('/', '-').replace(':', '.')}.xlsx")
    worksheet = workbook.add_worksheet(f"{str(datetime.datetime.now()).replace('/', '-').replace(':', '.')}")

    worksheet.write(0, 0, "x")
    worksheet.write(0, 1, "y")

    for i in range(len(displayX)):
        worksheet.write(i + 1, 0, displayX[i])
        worksheet.write(i + 1, 1, displayY[i])

    workbook.close()


def keyboard_hook(keyboard_event: keyboard.KeyboardEvent):
    global saveMode, width, xOffset

    if keyboard_event.event_type != "down":
        return

    if keyboard_event.name == "x":
        xOffset = 0
        saveMode = not saveMode

    elif keyboard_event.name == "up":
        width += 0.1
    elif keyboard_event.name == "down":
        width = max(0.1, width - 0.1)

    elif keyboard_event.name == "left":
        xOffset += 50000
    elif keyboard_event.name == "right":
        xOffset -= 50000

    elif keyboard_event.name == "e":
        export_current_fig()


keyboard.hook(keyboard_hook)

ser = serial.Serial("/dev/ttyUSB1", 115200, timeout=0.0)

buf = b""
x = []
y = []

plt.ion()
graph = plt.plot(x, y)[0]
plt.ylim(-.1, 3.4)
plt.xlabel("t / μs")
plt.ylabel("U / V")
plt.pause(.1)
n = 0

while True:
    if saveMode:
        plt.pause(.1)
        plt.xlim((x[-1] - width * 1000000) - xOffset, x[-1] - xOffset)
        plt.title(f"xOffset: {round(-xOffset / 1000)} ms, width: {round(width * 1000)} ms")
        continue
    l = ser.read(1)
    buf += l

    if len(buf) >= 4 and buf[-4:] == b"\xb3\x8f\x0f\xf8":
        if len(buf) != 10:
            buf = b""
            print("malformed")
            continue

        t = int.from_bytes(buf[:4], signed=False, byteorder="big")
        v = int.from_bytes(buf[4:6], signed=False, byteorder="big")

        v = (v / 4095) * 3.3

        x.append(t)
        y.append(v)

        if n % 200 == 0:
            graph.remove()
            graph = plt.plot(x, y, color='g')[0]
            plt.xlim((x[-1] - width * 1000000) - xOffset, x[-1] - xOffset)
            plt.title(f"xOffset: {round(-xOffset / 1000)} ms, width: {round(width * 1000)} ms")
            plt.pause(.0001)

        buf = b""
        n += 1
