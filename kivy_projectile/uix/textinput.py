from kivymd.uix.textfield import MDTextField
from kivy_projectile.app import M3ThemableBehavior


class BaseTextInput(M3ThemableBehavior, MDTextField):
    def __init__(self, *args, **kwargs):

        # تنظیم پراپرتی‌های هدف برای ارث‌بری رنگ‌ها
        self.target_bg_prop = ["text_color_normal", "line_color_normal"]
        self.target_fg_prop = ["text_color_focus", "line_color_focus"]

        super().__init__(*args, **kwargs)
