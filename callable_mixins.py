import typing


class CatchingExceptionsMixin:
    def __init__(self, *args, exceptions_catched: typing.List = [], **kwargs):
        super().__init__(*args, **kwargs)
        self.exceptions_catched = exceptions_catched

    def __call__(self, container):
        if container.last_exception in self.exceptions_catched:
            container = super().__call__(container)
            container.remove_exception()
            return container
        else:
            return container


class ConditionallyAppliedMixin:
    def __init__(self, *args, check_if_appliable=lambda container: container.exceptions == [], exception_if_nonappliable=None, metadata_func_if_nonappliable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_if_appliable = check_if_appliable
        self.exception_if_nonappliable = exception_if_nonappliable
        self.metadata_func_if_nonappliable = metadata_func_if_nonappliable

    def __call__(self, container):
        if self.check_if_appliable(container):
            container = super().__call__(container)
        else:
            if self.exception_if_nonappliable:
                container.add_exception(self.exception_if_nonappliable)
            if self.metadata_func_if_nonappliable:
                container.update_metadata(self.metadata_func_if_nonappliable)
        return container


class DispatchSetterMixin:
    # most likely we don't want this as mixin'
    def __init__(self, *args, dispatch_setter_func=None, **kwargs):
        self._dispatch_setter_func = dispatch_setter_func
        super().__init__(*args, **kwargs)

    def __call__(self, container):
        super().__call__(container)
        if self._dispatch_setter_func:
            container.set_dispatch(self._dispatch_setter_func)
