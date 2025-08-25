from kivymd.uix.bottomnavigation import MDBottomNavigation

from kivy_projectile.app import M3ThemableBehavior


class BaseBottomNavigation(M3ThemableBehavior, MDBottomNavigation):

    def __init__(self, *args, **kwargs):
        self.target_bg_prop = ["panel_color"]
        self.target_fg_prop = ["text_color_normal"]
        self.target_outline_prop = ["selected_color_background"]
        self.target_optional_prop = ["text_color_active"]
        super().__init__(*args, **kwargs)