def transpose(data):
    visited = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if (y, x) not in visited:
                data[y][x], data[x][y] = data[x][y], data[y][x]
                visited.append((x, y))


if __name__ == '__main__':
    data = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [1, 1, 1, 1]
    ]
    expected = [
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1],
        [0, 1, 0, 1]
    ]

    transpose(data)
    print(data)
