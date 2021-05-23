from callable_base_classes import CallableBaseClass
from callable_mixins import ConditionallyAppliedMixin, CatchingExceptionsMixin, DispatchSetterMixin


class AtomicCallable(CallableBaseClass):
    def __init__(self, func, **kwargs):
        self.func = func
        super().__init__(**kwargs)

    def _apply_to_container(self, container):
        container.data = self.func(container.data)
        return container


class SideEffectCallable(AtomicCallable):
    def _apply_to_container(self, container):
        self.func(container)
        return container


class SideEffectHandler(ConditionallyAppliedMixin, SideEffectCallable):
    pass


class AtomicHandler(ConditionallyAppliedMixin, AtomicCallable):
    pass


class AtomicCatcher(CatchingExceptionsMixin, AtomicCallable):
    pass


class AtomicDispatchSetter(DispatchSetterMixin, AtomicCallable):
    pass


class DispatchSetter:
    def __init__(self, *, dispatch_key_func):
        self.dispatch_key_func = dispatch_key_func

    def __call__(self, container):
        container.set_dispatch(self.dispatch_key_func)
        return container
