from collections import defaultdict
from typing import Callable, Any, List


# def raw(val: str, suffix: str = "", index=0):
#     return val.split(";")[index].split()[-1].rstrip(suffix)


class GlobalStorage:
    __data = {
        # General
        "primary_color": "#FFFFFF",
        "secondary_color": "#323232",
        "placeholder_color": "#808080",
        "input_font-family": "Arial",
        "buttons_background-color": "#a9a9a9",

        # InputWidget
        "cursor_color": "#a9a9a9",
        "error_color": "#ff3333",
        "blank_color": "#bf9494",
        "input_font-size": "30px",
        "logo_font-size": "50px",
        "results_font-size": "20px"
    }

    __listeners = defaultdict(list)
    __stylesheet_styles = defaultdict(list)

    @classmethod
    def add_listener(cls, styles: List[str], callback: Callable):
        for attr in styles:
            if attr not in cls.__data:
                raise ValueError(f"No key: {attr} in __data")
            cls.__listeners[attr].append(callback)
        callback(*(cls.__data[attr] for attr in styles))

    @classmethod
    def add_stylesheet_listener(cls, obj, styles: List[str]):
        assert hasattr(obj, 'setStyleSheet')

        def update_attr(*values):
            style = " ".join([f"{name.partition('_')[2]}: {value};" for name, value in zip(styles, values)])
            getattr(obj, 'setStyleSheet')(style)

        cls.add_listener(styles, update_attr)

    @classmethod
    def add_dict_listener(cls, dct):
        styles = dct.keys()

        def update_attr(*values):
            for name, value in zip(styles, values):
                dct[name] = value

        cls.add_listener(styles, update_attr)

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
