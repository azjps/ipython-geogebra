"""
An IPython extension for generating and displaying asymptote figures within
an IPython notebook. Refer to examples directory for usage examples.
"""
import xml

from IPython.core.magic import (
    magics_class, line_cell_magic, Magics)
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring)
from IPython.display import HTML

@magics_class
class GeogebraMagic(Magics):
    """
    Define a few line/cell IPython magics %ggb, %ggb_tube
    which takes geogebra files and outputs embedded
    applet or HTML5 application.
    
    TODO: write ggb_tube
    """
    
    def __init__(self, shell, cache_display_data=False):
        super(GeogebraMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data
        
    @magic_arguments()
    @argument(
        'ggb_file', action="store",
        help="Name of existing .ggb file"
        )
    @argument(
        '-h', '--height', type=int, default=600,
        help="Height of applet")
    @argument(
        '-w', '--width', type=int, default=1000,
        help="Width of applet")
    @line_cell_magic
    def ggb(self, line, cell=None):
        """Display a geogebra applet.
        
        To embed an existing GeoGebra file, use the IPython magic:
        
            %ggb filename.ggb
            
        TODO: lots of parameters to add
        TODO: cell read as geogebra commands
        """
        args = parse_argstring(self.ggb, line)
        
        ggb_applet="""
<applet code="geogebra.GeoGebraApplet"
codebase="http://www.geogebra.org/webstart/4.2/unsigned/"
archive="http://www.geogebra.org/webstart/4.2/geogebra.jar"
width="{width}" height="{height}">
<param name="filename" value="{ggb_file}"/>
<param name="framePossible" value="false" />
<param name="image" value="http://www.geogebra.org/webstart/loading.gif" />
<param name="boxborder" value="false" />
<param name="centerimage" value="true" />
<param name="java_arguments" value="-Xmx512m -Djnlp.packEnabled=true" />
<param name="framePossible" value="false" />
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
""".format(width=args.width, height=args.height, ggb_file=args.ggb_file)
        # Other parameters?
        """
<param name="cache_archive" value="geogebra.jar, geogebra_main.jar, geogebra_gui.jar, geogebra_cas.jar, geogebra_export.jar, geogebra_properties.jar" />
<param name="cache_version" value="3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0, 3.2.47.0" />
"""
        return HTML(ggb_applet)        

def load_ipython_extension(ipython):
    ipython.register_magics(GeogebraMagic)