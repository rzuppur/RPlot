#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2016 Reino Zuppur
reino.zuppur@gmail.com

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
"""


import rplot
import gui
import sys

def main():
    # INIT CONFIG
    w = 800
    h = 600

    app = gui.create_app(sys.argv)

    try:
        try:
            # CHECK COMMAND LINE ARGUMENTS
            window = gui.Window(rplot.RPlot(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
        except:
            window = gui.Window(rplot.RPlot(sys.argv[1]), w, h)
    except:
        # LAUNCH WITH DEFAULT CONFIG
        window = gui.Window(rplot.RPlot("sin(z)"), w, h)

    print("Plotting: " + str(window.rplot))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()