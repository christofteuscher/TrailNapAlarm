import numpy as np
import math
import pandas as pd
from scipy.io.wavfile import write
import time

# This program imports a .npz file format and extracts
# it into 60 second segmented .wav files
# This was written specifically for the dataset
# included in the yasa documentation

# npz data
x = np.load('../res/data/yasaDatasets/data_full_6hrs_100Hz_Cz+Fz+Pz.npz')
data, ch_names = x['data'], x['chan']
fs = 100
times = np.arange(data.size) / fs

# extract Fz channel and write to wav
Fz = data[1:2].ravel()
#duration  = data.shape[1]*(1/fs)
#print(f"duration: {duration/(60*60):.2f} hrs")
writePath = "../res/data/yasaDatasets/Fz.wav"
# write long file
write(writePath,fs,Fz.astype(np.int16))

# npz separation
# extract 1st hour of same channel into epochs for analysis
N = Fz.size
Ncut = N // 6   # num of samples in 1st hour
Nepoch = 60*5*fs  # number of samples for 5 mins
numEpochs = int(math.floor(Ncut/Nepoch))

i = 0
while i <= numEpochs:
    startindex = i * Nepoch
    endindex = startindex + Nepoch
    y = Fz[startindex:endindex]
    filename = f"Fz_{i}"
    write(f"../res/data/generatedData/{filename}.wav",fs,y.astype(np.int16))
    i += 1
    time.sleep(.5)

'''
# If the data is saved in the openBCI format:
filepath = 'OpenBCI-RAW-2022-05-17_15-04-27 1 channel 20 mins.txt'
fs = 250
# read data
df = pd.read_csv(filepath, sep=",")
N = len(df)
columns = list(df)
# extract a particular column:
Fz = df[columns[2]]
writePath = "../res/data/yasaDatasets/openBCI_Fz.wav"

# separate into 30 second epochs and write to wav files
N = Fz.size
seconds = 30
Nepoch = seconds * fs   # number of samples per epoch
numEpochs = int(math.floor(N/Nepoch))
print(numEpochs)

i = 0
while i <= numEpochs:
    startindex = i * Nepoch
    endindex = startindex + Nepoch
    y = Fz[startindex:endindex]
    filename = f"Fz_{i}"
    write(f"../res/data/sessions/prevsessions/unread_{filename}.wav",fs,y.astype(np.int16))
    i += 1
    time.sleep(.5)
'''