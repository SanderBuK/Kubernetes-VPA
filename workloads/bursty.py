import time
start = time.time()
# Run for 5 minutes
while (time.time() - start) < 300:
    for i in range(30000):
        print(i)
        time.sleep(0.0006)
    time.sleep(40)