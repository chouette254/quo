"""
Quo is a Python based Command Line toolkit for writing Command-Line Interface(CLI) applications. It improves programmer's productivity because it's easy to use and supports auto completion which means less time will be spent debugging. Simple to code, easy to learn, and does not come with needless baggage.

"""


import importlib
import os
import subprocess
from .application import Application
from .core import Arg
from .core import BaseCommand
from .core import Command
from .core import CommandCollection
from .core import Context
from .core import Tether
from .core import MultiCommand
from .core import App
from .core import Parameter
from .core import ShellDetectionFailure
from .text import ANSI, HTML
from quo.output import ColorDepth
from quo.shortcuts import button_dialog
from quo.shortcuts import message_dialog
from quo.shortcuts.utils import print_formatted_text
from quo.indicators import ProgressBar
from quo.shortcuts import Elicit
from quo.styles import Style
from quo.decorators import arg, command, tether, app
#from quo.decorators.decorate import arg
#from quo.decorators.decorate import command
#from quo.decorators import autoconfirm
#from quo.decorators.decorate import tether
#from quo.decorators import autohelp
#from quo.decorators.decorate import make_pass_decorator
#from quo.decorators.decorate import app
from quo.decorators import contextualize, objectualize, make_pass_decorator, autoversion, autopasswd, autohelp, autoconfirm
#from quo.decorators.decorate import contextualize
#from quo.decorators.decorate import objectualize
#from quo.decorators import autopasswd, autoversion
#from quo.decorators import autoversion
from quo.outliers import Abort, BadArgUsage, BadAppUsage, BadParameter, QuoException, FileError, MissingParameter, NoSuchApp, UsageError
from .setout import HelpFormatter
from .setout import wraptext
from quo.context.current import currentcontext
from .parser import AppParser
from quo.expediency import echo, appdir, formatfilename, get_os_args, get_text_stream, get_binary_stream, openfile
from quo.i_o import flair, confirm, launch, interpose, edit, terminalsize, pause, style, unstyle, prompt, clear
from quo.shortcuts import print_container
from quo.widgets import TextArea, Frame
from quo.shortcuts import elicit
from .types import BOOL, Choice, DateTime, File, FLOAT, FloatRange, INT, IntRange, ParamType, Path, STRING, Tuple, UNPROCESSED, UUID

__version__ = "2021.3"
