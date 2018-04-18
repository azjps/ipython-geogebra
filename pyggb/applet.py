import functools
from xml.etree import ElementTree

from IPython.core.magic_arguments import argument

def _indent(elem, level=0, no_newline_tags=None):
    """Commonly cited method for in-place indentation of xml element.
    no_newline_elems: list of elem tags to not add newline
    """
    indentation = "\n" + (level * "  ")
    if len(elem):
        use_newline = True
        if not elem.text or not elem.text.strip():
            if no_newline_tags and elem.tag in no_newline_tags:
                use_newline = False
                elem.text = ""
            else:
                elem.text = indentation + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indentation
        for elem in elem:
            _indent(elem, level+1, no_newline_tags=no_newline_tags)
        if not elem.tail or not elem.tail.strip():
            if use_newline:
                elem.tail = indentation
            else:
                elem.tail = ""
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indentation

class JavaApplet(object):
    """"""
    bool_params = ["enableRightClick",
                   "enableLabelDrags",
                   "enableShiftDragZoom",
                   "errorDialogsActive",
                   "showMenuBar",
                   "showToolBar",
                   "showToolBarHelp",
                   "showAlgebraInput",
                   "showResetIcon",
                   "allowStyleBar",
                   "useBrowserForJS",
                   "framePossible",
                   "allowRescaling",
                   "boxborder",
                   "centerimage"]
    no_java_text = """Sorry, the GeoGebra Applet could not be started.
Please make sure that Java 1.4.2 (or later) is installed and activated.
(<a href="http://java.sun.com/getjava">Click here to install Java now</a>)"""

    def __init__(self, js_id, filename, width, height, applet_params):
        """Constructor should at very least pass id and filename,
        outside class will want to be able to introspect.
        """
        self.webstart_url = "http://www.geogebra.org/webstart/"
        self.webstart_version = "4.2"
        self.id = js_id
        self.filename = filename
        self.width = width
        self.height = height
        self.applet_params = applet_params
        self.load_html(self.applet_params)

    def load_html(self, applet_params):
        self.xml_root = ElementTree.Element("applet")
        self.xml_root.attrib = \
            {"code": "geogebra.GeoGebraApplet",
             "id": "ggb_applet_" + str(self.id),
             "width": str(self.width),
             "height": str(self.height),
             "codebase": self.webstart_url + self.webstart_version + "/unsigned/",
             "archive": self.webstart_url + self.webstart_version + "/geogebra.jar"}
        self.xml_root.text = JavaApplet.no_java_text
        self.append_bool_params(applet_params)

        xml_param = ElementTree.SubElement(self.xml_root, "param", attrib=
             {'name': "filename",
              'value': self.filename})
        xml_param = ElementTree.SubElement(self.xml_root, "param", attrib=
             {'name': "java_arguments",
              'value': "-Xmx512m -Djnlp.packEnabled=true"})
        xml_param = ElementTree.SubElement(self.xml_root, "param", attrib=
             {'name': "image",
              'value': "http://www.geogebra.org/webstart/loading.gif"})

        _indent(self.xml_root)

    def append_bool_params(self, applet_params):
        """Refer to http://wiki.geogebra.org/en/Reference:Applet_Parameters"""
        for param in JavaApplet.bool_params:
            if param in applet_params and applet_params[param] is not None:
                xml_param = ElementTree.SubElement(self.xml_root, "param")
                xml_param.attrib = \
                    {'name': param,
                     'value': "true" if applet_params[param] else "false"}

    def __str__(self):
        return ElementTree.tostring(self.xml_root).decode()

    @classmethod
    def param_arguments(cls, ggb_ipython_magic):
        # TODO: everything referring to ipython should be removed from this file
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
        @argument(
            '--java_arguments', '--java', default='',
            help="Arguments to pass to java")
        def wrapped_magic(self, line, cell=None):
            return ggb_ipython_magic(self, line, cell)
        for param in cls.bool_params:
            wrapped_magic = argument('--' + param, metavar='0/1', type=int, help=param)(wrapped_magic)

        return wrapped_magic

class HTML5IFrame(object):
    """"""
    bool_params = [
        ("enableRightClick", "rc", "Enable right click and zooming"),
        ("showInputBar", "ai", "Show input bar"),
        ("enableShiftDragZoom", "sdz", "Enable shift-to-drag and zoom"),
        ("showMenuBar", "smb", "Show menu bar"),
        ("showToolBar", "stb", "Show tool bar"),
        ("showToolBarHelp", "stbh", "Show tool bar help"),
        ("enableLabelDrags", "ld", "Allow labels to be draggable"),
        ("showResetIcon", "sri", "Display refresh icon to reset at original"
                                 "applet state")
        ]

    def __init__(self, js_id, ggbtube_id, width, height, applet_params):
        """"""
        self.applet_type = "preferhtml5"
        self.js_id = js_id
        self.ggbtube_id = ggbtube_id
        self.width = str(width)
        self.height = str(height)
        self.applet_params = applet_params
        self.load_html(applet_params)

    def load_html(self, applet_params):
        base_ggbtube_url = "http://www.geogebratube.org/material/iframe"
        self.ggbtube_url = \
            "{base_url}/id/{id}/width/{width}/height/{height}" \
            "/border/888888/at/{applet_type}".format(
                base_url=base_ggbtube_url, id=self.ggbtube_id,
                width=self.width, height=self.height,
                applet_type=self.applet_type)
        for long_arg, short_arg, _ in HTML5IFrame.bool_params:
            if long_arg in applet_params and applet_params[long_arg] is not None:
                self.ggbtube_url += "/{param}/{value}".format(
                    param=short_arg,
                    value="true" if applet_params[long_arg] else "false")

        self.xml_root = ElementTree.Element("iframe")
        self.xml_root.attrib = \
            {"scrolling": "no",
             "src": self.ggbtube_url,
             "width": self.width + "px",
             "height": self.width + "px",
             "style": "border:0px;"}

    def __str__(self):
        return ElementTree.tostring(self.xml_root).decode()
