# uix/label.py
from kivymd.uix.label import MDLabel
from kivy_projectile.app import M3ThemableBehavior


class BaseLabel(MDLabel, M3ThemableBehavior):

    def __init__(self, *args, **kwargs):
        self.theme_text_color = "Custom"

        self.target_fg_prop = ["text_color"]
        self.target_outline_prop = ["line_color"]

        super().__init__(*args, **kwargs)
