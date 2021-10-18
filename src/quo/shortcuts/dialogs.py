import functools
from asyncio import get_event_loop
from typing import (
        Any, 
        Callable, 
        List,
        Optional, 
        Tuple, 
        TypeVar
        )

from quo.application import Suite
from quo.application.current import get_app
from quo.buffer import Buffer
from quo.completion import Completer
from quo.eventloop import run_in_executor_with_context
from quo.filters import FilterOrBool
from quo.text import Textual
from quo.keys.key_binding.bindings.focus import focus_next, focus_previous
from quo.keys.key_binding.defaults import load_key_bindings
from quo.keys import KeyBinder
from quo.keys.key_binding.key_bindings import merge_key_bindings
from quo.layout.layout import Layout
from quo.layout.containers import AnyContainer, HSplit
from quo.layout.dimension import Dimension as D
from quo.styles import BaseStyle
from quo.validation import Validator
from quo.widget import (
    Box,
    Button,
    CheckboxList,
    Dialog,
    Label,
    ProgressBar,
    RadioList,
    TextArea,
    ValidationToolbar,
)

__all__ = [
    "yes_no_dialog",
    "button",
    "evoke",
    "message",
    "radiolist_dialog",
    "checkbox",
    "progress",
]


def yes_no_dialog(
    title: Textual = "",
    text: Textual = "",
    yes: str = "Yes",
    no: str = "No",
    style: Optional[BaseStyle] = None,
) -> Suite[bool]:
    """
    Display a Yes/No dialog.
    This will return a boolean.
    """

    def yes_handler() -> None:
        get_app().exit(result=True)

    def no_handler() -> None:
        get_app().exit(result=False)

    dialog = Dialog(
        title=title,
        body=Label(text=text, dont_extend_height=True),
        buttons=[
            Button(text=yes, handler=yes_handler),
            Button(text=no, handler=no_handler),
        ],
        background=True,
    )

    return _create_app(dialog, style)


_T = TypeVar("_T")


def button(
    title: Textual = "",
    text: Textual = "",
    buttons: List[Tuple[str, _T]] = [],
    style: Optional[BaseStyle] = None,
) -> Suite[_T]:
    """
    Display a dialog with button choices (given as a list of tuples).
    Return the value associated with button.
    """

    def button_handler(v: _T) -> None:
        get_app().exit(result=v)

    dialog = Dialog(
        title=title,
        body=Label(text=text, dont_extend_height=True),
        buttons=[
            Button(text=t, handler=functools.partial(button_handler, v))
            for t, v in buttons
        ],
        background=True,
    )

    return _create_app(dialog, style)


def evoke(
    title: Textual = "",
    text: Textual = "",
    ok_text: str = "OK",
    cancel_text: str = "Cancel",
    completer: Optional[Completer] = None,
    validator: Optional[Validator] = None,
    password: FilterOrBool = False,
    style: Optional[BaseStyle] = None,
) -> Suite[str]:
    """
    Display a text input box.
    Return the given text, or None when cancelled.
    """

    def accept(buf: Buffer) -> bool:
        get_app().layout.focus(ok_button)
        return True  # Keep text.

    def ok_handler() -> None:
        get_app().exit(result=textfield.text)

    ok_button = Button(text=ok_text, handler=ok_handler)
    cancel_button = Button(text=cancel_text, handler=_return_none)

    textfield = TextArea(
        multiline=False,
        password=password,
        completer=completer,
        validator=validator,
        accept_handler=accept,
    )

    dialog = Dialog(
        title=title,
        body=HSplit(
            [
                Label(text=text, dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        ),
        buttons=[ok_button, cancel_button],
        background=True,
    )

    return _create_app(dialog, style)


def message(
    title: Textual = "",
    text: Textual = "",
    ok_text: str = "Ok",
    style: Optional[BaseStyle] = None,
) -> Suite[None]:
    """
    Display a simple message box and wait until the user presses enter.
    """
    dialog = Dialog(
        title=title,
        body=Label(text=text, dont_extend_height=True),
        buttons=[Button(text=ok_text, handler=_return_none)],
        background=True,
    )

    return _create_app(dialog, style)


def radiolist_dialog(
    title: Textual = "",
    text: Textual = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, Textual]]] = None,
    style: Optional[BaseStyle] = None,
) -> Suite[_T]:
    """
    Display a simple list of element the user can choose amongst.

    Only one element can be selected at a time using Arrow keys and Enter.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    if values is None:
        values = []

    def ok_handler() -> None:
        get_app().exit(result=radio_list.current_value)

    radio_list = RadioList(values)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=text, dont_extend_height=True), radio_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        background=True,
    )

    return _create_app(dialog, style)


def checkbox(
    title: Textual = "",
    text: Textual = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: Optional[List[Tuple[_T, Textual]]] = None,
    style: Optional[BaseStyle] = None,
) -> Suite[List[_T]]:
    """
    Display a simple list of element the user can choose multiple values amongst.

    Several elements can be selected at a time using Arrow keys and Enter.
    The focus can be moved between the list and the Ok/Cancel button with tab.
    """
    if values is None:
        values = []

    def ok_handler() -> None:
        get_app().exit(result=cb_list.current_values)

    cb_list = CheckboxList(values)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [Label(text=text, dont_extend_height=True), cb_list],
            padding=1,
        ),
        buttons=[
            Button(text=ok_text, handler=ok_handler),
            Button(text=cancel_text, handler=_return_none),
        ],
        background=True,
    )

    return _create_app(dialog, style)


def progress(
    title: Textual = "",
    text: Textual = "",
    run_callback: Callable[[Callable[[int], None], Callable[[str], None]], None] = (
        lambda *a: None
    ),
    style: Optional[BaseStyle] = None,
) -> Suite[None]:
    """
    :param run_callback: A function that receives as input a `set_percentage`
        function and it does the work.
    """
    loop = get_event_loop()
    progressbar = ProgressBar()
    text_area = TextArea(
        focusable=False,
        # Prefer this text area as big as possible, to avoid having a window
        # that keeps resizing when we add text to it.
        height=D(preferred=10 ** 10),
    )

    dialog = Dialog(
        body=HSplit(
            [
                Box(Label(text=text)),
                Box(text_area, padding=D.exact(1)),
                progressbar,
            ]
        ),
        title=title,

        background=True,
    )
    app = _create_app(dialog, style)

    def set_percentage(value: int) -> None:
        progressbar.percentage = int(value)
        app.invalidate()

    def log_text(text: str) -> None:
        loop.call_soon_threadsafe(text_area.buffer.insert_text, text)
        app.invalidate()

    # Run the callback in the executor. When done, set a return value for the
    # UI, so that it quits.
    def start() -> None:
        try:
            run_callback(set_percentage, log_text)
        finally:
            app.exit()

    def pre_run() -> None:
        run_in_executor_with_context(start)

    app.pre_run_callables.append(pre_run)

    return app


def _create_app(dialog: AnyContainer, style: Optional[BaseStyle]) -> Suite[Any]:
    # Key bindings.
    bindings = KeyBinder()
    bindings.add("tab")(focus_next)
    bindings.add("s-tab")(focus_previous)

    return Suite(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )


def _return_none() -> None:
    "Button handler that returns None."
    get_app().exit()
