def forever(f):
    while True:
        try:
            f()
        except:
            break
