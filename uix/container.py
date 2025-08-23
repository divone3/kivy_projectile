# uix/container.py
import importlib.util
import os
from pathlib import Path

from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class BaseContainer(MDResponsiveLayout, MDScreen):
    """
    کانتینر پایه برای اپلیکیشن:
    - نگهداری state سراسری
    - بارگذاری اتوماتیک ویوهای mobile, tablet, desktop
    """

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.name = "container"
        # state سراسری
        self.state = {}

        # dict ویوهای responsive
        self.responsive_view = {}

        # بارگذاری اتوماتیک
        self.load_views()
        self.clear_widgets()
        self.add_widget(self.mobile_view)

    # ----------------------
    # مدیریت state سراسری
    # ----------------------
    def set_state(self, key, value):
        self.state[key] = value

    def get_state(self, key, default=None):
        return self.state.get(key, default)

    # ----------------------
    # بارگذاری ویوها
    # ----------------------
    def load_views(self):
        for device in ("mobile", "tablet", "desktop"):
            view_class = self._load_view_class(device)
            if view_class:
                # ایجاد نمونه از کلاس ویو
                view_instance = view_class()
                self.responsive_view[device] = view_instance
            else:
                # fallback به یک MDBoxLayout نمونه‌سازی شده
                view_instance = MDBoxLayout()
                self.responsive_view[device] = view_instance

            setattr(self, f"{device}_view", view_instance)

    def _load_view_class(self, device_name):
        BASE_URL = MDApp.get_running_app().BASE_DIR
        ui_dir = os.path.join(BASE_URL, "ui", device_name)
        module_file = os.path.join(ui_dir, "__init__.py")

        if not os.path.exists(module_file):
            return None

        spec = importlib.util.spec_from_file_location(f"ui.{device_name}", module_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # فعال کردن این خط

        view_class = getattr(module, "VIEW", None)
        return view_class
    # ----------------------
    # اضافه کردن ویجت به صورت امن
    # ----------------------
    # def add_widget_safe(self, widget):
    #     super().add_widget(widget)
