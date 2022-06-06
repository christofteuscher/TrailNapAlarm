import yasa
import numpy as np
from scipy.io.wavfile import read
from mne.filter import filter_data
import matplotlib.pyplot as plt

# This file defines functions for visualizing
# yasa detection functions
# much of this code was copied from 
# yasa notebooks by Raphael Vallat
# https://github.com/raphaelvallat/yasa/tree/master/notebooks

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

def spindlePlot(fs,indata,epochNum,title,window):

    # extract specified epoch
    start = 30 * epochNum * fs
    stop = 30 * (epochNum + 1) * fs
    data = indata[start:stop]
    ts = 1/fs
    N = len(data)
    t = np.arange(0,N*ts,ts)

    # detect sleep spindles
    sp = yasa.spindles_detect(data,fs)
    # check if sp detected spindles, if not, skip epoch
    if sp is None:
        y = applyFilt(data,window)
        print("No spindles detected")
        plt.figure(figsize=(14, 4))
        plt.plot(t, y, 'k')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([0, t[-1]])
        plt.title(f'{title} stage sleep for epoch {epochNum} (no spindles detected)')
        plt.tight_layout()
        return 1

    print(sp.summary().size)

    # bool vector indicating for each sample
    mask = sp.get_mask()

    y = applyFilt(data,window)

    spindles_highlight = y * mask
    spindles_highlight[spindles_highlight == 0] = np.nan

    plt.figure(figsize=(14, 4))
    plt.plot(t, y, 'k')
    plt.plot(t, spindles_highlight, 'indianred')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude (uV)')
    plt.xlim([0, t[-1]])
    plt.title(f'{title} stage sleep for epoch {epochNum} (spindles detected)')
    plt.tight_layout()
    # plt.savefig('detection.png', dpi=300, bbox_inches='tight')

def thresholdPlot(fs,indata,epochNum):
    title = 'spindles'

    # extract specified epoch
    start = 30 * epochNum * fs
    stop = 30 * (epochNum + 1) * fs
    data = indata[start:stop]
    ts = 1/fs
    N = len(data)
    t = np.arange(0,N*ts,ts)

    # detect sleep spindles
    sp = yasa.spindles_detect(data,fs)
    #print(sp.summary())

    # check if sp detected spindles, if not, skip epoch
    if sp is None:
        print("No spindles detected")
        return 1

    # assign peak spindle time to index array
    spTime = sp.summary()['Peak']

    # plot time series
    fig1 = plt.figure(figsize=(14,4))
    plt.plot(t,data)
    # min,max values in array
    lo,hi = [min(data),max(data)]
    # plot red vertical lines at every spindle peak
    for i in spTime:
        plt.vlines(i, lo, hi, colors='r')
    plt.title(f"{title} time series")
    plt.xlabel('time (s)')
    plt.ylabel('amplitude (uV)')
    # save and close figure
    plt.savefig(f"{title}_timeseries.png")
    plt.close()

    # threshold 1: sigma band detection
    # Broadband (1 - 30 Hz) bandpass filter
    freq_broad = (1, 30)
    data_broad = filter_data(data, fs, freq_broad[0], freq_broad[1], method='fir',verbose=0)

    # Compute the pointwise relative power using STFT and cubic interpolation
    f, t, Sxx = yasa.stft_power(data_broad, fs, window=2, step=.2, band=freq_broad, norm=True, interp=True)

    # Extract the relative power in the sigma band
    idx_sigma = np.logical_and(f >= 11, f <= 16)
    rel_pow = Sxx[idx_sigma].sum(0)

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    plt.subplots_adjust(hspace=.25)
    im = ax1.pcolormesh(t, f, Sxx, cmap='Spectral_r', vmax=0.2)
    ax1.set_title('Spectrogram')
    ax1.set_ylabel('Frequency (Hz)')
    ax2.plot(t, rel_pow)
    ax2.set_ylabel('Relative power (% $uV^2$)')
    ax2.set_xlim(t[0], t[-1])
    ax2.set_xlabel('Time (sec)')
    ax2.axhline(0.20, ls=':', lw=2, color='indianred', label='Threshold #1')
    plt.legend()
    _ = ax2.set_title('Relative power in the sigma band')
    plt.tight_layout()
    # save figure
    #plt.savefig(f"{title}_sigma_rel_power.png")

    # threshold 2: moving correlation
    data_sigma = filter_data(data, fs, 12, 15, l_trans_bandwidth=1.5, 
                         h_trans_bandwidth=1.5, method='fir', verbose=0)
    
    # window size 300ms, step size 100ms
    t, mcorr = yasa.moving_transform(data_sigma, data_broad, fs, window=.3, step=.1, method='corr', interp=True)

    plt.figure(figsize=(14, 4))
    plt.plot(t, mcorr)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Pearson correlation')
    plt.axhline(0.65, ls=':', lw=2, color='indianred', label='Threshold #2')
    plt.legend()
    plt.title('Moving correlation between $EEG_{bf}$ and $EEG_{\sigma}$')
    _ = plt.xlim(0, t[-1])
    plt.tight_layout()
    #plt.savefig(f"{title}_movcorrel.png")

    # threshold 3: moving rms
    t, mrms = yasa.moving_transform(data_sigma, data, fs, window=.3, step=.1, method='rms', interp=True)

    # Define threshold
    trimmed_std = yasa.trimbothstd(mrms, cut=0.025)
    thresh_rms = mrms.mean() + 1.5 * trimmed_std

    plt.figure(figsize=(14, 4))
    plt.plot(t, mrms)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Root mean square')
    plt.axhline(thresh_rms, ls=':', lw=2, color='indianred', label='Threshold #3')
    plt.legend()
    plt.title('Moving RMS of $EEG_{\sigma}$')
    _ = plt.xlim(0, data[-1])
    plt.tight_layout()
    #plt.savefig(f"{title}_movrms.png")

