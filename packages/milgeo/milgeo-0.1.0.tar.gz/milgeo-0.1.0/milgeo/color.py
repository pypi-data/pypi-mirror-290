import re
import webcolors


class ColorFinder:
    color_names = [
        "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque",
        "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue",
        "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan",
        "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkgrey",
        "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
        "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey",
        "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dimgrey",
        "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
        "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "grey", "honeydew",
        "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush",
        "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
        "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink",
        "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey",
        "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon",
        "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
        "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred",
        "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace",
        "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen",
        "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum",
        "powderblue", "purple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon",
        "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue",
        "slategray", "slategrey", "snow", "springgreen", "steelblue", "tan", "teal", "thistle",
        "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"
    ]
    color_name_patterns = {name: re.compile(re.escape(name), re.IGNORECASE) for name in color_names}
    hex_color_regex = re.compile(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})')
    rgb_color_regex = re.compile(r'rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)')
    kml_color_regex = re.compile(r'\b[0-9a-fA-F]{8}\b')

    @staticmethod
    def _rgb_to_hex(rgb_color):
        r, g, b = map(int, rgb_color)
        return webcolors.rgb_to_hex((r, g, b))

    @staticmethod
    def _kml_color_to_hex(kml_color):
        return f"#{kml_color[6:8]}{kml_color[4:6]}{kml_color[2:4]}"

    def find_hex_color(self, color_string):
        if color_string is None:
            return None

        if isinstance(color_string, bytes):
            color_string = color_string.decode('utf-8')

        color_string = color_string.strip().lower()

        hex_match = self.hex_color_regex.search(color_string)
        if hex_match:
            return hex_match.group(0)

        for name, pattern in self.color_name_patterns.items():
            if pattern.search(color_string):
                return webcolors.name_to_hex(name)

        rgb_match = self.rgb_color_regex.search(color_string)
        if rgb_match:
            return self._rgb_to_hex(rgb_match.groups())

        kml_match = self.kml_color_regex.search(color_string)
        if kml_match:
            return self._kml_color_to_hex(kml_match.group(0))

        return None
