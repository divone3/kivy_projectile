# uix/layout.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy_projectile.app import M3ThemableBehavior


class BaseBoxLayout(M3ThemableBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        # تنظیم پیش‌فرض‌ها قبل از فراخوانی super
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")
        super().__init__(**kwargs)

        # تنظیم target properties برای layoutها
        self.target_bg_prop = "md_bg_color"


class BaseGridLayout(M3ThemableBehavior, MDGridLayout):
    def __init__(self, **kwargs):
        # تنظیم پیش‌فرض‌ها قبل از فراخوانی super
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")
        super().__init__(**kwargs)

        # تنظیم target properties برای layoutها
        self.target_bg_prop = "md_bg_color"


class BaseFloatLayout(M3ThemableBehavior, MDFloatLayout):
    def __init__(self, **kwargs):
        # تنظیم پیش‌فرض‌ها قبل از فراخوانی super
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")
        super().__init__(**kwargs)

        # تنظیم target properties برای layoutها
        self.target_bg_prop = "md_bg_color"