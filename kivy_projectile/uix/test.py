# theme/md_widgets.py
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFillRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.chip import MDChip
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.snackbar import MDSnackbar

from kivy_projectile.app import M3ThemableBehavior




class BaseFlatButton(M3ThemableBehavior, MDFlatButton):
    """دکمه تخت M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_fg_prop = "text_color"
        self.bg_token = "transparent"  # پس زمینه شفاف


class BaseIconButton(M3ThemableBehavior, MDIconButton):
    """دکمه آیکن M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_fg_prop = "icon_color"
        self.bg_token = "transparent"


class BaseCard(M3ThemableBehavior, MDCard):
    """کارت M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "md_bg_color"
        self.elevation = 1


class BaseTextField(M3ThemableBehavior, MDTextField):
    """فیلد متنی M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "background_color"
        self.target_fg_prop = "foreground_color"
        self.target_outline_prop = "line_color_normal"
        self.bg_token = "surface"
        self.fg_token = "on_surface"
        self.outline_token = "outline"


class BaseTopAppBar(M3ThemableBehavior, MDTopAppBar):
    """نوار بالا M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "md_bg_color"
        self.target_fg_prop = "specific_text_color"
        self.bg_token = "primary"
        self.fg_token = "on_primary"


class BaseListItem(M3ThemableBehavior, OneLineListItem):
    """آیتم لیست M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "bg_color"
        self.target_fg_prop = "text_color"
        self.bg_token = "surface"
        self.fg_token = "on_surface"


class BaseChip(M3ThemableBehavior, MDChip):
    """چیپ M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "md_bg_color"
        self.target_fg_prop = "text_color"
        self.bg_token = "secondary_container"
        self.fg_token = "on_secondary_container"


class BaseCheckbox(M3ThemableBehavior, MDCheckbox):
    """چک‌باکس M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_fg_prop = "color"
        self.fg_token = "primary"


class BaseSwitch(M3ThemableBehavior, MDSwitch):
    """سوئیچ M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # سوئیچ نیاز به تنظیمات خاص دارد


class BaseProgressBar(M3ThemableBehavior, MDProgressBar):
    """نوار پیشرفت M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "color"
        self.bg_token = "primary"


class BaseSnackbar(M3ThemableBehavior, MDSnackbar):
    """اسنک‌بار M3"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_bg_prop = "bg_color"
        self.target_fg_prop = "text_color"
        self.bg_token = "inverse_surface"
        self.fg_token = "inverse_on_surface"