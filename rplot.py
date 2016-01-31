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


import numpy as np
from scipy import misc
import warnings

# MATH FUNCTIONS ============================================

from numpy import sin, cos, tan, arcsin, arccos, arctan, log, e, pi
from scipy.special import gamma, digamma, lambertw, zetac
i = 1j


def isin(x):
    return i*sin(x)

def c(x, y):
    return x + i*y

# ===========================================================

class RPlot:

    # TODO: make aborting plot faster

    def __init__(self, funktsioon, h_size=800, v_size=600, scale=80, n_distance=1, offset_x=0, offset_y=0, use_log=True):
        """ Komplekstasandil funktsioonide kujutamine kahemõõtmeliselt.

        @param funktsioon: str   Kujutatav funktsioon, nt. "sin(z)"
        @param h_size:     int   Graafiku laius
        @param v_size:     int   Graafiku kõrgus
        @param scale:      float Graafiku suurendus
        @param n_distance: float Graafiku kõrgusjoonte vahe
        @param offset_x:   float Graafiku horisontaalne offset
        @param offset_y:   float Graafiku vertikaalne offset
        @param use_log     bool  Kasuta kujutamisel logaritmi
        @return:           None  None
        """
        self._f_stiring = funktsioon
        self.h_size = int(h_size)
        self.v_size = int(v_size)
        self.scale = scale
        self.n_distance = n_distance
        self.offset_x = offset_x/self.scale
        self.offset_y = offset_y/self.scale
        self.use_log = use_log
        self.use_normalization = True

        self._b_grid = None
        self._f_values = None
        self.img = None

        warnings.filterwarnings("ignore")

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """http://fwarmerdam.blogspot.com.ee/2010/01/hsvmergepy.html

        @param h: 0-1
        @param s: 0-1
        @param v: 0-255
        @return: rgb ([y],[x],[r,g,b]) as uint8 (0-255)
        """
        i = (h*6.0).astype(int)
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        r = i.choose(v,q,p,p,t,v,mode="clip")
        g = i.choose(t,v,v,q,p,p,mode="clip")
        b = i.choose(p,p,t,v,v,q,mode="clip")

        rgb = np.rollaxis(np.asarray([r,g,b]).astype(np.uint8), 0, 3)

        return rgb

    def __str__(self):
        return self._f_stiring

    @property
    def function(self):
        return eval('lambda z: (' + self._f_stiring + ') + 0*z')

    @function.setter
    def function(self, value):
        nvalue = ""
        for l in range(len(value)):
            if value[l] == "i" and value[l-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                nvalue += "*"
            nvalue += value[l]

        self._f_stiring = nvalue

    def _create_values(self):
        """ Create complex plane and compute function values
        """
        hx, hy = self.h_size/2, self.v_size/2

        _y, _x = np.mgrid[0:self.v_size,0:self.h_size]

        _x = (_x - hx)/self.scale
        _y = (hy - _y)/self.scale

        _x += self.offset_x
        _y += self.offset_y

        self._b_grid = [_x, _y]
        z = _x + _y*1j

        global x, y
        x = _x
        y = _y
        f = self.function(z)

        return f

    def _compute_magnitudes(self, values):
        """ Compute complex value magnitudes and normalize them between 0-1
        """
        v = np.abs(values)

        # USE LOG TO MAKE MORE READABLE
        if self.use_log:
            v = np.log(v)

        nv = (v % self.n_distance) / self.n_distance

        nv = np.abs( nv-.5 )*2

        return nv

    def create_graph(self):
        """ Computes graph of function function and stores as image to self.img
        """
        self._f_values = self._create_values()

        if self.use_normalization:
            magnitudes = self._compute_magnitudes(self._f_values)

            h = (np.angle(self._f_values) % (2 * pi)) / (2 * pi)
            s = 1 - (magnitudes[:,:]**10)*.75
            v = (.2 + (magnitudes[:,:]**.3)*.8)*256
        else:
            if self.use_log:
                magnitudes = 1- (np.clip(log(abs(self._f_values)), 0.01, 2)*.5)
            else:
                magnitudes = 1-np.clip(abs(self._f_values), 0, 1)

            h = (np.angle(self._f_values) % (2 * pi)) / (2 * pi)
            s = 1 - (magnitudes[:,:])*.7
            v = (.15 + (magnitudes[:,:])*.85)*256

        plot = self.hsv_to_rgb(h, s, v)
        self.img = misc.toimage(plot, cmin=0, cmax=255)

    def get_image(self):
        return self.img

    def get_values(self):
        return self._f_values, self._b_grid

    def set_offset_x(self, offset):
        self.offset_x += offset/self.scale

    def set_offset_y(self, offset):
        self.offset_y += offset/self.scale

    def move(self, x, y):
        self.set_offset_x(x)
        self.set_offset_y(y)

    def show_graph(self):
        """ Show computed image without GUI
        """
        self.img.show()


if __name__ == "__main__":
    print("Plotting sin(z)")

    rp = RPlot("sin(z)", h_size=800, v_size=600)
    rp.create_graph()

    print("Done!")
    rp.show_graph()
