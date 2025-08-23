# uix/textinput.py
from kivymd.uix.textfield import MDTextField
from kivy_projectile.app import M3ThemableBehavior


class BaseTextInput(M3ThemableBehavior, MDTextField):
    """
    TextInput سفارشی که توکن‌های رنگ Material 3 را به صورت خودکار اعمال می‌کند.
    """

    def __init__(self, **kwargs):
        # پیش‌فرض‌های تم
        kwargs.setdefault("bg_token", "surface")  # پس‌زمینه
        kwargs.setdefault("fg_token", "on_surface")  # رنگ متن
        kwargs.setdefault("outline_token", "outline")  # رنگ خط/بوردر
        super().__init__(**kwargs)
