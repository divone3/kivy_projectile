# theme/theme.py
from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty, ListProperty
from kivy.utils import get_color_from_hex
import math
import colorsys


class ThemeResolveError(KeyError):
    pass


# توابع تبدیل رنگ
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
    """تبدیل RGB به HCT (Hue, Chroma, Tone)"""
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    # محاسبه Chroma (اشباع)
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    chroma = max_val - min_val

    # Tone (روشنی) - مشابه Lightness اما برای Material Design
    tone = l * 100

    return h * 360, chroma * 100, tone


def hct_to_rgb(hue, chroma, tone):
    """تبدیل HCT به RGB"""
    # تبدیل Tone به Lightness (0-1)
    l = tone / 100.0

    # تبدیل Chroma به Saturation
    s = chroma / 100.0 if chroma > 0 else 0

    # تبدیل Hue به محدوده 0-1
    h = hue / 360.0

    # تبدیل HLS به RGB
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return r, g, b


def hct_to_hex(hue, chroma, tone):
    rgb = hct_to_rgb(hue, chroma, tone)
    return rgb_to_hex(rgb)


def hex_to_hct(hex_color):
    rgb = hex_to_rgb(hex_color)
    return rgb_to_hct(rgb)


class M3ResolverMixin:
    """
    Material 3 Color Token Resolver با پیاده‌سازی HCT
    """
    _ROLE_BUCKETS = ("primary", "secondary", "tertiary", "error", "neutral", "neutral_variant", "surface", "outline")
    _TONAL_PALETTE_TONES = ("0", "4", "5", "6", "10", "12", "17", "20", "22", "24", "25", "30", "40", "50",
                            "60", "70", "80", "87", "90", "92", "94", "95", "96", "98", "99", "100")

    def get_hex(self, token: str) -> str:
        token = str(token).strip().lower()

        # بررسی نقش‌های اصلی
        for bucket in self._ROLE_BUCKETS:
            d = getattr(self, bucket, None) or {}
            if token in d:
                return d[token]

        # بررسی توکن‌های ترکیبی (مثل primary.40)
        if "." in token:
            role, tone = token.split(".", 1)
            if role in ("primary", "secondary", "tertiary", "error", "neutral", "neutral_variant"):
                palettes = {
                    "primary":self._generate_tonal_palette(self.source_primary),
                    "secondary":self._generate_tonal_palette(self.source_secondary),
                    "tertiary":self._generate_tonal_palette(self.source_tertiary),
                    "error":self._generate_tonal_palette(self.source_error),
                    "neutral":self._generate_tonal_palette(self.source_neutral),
                    "neutral_variant":self._generate_tonal_palette(self.source_neutral_variant),
                }
                pal = palettes.get(role, {})
                if tone in pal:
                    return pal[tone]

        raise ThemeResolveError(f"Unknown color token: {token}")

    def get_rgba(self, token: str, alpha: float = 1.0):
        hex_color = self.get_hex(token)
        color = get_color_from_hex(hex_color)
        return [color[0], color[1], color[2], alpha]


