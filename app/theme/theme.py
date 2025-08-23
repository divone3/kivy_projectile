# theme/theme.py
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty
from kivy.utils import get_color_from_hex
from colorsys import rgb_to_hls, hls_to_rgb


class ThemeResolveError(KeyError):
    pass


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(
        int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
    )


def adjust_lightness(hex_color, factor):
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = rgb_to_hls(r, g, b)
    l = min(1, max(0, l * factor))
    r, g, b = hls_to_rgb(h, l, s)
    return rgb_to_hex((r, g, b))


class M3ResolverMixin:
    """
    افزونه برای BaseTheme: تبدیل نام توکن به hex و rgba
    """
    _ROLE_BUCKETS = ("primary", "secondary", "tertiary", "error", "surface", "outline")

    def get_hex(self, token: str) -> str:
        token = str(token).strip()
        for bucket in self._ROLE_BUCKETS:
            d = getattr(self, bucket, None) or {}
            if token in d:
                return d[token]
        # token مثل primary.40
        if "." in token:
            head, tone = token.split(".", 1)
            if head in ("primary", "secondary", "tertiary", "error"):
                palettes = {
                    "primary": self._generate_tonal_palette(self.source_primary),
                    "secondary": self._generate_tonal_palette(self.source_secondary),
                    "tertiary": self._generate_tonal_palette(self.source_tertiary),
                    "error": self._generate_tonal_palette(self.source_error),
                }
                pal = palettes[head]
                tone = tone.strip()
                if tone in pal:
                    return pal[tone]
        raise ThemeResolveError(f"Unknown color token: {token}")

    def get_rgba(self, token: str, alpha: float = 1.0):
        rgba = list(get_color_from_hex(self.get_hex(token)))
        rgba[3] = alpha
        return rgba


class BaseTheme(EventDispatcher, M3ResolverMixin):
    """
    Material 3 Theme Manager + Resolver
    """
    source_primary = StringProperty("#6750A4")
    source_secondary = StringProperty("#625B71")
    source_tertiary = StringProperty("#7D5260")
    source_error = StringProperty("#B3261E")
    source_neutral = StringProperty("#605D62")

    primary = DictProperty({})
    secondary = DictProperty({})
    tertiary = DictProperty({})
    error = DictProperty({})
    surface = DictProperty({})
    outline = DictProperty({})

    mode = StringProperty("light")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generate_all_palettes()

    def _generate_tonal_palette(self, hex_color: str) -> dict:
        tones = {
            0: adjust_lightness(hex_color, 0.1),
            10: adjust_lightness(hex_color, 0.25),
            20: adjust_lightness(hex_color, 0.35),
            30: adjust_lightness(hex_color, 0.55),
            40: adjust_lightness(hex_color, 0.75),
            50: hex_color,
            60: adjust_lightness(hex_color, 1.15),
            70: adjust_lightness(hex_color, 1.3),
            80: adjust_lightness(hex_color, 1.5),
            90: adjust_lightness(hex_color, 1.7),
            95: adjust_lightness(hex_color, 1.85),
            99: "#FFFFFF",
            100: "#FFFFFF"
        }
        return {str(k): v for k, v in tones.items()}

    def _map_roles(self, palette: dict, role: str) -> dict:
        if role == "primary":
            return {
                "primary": palette["40"] if self.mode == "light" else palette["80"],
                "on_primary": palette["100"] if self.mode == "light" else palette["20"],
                "primary_container": palette["90"] if self.mode == "light" else palette["30"],
                "on_primary_container": palette["10"] if self.mode == "light" else palette["90"],
            }
        elif role == "secondary":
            return {
                "secondary": palette["40"] if self.mode == "light" else palette["80"],
                "on_secondary": palette["100"] if self.mode == "light" else palette["20"],
                "secondary_container": palette["90"] if self.mode == "light" else palette["30"],
                "on_secondary_container": palette["10"] if self.mode == "light" else palette["90"],
            }
        elif role == "tertiary":
            return {
                "tertiary": palette["40"] if self.mode == "light" else palette["80"],
                "on_tertiary": palette["100"] if self.mode == "light" else palette["20"],
                "tertiary_container": palette["90"] if self.mode == "light" else palette["30"],
                "on_tertiary_container": palette["10"] if self.mode == "light" else palette["90"],
            }
        elif role == "error":
            return {
                "error": palette["40"] if self.mode == "light" else palette["80"],
                "on_error": palette["100"] if self.mode == "light" else palette["20"],
                "error_container": palette["90"] if self.mode == "light" else palette["30"],
                "on_error_container": palette["10"] if self.mode == "light" else palette["90"],
            }
        return {}

    def _generate_surface_roles(self):
        if self.mode == "light":
            return {
                "surface": "#FFFBFE",
                "on_surface": "#1C1B1F",
                "surface_variant": "#E7E0EC",
                "on_surface_variant": "#49454F",
            }
        else:
            return {
                "surface": "#1C1B1F",
                "on_surface": "#E6E1E5",
                "surface_variant": "#49454F",
                "on_surface_variant": "#CAC4D0",
            }

    def _generate_outline_roles(self):
        if self.mode == "light":
            return {"outline": "#79747E", "outline_variant": "#C4C7C5"}
        else:
            return {"outline": "#938F99", "outline_variant": "#444746"}

    def _generate_all_palettes(self):
        p = self._generate_tonal_palette(self.source_primary)
        s = self._generate_tonal_palette(self.source_secondary)
        t = self._generate_tonal_palette(self.source_tertiary)
        e = self._generate_tonal_palette(self.source_error)

        self.primary = self._map_roles(p, "primary")
        self.secondary = self._map_roles(s, "secondary")
        self.tertiary = self._map_roles(t, "tertiary")
        self.error = self._map_roles(e, "error")
        self.surface = self._generate_surface_roles()
        self.outline = self._generate_outline_roles()

    def switch_mode(self, mode: str):
        self.mode = mode
        self._generate_all_palettes()

    def update_sources(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, f"source_{k}"):
                setattr(self, f"source_{k}", v)
        self._generate_all_palettes()
