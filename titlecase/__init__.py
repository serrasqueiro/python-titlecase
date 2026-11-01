# -*- coding: utf-8 -*-

""" Python titlecase
Original Perl version by: John Gruber http://daringfireball.net/ 10 May 2008
Python version by Stuart Colville http://muffinresearch.co.uk
License: http://www.opensource.org/licenses/mit-license.php
"""

from .maincase import titlecase
from .english import EnglishStatic, EnglishTitleCase
from .wordlists import cmd

__version__ = '3.4.2'

__all__ = [
    "titlecase",
    "EnglishTitleCase",
    "EnglishStatic",
    "cmd",
]
