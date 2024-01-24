import itertools


class Bunch(dict):
    """Dictionary whose elements can be accessed as object attributes."""

    def __init__(self, *args, **kwargs):
        """Same constructor of dict type."""
        if args == (None,) and not kwargs:
            super().__init__()
        else:
            super().__init__(*args, **kwargs)

    def __reduce__(self):
        """If serializing, we convert the object to a dictionary.

        Returns:
            _type_:
        """
        return self.__class__, (dict(self),)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    @classmethod
    def deep(cls, d):
        """Deep-conversion of a dictionary to a Bunch.

        Args:
            d (_type_): dict object to convert.

        Returns:
            _type_: Bunch object.
        """
        if isinstance(d, Bunch):
            return d
        elif not isinstance(d, dict):
            return d
        else:
            return Bunch({k: Bunch.deep(v) for k, v in d.items()})

    def cartesian_product(self):
        """Cartesian product of arguments.

        Yields:
            _type_: Iterator returning dictionaries of each possible combination.
        """
        for instance in itertools.product(*self.values()):
            yield dict(zip(self.keys(), instance))
