# uix/button.py
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDRectangleFlatButton
from kivy_projectile.app import M3ThemableBehavior


class BaseRaisedButton(M3ThemableBehavior, MDRaisedButton):
    """دکمه M3 با استایل صحیح"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "md_bg_color"
        self.target_fg_prop = "text_color"


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
