import time
# Run for 5 minutes
start = time.time()
while (time.time() - start) < 300:
    for i in range(30000):
        print(i)
    time.sleep(20)
