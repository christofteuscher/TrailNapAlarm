
# Setup PocketBeagle with YASA

Our core processing libraries are [YASA](https://github.com/raphaelvallat/yasa) and [MNE](https://mne.tools/stable/index.html). Setting them up on the device was core to the success of the design. Unfortunatly we have failed at that and were unable to do so. For those that have continued this is a small list of what was tried.

Many dependencies would cause crashes sometime durring the build of the python libraries.

## Trying to bringup YASA on PocketBeagle


conda install numpy scipy matplotlib mne lightgbm`


pip3 install --no-deps yasa
pip3 install --no-deps mne==1.0.3
pip3 install --no-deps pandas==1.4.2 # No version.
pip3 install --no-deps pandas==1.3.5 # Largest version found.
pip3 install pandas==1.3.5 # Has reasonable ammount of things
# builds a numpy which takes a very very long time...
pip3 install sklearn
> Successfully installed joblib-1.1.0 scikit-learn-1.0.2 sklearn-0.0 threadpoolctl-3.1.0

`debian@beaglebone:~/Capstone/setup/TrailNapAlarm$ source ./test`
> Length of files: 50
> Traceback (most recent call last):
>   File "src/analysis.py", line 1, in <module>
>     import yasa
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/__init__.py", line 2, in <module>
>     from .detection import *
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/detection.py", line 21, in <module>
>     from .numba import _detrend, _rms
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/numba.py", line 5, in <module>
>     from numba import jit
> ModuleNotFoundError: No module named 'numba'

`pip3 install numba`
> Install Failed with missing llvmlite.
> https://llvmlite.readthedocs.io/en/latest/admin-guide/install.html#using-pip

`sudo apt install python3-llvmlite`
> Need to get 36.2 MB of archives.
> After this operation, 211 MB of additional disk space will be used.
> Do you want to continue? [Y/n] Y

`pip3 install numba`
> RuntimeError: Could not find a `llvm-config` binary. There are a number of reasons this could occur, please see: https://llvmlite.readthedocs.io/en/latest/admin-guide/install.html#using-pip for help.

`sudo apt install python3-numb`
> Need to get 6,632 kB of archives.
> After this operation, 28.2 MB of additional disk space will be used.
> Do you want to continue? [Y/n] Y

`source ./test`
> Length of files: 50
> /usr/lib/python3/dist-packages/numba/errors.py:104: UserWarning: Insufficiently recent colorama version found. Numba requires colorama >= 0.3.9
>   warnings.warn(msg)
> Traceback (most recent call last):
>   File "src/analysis.py", line 1, in <module>
>     import yasa
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/__init__.py", line 3, in <module>
>     from .features import *
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/features.py", line 24, in <module>
>     import antropy as ant
> ModuleNotFoundError: No module named 'antropy'

`sudo apt install python3-sklearn-lib`
> Reading package lists... Done
> Building dependency tree
> Reading state information... Done
> The following additional packages will be installed:
>   libatlas3-base
> The following NEW packages will be installed:
>   libatlas3-base python3-sklearn-lib
> 0 upgraded, 2 newly installed, 0 to remove and 171 not upgraded.
> Need to get 3,665 kB of archives.
> After this operation, 12.9 MB of additional disk space will be used.
> Do you want to continue? [Y/n] Y

`pip install -U pip`
>  Updated.


`pip install antropy`
> Out of Space.



### Resize Main system Partition

Default SD card config does not use all of the space. We will upgrade it. [Guide](http://eprojects.ljcv.net/2018/06/pocketbeagle-how-to-increase-root.html).

```
sudo -s
```

> Command (m for help): p
> 
> Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors
> Units: sectors of 1 * 512 = 512 bytes
> Sector size (logical/physical): 512 bytes / 512 bytes
> I/O size (minimum/optimal): 512 bytes / 512 bytes
> Disklabel type: dos
> Disk identifier: 0x3244345d
> 
> Device         Boot Start     End Sectors  Size Id Type
> /dev/mmcblk0p1 *     8192 7372799 7364608  3.5G 83 Linux

> Command (m for help): p
> 
>Disk /dev/mmcblk0: 14.4 GiB, 15489564672 bytes, 30253056 sectors
>Units: sectors of 1 * 512 = 512 bytes
>Sector size (logical/physical): 512 bytes / 512 bytes
>I/O size (minimum/optimal): 512 bytes / 512 bytes
>Disklabel type: dos
>Disk identifier: 0x3244345d
>
>Device         Boot Start      End  Sectors  Size Id Type
>/dev/mmcblk0p1       8192 30253055 30244864 14.4G 83 Linux

`reboot`

root@beaglebone:/home/debian# `resize2fs /dev/mmcblk0p1`
> resize2fs 1.44.5 (15-Dec-2018)
> Filesystem at /dev/mmcblk0p1 is mounted on /; on-line resizing required
> old_desc_blocks = 1, new_desc_blocks = 2
> The filesystem on /dev/mmcblk0p1 is now 3780608 (4k) blocks long.

root@beaglebone:/home/debian# `df -h`
> Filesystem      Size  Used Avail Use% Mounted on
> udev            215M     0  215M   0% /dev
> tmpfs            49M  1.5M   47M   4% /run
> /dev/mmcblk0p1   15G  3.2G   11G  24% /
> tmpfs           242M     0  242M   0% /dev/shm
> tmpfs           5.0M     0  5.0M   0% /run/lock
> tmpfs           242M     0  242M   0% /sys/fs/cgroup
> tmpfs            49M     0   49M   0% /run/user/1000


### Continue Installation

`pip3 install antropy`

`pip3 install yasa`
> Installed and good.

`souce ./test`
> source ./test
> Length of files: 50
> /usr/lib/python3/dist-packages/numba/errors.py:104: UserWarning: Insufficiently recent colorama version found. Numba requires colorama >= 0.3.9
>   warnings.warn(msg)

`pip3 show colorama`
> Name: colorama
> Version: 0.3.7
> Summary: Cross-platform colored terminal text.
> Home-page: https://github.com/tartley/colorama
> Author: Arnon Yaari
> Author-email: tartley@tartley.com
> License: BSD
> Location: /usr/lib/python3/dist-packages
> Requires:
> Required-by:

`pip3 install -U colorama>=0.3.9`
> Installed but did not report anything for some reason.

`pip3 show colorama`
> Name: colorama
> Version: 0.4.4
> Summary: Cross-platform colored terminal text.
> Home-page: https://github.com/tartley/colorama
> Author: Jonathan Hartley
> Author-email: tartley@tartley.com
> License: BSD
> Location: /home/debian/.local/lib/python3.7/site-packages
> Requires:
> Required-by:

`souce ./test`
> Length of files: 50
> Traceback (most recent call last):
>   File "/usr/lib/python3/dist-packages/numba/errors.py", line 617, in new_error_context
>     yield
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 259, in lower_block
>     self.lower_inst(inst)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 308, in lower_inst
>     val = self.lower_assign(ty, inst)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 454, in lower_assign
>     return self.lower_expr(ty, value)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 883, in lower_expr
>     res = self.lower_call(resty, expr)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 849, in lower_call
>     res = impl(self.builder, argvals, self.loc)
>   File "/usr/lib/python3/dist-packages/numba/targets/base.py", line 1124, in __call__
>     return self._imp(self._context, builder, self._sig, args, loc=loc)
>   File "/usr/lib/python3/dist-packages/numba/targets/base.py", line 1147, in wrapper
>     return fn(*args, **kwargs)
>   File "/usr/lib/python3/dist-packages/numba/unsafe/ndarray.py", line 32, in codegen
>     res = _empty_nd_impl(context, builder, arrty, shapes)
>   File "/usr/lib/python3/dist-packages/numba/targets/arrayobj.py", line 3167, in _empty_nd_impl
>     arrlen = builder.mul(arrlen, s)
>   File "/usr/lib/python3/dist-packages/llvmlite/ir/builder.py", line 24, in wrapped
>     % (lhs.type, rhs.type))
> ValueError: Operands must be the same type, got (i32, i64)
> 
> During handling of the above exception, another exception occurred:
> 
> Traceback (most recent call last):
>   File "src/analysis.py", line 1, in <module>
>     import yasa
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/__init__.py", line 3, in <module>
>     from .features import *
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/features.py", line 24, in <module>
>     import antropy as ant
>   File "/home/debian/.local/lib/python3.7/site-packages/antropy/__init__.py", line 4, in <module>
>     from .fractal import *
>   File "/home/debian/.local/lib/python3.7/site-packages/antropy/fractal.py", line 303, in <module>
>     @jit('f8(f8[:])', nopython=True)
>   File "/usr/lib/python3/dist-packages/numba/decorators.py", line 183, in wrapper
>     disp.compile(sig)
>   File "/usr/lib/python3/dist-packages/numba/compiler_lock.py", line 32, in _acquire_compile_lock
>     return func(*args, **kwargs)
>   File "/usr/lib/python3/dist-packages/numba/dispatcher.py", line 655, in compile
>     cres = self._compiler.compile(args, return_type)
>   File "/usr/lib/python3/dist-packages/numba/dispatcher.py", line 82, in compile
>     pipeline_class=self.pipeline_class)
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 926, in compile_extra
>     return pipeline.compile_extra(func)
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 374, in compile_extra
>     return self._compile_bytecode()
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 857, in _compile_bytecode
>     return self._compile_core()
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 844, in _compile_core
>     res = pm.run(self.status)
>   File "/usr/lib/python3/dist-packages/numba/compiler_lock.py", line 32, in _acquire_compile_lock
>     return func(*args, **kwargs)
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 255, in run
>     raise patched_exception
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 246, in run
>     stage()
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 717, in stage_nopython_backend
>     self._backend(lowerfn, objectmode=False)
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 666, in _backend
>     lowered = lowerfn()
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 653, in backend_nopython_mode
>     self.metadata)
>   File "/usr/lib/python3/dist-packages/numba/compiler.py", line 1048, in native_lowering_stage
>     lower.lower()
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 178, in lower
>     self.lower_normal_function(self.fndesc)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 219, in lower_normal_function
>     entry_block_tail = self.lower_function_body()
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 244, in lower_function_body
>     self.lower_block(block)
>   File "/usr/lib/python3/dist-packages/numba/lowering.py", line 259, in lower_block
>     self.lower_inst(inst)
>   File "/usr/lib/python3.7/contextlib.py", line 130, in __exit__
>     self.gen.throw(type, value, traceback)
>   File "/usr/lib/python3/dist-packages/numba/errors.py", line 625, in new_error_context
>     six.reraise(type(newerr), newerr, tb)
>   File "/usr/lib/python3/dist-packages/numba/six.py", line 659, in reraise
>     raise value
> numba.errors.LoweringError: Failed in nopython mode pipeline (step: nopython mode backend)
> Operands must be the same type, got (i32, i64)
> 
> File "../.local/lib/python3.7/site-packages/antropy/fractal.py", line 313:
> def _dfa(x):
>     <source elided>
> 
>     for i_n, n in enumerate(nvals):
>     ^
> 
> [1] During: lowering "array.79 = call empty_func.80(size_tuple.78, func=empty_func.80, args=(Var(size_tuple.78, /home/debian/.local/lib/python3.7/site-packages/antropy/fractal.py (313)),), kws=[], vararg=None)" at /home/debian/.local/lib/python3.7/site-packages/antropy/fractal.py (313)


Something with dependencies could be wrong. Trying to update yasa again.

`pip3 install -U yasa`
> All checked. Still no luck.

Trying to use pip3 llvm.

`pip3 install -U llvmlite`
> Crash.

Following the llvmlite manual install [guide]().

`sudo apt install libedit-dev`
`sudo apt install llvm-dev`
> Installed!

`pip3 install -U llvmlite`
> RuntimeError: Building llvmlite requires LLVM 11.x.x, got '7.0.1'. Be sure to set LLVM_CONFIG to the right executable path.
> Read the documentation at http://llvmlite.pydata.org/ for more information about building llvmlite.

### Build LLVM

Via [guide](https://github.com/llvm/llvm-project/releases/download/llvmorg-11.1.0/llvm-11.1.0.src.tar.xz).
```
mkdir TrailNapAlarm/setup
cd TrailNapAlarm/setup
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-11.1.0/llvm-11.1.0.src.tar.xz
git clone --depth=1 https://github.com/numba/llvmlite
tar xf llvm-11.1.0.src.tar.xz
ls
> llvm-11.1.0.src  llvm-11.1.0.src.tar.xz  llvmlite
cd llvm-11.1.0.src/
# Some Patches skipped... irrellivant or did not work.
patch -p1 -i ../llvmlite/conda-recipes/0001-Revert-Limit-size-of-non-GlobalValue-name.patch
> patching file lib/IR/Value.cpp
> Hunk #1 succeeded at 38 (offset 1 line).
> Hunk #2 succeeded at 290 (offset 56 lines).
> patching file test/Bitcode/value-with-long-name.ll
export PREFIX=../llvm/ CPU_COUNT=1
sudo apt install cmake
rmdir build
bash ../llvmlite/conda-recipes/llvmdev/build.sh
> Really long build...



> Crashed...
```


# To Try....

`LLVM_CONFG=/usr/bin/llvm-config`






### Install Miniconda

armv7l

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-armv7l.sh
bash Miniconda3-latest-Linux-armv7l.sh

Setup environment for yaml file.

> Unable to install some packages.
> matplotlib not available.
*Removed from list as we will not plot anything here."


> openblas and blas not available.
*Looking for way to install. Should be available on system via apt.

`sudo apt seach blas`
> libblas-dev/oldstable 3.8.0-2 armhf
>   Basic Linear Algebra Subroutines 3, static library
> 
> libblas-test/oldstable 3.8.0-2 armhf
>   Basic Linear Algebra Subroutines 3, testing programs
> 
> libblas3/oldstable,now 3.8.0-2 armhf [installed]
>   Basic Linear Algebra Reference implementations, shared library
> 
> libblis-dev/oldstable 0.5.1-11 armhf
>   BLAS-like Library Instantiation Software Framework

`sudo apt search openblas`
> libopenblas-base/oldstable 0.3.5+ds-3 armhf
>   Optimized BLAS (linear algebra) library (shared library)
> 
> libopenblas-dev/oldstable 0.3.5+ds-3 armhf
>   Optimized BLAS (linear algebra) library (development files)

`sudo apt install libblas3 libblas-dev libopenblas-base libopenblas-dev`
Need to get 4,225 kB of archives.
After this operation, 22.3 MB of additional disk space will be used.

`cat environment.jml`
> name: TrailAlarm
> channels:
>   - conda-forge
> dependencies:
>   - python
>   - pip
>   - numpy
>   - scipy
>   - mne
>   - pip:
>     - yasa

`~/miniconda3/bin/conda install -f environment.yml`
> Error: No packages found in current linux-armv7l channels matching: environment.yml

`~/miniconda3/bin/conda env create -f environment.yml`
> Error: Could not find some dependencies for numpy: blas * openblas

Without conda forge.
> Error: No packages found in current linux-armv7l channels matching: mne


**CONTINUE HERE**

### Install One at at time...
`~/miniconda3/bin/conda create -n Capstone python=3 pip`
>  Ok.

`source ~/miniconda3/bin/activate Capstone`
> Ok

`conda install numpy`
> Error: Could not find some dependencies for numpy: blas * openblas


`conda install -c conda-forge numpy`
> Error: Could not find some dependencies for numpy: blas * openblas

`conda install -c conda-forge numpy --no-deps`
> Error: No packages found in current linux-armv7l channels matching: libblas
> 
> You can search for this package on anaconda.org with
> 
>     anaconda search -t conda libblas
> 
> You may need to install the anaconda-client command line client with
> 
>     conda install anaconda-client

`conda install anaconda-client`
> Ok.
`anaconda search -t conda blas * openblas`
> * import too much...
`anaconda search -t conda openblas`
`anaconda search -t conda openblas | grep linux-armv7l`
> Using binstar api site https://api.anaconda.org
>     microsoft-ell/openblas    |    0.3.6 | conda           | linux-armv7l
>     poppy-project/openblas    |   0.2.15 | conda           | linux-armv7l
>     rpi/openblas              |   0.2.19 | conda           | linux-armv6l, linux-armv7l
>     tballance/openblas        |   0.2.19 | conda           | linux-armv7l

`anaconda search -t conda blas | grep linux-armv7l`
>     rpi/blas                  |      1.1 | conda           | linux-armv7l
>     rpi/openblas              |   0.2.19 | conda           | linux-armv6l, linux-armv7l

Can search for Aarmv7l packages [online](https://anaconda.org/search?q=platform%3Alinux-armv7l) as well. Install them as channel/package specification to conda.
`conda install -c rpi blas`
>   blas:        1.1-openblas
>   libgfortran: 3.0.0-0
>   openblas:    0.2.19-0


`conda install -c  microsoft-ell openblas`
> Good

`conda install -c rpi numpy scipy`
> Hint: the following packages conflict with each other:
>   - scipy
>   - python 3.4*
> 
> Use 'conda info scipy' etc. to see the dependencies for each package.
> 
> Note that the following features are enabled:
>   - blas_openblas

`conda install -c rpi numpy`
> Conflict with python.

`conda install -c rpi python`
> Complete.

`conda install -c rpi numpy`
> Hint: the following packages conflict with each other:
>   - numpy
>   - python 3.4*
> 
> Use 'conda info numpy' etc. to see the dependencies for each package.
> 
> Note that the following features are enabled:
>   - blas_openblas

`conda uninstall python`
`conda install -c rpi python=2 numpy`
`conda install -c rpi pip`
> Environment seems broken... 
`conda remove python pip`
`conda install python=3 pip`
> Yay!
`pip install --updatedupgrade pip`

`pip install mne`
> Start build. Nope

`conda install -c rpi python=3`
> Upgrading some. python 3.6 now.
`conda install -c rpi typing`
> Nope. Conflict. Probably not needed...

`pip install mne`
> Start build. Crashed and hung board.

`source ~/miniconda3/bin/activate TrailAlarm`
`pip install mne --no-deps`
> Installed. May need dependencies later.
`pip install yasa`
> 



**Manual Install of mne and yasa**


`cat environment.yml`
> name: TrailAlarm
> channels:
>   - rpi
> dependencies:
>   - python
>   - pip
>   - numpy
>   - scipy
>   - pip:
>     - mne
>     - yasa
`debian@beaglebone:~/TrailNapAlarm/setup$ ~/miniconda3/bin/conda env create -f environment.yml`
> Lots of wheels downloading.
> Building for a long time. Currently scipy...
> Collecting scipy>=1.1.0 (from mne)
> Collecting matplotlib (from yasa)

Try again. Closed with an accidental Ctrl-c....

Now need to log in and install with pip...

`pip install mne`
> Crashed system again...

**HERE**

`pop install yasa`

*Missing fortran. *
`sudo apt install gfortran`
`pip install mne`
> Crashed system again...

`pip install --no-deps mne`
`pip install yasa'
-- Crashed system on scipy install again.
`pip install --no-deps yasa`

Manually adding dependencies.

`pip install pandas`
> Crashed.

`pip install pandas --no-deps`





**ANOTHER TRY**

`cat environment.yml`
> name: TrailAlarm
> channels:
>   - rpi
> dependencies:
>   - python
>   - pip
>   - numpy
>   - scipy
>   - mne
>   - pip:
>     - yasa

`debian@beaglebone:~/TrailNapAlarm/setup$ ~/miniconda3/bin/conda env create -f environment.yml`
> Error: No packages found in current linux-armv7l channels matching: mne






## Backup SD card

[Guide](http://www.ofitselfso.com/BeagleNotes/CloningABootableBeagleboneBlackSDCard.php) to follow.












# Possibly Useful Possibly Not... Lost track.
## Bringup on BBP

> Traceback (most recent call last):
>   File "src/analysis.py", line 1, in <module>
>     import yasa
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/__init__.py", line 2, in <module>
>     from .detection import *
>   File "/home/debian/.local/lib/python3.7/site-packages/yasa/detection.py", line 18, in <module>
>     from sklearn.ensemble import IsolationForest
> ModuleNotFoundError: No module named 'sklearn'

pip3 install sklearn




< AAgain....

Installing collected packages: webencodings, wcwidth, Send2Trash, ptyprocess, pickleshare, mistune, littleutils, ipython-genutils, fastjsonschema, backcall, appdirs, zipp, urllib3, traitlets, tornado, tinycss2, soupsieve, pyzmq, pyrsistent, pygments, pycparser, psutil, prompt-toolkit, prometheus-client, pexpect, parso, pandocfilters, nest-asyncio, MarkupSafe, jupyterlab-widgets, jupyterlab-pygments, entrypoints, defusedxml, debugpy, charset-normalizer, certifi, bleach, attrs, terminado, tensorpac, requests, matplotlib-inline, matplotlib, lspopt, jupyter-core, jinja2, jedi, importlib-resources, importlib-metadata, cffi, beautifulsoup4, seaborn, pyriemann, pooch, outdated, jupyter-client, jsonschema, ipython, argon2-cffi-bindings, nbformat, ipykernel, argon2-cffi, nbclient, nbconvert, notebook, widgetsnbextension, ipywidgets
Successfully installed MarkupSafe-2.1.1 Send2Trash-1.8.0 appdirs-1.4.4 argon2-cffi-21.3.0 argon2-cffi-bindings-21.2.0 attrs-21.4.0 backcall-0.2.0 beautifulsoup4-4.11.1 bleach-5.0.0 certifi-2022.5.18.1 cffi-1.15.0 charset-normalizer-2.0.12 debugpy-1.6.0 defusedxml-0.7.1 entrypoints-0.4 fastjsonschema-2.15.3 importlib-metadata-4.11.4 importlib-resources-5.7.1 ipykernel-6.13.0 ipython-7.34.0 ipython-genutils-0.2.0 ipywidgets-7.7.0 jedi-0.18.1 jinja2-3.1.2 jsonschema-4.6.0 jupyter-client-7.3.1 jupyter-core-4.10.0 jupyterlab-pygments-0.2.2 jupyterlab-widgets-1.1.0 littleutils-0.2.2 lspopt-1.1.1 matplotlib-3.5.2 matplotlib-inline-0.1.3 mistune-0.8.4 nbclient-0.6.4 nbconvert-6.5.0 nbformat-5.4.0 nest-asyncio-1.5.5 notebook-6.4.11 outdated-0.2.1 pandocfilters-1.5.0 parso-0.8.3 pexpect-4.8.0 pickleshare-0.7.5 pooch-1.6.0 prometheus-client-0.14.1 prompt-toolkit-3.0.29 psutil-5.9.1 ptyprocess-0.7.0 pycparser-2.21 pygments-2.12.0 pyriemann-0.2.7 pyrsistent-0.18.1 pyzmq-23.1.0 requests-2.27.1 seaborn-0.11.2 soupsieve-2.3.2.post1 tensorpac-0.6.5 terminado-0.15.0 tinycss2-1.1.1 tornado-6.1 traitlets-5.2.2.post1 urllib3-1.26.9 wcwidth-0.2.5 webencodings-0.5.1 widgetsnbextension-3.6.0 zipp-3.8.0

## Other Resources (UNUSED)

### Super quick boot on BB angstrom

[Slides](https://elinux.org/images/b/b3/Elce11_koen.pdf) on how to quick boot BeagleBoard angstrom. Different device. Maybe applicable.

[Thread](https://www.reddit.com/r/embedded/comments/j7cwnn/beaglebone_boottime_reduction/) on a quick boot.

### Custom boot image

[Guide](http://www.blackpeppertech.com/pepper/tech-tree/boot-your-beaglebone-black-in-60-minutes/) to build custom Linux image for BB?.

### Down-clock Pocket Beagle for less power draw

Frequency scaling available through linux file api.

```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed
```

### Disconnect USB power.

[Guide](https://forum.beagleboard.org/t/turn-usb-power-on-off/30700/4) that reports how to disconnect by write to internal GPIO. May have some issues.