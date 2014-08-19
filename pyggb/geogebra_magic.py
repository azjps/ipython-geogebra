"""
An IPython extension for embedding GeoGebra applets within
an IPython notebook. Refer to examples directory for usage examples.
"""

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
        filename = _consume_arg(args, "ggb_file")
        java_applet = applet.JavaApplet(js_id, filename, args)
        self.cache_applets[js_id] = java_applet
        return HTML(data=str(java_applet))
        
        # Ignore everything below this line
        
        # TODO: offer option to convert to b64 format at any point during
        # construction.
        ggb_applet="""
<applet code="geogebra.GeoGebraApplet" id="ggb_applet{id}"
codebase="http://www.geogebra.org/webstart/4.2/unsigned/"
archive="http://www.geogebra.org/webstart/4.2/geogebra.jar"
width="{width}" height="{height}">
<param name="filename" value="{ggb_file}"/>
<param name="image" value="http://www.geogebra.org/webstart/loading.gif" />
<param name="java_arguments" value="-Xmx512m -Djnlp.packEnabled=true" />
<param name="framePossible" value="false" />

<param name="boxborder" value="false" />
<param name="centerimage" value="true" />

<param name="showResetIcon" value="true" />
<param name="showAnimationButton" value="true" />
<param name="enableRightClick" value="true" />
<param name="errorDialogsActive" value="true" />
<param name="enableLabelDrags" value="true" />
<param name="showMenuBar" value="false" />
<param name="showToolBar" value="false" />
<param name="showToolBarHelp" value="true" />
<param name="showAlgebraInput" value="true" />
<param name="allowRescaling" value="true" />
Sorry, the GeoGebra Applet could not be started. Please make sure that
Java 1.4.2 (or later) is installed and activated. (<a
href="http://java.sun.com/getjava">click here to install Java now</a>)
</applet>
""".format(id=self.ggb_id, width=args.width, height=args.height, ggb_file=args.ggb_file)
        self.ggb_id += 1
        # Other parameters?
        """
<param name="cache_archive" value="geogebra.jar, geogebra_main.jar, geogebra_gui.jar, geogebra_cas.jar, geogebra_export.jar, geogebra_properties.jar" />
<param name="cache_version" value="3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0" />
"""
        # TODO: read commands from cell and apply
        # TODO: cache output data
        print(ggb_applet)
        return HTML(ggb_applet)        

def load_ipython_extension(ipython):
    # TODO: use unsigned applet loading:
    # http://www.geogebra.org/en/wiki/index.php/Unsigned_GeoGebra_Applets
    ipython.register_magics(GeogebraMagic)