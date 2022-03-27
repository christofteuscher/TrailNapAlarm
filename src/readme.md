This folder contains functions to break up a yasa dataset into 60 second epochs and then analyze each epoch with plots using yasa algorithms for sleep spindle and slow wave detection.

The order in which to use these programs is:

* datasetup.py breaks apart the yasa dataset included in ../res/ subfolder into 60s epochs
* the epochs are stored as wav files in ../res/data/generatedData
* test.py calls functions in defEpoch.py using the Epoch class
* figures are produced which will be stored in ../res/generatedFigs/ subfolder

The generatedData and generatedFigs subfolders are ignored by git so that they don't get clogged with each person's use of the program.