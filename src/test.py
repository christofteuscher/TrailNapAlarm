from defEpochPlot import spindlePlot, swPlot
import glob
import os
import time

# This program calls custom functions defined
# to use for visualizing yasa detection functions
# no output will be plotted if event isn't detected

# import and sort file paths into array
files = sorted(glob.glob('../res/data/generatedData/*.wav'), key=os.path.getmtime)

# choose which segment to plot
file = files[11]

begin = time.time()
spindlePlot(file)
end = time.time()

print(f"analyzeEpoch runtime is {end - begin}")

begin = time.time()
swPlot(file)
end = time.time()

print(f"swdetect runtime is {end - begin}")