# dsc-qx.playmemories

This is a quick and dirty python application that allows my 2 Sony Lens-Style DSC-QX 10 & 100 cameras to use on my laptop.

I learned from this this website (https://developer.sony.com/develop/cameras/)

## Prerequsites

Install and create new virtualenv,

```bash
$ sudo apt install -y virtualenv
$ virtualenv ~/.python-venv/dsc-qx-playmemories
```

## Usage

Connect to your computer wifi locally `ad-hoc` with `Sony DSC-QX Lens-Style` Camera first,

And then, run the application in Python Virtual Environment,

```bash
$ cd ~/.python-venv/dsc-qx-playmemories/bin
$ source activate
$ (dsc-qx-playmemories) python dsc-qx-playmemories.py
```

To exit the Python Virtual Environment,

```bash
$ (dsc-qx-playmemories) deactivate
```
