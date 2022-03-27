This folder contains functions to break up a yasa dataset into 60 second epochs and then analyze each epoch with plots using yasa algorithms for sleep spindle and slow wave detection.

Required libraries:
* numpy
* scipy
* yasa
* mne
* matplotlib

It is recommended to use a virtual environment to easily keep track of dependencies. Anaconda is a package handler for python which is useful for this, and includes some required libraries.

The order in which to use these programs is:

* datasetup.py breaks apart the yasa dataset included in ../res/ subfolder into 60s epochs
* the epochs are stored as wav files in ../res/data/generatedData
* test.py calls functions in defEpoch.py using the Epoch class
* figures are produced which will be stored in ../res/generatedFigs/ subfolder

The generatedData and generatedFigs subfolders are ignored by git so that they don't get clogged with each person's use of the program.