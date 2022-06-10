# Description of program files and their context

Core application function is handled by record.py, analysis.py, and buzzer.py.

Python programs are connected via piping to form the core function.

## record.py

Sample and record brainwave data from ADC. Send data to analysis.py for processing. 

```
Usage: record.py [options]

Record sampled EEG data.

Options:
  -h, --help            show this help message and exit
  --wav                 Save epoch as wav file format.
  --csv                 Save epoch as csv file format. (Not Implemented)
  -s EPOCH_SECONDS, --seconds=EPOCH_SECONDS
                        Number of seconds in each epoch.
  -n NUM_EPOCHS, --num_epochs=NUM_EPOCHS
                        Number of epochs to record.
  -v, --view_samples    Display samples at a reduced rate.
```

Command line options exist for testing and debug. We can set epoch size and the number of epochs to record as well as enable viewing scaled sample values directly from command line.

We usually run with `python3 record.py --wav` and pipe output into the `analysis.py` program for processing.

### ADS1115 Configuration

We configure the ADS1115 to read data in the ±1.024 range. We sample data on the AIN2 pin with AIN3 as the zero reference. The configuration string `0b0_011_011_0_101_00000` is sent over I2C to initialize the continuous sampling. The device is configured to send interrupts when the data is ready.

We setup an interrupt service routine to watch for interrupts on the device.

### Checking the Timing of the ADS1115

Readings were taking a longer then expected time for the configured Samples Per Second (SPS) value. Used the oscilloscope to check the timing of the interrupt pulses. We noticed the rate was not correct. Checked generated rate by scope for 250 SPS and measured 243 Hz. Added code to time elapsed time over the span of a 30s epoch. We have the optoion to correct the recored rate based on the first measured samplerate.

*Timing is still a bit off. Perhaps we look into device driven data rate again.*

## analysis.py

This program implements the YASA sleep staging algorithm and determines when to wake the user based on a specified N2 epoch count threshold. It takes a file path as a command line argument and concatenates it to an ongoing array of the current sleep session's EEG time series data, with a corresponding sample rate. Once the array of data has surpassed the minimum analysis duration of 5 minutes, as well as the minimum sleep duration specified, it creates a SleepStaging instance to determine the predicted sleep stages for each epoch of recorded data. It repeats this each time it recieves a new filepath, which is every 30 seconds. Once the previous conditions are met, and an N2 threshold is surpassed or the maximum sleep duration has passed, the program activates the alarm system.

User preferences are defined at the top of this file:

minNapMinutes: integer, the minimum number of minutes that the nap should last. The program will not start counting N2 stages detected before this time. This is especially helpful at the start of the program, when predicted sleep stages can be less reliable, so we don't accidentally wake the user too soon.

maxNapMinutes: integer, the maximum number of minutes that the nap should last. As a default, in case the N2 threshold count is not met, the program will wake the user after this number of minutes has elapsed.

minN2epochs: integer, the N2 threshold count. The program will wake the user after this many epochs (30 second segments) have been predicted as stage N2 sleep.

## buzzer.py

This module contains code to play notificaitons on the buzzer. Commands are piped in line by line and the program reacts. Internally the program uses signals to time tones.

- 'READY' plays when the device is connected and ready to start recording.
- 'WAKEUP' command plays the alarm tone to awake the user.
- 'STOP' stops any playing sounds.
- 'TEST' plays a test signal to test the range of values.

The program watches carefully for signals to stop playing a sound if anything goes wrong or the program is stopped.

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

## test_buzzer.py

This module contains initial code to verify that the buzzer is working.

## test_interrupt.py

This module contains initial code to verify interrupt processing is working.

## Unused/Retired Files

We archive unused files in the `_unused` folder.

-  `btnWake.py` Poll for a change on an analog read pin as a makeshift interrupt. Used for initial i2c bringup. Owner: Michael
- `collectData_0.1.py` Initial pass at i2c code without interurpt. Timing was a problem even here. Owner: Michael
- `collectData_0.2.py` Version 2 of i2c code. This eventually formed into `record.py`. Owner: Julia
- `every.py` Attempt at abstracting away precise timing with python. Retired for interrupt based timing from ADC source. Could be useful for future work. Owner: Julia
- `pollData.py` Initial implementation of i2c code. Owner: Michael
- `pollStart.py` Initial implementation of i2c code. Owner: Michael

