# using mne-notebook env
import numpy as np
import scipy as sp

# define epoch class
class Epoch:

    # init constructor
    def __init__(self, fs, tSeries):
        self.tSeries = tSeries
        self.fs = fs
        self.t = np.arange(tSeries.size) / fs
        self.duration = tSeries.size / fs
    
    # fft spectrum method
    def spectrum(self):
        spect = 20*np.log10(abs(sp.fft.fft(self.tSeries)))
        spect = spect[:spect.size//2]
        f = np.linspace(0,self.fs,spect.size)
        return f,spect

    # state variable defaults to "raw" unanalyzed data
    # when not default, stores detected sleep stage
    state = "raw"
