# utils/with_id.py
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp


class WithID:
    widget_id = StringProperty(allownone = True)

    def __init__(self, widget_id = None, **kwargs):
        # اول اجازه بده کلاس‌های پایه مقداردهی شن
        super().__init__(**kwargs)
        if widget_id:
            self.widget_id = widget_id

        # ثبت با تاخیر یک فریم تا مطمئن باشیم app.container ست شده
        Clock.schedule_once(self._late_register, 0)

    def _late_register(self, *_):
        app = MDApp.get_running_app()
        container = getattr(app, "container", None)
        if container and self.widget_id:
            container.register_id(self.widget_id, self)
