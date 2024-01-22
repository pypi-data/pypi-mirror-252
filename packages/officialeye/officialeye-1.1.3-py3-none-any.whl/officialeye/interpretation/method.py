import abc
from typing import Dict

# noinspection PyPackageRequirements
import cv2

from officialeye.context.context import Context
from officialeye.interpretation.serializable import Serializable
from officialeye.interpretation.config import InterpretationMethodConfig


class InterpretationMethod(abc.ABC):

    def __init__(self, context: Context, method_id: str, config_dict: Dict[str, any], /):
        super().__init__()

        self.method_id = method_id

        self._config = InterpretationMethodConfig(config_dict, method_id)
        self._context = context

    def get_config(self) -> InterpretationMethodConfig:
        return self._config

    @abc.abstractmethod
    def interpret(self, feature_img: cv2.Mat, feature_id: str, /) -> Serializable:
        raise NotImplementedError()
