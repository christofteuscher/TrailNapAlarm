import yasa
from buildRaw import buildRawFromArray
from scipy.io.wavfile import read
import pandas as pd

filepath = 'res/data/openBCI_Fz.wav'
#filepath = '../res/data/yasaDatasets/Fz.wav'
fs, data = read(filepath)
raw = buildRawFromArray(fs,data)

#filepath = 'res/data/yasaDatasets/sub-02_mne_raw.fif'
#raw = mne.io.read_raw_fif(filepath, preload=True, verbose=False)
print('The channels are:', raw.ch_names)
print('The sampling frequency is:', raw.info['sfreq'])

sls = yasa.SleepStaging(raw, eeg_name="Fz")
y_proba = sls.predict_proba()
confidence = y_proba.max(1)
print(confidence)
print(y_proba)

print(y_proba['N2'])