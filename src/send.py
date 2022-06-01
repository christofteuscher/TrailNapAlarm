
import sys
import time
import glob
import os

print("RESET", flush=True)
#for i in range(0, 60):
#	time.sleep(1)
#	print("FILE", "filname{}.wav".format(i), flush=True)

# test with local files
path_to_files = "../res/data/sessions/prevsession/"
pathname = f"{path_to_files}unread_*.wav"
files = sorted(glob.glob(pathname), key=os.path.getmtime)
for file in files:
    time.sleep(1)
    print(file,flush=True)

# py -3 send.py | py -3 -u read.py