def swPlot(fs,indata,epochNum,title,window):

    # extract specified epoch
    start = 30 * epochNum * fs
    stop = 30 * (epochNum + 1) * fs
    data = indata[start:stop]
    ts = 1/fs
    N = len(data)
    t = np.arange(0,N*ts,ts)

    sw = yasa.sw_detect(data, fs)
    # check if sp detected spindles, if not, skip epoch
    if sw is None:
        print("No slow waves detected")
        y = applyFilt(data,window)
        plt.figure(figsize=(14, 4))
        plt.plot(t, y, 'k')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude (uV)')
        plt.xlim([0, t[-1]])
        plt.title(f'{title} stage sleep for epoch {epochNum} (no slow waves detected)')
        plt.tight_layout()
        return 1
    # To get the full detection dataframe, we use the .summary() method
    events = sw.summary()
    #print(events.round(2))

    # mask indicating for each sample
    mask = sw.get_mask()
    
    y = applyFilt(data,window)

    sw_highlight = y * mask
    sw_highlight[sw_highlight == 0] = np.nan

    plt.figure(figsize=(16, 4.5))
    plt.plot(t, y, 'k')
    plt.plot(t, sw_highlight, 'indianred')
    plt.plot(events['NegPeak'], sw_highlight[(events['NegPeak'] * fs).astype(int)], 'bo', label='Negative peaks')
    plt.plot(events['PosPeak'], sw_highlight[(events['PosPeak'] * fs).astype(int)], 'go', label='Positive peaks')
    plt.plot(events['Start'], data[(events['Start'] * fs).astype(int)], 'ro', label='Start')

    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude (uV)')
    plt.xlim([0, t[-1]])
    plt.title(f'{title} stage sleep for epoch {epochNum}')
    plt.legend()
    plt.tight_layout()
    #plt.savefig(f"{title}_slowwaves.png")
