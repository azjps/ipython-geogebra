ipython-geogebra
================

Jupyter/IPython magic extension for embedding GeoGebra applets in Jupyter (IPython) notebooks.

GeoGebra is a [open source 2D and 3D geometry software](http://www.geogebra.org/cms/en/).
This extension is mostly a wrapper around the
[html embedding features](http://wiki.geogebra.org/en/Embedding_in_Webpages) available
from GeoGebra. While GeoGebra primarily uses a Java backend, it can be embedded as both
a Java applet and a HTML5 applet on a webpage, such as an Jupyter notebook.

Unfortunately, a short-lived python-to-geogebra interface no longer seems to exist.
We can mimic some features of the interface via JavaScript.

See some examples here:
* [Java applets introduction](http://nbviewer.ipython.org/github/azjps/ipython-geogebra/blob/master/examples/geogebra_introduction.ipynb)
* [HTML5 applets](http://nbviewer.ipython.org/github/azjps/ipython-geogebra/blob/master/examples/geogebratube_iframe.ipynb)

To use, clone this repository:

`git clone https://github.com/azjps/ipython-geogebra.git`

(To-do: installation via pip, etc)

Please note that this was a personal project and is not maintained by any
developers of GeoGebra. It has not been updated in a while and may have fallen
out of line with any newer changes to GeoGebra's webapp API. Please feel free to
submit PRs or fork as needed. :)

