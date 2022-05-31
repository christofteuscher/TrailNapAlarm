
import sys
import time

print("RESET", flush=True)
for i in range(0, 60):
	time.sleep(1)
	print("FILE", "filname{}.wav".format(i), flush=True)

# py -3 send.py | py -3 -u read.py