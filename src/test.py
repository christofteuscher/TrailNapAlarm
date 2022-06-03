import yasa
from buildRaw import buildRawFromArray
from scipy.io.wavfile import read
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mne.filter import filter_data
from testPlots import spindlePlot

# defined functions
# mov avg to smooth plot
def moving_avg(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def applyFilt(data,w):
    N = len(data)
    v = np.zeros(N)
    g = moving_avg(data,w)
    if len(g) <= N:
        v[:len(g)] = g
    else:
        v = g[:N]
    return v

#OpenBCI Raw EEG Data
#Number of channels = 8
#Sample Rate = 250 Hz
#Board = OpenBCI_GUI$BoardCytonSerial

# read from our recorded data
filepath = 'res/data/openBCI_Fz.wav'
#filepath = '../res/data/yasaDatasets/Fz.wav'
fs, data = read(filepath)
data = data.astype(float)
raw = buildRawFromArray(fs,data)

# read from yasa example data
#filepath = 'res/data/yasaDatasets/sub-02_mne_raw.fif'
#raw = mne.io.read_raw_fif(filepath, preload=True, verbose=False)

sls = yasa.SleepStaging(raw, eeg_name="Fz")
y_pred = sls.predict()
y_proba = sls.predict_proba()
confidence = y_proba.max(1)
#print(y_proba['N2'])
print(y_pred)

# filter
# threshold 1: sigma band detection
# Broadband (1 - 40 Hz) bandpass filter
freq_broad = (1, 30)
filtered = filter_data(data, fs, freq_broad[0], freq_broad[1], method='fir',verbose=0)

# filter for plotting
y = applyFilt(filtered,15)

# choose epoch to plot
epoch = 20
pred = y_pred[epoch]
Nstart = fs * 30 * epoch
Nend = Nstart + (fs * 30)
segment = y[Nstart:Nend]
ts = 1/fs
N = len(segment)
t = np.arange(0,N*ts,ts)

#segment = np.where(abs(y) <= 0.2, y, 0)

# times series plot
#fig, ax = plt.subplots(figsize=(10,4))
#ax.set_title('EEG time series with corresponding sleep stages')
#ax.set_xlabel('time (s)')
#ax.set_ylabel('Amplitude')

#ax.plot(t,segment)
#ax.set_xlabel('time (s)')

spindlePlot(fs,filtered,31)
plt.tight_layout()
plt.show()

'''
# frequency spectrum plot
Nf = len(x2)
f = np.linspace(0,fs,Nf)
spect = 20*np.log10(abs(sp.fft.fft(x2)))
pltlen = Nf//4
fig2 = plt.figure(figsize=(14,4))
plt.plot(f[:pltlen],spect[:pltlen])
plt.title("Power Spectral Density")
plt.xlabel('frequency (Hz)')
plt.ylabel('magnitude (dB)')
#plt.show()


# show stages
y = y_pred[:]
#y += [y[-1]] # add last string to list so last plot line shows
x = list(range(0, len(y)*30, 30))
ax2 = ax.twinx()
ax2.step(x,y,where='post',color='red')
ax2.set_ylabel('Sleep stage')
plt.tight_layout()
plt.show()
'''