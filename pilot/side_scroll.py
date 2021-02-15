from random import randint
from time import sleep
import fcntl
import termios
import struct


def terminal_size():
    th, tw, hp, wp = struct.unpack(
        'HHHH',
        fcntl.ioctl(
            0, termios.TIOCGWINSZ,
            struct.pack(
                'HHHH', 0, 0, 0, 0)))
    return tw, th


height, width = terminal_size()


def blank(count=8):
    output = []
    for _ in range(count):
        output.append(0)
    return output


if __name__ == "__main__":

    data = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        data.append(row)

    states = " X"
    index = width // 2
    while True:
        data.remove(data[0])
        index += randint(-1, +1)
        fresh = blank(width)
        fresh[index % width] = 1
        data.append(fresh)
        print('\033[2J')
        text = "\n"
        for x in range(len(data[0])):
            for y in range(len(data)):
                text += states[data[y][x]]
            text += "\n"
        print(text, end="")
        sleep(0.04)
