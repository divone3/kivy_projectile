# uix/label.py
from kivymd.uix.label import MDLabel
from kivy_projectile.app import M3ThemableBehavior

class BaseLabel(M3ThemableBehavior, MDLabel):
    def __init__(self, **kwargs):
        # پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "surface")   # پس‌زمینه
        kwargs.setdefault("fg_token", "on_surface")  # رنگ متن
        super().__init__(**kwargs)
