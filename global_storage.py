from collections import defaultdict
from typing import Callable, Any


def raw(val: str, suffix: str = ""):
    return val.split()[-1].rstrip(suffix + ";")


class GlobalStorage:
    __data = dict(
        # General
        primary_color="color: #000000;",
        secondary_color="secondary_color: white;",
        placeholder_color="color: gray;",

        # InputWidget
        error_color="color: #ff3333;",
        blank_color="color: gray;",#"color: #ffa5a5;",
        input_font_size="font-size: 30px;",
    )
    __listeners = defaultdict(lambda: list())

    @classmethod
    def add_listener(cls, attr: str, callback: Callable[[Any], Any]):
        if attr not in cls.__data:
            raise ValueError(f"No key: {attr} in __data")
        cls.__listeners[attr].append(callback)
        callback(cls.__data[attr])

    @classmethod
    def remove_listener(cls, attr: str, callback: Callable[[Any], Any]):
        if attr not in cls.__data:
            raise ValueError(f"No key: {attr} in __data")
        cls.__listeners[attr].remove(callback)

    @classmethod
    def change(cls, attr, value):
        if attr not in cls.__data:
            raise ValueError(f"No key: {attr} in __data")
        cls.__data[attr] = value
        for callback in cls.__listeners[attr]:
            callback(value)

    @classmethod
    def get(cls, attr):
        return cls.__data[attr]
