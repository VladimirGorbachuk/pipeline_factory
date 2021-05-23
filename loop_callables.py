import warnings
from callable_base_classes import CallableBaseClass
from constants import StrictnessModesEnum


class CallableConditionalLooper(CallableBaseClass):
    def __init__(self, callable, *, break_func, **kwargs):
        self.callable = callable
        if self.callable._strictness_mode != StrictnessModesEnum.STRICT:
            warnings.warn("callable is not strict, loop can turn endless")
        self._break_func = break_func
        super().__init__(**kwargs)

    def _apply_to_container(self, container):
        raise NotImplemented

    def __call__(self, container):
        while not self._break_func(container):
            container = self.callable(container)
        return container
