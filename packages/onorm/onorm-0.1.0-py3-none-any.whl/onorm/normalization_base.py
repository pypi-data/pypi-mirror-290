from abc import ABCMeta, abstractmethod


class Normalizer(metaclass=ABCMeta):
    """**Base class**

    This is the base class for all normalizers. They use a standard API.
    """

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def partial_fit(self, x):
        raise NotImplementedError

    @abstractmethod
    def transform(self, x):
        raise NotImplementedError

    def partial_fit_transform(self, x):
        self.partial_fit(x)
        return self.transform(x)
