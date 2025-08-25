# theme/theme.py
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty
from kivy.utils import get_color_from_hex
from enum import Enum
import colorsys


class ThemeResolveError(KeyError):
    pass


# ================================
# 🎨 Enum برای توکن‌ها
# ================================
class M3ColorTokens(str, Enum):
    PRIMARY = "primary"
    ON_PRIMARY = "on_primary"
    PRIMARY_CONTAINER = "primary_container"
    ON_PRIMARY_CONTAINER = "on_primary_container"
    SECONDARY = "secondary"
    ON_SECONDARY = "on_secondary"
    SECONDARY_CONTAINER = "secondary_container"
    ON_SECONDARY_CONTAINER = "on_secondary_container"
    TERTIARY = "tertiary"
    ON_TERTIARY = "on_tertiary"
    TERTIARY_CONTAINER = "tertiary_container"
    ON_TERTIARY_CONTAINER = "on_tertiary_container"
    ERROR = "error"
    ON_ERROR = "on_error"
    ERROR_CONTAINER = "error_container"
    ON_ERROR_CONTAINER = "on_error_container"
    SURFACE = "surface"
    ON_SURFACE = "on_surface"
    OUTLINE = "outline"
    TRANSPARENT = "transparent"


# ================================
# 🎨 توابع رنگی ساده (Hex ↔ RGB/HCT)
# ================================
def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    return tuple(int(hex_color[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


def rgb_to_hct(rgb):
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    max_val, min_val = max(rgb), min(rgb)
    chroma = max_val - min_val
    return h * 360, chroma * 100, l * 100


def hct_to_rgb(h, c, t):
    l = t / 100.0
    s = c / 100.0 if c > 0 else 0
    h = h / 360.0
    return colorsys.hls_to_rgb(h, l, s)


def hct_to_hex(h, c, t):
    return rgb_to_hex(hct_to_rgb(h, c, t))


def hex_to_hct(hex_color):
    return rgb_to_hct(hex_to_rgb(hex_color))


# ================================
# 🎨 M3 Theme Manager
# ================================
class BaseTheme(EventDispatcher):
    # رنگ‌های منبع
    source_primary = StringProperty("#6750A4")
    source_secondary = StringProperty("#625B71")
    source_tertiary = StringProperty("#7D5260")
    source_error = StringProperty("#B3261E")
    source_neutral = StringProperty("#605D62")
    source_neutral_variant = StringProperty("#605D62")

    # نقش‌های رنگی (توکن‌ها)
    tokens = DictProperty({})

    # حالت تم
    mode = StringProperty("light")  # light / dark

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(
            source_primary=self._regenerate,
            source_secondary=self._regenerate,
            source_tertiary=self._regenerate,
            source_error=self._regenerate,
            source_neutral=self._regenerate,
            source_neutral_variant=self._regenerate,
            mode=self._regenerate,
        )
        self._regenerate()

    # -----------------------------
    # ساخت پالت تونال
    # -----------------------------
    def _generate_tonal_palette(self, hex_color: str) -> dict:
        h, c, _ = hex_to_hct(hex_color)
        tones = {str(t): hct_to_hex(h, c, t) for t in range(0, 101, 10)}
        tones.update({"95": hct_to_hex(h, c, 95), "98": hct_to_hex(h, c, 98), "6":hct_to_hex(h, c, 6)})
        return tones

    # -----------------------------
    # ساخت کل نقش‌های رنگی
    # -----------------------------
    def _regenerate(self, *args):
        is_dark = self.mode == "dark"

        # پالت‌ها
        primary_pal = self._generate_tonal_palette(self.source_primary)
        secondary_pal = self._generate_tonal_palette(self.source_secondary)
        tertiary_pal = self._generate_tonal_palette(self.source_tertiary)
        error_pal = self._generate_tonal_palette(self.source_error)
        neutral_pal = self._generate_tonal_palette(self.source_neutral)
        neutral_var_pal = self._generate_tonal_palette(self.source_neutral_variant)

        # نقش‌ها
        self.tokens = {
            # primary
            "primary": primary_pal["60"] if not is_dark else primary_pal["10"],
            "on_primary": primary_pal["10"] if not is_dark else primary_pal["90"],
            "primary_container": primary_pal["80"] if not is_dark else primary_pal["40"],
            "on_primary_container": primary_pal["20"] if not is_dark else primary_pal["70"],

            # secondary
            "secondary": secondary_pal["60"] if not is_dark else secondary_pal["10"],
            "on_secondary": secondary_pal["10"] if not is_dark else secondary_pal["90"],
            "secondary_container": secondary_pal["80"] if not is_dark else secondary_pal["40"],
            "on_secondary_container": secondary_pal["20"] if not is_dark else secondary_pal["70"],

            # tertiary
            "tertiary": tertiary_pal["60"] if not is_dark else tertiary_pal["10"],
            "on_tertiary": tertiary_pal["10"] if not is_dark else tertiary_pal["90"],
            "tertiary_container": tertiary_pal["80"] if not is_dark else tertiary_pal["40"],
            "on_tertiary_container": tertiary_pal["20"] if not is_dark else tertiary_pal["70"],

            # error
            "error": error_pal["60"] if not is_dark else error_pal["10"],
            "on_error": error_pal["10"] if not is_dark else error_pal["90"],
            "error_container": error_pal["80"] if not is_dark else error_pal["40"],
            "on_error_container": error_pal["20"] if not is_dark else error_pal["70"],

            # surface + outline
            "surface": neutral_pal["80"] if not is_dark else neutral_pal["10"],
            "on_surface": neutral_pal["10"] if not is_dark else neutral_pal["80"],
            "surface_container":neutral_pal["90"] if not is_dark else neutral_pal["20"],
            "on_surface_container":neutral_pal["20"] if not is_dark else neutral_pal["90"],

            "outline": neutral_var_pal["50"] if not is_dark else neutral_var_pal["60"],

            # شفاف
            "transparent": "#00000000",
        }

    # -----------------------------
    # گرفتن رنگ
    # -----------------------------
    def get_hex(self, token: str) -> str:
        token = str(token)
        if token in self.tokens:
            return self.tokens[token]
        raise ThemeResolveError(f"Unknown token: {token}")

    def get_rgba(self, token: str, alpha: float = 1.0):
        hex_color = self.get_hex(token)
        color = get_color_from_hex(hex_color)
        return [color[0], color[1], color[2], alpha]

    # -----------------------------
    # تغییر حالت
    # -----------------------------
    def toggle_mode(self):
        self.mode = "dark" if self.mode == "light" else "light"
        self._regenerate()
