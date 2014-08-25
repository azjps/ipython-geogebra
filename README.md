ipython-geogebra
================

IPython magic extension for embedding GeoGebra applets in IPython notebooks.

GeoGebra is a [open source 2D and 3D geometry software](http://www.geogebra.org/cms/en/).
This extension is mostly a wrapper around the
[html embedding features](http://wiki.geogebra.org/en/Embedding_in_Webpages) available
from GeoGebra. While GeoGebra primarily uses a Java backend, it can be embedded as both
a Java applet and a HTML5 applet on a webpage, such as an IPython notebook.

Unfortunately, a short-lived python-to-geogebra interface no longer seems to exist.
We can mimic some features of the interface via JavaScript.

See some examples here:
* [Java applets introduction](http://nbviewer.ipython.org/github/azjps/ipython-geogebra/blob/master/examples/geogebra_introduction.ipynb)
* [HTML5 applets](http://nbviewer.ipython.org/github/azjps/ipython-geogebra/blob/master/examples/geogebratube_iframe.ipynb)