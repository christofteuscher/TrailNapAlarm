
import sys
import time
import glob
import os

#print("RESET", flush=True)
#for i in range(0, 60):
#	time.sleep(1)
#	print("FILE", "filname{}.wav".format(i), flush=True)

# test with local files
#path_to_files = "res/data/sessions/prevsessions/"
path_to_files = "res/data/sessions/2022-06-06_Rec1_12v_76dB_Adh_DangSleep/"
pathname = f"{path_to_files}*.wav"
files = sorted(glob.glob(pathname), key=os.path.getmtime)

if __debug__:
    print(f"Length of files: {len(files)}", file=sys.stderr)

for file in files:
    time.sleep(.01)
    print("FILE", file, flush=True)

print("DONE")

# py -3 send.py | py -3 -u analysis.py
# python src/send.py | python -u src/analysis.py