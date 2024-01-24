import logging
import os
from configparser import ConfigParser, SectionProxy
from importlib import import_module
from inspect import isabstract, isclass
from pathlib import Path
from pkgutil import iter_modules

class TestClass:
    def __init__(self, a) -> None:
        self.a = a
