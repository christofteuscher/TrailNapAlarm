# Description of program files and their context

Core application function is handled by record.py, analysis.py, and buzzer.py.

Python programs are connected via piping to form the core function.

## record.py

## analysis.py

This program implements the YASA sleep staging algorithm and determines when to wake the user based on a specified N2 epoch count threshold. It takes a file path as a command line argument and concatenates it to an ongoing array of the current sleep session's EEG time series data, with a corresponding sample rate. Once the array of data has surpassed the minimum analysis duration of 5 minutes, as well as the minimum sleep duration specified, it creates a SleepStaging instance to determine the predicted sleep stages for each epoch of recorded data. It repeats this each time it recieves a new filepath, which is every 30 seconds. Once the previous conditions are met, and an N2 threshold is surpassed or the maximum sleep duration has passed, the program activates the alarm system.

User preferences are defined at the top of this file:

minNapMinutes: integer, the minimum number of minutes that the nap should last. The program will not start counting N2 stages detected before this time. This is especially helpful at the start of the program, when predicted sleep stages can be less reliable, so we don't accidentally wake the user too soon.

maxNapMinutes: integer, the maximum number of minutes that the nap should last. As a default, in case the N2 threshold count is not met, the program will wake the user after this number of minutes has elapsed.

minN2epochs: integer, the N2 threshold count. The program will wake the user after this many epochs (30 second segments) have been predicted as stage N2 sleep.

## buzzer.py


## buildRaw.py

This module contains definitions for functions which translate different data formats into the MNE "raw" object type. The YASA SleepStaging class takes a raw object type. The current formats are .npz, .wav, and array with a corresponding sample rate.

buildRawFromNpz(fs, filepath)

    fs:         integer, sample rate
    filepath:   string, path to the file

buildRawFromWav(filepath)

    filepath:   string, path to the file

buildRawFromArray(fs, array)

    fs:         integer, sample rate
    filepath:   string, path to the file



## dataSetup.py

This program is used entirely for testing and development, and is not implemented in the functioning of the device itself. It was written as a sandboxing tool for reading different recording file times, from various datasets and devices, and cutting them up into 30 second .wav files to simulate data being fed to analysis.py

## read.py

A test file used in conjunction with send.py. This program is piped a command and a file name from send.py and follows the command sent.


## send.py

A test file that creates a list of files in a directory, then sends the path name to analysis.py one at a time to test the functioning of piping recording file names to the analysis program.

## test.py

Uses functions defined in testPlots.py to make certain plots and analyses on datasets gathered by the team. Given a directory with a .wav file of sleep data, it returns the predicted sleep stages of that dataset and makes a plot of a specified epoch with any detected sleep spindles highlighted.

## testPlots.py

This module contains definitions for functions used in test.py.

spindlePlot(fs,indata,epochNum,title,window)

    fs:         integer, specifies the sample rate of the data
    indata:     array of real-valued data to be plotted
    epochNum:   integer, which 30 second segment to display
    title:      string, the predicted sleep stage of the plotted epoch
    window:     integer, length in samples of the moving average window to smooth plot output (doesn't affect analysis)

The other functions in testPlots.py weren't used in this project.

## Unused/Retired Files

We archive unused files in the `_unused` folder.

-  `btnWake.py` Poll for a change on an analog read pin as a makeshift interrupt. Used for initial i2c bringup. Owner: Michael
- `collectData_0.1.py` Initial pass at i2c code without interurpt. Timing was a problem even here. Owner: Michael
- `collectData_0.2.py` Version 2 of i2c code. This eventually formed into `record.py`. Owner: Julia
- `every.py` Attempt at abstracting away precise timing with python. Retired for interrupt based timing from ADC source. Could be useful for future work. Owner: Julia
- `pollData.py` Initial implementation of i2c code. Owner: Michael
- `pollStart.py` Initial implementation of i2c code. Owner: Michael

