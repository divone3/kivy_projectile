# uix/label.py
from kivymd.uix.label import MDLabel
from kivy_projectile.app import M3ThemableBehavior


class BaseLabel(M3ThemableBehavior, MDLabel):
    def __init__(self, **kwargs):
        # ابتدا target properties را تنظیم کنید
        self.target_bg_prop = "md_bg_color"
        self.target_fg_prop = "text_color"

        # سپس پیش‌فرض‌ها را تنظیم کنید
        kwargs.setdefault("bg_token", "transparent")
        kwargs.setdefault("fg_token", "on_surface")

        # در نهایت super() را فراخوانی کنید
        super().__init__(**kwargs)