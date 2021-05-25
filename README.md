# Lekhaka -- The Indic Scribe

# Mission
We use `Cairo` and `CFFI` to print complex scripts to slabs of images, 
which are then loaded into `numpy` arrays. These will be used to train 
`Convolutional Recurrent Neural Networks`.

# Python Dependencies
1. numpy
1. scipy
1. PIL
1. cairo
1. cairocffi


# Setup

```
git clone https://github.com/rakeshvar/Lekhaka
cd Lekhaka
./scripts/install.sh
```

## Fonts
You will need a lot of fonts for a language you want to train on.
You can get numerous Telugu fonts from [here](https://github.com/TeluguOCR/Fonts).
Just copy all the fonts to your `~/.fonts` directory on linux.

## Checking
Given the complicated dependencies, you can first check if you have all the dependencies as

```sh
cd tests
python3 test_scribe_random.py
python3 test_scribe_all_fonts.py <(echo 'క్రైః') > kraih.txt
# The output should contain the text rendered in various fonts
```

# Files
1. `line_seperate.py` Clever code to split a text page image into individual lines.
1. `scribe.py` Scribes a given Unicode text to a image slab. (Wrapper class.)
1. `scribe_interface.py` Interface code to CFFI based code.
1. `parscribe.py` Parallel Scribe (text from the given language).
1. `trimmers.py` Trim a Black and White image to remove empty space around.
1. `utils.py` Utilities to print images and Probabilities to terminal, etc.

# Troubleshooting
Although in Ubuntu 20.04 Desktop, just installing above mentioned requirements was enough,
but on a server or on different versions of linux, or in case you do not have root access,
the following legacy trouble shooting tips may be useful.

## Dependencies

You should have `libffi`, `cffi` and `cairocffi` installed.
These are constantly changing and are works in progress.
More over you might need root privileges to install libraries (libffi).

If `cffi` is complaining that it needs `libffi` then try to install it as

### Ubuntu

```sh
sudo apt-get install libffi-dev
```

### RHEL, CentOS

```sh
yum install libffi
```

But then if you are **not** root on an RHEL machine (which is the case if you are on a server) then
try

```sh
mkdir ~/software/
cd ~/software/
wget ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz
tar -xvf libffi-3.2.1.tar.gz
cd libffi-3.2.1/
./configure --prefix=/home/<NAME>/usr
make -j4
make check
make install
```

Open `.bashrc` file and add these lines

```
export PATH=$PATH:~/usr/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/usr/lib:~/usr/lib64
export C_INCLUDE_PATH=$C_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:~/usr/include:~/usr/lib/libffi-3.2.1/include
```

Try installing those packages again

```sh
LDFLAGS=-L/home/<NAME>/usr/lib64 pip3 install cffi
pip3 install cairocffi
```

## Other Problems
* If your PIL / Pillow is not able to open tiff image files.
Follow this: http://stackoverflow.com/a/10109941
If you do not have root priveleges are installing `libtiff` etc. locally,
make sure your `LD_LIBRARY_PATH` points to something like `~/usr/lib` that has `libtiff` etc.
