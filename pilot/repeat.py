def forever(f: function):
    while True:
        try:
            f()
        except e:
            break
