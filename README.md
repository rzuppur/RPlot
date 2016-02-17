RPlot
======
Visualizing functions in complex plane using Python and Numpy.
_A student project for first year programming course._

![rplot](http://i.imgur.com/nASl52F.png "RPlot")


Running RPlot
======

You need to have __Numpy__, __Scipy__ and __PySide__ installed to run RPlot. Also __Python 3.4__. After downloading and installing dependencies run _run.py_.

No binaries are provided at this point because all tried freezing utilities failed.


Using RPlot
======

The function you want to visualize can be entered to the text box at top. You can move arond by dragging with mouse and using scrollwheel to zoom. Two checkboxes change between different modes for visualizing.


####Keyboard shortcuts:
* __Page Up__ - Zoom in
* __Page Down__ - Zoom out
* __F1__ - Toggle Log
* __F2__ - Toggle Normalization

####Command line arguments:

* run.py __[function]__
* run.py __[function]__ __[window width]__ __[window height]__

Example: _run.py gamma(z) 800 300_

 

TODO
======
* Better text input
* Reset button

