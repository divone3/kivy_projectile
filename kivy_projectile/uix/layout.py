# uix/layout.py
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy_projectile.app import M3ThemableBehavior


class BaseBoxLayout(MDBoxLayout, M3ThemableBehavior):
    def __init__(self, *args, **kwargs):
        self.target_bg_prop = ["md_bg_color"]

        super().__init__(*args, **kwargs)



class BaseGridLayout(MDGridLayout, M3ThemableBehavior):
    def __init__(self, *args, **kwargs):
        self.target_bg_prop = ["md_bg_color"]

        super().__init__(*args, **kwargs)


class BaseFloatLayout(MDFloatLayout, M3ThemableBehavior):
    def __init__(self, *args, **kwargs):

        self.target_bg_prop = ["md_bg_color"]
        super().__init__(*args, **kwargs)
