import yasa
import sys
from buildRaw import buildRawFromArray
import numpy as np
from pathlib import Path
from scipy.io.wavfile import read
import os

# suppress sklearn pickle warning
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# data storage setup
# define array in which to concat entire session data
fullData = np.array([])
# define arrays of yasa prediction arrays
predictSets = []
probSets = []

# define minimum nap length
minNapMinutes = 8
minNapEpochs = minNapMinutes * 2
minN2epochs = 6

# set up stream
#os.environ["PYTHONUNBUFFERED"] = "1"

for line in sys.stdin:

    match line.split():

        case ["DONE"]:
            os.exit()

        case ["RESET"]:
            print("Do Reset")

        case ["FILE", filename]:
            if __debug__:
                print("retreiving file ", filename)
            # get directory to save data to
            dirname = os.path.dirname(filename)
            print(f'directory: {dirname}')
            # read file
            name = Path(filename).stem
            fs, epoch = read(filename)
            # 5 min minimum length of data to analyse
            Nmin = fs * 60 * 5
            # minimum nap length in samples
            minNapSamples = fs * minNapMinutes * 60
            # concat to fullData
            fullData = np.concatenate((fullData,epoch), axis=None)

            if len(fullData) < Nmin:
                pass
            else:
                # build mne raw object
                raw = buildRawFromArray(fs,fullData)
                # apply yasa analysis
                sls = yasa.SleepStaging(raw, eeg_name="Fz")
                y_pred = sls.predict()
                y_prob = sls.predict_proba()
                # add array of predictions for this chunk to array of chunk predictions
                predictSets.append(y_pred)
                probSets.append(y_prob)
                if __debug__:
                    print(f"{len(fullData)/fs} seconds analyzed")

            if len(fullData) > minNapSamples:
                count = np.count_nonzero(y_pred[minNapEpochs:] == "N2")
                print(f"counted {count} N2 stages")
                if count >= minN2epochs:
                    print("WAKEUP!")
                    break

if dirname:
    with open(f'{dirname}/predictions.txt', 'w') as f:
        for line in predictSets:
            print(' '.join(line).replace('W','W ').replace('R','R '), file=f)

    with open(f'{dirname}/predictprob.txt', 'w') as f:
        for line in probSets:
            print(line, file=f)