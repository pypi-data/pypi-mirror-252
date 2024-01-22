from typing import Dict

from officialeye.diffobject.exception import DiffObjectException
from officialeye.error.errors.template import ErrTemplateInvalidFeatureClass
from officialeye.template.feature_class.feature_class import FeatureClass
from officialeye.template.feature_class.const import IMPLICIT_FEATURE_CLASS_BASE_INSTANCE_ID


class FeatureClassManager:

    def __init__(self, template_id: str, /):
        self.template_id = template_id
        self._classes: Dict[str, FeatureClass] = {
            IMPLICIT_FEATURE_CLASS_BASE_INSTANCE_ID: FeatureClass(self, IMPLICIT_FEATURE_CLASS_BASE_INSTANCE_ID, {
                "abstract": True
            })
        }

    def get_global_base_class(self) -> FeatureClass:
        return self._classes[IMPLICIT_FEATURE_CLASS_BASE_INSTANCE_ID]

    def get_class(self, class_id: str, /):
        assert class_id in self._classes
        return self._classes[class_id]

    def contains_class(self, class_id: str, /) -> bool:
        return class_id in self._classes

    def add_class(self, class_id: str, class_dict: Dict[str, any], /):
        assert class_id not in self._classes
        self._classes[class_id] = FeatureClass(self, class_id, class_dict)

    def inline_all_classes(self):

        try:
            for class_id in self._classes:
                self._classes[class_id].inline()
        except DiffObjectException as err:
            raise ErrTemplateInvalidFeatureClass(
                f"while loading feature classes of template '{self.template_id}'.",
                err.problem
            )
