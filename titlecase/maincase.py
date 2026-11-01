""" maincase -- formerly titlecase() function
"""

import string
from .expressions import SMALL, SMALL_WORDS, SMALL_FIRST, SMALL_LAST, \
     MR_MRS_MS_DR, CAPFIRST, \
     UC_ELSEWHERE, UC_INITIALS, \
     APOS_SECOND, \
     MAC_MC, \
     INLINE_PERIOD, \
     SUBPHRASE, \
     PUNCT

try:
    import regex
except ImportError:
    import re as regex

# pylint: disable=unnecessary-pass, too-few-public-methods, consider-using-f-string


class Immutable:
    """ Immutable object. """
    def gettable(self):
        """ Dummy get. """
        return True

class ImmutableString(str, Immutable):
    """ Immutable string object. """
    pass

class ImmutableBytes(bytes, Immutable):
    """ Immutable bytes stuff. """
    pass


def _mark_immutable(text):
    if isinstance(text, bytes):
        return ImmutableBytes(text)
    return ImmutableString(text)


def titlecase(
    text,
    callback=None,
    small_first_last=True,
    preserve_blank_lines=False,
    normalise_space_characters=False,
    ):
    """ TitleCase conversion result consistency checking. """
    res = a_titlecase(
        text,
        callback,
        small_first_last,
        preserve_blank_lines,
        normalise_space_characters,
    )
    assert isinstance(res, str), "titlecase(): Not a string"
    return res


def a_titlecase(
    text,
    callback=None,
    small_first_last=True,
    preserve_blank_lines=False,
    normalise_space_characters=False,
    ):
    """ TitleCase conversion without checks. """
    return maincase(
        text,
        callback,
        small_first_last,
        preserve_blank_lines,
        normalise_space_characters,
    )


def maincase(text, callback, small_first_last, preserve_blank_lines, normalise_space_characters):
    """
    :param text: Titlecases input text
    :param callback: Callback function that returns the titlecase version of a specific word
    :param small_first_last: Capitalize small words (e.g. 'A') at the beginning;
				disabled when recursing
    :param preserve_blank_lines: Preserve blank lines in the output
    :param normalise_space_characters: Convert all original spaces to normal space characters
    :type text: str
    :type callback: function
    :type small_first_last: bool
    :type preserve_blank_lines: bool
    :type normalise_space_characters: bool

    This filter changes all words to Title Caps, and attempts to be clever
    about *un*capitalizing SMALL words like a/an/the in the input.

    The list of "SMALL words" which are not capped comes from
    the New York Times Manual of Style, plus 'vs' and 'v'.
    """
    # pylint: disable=too-many-locals, too-many-statements, too-many-branches
    if preserve_blank_lines:
        lines = regex.split('[\r\n]', text)
    else:
        lines = regex.split('[\r\n]+', text)
    processed = []
    for line in lines:
        all_caps = line.upper() == line
        split_line = regex.split(r'(\s)', line)
        words = split_line[::2]
        spaces = split_line[1::2]
        tc_line = []
        for word in words:
            if callback:
                new_word = callback(word, all_caps=all_caps)
                if new_word:
                    # Address #22: If a callback has done something
                    # specific, leave this string alone from now on
                    tc_line.append(_mark_immutable(new_word))
                    continue

            if all_caps:
                if UC_INITIALS.match(word):
                    tc_line.append(word)
                    continue

            if APOS_SECOND.match(word):
                if len(word[0]) == 1 and word[0] not in 'aeiouAEIOU':
                    word = word[0].lower() + word[1] + word[2].upper() + word[3:]
                else:
                    word = word[0].upper() + word[1] + word[2].upper() + word[3:]
                tc_line.append(word)
                continue

            match = MAC_MC.match(word)
            if match:
                tc_line.append("%s%s" % (match.group(1).capitalize(),
                                         a_titlecase(match.group(2), callback, True)))
                continue

            match = MR_MRS_MS_DR.match(word)
            if match:
                word = word[0].upper() + word[1:]
                tc_line.append(word)
                continue

            if INLINE_PERIOD.search(word) or (not all_caps and UC_ELSEWHERE.match(word)):
                tc_line.append(word)
                continue
            if SMALL_WORDS.match(word):
                tc_line.append(word.lower())
                continue

            if "/" in word and "//" not in word:
                slashed = map(
                    lambda t: a_titlecase(t,callback,False),
                    word.split('/')
                )
                tc_line.append("/".join(slashed))
                continue

            if '-' in word:
                hyphenated = map(
                    lambda t: a_titlecase(t, callback, False),
                    word.split('-')
                )
                tc_line.append("-".join(hyphenated))
                continue

            if all_caps:
                word = word.lower()

            # A term with all consonants should be considered an acronym.  But if it's
            # too short (like "St", don't apply this)
            consonants = ''.join(set(string.ascii_lowercase)
                                 - {'a', 'e', 'i', 'o', 'u', 'y'})
            is_all_consonants = regex.search(r'\A[' + consonants + r']+\Z', word,
                                             flags=regex.IGNORECASE)
            if is_all_consonants and len(word) > 2:
                tc_line.append(word.upper())
                continue

            # Just a normal word that needs to be capitalized
            tc_line.append(CAPFIRST.sub(lambda m: m.group(0).upper(), word))

        if small_first_last and tc_line:
            if not isinstance(tc_line[0], Immutable):
                tc_line[0] = SMALL_FIRST.sub(lambda m: '%s%s' % (
                    m.group(1),
                    m.group(2).capitalize()
                ), tc_line[0])

            if not isinstance(tc_line[-1], Immutable):
                tc_line[-1] = SMALL_LAST.sub(
                    lambda m: m.group(0).capitalize(), tc_line[-1]
                )

        if normalise_space_characters:
            result = " ".join(tc_line)
        else:
            line_to_be_joined = tc_line + spaces
            line_to_be_joined[::2] = tc_line
            line_to_be_joined[1::2] = spaces
            result = "".join(line_to_be_joined)

        result = SUBPHRASE.sub(lambda m: '%s%s' % (
            m.group(1),
            m.group(2).capitalize()
        ), result)

        processed.append(result)

    result = "\n".join(processed)
    return result


def set_small_word_list(small=SMALL):
    """ Rewrite small word list. """
    # pylint: disable=global-statement
    global SMALL_WORDS
    global SMALL_FIRST
    global SMALL_LAST
    global SUBPHRASE
    SMALL_WORDS = regex.compile(r'^(%s)$' % small, regex.I)
    SMALL_FIRST = regex.compile(r'^([%s]*)(%s)\b' % (PUNCT, small), regex.I)
    SMALL_LAST = regex.compile(r'\b(%s)[%s]?$' % (small, PUNCT), regex.I)
    SUBPHRASE = regex.compile(r'([:.;?!][ ])(%s)' % small)
