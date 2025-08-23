# library/app/app.py
import os
import sys
from pathlib import Path
from importlib import import_module

from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy_projectile.app import BaseTheme

class BaseApp(MDApp):
    """
    اپ پایه:
    - ابتدا settings.py را می‌خواند
    - BASE_DIR و base_url را از settings استخراج می‌کند
    - سپس کانتینر اصلی UI را بارگذاری می‌کند
    - در صورت عدم موفقیت، fallback یک MDWidget خالی نمایش داده می‌شود
    - Theme Material3 (BaseTheme) ایجاد و در دسترس ویجت‌ها قرار می‌دهد
    """

    container_class_name = "AppContainer"  # نام کلاس کانتینر داخل container.py
    container_module_name = "container"  # نام فایل کانتینر
    ui_folder_name = "ui"  # مسیر پوشه ui
    core_folder_name = "core"  # مسیر پوشه core

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BASE_DIR = None
        self.base_url = None
        self.settings_module = None
        self.dynamic_config = None

        # ---------- Theme ----------
        self.theme = BaseTheme(
            source_primary="#6750A4",
            source_secondary="#625B71",
            source_tertiary="#7D5260",
            source_error="#B3261E",
            mode="light"
        )

        self._load_settings()
        self.load_config()

    # -----------------------------
    def _load_settings(self):
        project_root = Path(__file__).resolve().parent.parent.parent  # library/app/ -> Project/
        core_path = project_root / "android" / "core"

        if str(core_path) not in sys.path:
            sys.path.insert(0, str(core_path))

        try:
            self.settings_module = import_module("settings")
            self.BASE_DIR = getattr(self.settings_module, "BASE_DIR", project_root)
            allowed_hosts = getattr(self.settings_module, "ALLOWED_HOST", [None])
            self.base_url = allowed_hosts[0] if allowed_hosts else None
        except ModuleNotFoundError:
            print(f"settings.py not found in {core_path}")
            self.BASE_DIR = project_root
            self.base_url = None

    # -----------------------------
    def build(self):
        container_cls = self._load_container_class()
        if container_cls:
            self.container = container_cls()
        else:
            self.container = MDWidget()
        return self.container

    # -----------------------------
    def _load_container_class(self):
        project_path = Path(self.BASE_DIR) if self.BASE_DIR else Path(os.getcwd())
        ui_path = project_path / self.ui_folder_name

        if not ui_path.is_dir():
            print(f"UI folder not found: {ui_path}")
            return None

        if str(ui_path) not in sys.path:
            sys.path.insert(0, str(ui_path))

        try:
            module = import_module(self.container_module_name)
            container_cls = getattr(module, self.container_class_name)
            return container_cls
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error loading container: {e}")
            return None

    # -----------------------------
    def load_config(self):
        app_dir = Path(self.BASE_DIR) / self.core_folder_name
        config_path = app_dir / "config.py"

        if config_path.exists():
            if str(app_dir) not in sys.path:
                sys.path.insert(0, str(app_dir))
            try:
                spec = import_module("config")
                self.dynamic_config = getattr(spec, "config", spec)
            except Exception as e:
                print(f"Error loading config.py: {e}")
                class AppConfig:
                    pass
                self.dynamic_config = AppConfig()
        else:
            class AppConfig:
                pass
            self.dynamic_config = AppConfig()

    # -----------------------------
    # متدهای کمکی برای Theme
    def switch_theme_mode(self, mode: str):
        """سوییچ بین light و dark"""
        self.theme.switch_mode(mode)

    def update_theme_colors(self, **kwargs):
        """به روزرسانی رنگ‌های اصلی (primary, secondary, etc.)"""
        self.theme.update_sources(**kwargs)
