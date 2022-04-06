import mne
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt

# this file loads data into an raw mne format
# storing data like this allows us to include metadata in a way
# that can be implemented with mne functions and saved as an edf file

def buildRawFromNpz(fs, filepath):

    # load data
    x = np.load(filepath)
    data, chan_names = x['data'], x['chan']
    #times = np.arange(data.size) / fs
    num_chan = data.shape[0]

    # verify data
    print(data.shape, chan_names)
    print(np.round(data[:, 0:5], 3))

    # create metadata for raw edf
    ch_names = []
    for name in chan_names:
        ch_names.append(f"{name}")
    ch_types = ['eeg'] * num_chan
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=fs)
    # standard spatial orientation based on channel names
    info.set_montage('standard_1020')

    # save as raw format
    raw = mne.io.RawArray(data, info)

    # sample data is not in SI units, which is what mne raw expects
    # we have to scale the data to the expected uV range
    raw.apply_function(lambda x: x * .2e-6)
    raw.plot(show_scrollbars=False, show_scalebars=False)
    plt.show()

    return raw

def buildRawFromWav(filepath):
    # read sample freq and data from file
    fs, data = read(filepath)
    N = data.size
    data = [data,np.zeros(N)]

    num_chan = 2
    ch_names = ['Fz', 'Fp1']
    ch_types = ['eeg'] * num_chan
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=fs)
    # standard spatial orientation based on channel names
    info.set_montage('standard_1020')

    # save as raw format
    raw = mne.io.RawArray(data, info)

    # sample data is not in SI units, which is what mne raw expects
    # we have to scale the data to the expected uV range
    raw.apply_function(lambda x: x * .2e-6)
    #raw.plot(show_scrollbars=False, show_scalebars=False)
    #plt.show()

    return raw

def buildRawFromArray(fs, array):
    N = len(array)
    array = [array,np.zeros(N)]

    num_chan = 2
    ch_names = ['Fz', 'Fp1']
    ch_types = ['eeg'] * num_chan
    info = mne.create_info(ch_names, ch_types=ch_types, sfreq=fs)
    # standard spatial orientation based on channel names
    info.set_montage('standard_1020')

    # save as raw format
    raw = mne.io.RawArray(array, info)

    # sample data is not in SI units, which is what mne raw expects
    # we have to scale the data to the expected uV range
    raw.apply_function(lambda x: x * .2e-6)
    raw.plot(show_scrollbars=False, show_scalebars=False)
    plt.show()

    return raw

# test functions
#filepath = '../res/data/yasaDatasets/data_full_6hrs_100Hz_Cz+Fz+Pz.npz'
#buildRawFromNpz(100, filepath)

filepath = '../res/data/generatedData/Fz_10.wav'
raw = buildRawFromWav(filepath)