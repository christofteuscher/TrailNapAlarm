import numpy as np
import math
from scipy.io.wavfile import write

# This program imports a .npz file format and extracts
# it into 60 second segmented .wav files
# This was written specifically for the dataset
# included in the yasa documentation

# npz data
x = np.load('../res/data/yasaDatasets/data_full_6hrs_100Hz_Cz+Fz+Pz.npz')
data, ch_names = x['data'], x['chan']
fs = 100
times = np.arange(data.size) / fs

# display head of npz data and duration
#print(data.shape, ch_names)
#print(np.round(data[:, 0:5], 3))

# extract Fz channel and write to wav
Fz = data[1:2].ravel()
duration  = data.shape[1]*(1/fs)
#print(f"duration: {duration/(60*60):.2f} hrs")
write("../res/data/yasaDatasets/Fz.wav",fs,Fz.astype(np.int16))

# extract 1st hour of same channel into epochs for analysis
N = Fz.size
Ncut = N // 6   # num of samples in 1st hour
Nepoch = 60*fs  # number of samples for 60 s
numEpochs = int(math.floor(Ncut/Nepoch))
i = 0
while i <= numEpochs:
    startindex = i * Nepoch
    endindex = startindex + Nepoch
    y = Fz[startindex:endindex]
    filename = f"Fz_{i}"
    write(f"../res/data/generatedData/{filename}.wav",fs,y.astype(np.int16))
    i += 1
    