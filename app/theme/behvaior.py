# theme/behavior.py
from app import BaseApp
from kivy.event import EventDispatcher
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty
)

class M3ThemableBehavior(EventDispatcher):
    """
    Behavior عمومی: توکن‌های رنگی M3 را به ویژگی‌های ویجت اعمال می‌کند.
    - bg_token     : توکن پس‌زمینه (e.g. 'surface', 'primary', 'primary_container')
    - fg_token     : توکن متن/آیکن (e.g. 'on_surface', 'on_primary')
    - outline_token: توکن خط/بوردر (e.g. 'outline', 'outline_variant')
    - elevation    : صرفاً برای سازگاری آینده (surface blending)، فعلاً تزئینی
    - use_container: اگر True و توکن خانواده‌ی primary/secondary/tertiary بود، از containerها استفاده کن
    """
    theme = ObjectProperty(None, rebind=True)  # اشاره به BaseTheme توسعه‌یافته
    bg_token = StringProperty("surface")
    fg_token = StringProperty("on_surface")
    outline_token = StringProperty("outline")
    elevation = NumericProperty(0)
    use_container = BooleanProperty(False)

    # اگر ویجت بخواهد از نام‌های property سفارشی استفاده کند:
    target_bg_prop = StringProperty("md_bg_color")
    target_fg_prop = StringProperty("text_color")
    target_outline_prop = StringProperty("line_color")  # برای TextFields/Buttons/Dividers

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # تلاش برای گرفتن theme از اپ
        if self.m3theme is None:
            app = BaseApp.get_running_app()
            self.theme = getattr(app, "theme", None)

        # bind به تغییرات تم
        if self.theme is not None:
            self._bind_theme(self.m3theme)

        # هر تغییری در توکن‌ها → اعمال مجدد
        for p in ("bg_token", "fg_token", "outline_token",
                  "elevation", "use_container",
                  "target_bg_prop", "target_fg_prop", "target_outline_prop"):
            self.fbind(p, lambda *_: self.apply_m3_theme())

    # ---------- اتصال به تغییرات تم ----------
    def _bind_theme(self, theme):
        # وقتی user مَد عوض می‌کند یا منبع رنگ‌ها تغییر می‌کند، DictPropertyهای نقش‌ها عوض می‌شوند
        for name in ("primary", "secondary", "tertiary", "error", "surface", "outline", "mode"):
            theme.fbind(name, lambda *_: self.apply_m3_theme())
        # برای سازگاری با تغییر مراجع theme
        self.fbind("theme", lambda *_: self.apply_m3_theme())

    # ---------- انتخاب توکن نهایی بر اساس use_container ----------
    def _maybe_containerize(self, token: str) -> str:
        if not self.m3_use_container:
            return token
        base = token.strip()
        # اگر primary/secondary/tertiary انتخاب شده و container خواستیم:
        mapping = {
            "primary": ("primary_container", "on_primary_container"),
            "secondary": ("secondary_container", "on_secondary_container"),
            "tertiary": ("tertiary_container", "on_tertiary_container"),
        }
        if base in mapping:
            # پس‌زمینه container، متن on_container
            return mapping[base][0]
        if base.startswith("on_"):
            base2 = base.replace("on_", "")
            if base2 in mapping:
                return mapping[base2][1]
        return token

    # ---------- اعمال تم ----------
    def apply_m3_theme(self, *_):
        theme = self.m3theme
        if theme is None:
            return

        # محاسبه‌ی توکن‌های نهایی
        bg_token = self._maybe_containerize(self.bg_token)
        fg_token = self._maybe_containerize(self.fg_token)
        ol_token = self.outline_token

        try:
            bg = theme.get_rgba(bg_token)
            fg = theme.get_rgba(fg_token)
            ol = theme.get_rgba(ol_token)
        except Exception:
            # اگر توکن اشتباه بود، سایلنت: توسعه‌دهنده در لاگ خودش هندل کند
            return

        # تلاش برای ست کردن روی ویژگی‌های رایج ویجت‌ها
        # 1) پس زمینه
        if hasattr(self, self.target_bg_prop):
            try:
                setattr(self, self.target_bg_prop, bg)
            except Exception:
                pass
        # سازگاری با ویجت‌هایی که از background_color استفاده می‌کنند
        elif hasattr(self, "background_color"):
            try:
                self.background_color = bg
            except Exception:
                pass

        # 2) متن/آیکن
        if hasattr(self, self.target_fg_prop):
            try:
                setattr(self, self.target_fg_prop, fg)
            except Exception:
                pass
        # سازگاری با MDIcon/MDLabel خاص
        elif hasattr(self, "text_color"):
            try:
                self.text_color = fg
            except Exception:
                pass
        elif hasattr(self, "icon_color"):
            try:
                self.icon_color = fg
            except Exception:
                pass

        # 3) outline/border/line
        if hasattr(self, self.target_outline_prop):
            try:
                setattr(self, self.target_outline_prop, ol)
            except Exception:
                pass
        elif hasattr(self, "line_color_normal"):
            try:
                self.line_color_normal = ol
            except Exception:
                pass

        # 4) surface elevation blending (آینده)
        # اینجا می‌تونی براساس m3_elevation، blend انجام بدی و bg رو کمی با primary/neutral میکس کنی.
        # فعلاً نگه می‌داریم تا بعداً اضافه کنیم.
