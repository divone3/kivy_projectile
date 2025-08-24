# uix/layout.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy_projectile.app import M3ThemableBehavior


class BaseBoxLayout(M3ThemableBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        # ابتدا target properties را تنظیم کنید
        self.target_bg_prop = "md_bg_color"

        # سپس پیش‌فرض‌ها را تنظیم کنید
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")

        # در نهایت super() را فراخوانی کنید
        super().__init__(**kwargs)


class BaseGridLayout(M3ThemableBehavior, MDGridLayout):
    def __init__(self, **kwargs):
        # ابتدا target properties را تنظیم کنید
        self.target_bg_prop = "md_bg_color"

        # سپس پیش‌فرض‌ها را تنظیم کنید
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")

        # در نهایت super() را فراخوانی کنید
        super().__init__(**kwargs)


class BaseFloatLayout(M3ThemableBehavior, MDFloatLayout):
    def __init__(self, **kwargs):
        # ابتدا target properties را تنظیم کنید
        self.target_bg_prop = "md_bg_color"

        # سپس پیش‌فرض‌ها را تنظیم کنید
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")

        # در نهایت super() را فراخوانی کنید
        super().__init__(**kwargs)