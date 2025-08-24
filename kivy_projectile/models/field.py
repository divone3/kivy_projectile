from kivy import properties
from kivy.event import EventDispatcher

# -------------------------
# کلاس پایه فیلد
# -------------------------
class ModelField(properties.Property):
    def __init__(self, default=None, null=True, **kwargs):
        super().__init__(default,**kwargs)
        self.default = default
        self.null = null

    def validate(self, value):
        if value is None and not self.null:
            raise ValueError(f"{self.name} cannot be None")
        return value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        value = self.validate(value)
        old_value = instance.__dict__.get(self.name, self.default)
        instance.__dict__[self.name] = value

        # قطع اتصال قبلی اگر فیلد قبلی EventDispatcher بود
        if isinstance(old_value, EventDispatcher):
            old_value.unbind(on_change=lambda *a: None)

        # وصل اتصال جدید اگر EventDispatcher بود
        if isinstance(value, EventDispatcher):
            value.bind(on_change=lambda *a: instance.dispatch(f'on_{self.name}_change', value))

        if old_value != value:
            instance.dispatch(f'on_{self.name}_change', value)


# -------------------------
# فیلدهای پایه
# -------------------------
class IntegerField(ModelField):
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, int):
            raise TypeError(f"{self.name} must be int")
        return value

class StringField(ModelField):
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{self.name} must be str")
        return value

class BooleanField(ModelField):
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"{self.name} must be bool")
        return value

class FloatField(ModelField):
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, (float, int)):
            raise TypeError(f"{self.name} must be float")
        return float(value)


# -------------------------
# فیلدهای رابطه‌ای
# -------------------------
class RelationField(ModelField):
    """ پایه برای فیلدهای رابطه‌ای """
    def bind_related(self, instance, value):
        """ وصل تغییرات داخل objectهای مرتبط """
        if isinstance(value, EventDispatcher):
            value.bind(on_change=lambda *a: instance.dispatch(f'on_{self.name}_change', value))

    def unbind_related(self, value):
        if isinstance(value, EventDispatcher):
            value.unbind(on_change=lambda *a: None)


class ForeignKey(RelationField):
    def __init__(self, to, **kwargs):
        super().__init__(**kwargs)
        self.to = to

    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, EventDispatcher):
            raise TypeError(f"{self.name} must be an EventDispatcher instance")
        return value

    def __set__(self, instance, value):
        value = self.validate(value)
        old_value = instance.__dict__.get(self.name, self.default)

        self.unbind_related(old_value)
        instance.__dict__[self.name] = value
        self.bind_related(instance, value)

        if old_value != value:
            instance.dispatch(f'on_{self.name}_change', value)


class OneToManyField(RelationField):
    def __init__(self, to, **kwargs):
        super().__init__(default=[], **kwargs)
        self.to = to

    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, list):
            raise TypeError(f"{self.name} must be a list")
        for item in value:
            if not isinstance(item, EventDispatcher):
                raise TypeError(f"All items in {self.name} must be EventDispatcher instances")
        return value

    def __set__(self, instance, value):
        value = self.validate(value)
        old_value = instance.__dict__.get(self.name, self.default)

        for obj in old_value:
            self.unbind_related(obj)

        instance.__dict__[self.name] = value

        for obj in value:
            self.bind_related(instance, obj)

        if old_value != value:
            instance.dispatch(f'on_{self.name}_change', value)


class ManyToManyField(RelationField):
    def __init__(self, to, **kwargs):
        super().__init__(default=set(), **kwargs)
        self.to = to

    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, (set, list)):
            raise TypeError(f"{self.name} must be a set or list")
        for item in value:
            if not isinstance(item, EventDispatcher):
                raise TypeError(f"All items in {self.name} must be EventDispatcher instances")
        return set(value)

    def __set__(self, instance, value):
        value = self.validate(value)
        old_value = instance.__dict__.get(self.name, self.default)

        for obj in old_value:
            self.unbind_related(obj)

        instance.__dict__[self.name] = value

        for obj in value:
            self.bind_related(instance, obj)

        if old_value != value:
            instance.dispatch(f'on_{self.name}_change', value)
