from xml.etree import ElementTree

class JavaApplet(object):
    def __init__(self, id, webstart_version, width, height, applet_params):
        """"""
        ggb_webstart_base = "http://www.geogebra.org/webstart/"
        self.xml_root = ElementTree.Element("applet")
        self.xml_root.attrib = \
            {"code": "geogebra.GeoGebraApplet",
             "id": "ggb_applet_" + str(id),
             "width": str(width),
             "height": str(height),
             "codebase": ggb_webstart_base + webstart_version + "/unsigned/",
             "archive": ggb_webstart_base + webstart_version + "/geogebra.jar"}
        self.append_bool_params(applet_params)
        print ElementTree.tostring(self.xml_root)
    
    def append_bool_params(self, applet_params):
        """Refer to http://wiki.geogebra.org/en/Reference:Applet_Parameters"""
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
                       "allowRescaling"]
        for param in bool_params:
            if applet_params.__hasattr__(param):
                xml_param = ElementTree.SubElement("param", self.xml_root)
                xml_param.attrib = \
                    {'name': param,
                     'value': bool(applet_params.__getattr__(param))}        