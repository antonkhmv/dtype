from collections import defaultdict
from typing import Callable, Any, List


class StylesheetStorage:

    __data = {
        # General
        # "button_color": "#323232",
        "input_font-family": "Arial",
        "transparent_background-color": "rgba(0,0,0,0)",

        "button_background-color": "#a9a9a9",
        "primary_color": "white",
        "secondary_color": "#323232",
        "placeholder_color": "#808080",

        # InputWidget
        "cursor_color": "#a9a9a9",
        "error_color": "#ff3333",
        "blank_color": "#bf9494",

        "header_color": "#242424",
        "cell_color": "#2a2a2a",
        "stats_color": "#b0b0b0",

        # Immutable
        "input_font-size": "30px",

        "logo_font-size": "60px",
        "back_button_font-size": "40px",
        "button_font-size": "30px",
        "results_font-size": "20px",
        "stats_font-size": "20px",
        "radio_button_font-size": "16px",
    }

    __listeners = defaultdict(list)

    @classmethod
    def add_listener(cls, styles: List[str], callback: Callable):
        for attr in styles:
            if attr not in cls.__data:
                raise ValueError(f"No key: {attr} in __data")
            cls.__listeners[attr].append((callback, styles))
        callback(*(cls.__data[attr] for attr in styles))

    @classmethod
    def add_stylesheet_listener(cls, obj, styles: List[str]):
        assert hasattr(obj, 'setStyleSheet')

        def update_attr(*values):
            style = " ".join([f"{name.rpartition('_')[2]}: {value};" for name, value in zip(styles, values)])
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
    def change(cls, attr, value):
        if attr not in cls.__data:
            raise ValueError(f"No key: {attr} in __data")
        cls.__data[attr] = value
        for (callback, styles) in cls.__listeners[attr]:
            callback(*(cls.__data[attr] for attr in styles))

    @classmethod
    def get(cls, attr):
        return cls.__data[attr]
