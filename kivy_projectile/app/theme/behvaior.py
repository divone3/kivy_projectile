# theme/behavior.py
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivymd.app import MDApp
from .theme import BaseTheme


class M3ThemableBehavior(EventDispatcher):
    """
    Behavior عمومی برای ویجت‌های M3
    """
    theme: BaseTheme = ObjectProperty(None, rebind = True)

    bg_token = StringProperty("surface")
    fg_token = StringProperty("on_surface")
    outline_token = StringProperty("outline")
    optional_token = StringProperty("primary")
    elevation = NumericProperty(0)

    # نام پراپرتی مقصد در ویجت
    target_bg_prop = ListProperty([])
    target_fg_prop = ListProperty([])
    target_outline_prop = ListProperty([])
    target_optional_prop = ListProperty([])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bind_theme()
        self.apply_theme()

    def _bind_theme(self):
        if self.theme is None:
            app = MDApp.get_running_app()
            if app and hasattr(app, "m3_theme"):
                self.theme = app.m3_theme
        if self.theme:
            self.theme.bind(tokens = lambda *a:self.apply_theme())

    def apply_theme(self, *args):
        if not self.theme:
            return

        try:
            bg = self.theme.get_rgba(self.bg_token)
            fg = self.theme.get_rgba(self.fg_token)
            outline = self.theme.get_rgba(self.outline_token)
            optional = self.theme.get_rgba(self.optional_token)
            if self.target_bg_prop:
                for target in self.target_bg_prop:
                    if hasattr(self, target):
                        setattr(self, target, bg)

            if self.target_fg_prop:
                for target in self.target_fg_prop:
                    if hasattr(self, target):
                        setattr(self, target, fg)

            if self.target_outline_prop:
                for target in  self.target_outline_prop:
                    if hasattr(self, target):
                        setattr(self, target, outline)
            if self.target_optional_prop:
                for target in self.target_optional_prop:
                    if hasattr(self, target):
                        setattr(self, target, optional)
        except Exception as e:
            print("Error applying theme:", e)
