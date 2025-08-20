# registry.py
from collections import defaultdict
from typing import List, Tuple, Type

class RelationRegistry:
    """
    ثبت روابط ForeignKey برای اینکه:
    - مدل مقصد بفهمه چه related_name هایی باید داشته باشه
    - هنگام delete والد، بتونیم رفتار on_delete رو اعمال کنیم
    ساختار هر relation:
      (from_model, field_name, to_model, related_name, field_obj)
    """
    def __init__(self):
        self._relations: List[Tuple[type, str, type, str, object]] = []
        self._by_to_model = defaultdict(list)

    def register(self, from_model: Type, field_name: str, to_model: Type, related_name: str, field_obj):
        entry = (from_model, field_name, to_model, related_name, field_obj)
        self._relations.append(entry)
        self._by_to_model[to_model].append(entry)
        return entry

    def incoming_for(self, model_cls: Type) -> List[Tuple[type, str, type, str, object]]:
        """روابطی که به model_cls اشاره می‌کنند."""
        return list(self._by_to_model.get(model_cls, []))

# singleton
relation_registry = RelationRegistry()
