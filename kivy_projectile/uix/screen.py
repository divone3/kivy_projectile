# uix/screen.py
import importlib
import inspect
import os
from typing import Union, Type
from kivymd.uix.screen import MDScreen


class BaseScreen(MDScreen):
    """
    اسکرین پایه که به‌صورت خودکار Layout متناظر را بارگذاری می‌کند.

    پشتیبانی‌ها:
      - فایل «layout.py» کنار screen.py
      - پوشه «layout/» با __init__.py کنار screen.py (می‌تواند چند فایل داخلی داشته باشد)
      - مشخص‌کردن صریح کلاس Layout:
          * layout_class_name = SomeLayoutClass  (کلاس)
          * layout_class_name = "SomeLayoutClass" (نام رشته‌ای؛ داخل ماژول/پکیج layout جست‌وجو می‌شود)
      - نام پیش‌فرض کلاس Layout از نام فولدر اسکرین مشتق می‌شود (foo_bar → FooBarLayout)
      - اگر نام پیش‌فرض پیدا نشد، اولین کلاسی که با «Layout» تمام می‌شود استفاده می‌گردد.
    """

    # می‌تواند None، یا یک نام کلاس (str)، یا خود کلاس (type) باشد
    layout_class_name: Union[None, str, Type] = None

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_layout()

    # -------------------------
    # API قابل override توسط فرزند
    # -------------------------
    def get_layout_kwargs(self) -> dict:
        """آرگومان‌هایی که هنگام ساخت Layout پاس داده می‌شود."""
        return {}

    # -------------------------
    # پیاده‌سازی داخلی
    # -------------------------
    def _screen_module(self):
        """ماژول پایتونیِ کلاس فرزند را برمی‌گرداند."""
        return importlib.import_module(self.__class__.__module__)

    def _compute_default_layout_class_name(self) -> str:
        """نام پیش‌فرض کلاس Layout را از نام فولدر اسکرین می‌سازد (foo_bar -> FooBarLayout)."""
        module = self._screen_module()
        screen_dir = os.path.dirname(inspect.getfile(module))
        folder_name = os.path.basename(screen_dir)
        return ''.join(part.capitalize() for part in folder_name.split('_')) + 'Layout'

    def _import_layout_module(self):
        """تلاش می‌کند «.layout» هم‌پکیج با اسکرین را ایمپورت کند (چه فایل، چه پوشه)."""
        module = self._screen_module()
        pkg = getattr(module, '__package__', None)
        if not pkg:
            return None
        try:
            return importlib.import_module(f"{pkg}.layout")
        except ModuleNotFoundError:
            return None

    def _resolve_layout_class(self):
        """
        کلاس Layout را پیدا می‌کند بر اساس اولویت:
          1) اگر layout_class_name یک کلاس باشد، همان
          2) اگر layout_class_name نام (str) باشد، در ماژول/پکیج layout آن را برمی‌دارد
          3) نام پیش‌فرض از فولدر (FooBarLayout)
          4) fallback: اولین کلاس public که با «Layout» تمام می‌شود
        """
        # 1) کلاس داده‌شده به‌صورت مستقیم
        if isinstance(self.layout_class_name, type):
            return self.layout_class_name

        layout_module = self._import_layout_module()
        if not layout_module:
            return None

        # 2) نام مشخص‌شده (str)
        if isinstance(self.layout_class_name, str) and self.layout_class_name:
            if hasattr(layout_module, self.layout_class_name):
                return getattr(layout_module, self.layout_class_name)
            # اگر نبود، می‌ریم سراغ fallbackها

        # 3) نام پیش‌فرض از فولدر
        default_name = self._compute_default_layout_class_name()
        if hasattr(layout_module, default_name):
            return getattr(layout_module, default_name)

        # 4) fallback: اولین کلاس که با Layout تمام می‌شود
        export_names = getattr(layout_module, '__all__', None)
        candidates = export_names if export_names else dir(layout_module)
        for attr in candidates:
            if not attr or not attr.endswith('Layout'):
                continue
            try:
                obj = getattr(layout_module, attr)
            except Exception:
                continue
            if isinstance(obj, type):
                return obj

        return None

    def load_layout(self):
        layout_cls = self._resolve_layout_class()
        if not layout_cls:
            # اگر Layout پیدا نشد، سکوت می‌کنیم تا اسکرین‌هایی که Layout ندارند هم قابل استفاده باشند
            return
        self.layout = layout_cls(**self.get_layout_kwargs())
        self.add_widget(self.layout)
