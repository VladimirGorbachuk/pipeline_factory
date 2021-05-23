from abc import ABC, abstractmethod
from constants import StrictnessModesEnum
import typing


class CallableBaseClass(ABC):
    def __init__(
            self,
            *args,
            strictness_mode=StrictnessModesEnum.NONSTRICT,
            metadata_func: typing.Callable = (lambda container: {})):

        self._strictness_mode = strictness_mode
        self.metadata_func = metadata_func

    def __call__(self, container):
        try:
            container = self._apply_to_container(container)
            container.update_metadata(self.metadata_func)
        except Exception as e:
            if self._strictness_mode == StrictnessModesEnum.STRICT:
                raise e
            else:
                container.add_exception(e)
        return container

    @abstractmethod
    def _apply_to_container(self, container):
        pass

    def set_strictness_level(self,
                             strictness_level: StrictnessModesEnum):
        self._strictness_mode = strictness_level


class BaseCallableCollection(CallableBaseClass):
    def set_strictness_level(self, strictness_level: StrictnessModesEnum):
        super().set_strictness_level(strictness_level)
        for callable in self._callables_list:
            callable.set_strictness_level(strictness_level)
