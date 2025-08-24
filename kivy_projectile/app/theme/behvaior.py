# theme/behavior.py
from kivy.event import EventDispatcher
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty
)
from kivymd.app import MDApp


class M3ThemableBehavior(EventDispatcher):
    """
    Behavior عمومی: توکن‌های رنگی M3 را به ویژگی‌های ویجت اعمال می‌کند.
    """
    theme = ObjectProperty(None, rebind = True)
    bg_token = StringProperty("surface")
    fg_token = StringProperty("on_surface")
    outline_token = StringProperty("outline")
    elevation = NumericProperty(0)
    use_container = BooleanProperty(False)

    # نام‌های property سفارشی برای ویجت‌های مختلف
    target_bg_prop = StringProperty("md_bg_color")
    target_fg_prop = StringProperty("text_color")
    target_outline_prop = StringProperty("line_color")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # تلاش برای گرفتن theme از اپ
        if self.theme is None:
            app = MDApp.get_running_app()
            if hasattr(app, 'm3_theme'):
                self.theme = app.m3_theme

        # bind به تغییرات تم
        if self.theme is not None:
            self._bind_theme(self.theme)

        # bind به تغییرات properties
        for prop in ["bg_token", "fg_token", "outline_token", "elevation",
                     "use_container", "target_bg_prop", "target_fg_prop", "target_outline_prop"]:
            self.fbind(prop, self.apply_m3_theme)

        # اعمال اولیه تم
        self.apply_m3_theme()

    def _bind_theme(self, theme):
        """اتصال به تغییرات تم"""
        theme.bind(mode = self.apply_m3_theme)
        for role in ["primary", "secondary", "tertiary", "error", "surface", "outline"]:
            if hasattr(theme, role):
                getattr(theme, role).bind(self.apply_m3_theme)

    def _maybe_containerize(self, token: str) -> str:
        """تبدیل توکن به container version در صورت نیاز"""
        if not self.use_container:
            return token

        mapping = {
            "primary":"primary_container",
            "secondary":"secondary_container",
            "tertiary":"tertiary_container",
            "error":"error_container",
            "on_primary":"on_primary_container",
            "on_secondary":"on_secondary_container",
            "on_tertiary":"on_tertiary_container",
            "on_error":"on_error_container"
        }

        return mapping.get(token, token)

    def apply_m3_theme(self, *args):
        """اعمال تم M3 بر روی ویجت"""
        if self.theme is None:
            return

        try:
            # محاسبه توکن‌های نهایی
            final_bg_token = self._maybe_containerize(self.bg_token)
            final_fg_token = self._maybe_containerize(self.fg_token)

            # دریافت رنگ‌ها
            bg_color = self.theme.get_rgba(final_bg_token)
            fg_color = self.theme.get_rgba(final_fg_token)
            outline_color = self.theme.get_rgba(self.outline_token)

            # اعمال بر روی ویجت
            if hasattr(self, self.target_bg_prop):
                setattr(self, self.target_bg_prop, bg_color)

            if hasattr(self, self.target_fg_prop):
                setattr(self, self.target_fg_prop, fg_color)

            if hasattr(self, self.target_outline_prop):
                setattr(self, self.target_outline_prop, outline_color)

        except Exception as e:
            print(f"Error applying M3 theme: {e}")