import yasa
from buildRaw import buildRawFromArray
import numpy as np
from pathlib import Path
from scipy.io.wavfile import read
import os
import glob
import time

# This section checks for unread 30s files in the current session directory every 5 sec
# it reads unread files into a chunk array until the chunk is 5 mins long
# then it does sleep stage detection for N2 stage
# if N2 threshold not met, it deletes first 30s in chunk, shifts data left, then
# checks for new unread file and concats to chunk and repeats

# directory setup
path_to_files = "../res/data/sessions/currentsession/"
pathname = f"{path_to_files}unread_*.wav"

# chunk setup
epochLength = 30    # seconds
Nc = 10             # number of epochs per chunk
# define chunk array
chunk = np.array([])
# stand-in sample freq gets changed when reading wav file
fs = 250
fullChunkLength = epochLength * Nc * fs
# define array of yasa prediction arrays
# each array is the output of the yasa sleep stage prediction
# where W = awake, N1, N2, N3 are sleep stages, and R is REM
chunkPredictions = []

while 1:
    #files = glob.glob(pathname)
    files = sorted(glob.glob(pathname), key=os.path.getmtime)
    if files:

        print(files)
        # get most recent file
        #chosen_file = max(files, key=os.path.getctime)

        # get oldest file first
        chosen_file = files[0]
        name = Path(chosen_file).stem
        fs, epoch = read(chosen_file)

        #print(chosen_file)
        #print(name)

        # concat most recent file with previous chunk
        fullChunkLength = epochLength * Nc * fs
        print(f"fs = {fs}")
        if len(chunk) < fullChunkLength:
            #print("chunk size too small")
            #print(f"chunk size before concat: {len(chunk)} < {fullChunkLength}")
            chunk = np.concatenate((chunk,epoch), axis=None)
            #print(f"chunk size after concat: {len(chunk)} <= {fullChunkLength}")
        elif len(chunk) == fullChunkLength:
            #print(f"rolling chunk: length {len(chunk)}")
            # remove first epoch and resize chunk
            chunk = chunk[epochLength * fs:]
            chunk = np.concatenate((chunk,epoch), axis=None)
        else:
            print(f"chunk size {len(chunk)} unreasonable")

        if len(chunk) == fullChunkLength:
            # build mne raw object
            raw = buildRawFromArray(fs,chunk)
            # apply yasa analysis
            sls = yasa.SleepStaging(raw, eeg_name="Fz")
            y_pred = sls.predict()
            # add array of predictions for this chunk to array of chunk predictions
            chunkPredictions.append(y_pred)
            # keep track of epoch N2 predictions
            count = np.count_nonzero(y_pred == "N2")
            #print(y_pred)
            #print(count)
        
        # rename file as read so it won't be read again
        newName = name.replace("un","")
        new_pathname = f"{path_to_files}{newName}.wav"
        os.rename(chosen_file,new_pathname)
        
    elif not files:
        print("no new files")
        time.sleep(5)
