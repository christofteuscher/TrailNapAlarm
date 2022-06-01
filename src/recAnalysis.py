import yasa
import sys
from buildRaw import buildRawFromArray
import numpy as np
from pathlib import Path
from scipy.io.wavfile import read
import os
import glob
import time

# data storage setup
# define array in which to concat entire session data
fullData = np.array([])
# define array of yasa prediction arrays
# each array is the output of the yasa sleep stage prediction
# where W = awake, N1, N2, N3 are sleep stages, and R is REM
predictSets = []

# set up stream
os.environ["PYTHONUNBUFFERED"] = "1"

for line in sys.stdin:

    match line.split():

        case ["QUIT"]:
            os.exit()

        case ["RESET"]:
            print("Do Reset")

        case ["FILE", filename]:

            # get directory to save data to
            dirname = os.path.dirname(filename)
            # read file
            name = Path(filename).stem
            fs, epoch = read(filename)
            # min length of data to analyse
            Nmin = fs * 60 * 5
            # concat to fullData
            fullData = np.concatenate((fullData,epoch), axis=None)

            if len(fullData) < Nmin:
                continue
            else:
                # build mne raw object
                raw = buildRawFromArray(fs,fullData)
                # apply yasa analysis
                sls = yasa.SleepStaging(raw, eeg_name="Fz")
                y_pred = sls.predict()
                # add array of predictions for this chunk to array of chunk predictions
                predictSets.append(y_pred)
                print(f"{fs*len(fullData)} seconds analyzed")

            