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
files = ['../res/data/generatedData/Fz_9.wav',
         '../res/data/generatedData/Fz_10.wav',
         '../res/data/generatedData/Fz_11.wav',
         '../res/data/generatedData/Fz_12.wav',
         '../res/data/generatedData/Fz_13.wav',
         '../res/data/generatedData/Fz_14.wav',
         '../res/data/generatedData/Fz_15.wav',
         '../res/data/generatedData/Fz_16.wav',
         '../res/data/generatedData/Fz_17.wav',
         '../res/data/generatedData/Fz_18.wav',
         '../res/data/generatedData/Fz_19.wav',
         '../res/data/generatedData/Fz_20.wav',]
autoSleepScore(files)