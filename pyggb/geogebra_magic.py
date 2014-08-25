"""
An IPython extension for embedding GeoGebra applets within
an IPython notebook. Refer to examples directory for usage examples.
"""

import functools

from IPython.core.magic import (
    magics_class, line_cell_magic, Magics)
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring)
from IPython.display import display, HTML, Javascript

# TODO: setup.py, python modules
import applet

def _consume_arg(args_dict, key):
    """Helper"""
    try:
        val = args_dict[key]
        del args_dict[key]
        return val
    except KeyError:
        return None
                
@magics_class
class GeogebraMagic(Magics):
    """
    Define a few line/cell IPython magics %ggb, %ggb_tube
    which takes geogebra files and outputs embedded
    applet or HTML5 application.
    
    TODO: write ggb_tube HTML5 applet magic
    see http://wiki.geogebra.org/en/Reference:Applet_Embedding
    deployggb.js: http://wiki.geogebra.org/en/Reference:Applet_Parameters
    For some reason deployggb.js doesn't seem to work well with IPython
    notebook, at least in Windows 8.1 and Chrome.
    """
    
    def __init__(self, shell, cache_display_data=True):
        super(GeogebraMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data
        self.cache_applets = {}
        self.ggb_webstart_version = "4.2"
        self.ggb_id = 1  # counter for applet id

    @magic_arguments()
    @argument(
        'ggb_file', action="store",
        help="Name of existing .ggb file"
        )
    @argument(
        '--id', action="store",
        help="HTML id for applet, for document.getElementById")
    @applet.JavaApplet.param_arguments
    @line_cell_magic
    def ggb(self, line, cell=None):
        """Display a GeoGebra java applet from a .ggb file.
        
        To embed an existing GeoGebra file, use the IPython magic:
        
            %ggb filename.ggb
            
        TODO: lots of parameters to add
        TODO: cell read as geogebra commands
        """
        args = parse_argstring(self.ggb, line).__dict__
        js_id = _consume_arg(args, "id")
        if js_id is None:
            if self.cache_applets:
                js_id = max(self.cache_applets.keys()) + 1
            else:
                js_id = 1
        java_applet = applet.JavaApplet(js_id,
                                        _consume_arg(args, "ggb_file"),
                                        _consume_arg(args, "width"),
                                        _consume_arg(args, "height"),
                                        args)
        self.cache_applets[js_id] = java_applet
        return HTML(data=str(java_applet))
    
    # @classmethod
    def _html5iframe_args(ggb_ipython_magic):
        """Arguments common for GeoGebra applets (including
        Java applets, HTML5 applets, etc).
        """
    
        @functools.wraps(ggb_ipython_magic)
        @argument(
            '--width', type=int, default=1000,
            help="Width of applet, in pixels")
        @argument(
            '--height', type=int, default=600,
            help="Height of applet, in pixels")
        def wrapped_magic(self, line, cell=None):
            return ggb_ipython_magic(self, line, cell)
        for long_arg, short_arg, help in applet.HTML5IFrame.bool_params:
            wrapped_magic = argument('--' + long_arg, '--' + short_arg,
                                     metavar='0/1', type=int, help=help)(wrapped_magic)
        
        return wrapped_magic
    
    @magic_arguments()
    @argument(
        'ggbtube_id', action="store",
        help="Id of geogebra tube"
        )
    @argument(
        '--id', action="store",
        help="HTML id for applet, for document.getElementById")
    @_html5iframe_args
    @line_cell_magic
    def ggbtube(self, line, cell=None):
        args = parse_argstring(self.ggbtube, line).__dict__
        js_id = _consume_arg(args, "id")
        if js_id is None:
            if self.cache_applets:
                js_id = max(self.cache_applets.keys()) + 1
            else:
                js_id = 1
        html5_applet = applet.HTML5IFrame(js_id,
                                          _consume_arg(args, "ggbtube_id"),
                                          _consume_arg(args, "width"),
                                          _consume_arg(args, "height"),
                                          args)
        self.cache_applets[js_id] = html5_applet
        return HTML(data=str(html5_applet))
        
def load_ipython_extension(ipython):
    # TODO: use unsigned applet loading:
    # http://www.geogebra.org/en/wiki/index.php/Unsigned_GeoGebra_Applets
    ipython.register_magics(GeogebraMagic)