""" english.py: English TitleCase class wrappers.

This is part of titlecase package.
"""

# pylint: disable=missing-function-docstring

from .maincase import a_titlecase
from .dictionaries.words import ENGLISH_US_WORDS

class EnglishStatic:
    """ English title-casing helper with built-in capitalization rules
    for common acronyms, brands, and product names.
    """
    WORDS = ENGLISH_US_WORDS

    @classmethod
    def callback(cls, word, **kwargs):
        return cls.WORDS.get(word.lower())

    @classmethod
    def convert(cls, text: str) -> str:
        return a_titlecase(text, callback=cls.callback)

    @classmethod
    def is_title_case(cls, text: str) -> bool:
        return text == cls.convert(text)

    @classmethod
    def fallback(cls, text: str) -> bool:
        """ This is nearly the same as Python native title(). """
        return a_titlecase(text)


class EnglishTitleCase:
    """ English TitleCase class. """
    DEFAULT_WORDS = EnglishStatic.WORDS

    def __init__(self, extra_words=None):
        self._counts = 0
        self.words = dict(self.DEFAULT_WORDS)
        if extra_words:
            self.words.update(extra_words)

    def callback(self, word, **kwargs):
        dude = self.words.get(word.lower())
        self._counts += int(dude is not None)
        return dude

    def convert(self, text):
        return a_titlecase(text, callback=self.callback)

    def titled(self, text):
        return a_titlecase(text)

    def num_conversions(self, reset=True):
        """ Just returns the number of conversions so far. """
        val = self._counts
        if reset:
            self._counts = 0
        return val
