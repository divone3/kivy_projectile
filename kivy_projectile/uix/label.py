# uix/label.py
from kivymd.uix.label import MDLabel
from kivy_projectile.app import M3ThemableBehavior


class BaseLabel(M3ThemableBehavior, MDLabel):
    def __init__(self, **kwargs):
        # تنظیم پیش‌فرض‌ها قبل از فراخوانی super
        kwargs.setdefault("bg_token", "surface")  # پس‌زمینه شفاف
        kwargs.setdefault("fg_token", "on_surface")  # رنگ متن
        super().__init__(**kwargs)

        # تنظیم target properties برای label
        self.target_bg_prop = "md_bg_color"
        self.target_fg_prop = "text_color"

        # برای labelها معمولاً نیازی به پس‌زمینه نیست
        # اما اگر bg_token تنظیم شده باشد، اعمال می‌شود