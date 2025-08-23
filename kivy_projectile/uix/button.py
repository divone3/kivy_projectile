# uix/button.py
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton, MDRectangleFlatButton
from kivy_projectile.app import M3ThemableBehavior


class BaseRaisedButton(M3ThemableBehavior, MDRaisedButton):
    def __init__(self, **kwargs):
        # اگر کاربر توکن داده باشد نگه می‌داریم، در غیر این صورت مقدار پیش‌فرض
        bg_token = kwargs.pop("bg_token", "primary")
        fg_token = kwargs.pop("fg_token", "on_primary")
        super().__init__(bg_token=bg_token, fg_token=fg_token, **kwargs)
        self.apply_m3_theme()  # اعمال تم به محض ساخت دکمه

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
