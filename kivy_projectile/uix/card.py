from kivymd.uix.card import MDCard

from kivy_projectile.app import M3ThemableBehavior


class BaseCard(MDCard, M3ThemableBehavior):

    def __init__(self, *args, **kwargs):
        self.target_bg_prop = ["md_bg_color"]
        # self.target_fg_prop = []
        # self.target_outline_prop = []
        # self.target_optional_prop = []

        super().__init__(*args, **kwargs)