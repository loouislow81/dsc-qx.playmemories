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
---

MIT License

Copyright (c) 2018 Loouis Low

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
