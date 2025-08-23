# uix/button.py
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDRectangleFlatButton
from kivy_projectile.app import M3ThemableBehavior


class BaseRaisedButton(M3ThemableBehavior, MDRaisedButton):
    def __init__(self, **kwargs):
        # پیش‌فرض‌ها
        kwargs.setdefault("bg_token", "primary")  # پس‌زمینه
        kwargs.setdefault("fg_token", "on_primary")  # متن/آیکن
        super().__init__(**kwargs)


class BaseFlatButton(M3ThemableBehavior, MDRectangleFlatButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("bg_token", "surface")
        kwargs.setdefault("fg_token", "primary")
        super().__init__(**kwargs)


class BaseFAB(M3ThemableBehavior, MDFloatingActionButton):
    def __init__(self, **kwargs):
        kwargs.setdefault("bg_token", "secondary")
        kwargs.setdefault("fg_token", "on_secondary")
        super().__init__(**kwargs)
