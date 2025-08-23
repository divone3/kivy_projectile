# uix/layout.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from app import M3ThemableBehavior


class BaseBoxLayout(M3ThemableBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        # پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")
        super().__init__(**kwargs)


class BaseGridLayout(M3ThemableBehavior, MDGridLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "on_surface")
        super().__init__(**kwargs)
