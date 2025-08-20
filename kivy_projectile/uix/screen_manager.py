import importlib
from typing import Any, Dict, Mapping, MutableMapping, Optional, Type, Union

from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import Screen


ScreenCls = Type[Screen]
PatternValue = Union[str, ScreenCls, Mapping[str, Any]]


class BaseScreenManager(MDScreenManager):
    """
    ScreenManager پایه که اسکرین‌ها را طبق الگوی تعریف‌شده در پکیج «screens» کنار فایل منیجر بارگذاری می‌کند.

    ویژگی‌ها:
      - پشتیبانی از تعریف پترن با **کلاس مستقیم** (ترجیح‌شده):

            # android/screens/__init__.py
            from .splash.screen import SplashScreen
            from .login.screen import LoginScreen
            from .home.screen import HomeScreen

            __all__ = ["SplashScreen", "LoginScreen", "HomeScreen"]

            SCREEN_PATTERNS = {
                "splash_screen": SplashScreen,
                "login_screen": LoginScreen,
                "home_screen": HomeScreen,
            }

      - سازگاری عقب‌رو با ساختار قدیمی:
            SCREEN_PATTERNS = {
                "splash_screen": {"path": "screens.SplashScreen", "kwargs": {"foo": 1}},
                "login_screen":  "screens.LoginScreen",   # رشته مسیر نقطه‌دار
            }
        در این حالت، «kwargs» قدیمی **اختیاری** است و در کنار خروجیِ
        `get_shared_kwargs(screen_name)` ادغام می‌شود (ارجحیت با `get_shared_kwargs`).

      - Lazy loading: اگر `lazy=True` باشد، اسکرین‌ها فقط هنگام اولین سوییچ ساخته می‌شوند.
      - بدون تداخل برای چند ScreenManager (هر منیجر اسکرین‌های خودش را مدیریت می‌کند).

    طرز کار:
      - ماژول screens هم‌پکیج با کلاس منیجر ایمپورت می‌شود (مثلاً `android.manager` → `android.screens`).
      - از روی `SCREEN_PATTERNS` کلاس/مسیر هر اسکرین استخراج و نمونه ساخته می‌شود.
    """

    screens_module_name: str = "screens"

    def __init__(self, lazy: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._lazy: bool = lazy
        self._screens_module = self._import_screens_module()
        self._patterns: Dict[str, PatternValue] = self._load_patterns(self._screens_module)

        if not self._lazy:
            self.preload_all_screens()

    # -------------------------
    # API قابل override توسط فرزند
    # -------------------------
    def get_shared_kwargs(self, screen_name: str) -> Dict[str, Any]:
        """پارامترهای مشترک برای ساخت اسکرین. در کلاس فرزند override کنید."""
        return {}

    # -------------------------
    # بارگذاری الگوها / ماژول‌ها
    # -------------------------
    def _import_screens_module(self):
        manager_module = importlib.import_module(self.__class__.__module__)
        pkg = getattr(manager_module, "screens", None)
        if not pkg:
            # اگر ماژول پکیج نداشت، از نام ماژول استفاده می‌کنیم و پکیج والد را جدا می‌کنیم
            pkg = self.__class__.__module__.rpartition(".")[0]
            if not pkg:
                raise ImportError(
                    f"Cannot resolve package for {self.__class__.__module__}; put your manager inside a package."
                )
        screens_module_path = f"{pkg}.{self.screens_module_name}"
        try:
            return importlib.import_module(screens_module_path)
        except ModuleNotFoundError as e:
            raise ImportError(
                f"Could not import screens module '{screens_module_path}'. Make sure there's a package with __init__.py."
            ) from e

    def _load_patterns(self, screens_module) -> Dict[str, PatternValue]:
        if not hasattr(screens_module, "SCREEN_PATTERNS"):
            raise ImportError(
                f"{screens_module.__name__} must define SCREEN_PATTERNS (dict of name -> class or path)."
            )
        patterns = getattr(screens_module, "SCREEN_PATTERNS")
        if not isinstance(patterns, MutableMapping):
            raise TypeError("SCREEN_PATTERNS must be a dict-like mapping.")
        return dict(patterns)

    # -------------------------
    # Utils
    # -------------------------
    def _resolve_class_from_str(self, dotted: str, default_module=None) -> ScreenCls:
        """مسیر نقطه‌دار را به کلاس تبدیل می‌کند. اگر نقطه نداشت، از ماژول پیش‌فرض برداشته می‌شود."""
        if "." in dotted:
            mod_path, cls_name = dotted.rsplit(".", 1)
            mod = importlib.import_module(mod_path)
            try:
                return getattr(mod, cls_name)
            except AttributeError as e:
                raise ImportError(f"Class '{cls_name}' not found in '{mod_path}'.") from e
        else:
            mod = default_module or self._screens_module
            try:
                return getattr(mod, dotted)
            except AttributeError as e:
                raise ImportError(f"Class '{dotted}' not found in module '{mod.__name__}'.") from e

    def _coerce_to_class(self, screen_name: str, value: PatternValue) -> ScreenCls:
        """ورودی پترن را به کلاس اسکرین تبدیل می‌کند (type)."""
        # dict سبک قدیمی
        if isinstance(value, Mapping):
            if "class" in value:
                return value["class"]  # type: ignore[index]
            if "path" in value:
                return self._resolve_class_from_str(str(value["path"]))
            raise ValueError(
                f"Pattern for '{screen_name}' must contain 'class' or 'path' when using dict style."
            )
        # رشته مسیر
        if isinstance(value, str):
            return self._resolve_class_from_str(value, default_module=self._screens_module)
        # کلاس مستقیم
        if isinstance(value, type):
            return value  # type: ignore[return-value]
        raise TypeError(
            f"Unsupported pattern type for '{screen_name}': {type(value).__name__}. Expected str, class, or dict."
        )

    def _extract_legacy_kwargs(self, value: PatternValue) -> Dict[str, Any]:
        """kwargs قدیمی داخل dict را برمی‌گرداند (برای سازگاری)."""
        if isinstance(value, Mapping):
            kw = value.get("kwargs")
            return dict(kw) if isinstance(kw, Mapping) else {}
        return {}

    # -------------------------
    # ساخت و افزودن اسکرین
    # -------------------------
    def _create_screen(self, screen_name: str, value: PatternValue) -> Screen:
        screen_cls = self._coerce_to_class(screen_name, value)

        # kwargs: legacy + shared
        legacy_kwargs = self._extract_legacy_kwargs(value)
        shared_kwargs = self.get_shared_kwargs(screen_name) or {}
        kwargs: Dict[str, Any] = {**legacy_kwargs, **shared_kwargs}

        # همیشه نام اسکرین را تنظیم می‌کنیم
        if "name" not in kwargs:
            kwargs["name"] = screen_name

        try:
            instance = screen_cls(**kwargs)
        except TypeError as e:
            # پیام خطا را خواناتر می‌کنیم
            raise TypeError(
                f"Failed to instantiate '{screen_cls.__name__}' for screen '{screen_name}' with kwargs={kwargs}.\n"
                f"Original error: {e}"
            ) from e
        return instance

    def _add_screen_if_absent(self, screen_name: str):
        if self.has_screen(screen_name):
            return
        if screen_name not in self._patterns:
            raise ValueError(f"Screen '{screen_name}' not found in SCREEN_PATTERNS.")
        value = self._patterns[screen_name]
        screen = self._create_screen(screen_name, value)
        # snake-case نام را به‌عنوان اتریبیوت هم قرار می‌دهیم تا دسترسی مستقیم ممکن باشد
        try:
            setattr(self, screen_name, screen)
        except Exception:
            # اگر نام نامعتبرِ اتریبیوت بود، صرف‌نظر می‌کنیم
            pass
        self.add_widget(screen)

    # -------------------------
    # API عمومی
    # -------------------------
    def preload_all_screens(self) -> None:
        for name in self._patterns.keys():
            self._add_screen_if_absent(name)

    def ensure_loaded(self, screen_name: str) -> None:
        self._add_screen_if_absent(screen_name)

    def switch_to(self, screen_name: str, **kwargs) -> None:  # type: ignore[override]
        if self._lazy and not self.has_screen(screen_name):
            self._add_screen_if_absent(screen_name)
        if not self.has_screen(screen_name):
            raise ValueError(f"Screen '{screen_name}' is not loaded and not present in patterns.")
        self.current = screen_name

    def list_known_screens(self):
        return list(self._patterns.keys())


# -------------------------
# نمونه استفاده (راهنمای سریع)
# -------------------------
#
# android/manager.py
# from kivymd.app import MDApp
# from .base_manager import BaseScreenManager
#
# class MainScreenManager(BaseScreenManager):
#     def get_shared_kwargs(self, screen_name: str):
#         # هر پارامتر مشترکی را که می‌خواهید به Layout/Screen پاس دهید برگردانید
#         return {"app": MDApp.get_running_app()}
#
# # android/screens/__init__.py
# from .splash.screen import SplashScreen
# from .login.screen import LoginScreen
# from .home.screen import HomeScreen
#
# __all__ = ["SplashScreen", "LoginScreen", "HomeScreen"]
#
# SCREEN_PATTERNS = {
#     "splash_screen": SplashScreen,
#     "login_screen": LoginScreen,
#     "home_screen": HomeScreen,
# }
#
# - اگر از ساختار قدیمی استفاده می‌کنید (path/kwargs)، همان‌طور که هست کار می‌کند.
# - برای Lazy Loading: MainScreenManager(lazy=True)
