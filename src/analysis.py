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
dirname = None
file_predictions = None
file_probabilities = None

for line in sys.stdin:

    match line.split():

        case ["DONE"]:
            if file_predictions:
                file_predictions.close()
                file_predictions = None
            if file_probabilities:
                file_probabilities.close()
                file_probabilities = None
            os.exit()

        case ["RESET"]:
            print("Do Reset", file=sys.stderr)

        case ["FILE", filename]:
            if __debug__:
                print("retreiving file ", filename, file=sys.stderr)
            # get directory to save data to
            dirname = os.path.dirname(filename)
            if file_predictions is None:
                file_predictions = open(f'{dirname}/predictions.txt', 'w')
            if file_probabilities is None:
                file_probabilities = open(f'{dirname}/predictprob.txt', 'w')

            print(f'directory: {dirname}', file=sys.stderr)
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
                #predictSets.append(y_pred)
                #probSets.append(y_prob)

                print(' '.join(y_pred).replace('W','W ').replace('R','R '), file=file_predictions)
                print(y_prob, file=file_probabilities)

                if __debug__:
                    print(f"{len(fullData)/fs} seconds analyzed", file=sys.stderr)

            if len(fullData) > minNapSamples:
                count = np.count_nonzero(y_pred[minNapEpochs:] == "N2")
                print(f"counted {count} N2 stages", file=sys.stderr)
                if count >= minN2epochs:
                    print("WAKEUP")
                    print("WAKEUP!", file=sys.stderr)
                    break
