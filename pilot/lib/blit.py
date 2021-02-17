def blit(source, target, ox, oy):
    for sy in range(len(source)):
        for sx in range(len(source[0])):
            target[sy + oy][sx + ox] = source[sy][sx]


def blit_wrap(source, target, ox, oy):
    for sy in range(len(source)):
        for sx in range(len(source[0])):
            target[(sy + oy) % len(target)][(sx + ox) % len(target[0])] = source[sy][sx]


if __name__ == "__main__":
    source = [
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1]
    ]
    target = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    blit_wrap(source, target, 5, 5)
    for row in target:
        for value in row:
            print(value, end="")
        print("")
