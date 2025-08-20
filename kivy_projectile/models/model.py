from kivy.event import EventDispatcher
from .field import ModelField
# -------------------------
# کلاس پایه مدل
# -------------------------
class BaseModel(EventDispatcher):
    def __init__(self, **kwargs):
        super().__init__()

        # ثبت همه فیلدها و تعریف رویدادها
        self._fields = {}
        for attr_name, attr_value in self.__class__.__dict__.items():
            if isinstance(attr_value, ModelField):
                self._fields[attr_name] = attr_value
                # ثبت رویداد تغییر فیلد
                self.register_event_type(f'on_{attr_name}_change')

                # مقدار اولیه از kwargs یا مقدار پیش‌فرض فیلد
                initial_value = kwargs.get(attr_name, attr_value.default)
                setattr(self, attr_name, initial_value)

    def to_dict(self):
        """ تبدیل مدل به دیکشنری ساده """
        data = {}
        for name, field in self._fields.items():
            value = getattr(self, name)
            if isinstance(value, BaseModel):
                data[name] = value.to_dict()
            elif isinstance(value, (list, set)):
                data[name] = [v.to_dict() if isinstance(v, BaseModel) else v for v in value]
            else:
                data[name] = value
        return data

    def __repr__(self):
        field_values = ", ".join(f"{name}={getattr(self, name)!r}" for name in self._fields)
        return f"<{self.__class__.__name__} {field_values}>"