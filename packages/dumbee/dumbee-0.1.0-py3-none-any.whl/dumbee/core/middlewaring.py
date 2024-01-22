import functools
import abc
import easytree
import typing


class Middleware(abc.ABC):
    """
    Abstract middleware class
    """

    def __init__(self, params: dict = None):
        self.params = easytree.dict(params if params is not None else {})

    def __call__(self, query, next):
        raise NotImplementedError


class Pipeline(Middleware):
    """
    Sequence of middlewares

    Note
    ----
    Middlewares are called in ordered: the first in
    the pipeline will be called before the second, etc.
    """

    def __init__(self, middlewares: typing.List[Middleware]):
        self.middlewares = middlewares

    def __call__(self, query, next):
        return self.wrap(next)(query)

    def wrap(self, func):
        """
        Wrap a function
        """
        return functools.reduce(
            lambda acc, func: lambda query: func(query, acc),
            reversed(self.middlewares),
            lambda query: func(query),
        )
