from callable_base_classes import BaseCallableCollection
from exceptions import CannotDispatchError
from single_callables import AtomicCallable


class CallablesChain(BaseCallableCollection):
    @classmethod
    def from_funcs_list(cls, functions_list):
        list_of_callables = [AtomicCallable(func) for func in functions_list]
        return cls(*list_of_callables)

    def __init__(self, *callables, **kwargs):
        super().__init__(**kwargs)
        self._callables = callables

    def _apply_to_container(self, container):
        for callable in self._callables:
            container = callable(container)
        return container


class CallableDispatcher(BaseCallableCollection):
    def __init__(self, callables_dict, *, deafult=None, **kwargs):
        super().__init__(**kwargs)
        self._callables = list(callables_dict.values())
        self._callables_dict = callables_dict

    def _apply_to_container(self, container):
        dispatch_key = container.get_dispatch()

        if dispatch_key in self._callables_dict:
            callable = self._callables_dict[dispatch_key]
            container = callable(container)
            return container
        elif self._strictness_mode == StrictnessModesEnum.STRICT:
            raise CannotDispatchError
        else:
            container.add_exception(CannotDispatchError)
            return container
