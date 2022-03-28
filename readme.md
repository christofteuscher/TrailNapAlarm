# Trail Nap Alarm
## Overview
### Introduction and problem statement:
Ultra marathon runners, i.e., runners who run distances longer than a marathon, often do “trail naps,” i.e., they simply lay down on the trail and power nap for 5-10min. When it’s cold, one wakes up after a short period of time, but when it’s warm(er), it’s likely that the runner will sleep longerthan they want. Setting an alarm is tedious, time-consuming, and the alarm may not be heard. Also,sometimes it takes a few minutes to fall asleep, so estimating the wake-up time is hard and the resulting sleep time is rarely ideal.
The goal of this project is to build a device that monitors a runner’s sleep and wakes them up aftersleep stage N1, before they fall into a REM sleep pattern. Non-REM sleep has 3 stages ([Source:](https://www.uofmhealth.org/health-library/hw48331)):
* **Stage** N1 occurs right after you fall asleep and is very short (usually less than 10 minutes).It involves light sleep from which you can be awakened easily.
* **Stage N2** lasts from about 30 to 60 minutes. During this stage, your muscles become more
relaxed and you may begin to have slow-wave (delta) brain activity.
* **Stage N3** is deep sleep and lasts about 20 to 40 minutes. During this stage, delta brain activity increases and a person may have some body movements. It is very hard to wake up someone in stage N3.

### Specific project goals
1. Build a sensor system that allows to detect the different sleep patterns. The sensor system needs to be small, simple, non-invasive, and ultra-low power. E.g., an armband, electrodes embedded in a hat, etc.
2. Build a system that reliably wakes up a person. E.g., a combination of sound, vibration, etc. That part must also be small, simple, non-invasive, and ultra-low power.
3. An integration of these two sub-components into a fully functional system. Cables should be avoided. If communication between sub-systems is necessary, that should rely on Bluetooth or other protocols.
4. The system must be battery-powered. The batteries should last for at least 3 days (72 hours). The batteries should be rechargeable with a USB cable.
5. The overall system must be small, non-invasive, light, water-proof, easy to use, and have no on-off or other switches.
### Deliverables
* A fully functional prototype.
* Code (on Github), nicely documented
* A final report
* A final presentation

## Directory structure
* [src]()
    * Source code files belong here
* [tools]()
    * Tools like Makefile and other scripts belong here
* [docs]()
    * Documentation files belong here
* [dep]()
    * Dependencies belong here
* [res]()
    * Resource files belong here

## Citations and Licensing 

This project makes use of the Yasa sleep detection algorithm, as well as the MNE library.

* Vallat, Raphael, and Matthew P. Walker. "An open-source, high-performance tool for automated sleep staging." Elife 10 (2021). doi: https://doi.org/10.7554/eLife.70092

MNE-Python is **BSD-licenced** (3 clause):

This software is OSI Certified Open Source Software.
OSI Certified is a certification mark of the Open Source Initiative.

Copyright (c) 2011-2022, authors of MNE-Python.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

* Neither the names of MNE-Python authors nor the names of any
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

**This software is provided by the copyright holders and contributors
"as is" and any express or implied warranties, including, but not
limited to, the implied warranties of merchantability and fitness for
a particular purpose are disclaimed. In no event shall the copyright
owner or contributors be liable for any direct, indirect, incidental,
special, exemplary, or consequential damages (including, but not
limited to, procurement of substitute goods or services; loss of use,
data, or profits; or business interruption) however caused and on any
theory of liability, whether in contract, strict liability, or tort
(including negligence or otherwise) arising in any way out of the use
of this software, even if advised of the possibility of such
damage.**