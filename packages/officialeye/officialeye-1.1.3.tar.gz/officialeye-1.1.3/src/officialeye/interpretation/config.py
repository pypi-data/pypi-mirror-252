from typing import Dict

from officialeye.config.config import Config
from officialeye.error.errors.template import ErrTemplateInvalidInterpretation


class InterpretationMethodConfig(Config):

    def __init__(self, config_dict: Dict[str, any], interpretation_method: str, /):

        super().__init__(config_dict)

        self._interpretation_method = interpretation_method

    def _get_invalid_key_error(self, key: str, /):

        return ErrTemplateInvalidInterpretation(
            f"while reading configuration of the '{self._interpretation_method}' interpretation method.",
            f"Could not find a value for key '{key}'."
        )
