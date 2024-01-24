import copy
from contextlib import contextmanager


class BaseOptions:
    """Handle options (preferences) for the package.

    Raises:
        RuntimeError: _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

    _instance = None
    default_options = {}

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.options = copy.deepcopy(cls.default_options)
        return cls._instance

    def get(self, path):
        steps = path.split(".")

        d = self.options

        for step in steps:
            d = d[step]
        return d

    def set(self, path, value):
        *steps, last = path.split(".")

        d = self.options

        for step in steps:
            d = d.setdefault(step, {})
        d[last] = value

    def copy_from(self, options):
        self.options = copy.deepcopy(options)

    def reset(self, path=None):
        if path is None:
            return self.copy_from(self.default_options)

        steps = path.split(".")
        d = self.default_options
        for step in steps:
            d = d[step]
        self.set(path, d)

    def default_if_null(self, value, path):
        if value is not None:
            return value
        else:
            return self.get(path)

    @contextmanager
    def ctx(self, options):
        try:
            orig_options = copy.deepcopy(self.options)
            for k, v in options.items():
                self.set(k, v)
            yield self
        finally:
            self.options = orig_options