class BaseTheme(EventDispatcher, M3ResolverMixin):
    """
    Material 3 Theme Manager با پیاده‌سازی HCT
    """
    # رنگ‌های منبع
    source_primary = StringProperty("#6750A4")
    source_secondary = StringProperty("#958DA5")
    source_tertiary = StringProperty("#B58392")
    source_error = StringProperty("#B3261E")
    source_neutral = StringProperty("#605D62")
    source_neutral_variant = StringProperty("#605D62")

    # نقش‌های رنگی
    primary = DictProperty({})
    secondary = DictProperty({})
    tertiary = DictProperty({})
    error = DictProperty({})
    neutral = DictProperty({})
    neutral_variant = DictProperty({})
    surface = DictProperty({})
    outline = DictProperty({})

    # حالت تم
    mode = StringProperty("light")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            source_primary = self._generate_all_palettes,
            source_secondary = self._generate_all_palettes,
            source_tertiary = self._generate_all_palettes,
            source_error = self._generate_all_palettes,
            source_neutral = self._generate_all_palettes,
            source_neutral_variant = self._generate_all_palettes,
            mode = self._generate_all_palettes
        )
        self._generate_all_palettes()

    def _generate_tonal_palette(self, hex_color: str) -> dict:
        """تولید پالت تونال بر اساس الگوریتم HCT"""
        # تبدیل رنگ منبع به HCT
        hue, chroma, source_tone = hex_to_hct(hex_color)

        # tones بر اساس مشخصات M3
        tones = {
            "0":0.0, "4":4.0, "5":5.0, "6":6.0, "10":10.0, "12":12.0,
            "17":17.0, "20":20.0, "22":22.0, "24":24.0, "25":25.0, "30":30.0,
            "40":40.0, "50":50.0, "60":60.0, "70":70.0, "80":80.0, "87":87.0,
            "90":90.0, "92":92.0, "94":94.0, "95":95.0, "96":96.0, "98":98.0,
            "99":99.0, "100":100.0
        }

        palette = {}
        for tone_name, tone_value in tones.items():
            palette[tone_name] = hct_to_hex(hue, chroma, tone_value)

        return palette

    def _map_roles(self, palette: dict, role: str) -> dict:
        """نقش‌های رنگی بر اساس حالت تم"""
        is_dark = self.mode.lower() == "dark"

        if role == "primary":
            return {
                "primary":palette["40"] if not is_dark else palette["80"],
                "on_primary":palette["100"] if not is_dark else palette["20"],
                "primary_container":palette["90"] if not is_dark else palette["30"],
                "on_primary_container":palette["10"] if not is_dark else palette["90"],
                "inverse_primary":palette["80"] if not is_dark else palette["40"],
            }
        elif role == "secondary":
            return {
                "secondary":palette["40"] if not is_dark else palette["80"],
                "on_secondary":palette["100"] if not is_dark else palette["20"],
                "secondary_container":palette["90"] if not is_dark else palette["30"],
                "on_secondary_container":palette["10"] if not is_dark else palette["90"],
            }
        elif role == "tertiary":
            return {
                "tertiary":palette["40"] if not is_dark else palette["80"],
                "on_tertiary":palette["100"] if not is_dark else palette["20"],
                "tertiary_container":palette["90"] if not is_dark else palette["30"],
                "on_tertiary_container":palette["10"] if not is_dark else palette["90"],
            }
        elif role == "error":
            return {
                "error":palette["40"] if not is_dark else palette["80"],
                "on_error":palette["100"] if not is_dark else palette["20"],
                "error_container":palette["90"] if not is_dark else palette["30"],
                "on_error_container":palette["10"] if not is_dark else palette["90"],
            }
        return {}

    def _generate_surface_roles(self, neutral_palette: dict, neutral_variant_palette: dict) -> dict:
        """تولید نقش‌های سطحی بر اساس پالت خنثی"""
        is_dark = self.mode.lower() == "dark"

        if not is_dark:
            return {
                "surface":neutral_palette["98"],
                "on_surface":neutral_palette["10"],
                "surface_variant":neutral_variant_palette["90"],
                "on_surface_variant":neutral_variant_palette["30"],
                "surface_container":neutral_palette["94"],
                "surface_container_lowest":neutral_palette["100"],
                "surface_container_low":neutral_palette["96"],
                "surface_container_high":neutral_palette["92"],
                "surface_container_highest":neutral_palette["90"],
                "surface_bright":neutral_palette["98"],
                "surface_dim":neutral_palette["87"],
                "inverse_surface":neutral_palette["20"],
                "inverse_on_surface":neutral_palette["95"],
            }
        else:
            return {
                "surface":neutral_palette["6"],
                "on_surface":neutral_palette["90"],
                "surface_variant":neutral_variant_palette["30"],
                "on_surface_variant":neutral_variant_palette["80"],
                "surface_container":neutral_palette["12"],
                "surface_container_lowest":neutral_palette["4"],
                "surface_container_low":neutral_palette["10"],
                "surface_container_high":neutral_palette["17"],
                "surface_container_highest":neutral_palette["22"],
                "surface_bright":neutral_palette["24"],
                "surface_dim":neutral_palette["6"],
                "inverse_surface":neutral_palette["90"],
                "inverse_on_surface":neutral_palette["20"],
            }

    def _generate_outline_roles(self, neutral_variant_palette: dict) -> dict:
        """تولید نقش‌های outline"""
        is_dark = self.mode.lower() == "dark"

        if not is_dark:
            return {
                "outline":neutral_variant_palette["50"],
                "outline_variant":neutral_variant_palette["80"],
            }
        else:
            return {
                "outline":neutral_variant_palette["60"],
                "outline_variant":neutral_variant_palette["30"],
            }

    def _generate_all_palettes(self, *args):
        """تولید همه پالت‌ها و نقش‌ها"""
        # تولید پالت‌های تونال
        primary_palette = self._generate_tonal_palette(self.source_primary)
        secondary_palette = self._generate_tonal_palette(self.source_secondary)
        tertiary_palette = self._generate_tonal_palette(self.source_tertiary)
        error_palette = self._generate_tonal_palette(self.source_error)
        neutral_palette = self._generate_tonal_palette(self.source_neutral)
        neutral_variant_palette = self._generate_tonal_palette(self.source_neutral_variant)

        # نقش‌های رنگی
        self.primary = self._map_roles(primary_palette, "primary")
        self.secondary = self._map_roles(secondary_palette, "secondary")
        self.tertiary = self._map_roles(tertiary_palette, "tertiary")
        self.error = self._map_roles(error_palette, "error")
        self.neutral = neutral_palette
        self.neutral_variant = neutral_variant_palette

        # نقش‌های سطحی و outline
        self.surface = self._generate_surface_roles(neutral_palette, neutral_variant_palette)
        self.outline = self._generate_outline_roles(neutral_variant_palette)

    def switch_mode(self, mode: str):
        """تغییر حالت تم"""
        if mode.lower() in ["light", "dark"]:
            self.mode = mode.lower()
            self._generate_all_palettes()

    def toggle_mode(self):
        """تغییر وضعیت تم بین light و dark"""
        self.mode = "dark" if self.mode == "light" else "light"
        self._generate_all_palettes()

    def update_sources(self, **kwargs):
        """به روزرسانی رنگ‌های منبع"""
        for k, v in kwargs.items():
            if hasattr(self, f"source_{k}"):
                setattr(self, f"source_{k}", v)
        self._generate_all_palettes()

    def get_palette(self, role: str) -> dict:
        """دریافت پالت کامل برای یک نقش خاص"""
        if role == "primary":
            return self._generate_tonal_palette(self.source_primary)
        elif role == "secondary":
            return self._generate_tonal_palette(self.source_secondary)
        elif role == "tertiary":
            return self._generate_tonal_palette(self.source_tertiary)
        elif role == "error":
            return self._generate_tonal_palette(self.source_error)
        elif role == "neutral":
            return self._generate_tonal_palette(self.source_neutral)
        elif role == "neutral_variant":
            return self._generate_tonal_palette(self.source_neutral_variant)
        else:
            raise ThemeResolveError(f"Unknown palette role: {role}")

    def get_all_tokens(self) -> dict:
        """دریافت همه توکن‌های رنگی به صورت dictionary"""
        all_tokens = {}
        for bucket in self._ROLE_BUCKETS:
            d = getattr(self, bucket, {})
            for key, value in d.items():
                all_tokens[f"{bucket}.{key}"] = value
        return all_tokens
