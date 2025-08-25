# uix/button.py
from kivymd.uix.button import (
    MDRaisedButton,
    MDFloatingActionButton,
    MDRectangleFlatButton,
)
from kivy_projectile.app import M3ThemableBehavior


class BaseRaisedButton(M3ThemableBehavior, MDRaisedButton):
    """
    دکمه Raised با استایل M3
    """

    def __init__(self, **kwargs):
        # ۱. target props
        self.target_bg_prop = ["md_bg_color"]
        self.target_fg_prop = ["text_color"]

        # ۲. پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "primary")
        kwargs.setdefault("fg_token", "on_primary")

        # ۳. init اصلی
        super().__init__(**kwargs)


class BaseFlatButton(M3ThemableBehavior, MDRectangleFlatButton):
    """
    دکمه Flat (Outline/Rectangle) با استایل M3
    """

    def __init__(self, **kwargs):
        # ۱. target props
        self.target_bg_prop = ["md_bg_color"]
        self.target_fg_prop = ["text_color"]

        # ۲. پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "primary")

        # ۳. init اصلی
        super().__init__(**kwargs)


class BaseFAB(M3ThemableBehavior, MDFloatingActionButton):
    """
    دکمه شناور (FAB) با استایل M3
    """

    def __init__(self, **kwargs):
        # ۱. target props
        self.target_bg_prop = ["md_bg_color"]
        self.target_fg_prop = ["text_color"]

        # ۲. پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "secondary")
        kwargs.setdefault("fg_token", "on_secondary")

        # ۳. init اصلی
        super().__init__(**kwargs)
