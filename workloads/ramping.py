import time
for i in range(10):
    start = time.time()
    while (time.time() - start) < 60:
        print(i)
        time.sleep(1/(2**i))
        