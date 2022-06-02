
import sys
import time
import glob
import os

print("RESET", flush=True)
#for i in range(0, 60):
#	time.sleep(1)
#	print("FILE", "filname{}.wav".format(i), flush=True)

# test with local files
path_to_files = "res/data/sessions/prevsessions/"
pathname = f"{path_to_files}unread_*.wav"
files = sorted(glob.glob(pathname), key=os.path.getmtime)

if __debug__:
    print(f"Length of files: {len(files)}", file=sys.stderr)

for file in files:
    time.sleep(.01)
    print("FILE", file, flush=True)

# py -3 send.py | py -3 -u read.py
# python src/send.py | python -u src/analysis.py