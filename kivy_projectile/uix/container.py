# uix/container.py
import importlib.util
import os
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class BaseContainer(MDResponsiveLayout, MDScreen):
    """
    کانتینر پایه برای اپلیکیشن:
    - نگهداری state سراسری
    - بارگذاری اتوماتیک ویوهای mobile, tablet, desktop
    - رجیستر کردن ویجت‌ها در container.ids
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # خیلی مهم: container را همین ابتدا روی اپ ست کن تا هنگام ساخت view ها در دسترس باشد
        app = MDApp.get_running_app()
        app.container = self

        self.name = "container"
        self.state = {}
        self.responsive_view = {}
        self.ids = {}  # مثل ids در KV اما دستی

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
    # رجیستر/آنرجیستر
    # ----------------------
    def register_id(self, widget_id, widget):
        if widget_id:
            self.ids[widget_id] = widget

    def unregister_id(self, widget_id):
        self.ids.pop(widget_id, None)

    # رجیستر کل زیر‌درخت یک‌باره
    def _register_widget_tree(self, widget):
        wid = getattr(widget, "widget_id", None)
        if wid:
            self.register_id(wid, widget)
        # اگه بچه‌ها داشت، همه رو هم چک کن
        if hasattr(widget, "children"):
            for child in widget.children:
                self._register_widget_tree(child)

    # override: هر ویجتی به کانتینر اضافه شد، اتومات رجیسترش کن (خودش و بچه‌هاش)
    def add_widget(self, widget, index=0, canvas=None):
        res = super().add_widget(widget, index=index, canvas=canvas)
        self._register_widget_tree(widget)
        return res

    # ----------------------
    # بارگذاری ویوها
    # ----------------------
    def load_views(self):
        for device in ("mobile", "tablet", "desktop"):
            view_class = self._load_view_class(device)
            if view_class:
                # کانتینر را پاس بده (اختیاری، اگر می‌خواهی داخل ویو استفاده کنی)
                view_instance = view_class()
            else:
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
        spec.loader.exec_module(module)
        return getattr(module, "VIEW", None)
