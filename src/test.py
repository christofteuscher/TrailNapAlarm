import yasa
from buildRaw import buildRawFromArray
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
import numpy as np
from mne.filter import filter_data
from testPlots import spindlePlot,swPlot

# suppress sklearn pickle warning
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

#OpenBCI Raw EEG Data
#Number of channels = 8
#Sample Rate = 250 Hz
#Board = OpenBCI_GUI$BoardCytonSerial

# read from our recorded data:
filepath = 'res/data/openBCI_Fz.wav'
fs, data = read(filepath)
data = data.astype(float)
raw = buildRawFromArray(fs,data)

# OR read from yasa example data
#filepath = 'res/data/yasaDatasets/sub-02_mne_raw.fif'
#raw = mne.io.read_raw_fif(filepath, preload=True, verbose=False)

# set window size for plot smoothing (doesn't affect analysis)
window = int(round(.05 * fs))
# choose epoch to plot
epoch = 28

sls = yasa.SleepStaging(raw, eeg_name="Fz")
y_pred = sls.predict()
y_proba = sls.predict_proba()
confidence = y_proba.max(1)
# set the title of each plot with the predicted sleep stage for that epoch
title = y_pred[epoch]
# display sleep stage predictions for each epoch
print(y_pred)

# filter
# threshold 1: sigma band detection
# Broadband (1 - 40 Hz) bandpass filter
freq_broad = (1, 30)
filtered = filter_data(data, fs, freq_broad[0], freq_broad[1], method='fir',verbose=0)

# iterate over several epochs and plot each one
#for i in range(2):
#    epoch = 22 + i
#    spindlePlot(fs,filtered,epoch,title,window)
#    #swPlot(fs,filtered,epoch,title,window)

spindlePlot(fs,filtered,epoch,title,window)
plt.show()
