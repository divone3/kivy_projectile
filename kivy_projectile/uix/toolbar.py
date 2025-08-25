from kivymd.uix.toolbar import MDTopAppBar

from kivy_projectile.app import M3ThemableBehavior


class BaseTopAppBar(M3ThemableBehavior, MDTopAppBar):

    def __init__(self, *args, **kwargs):
        self.target_bg_prop = ["md_bg_color"]
        self.target_fg_prop = ["headline_text_color", "specific_text_color"]
        self.target_outline_prop = ["line_color"]

        super().__init__(*args, **kwargs)