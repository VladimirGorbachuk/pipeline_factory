class DataContainer:
    def __init__(self, data, *, wayback_mode=False, dispatch_key=None):
        self.data = data
        self.metadata = {}
        self.exceptions = []
        self._dispatch_key = dispatch_key
        self.wayback_mode = wayback_mode
        if self.wayback_mode:
            self._counter = 0
        else:
            self._counter = None

    def update_metadata(self, update_func):
        new_metadata = update_func(self)
        if self.wayback_mode:
            self.metadata[self._counter] = {
                "data": self.data, "metadata_upd": new_metadata}
            self._counter += 1
        else:
            self.metadata.update(new_metadata)

    def add_exception(self, exception):
        self.exceptions.append(exception)

    def get_dispatch(self):
        key = self._dispatch_key
        self._dispatch_key = None
        return key

    def set_dispatch(self, dispatch_setter_func):
        key = dispatch_setter_func(self)
        self._dispatch_key = key
