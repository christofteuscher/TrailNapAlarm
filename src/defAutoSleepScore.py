import yasa
import numpy as np
from defEpoch import Epoch
from buildRaw import buildRawFromArray
from scipy.io.wavfile import read

# yasa auto sleep scoring requries at least 5 mins of data
# this function concats 10 consecutive epochs for analysis
# it takes an array of file names

def autoSleepScore(files):
    # read each wav file and concat
    array = []
    for file in files:
        fs, data = read(file)
        array = np.append(array,data)

    #print(len(array))
    raw = buildRawFromArray(fs, array)

    sls = yasa.SleepStaging(raw, eeg_name="Fz")
    y_pred = sls.predict()
    print(y_pred)

#filepath = '../res/data/generatedData/Fz_10.wav'
files = []
for i in range(12):
    files.append(f"../res/data/generatedData/Fz_{i+8}.wav")

autoSleepScore(files)