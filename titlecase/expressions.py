# -*- coding: utf-8 -*-

""" Original Expressions
"""

try:
    import regex
except ImportError:
    import re as regex
    REGEX_AVAILABLE = False
else:
    REGEX_AVAILABLE = True


SMALL = r'a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?'
PUNCT = r"""!"“#$%&'‘()*+,\-–‒—―./:;?@[\\\]_`{|}~"""

SMALL_WORDS = regex.compile(r'^(%s)$' % SMALL, regex.I)

SMALL_FIRST = regex.compile(r'^([%s]*)(%s)\b' % (PUNCT, SMALL), regex.I)
SMALL_LAST = regex.compile(r'\b(%s)[%s]?$' % (SMALL, PUNCT), regex.I)
SUBPHRASE = regex.compile(r'([:.;?!\-–‒—―][ ])(%s)' % SMALL)
MAC_MC = regex.compile(r"^([Mm]c|MC)(\w.+)")
MR_MRS_MS_DR = regex.compile(r"^((m((rs?)|s))|Dr)$", regex.I)

if REGEX_AVAILABLE:
    INLINE_PERIOD = regex.compile(r'[\p{Letter}][.][\p{Letter}]', regex.I)
    UC_ELSEWHERE = regex.compile(r'[%s]*?[\p{Letter}]+[\p{Uppercase_Letter}]+?' % PUNCT)
    CAPFIRST = regex.compile(r"^[%s]*?([\p{Letter}])" % PUNCT)
    APOS_SECOND = regex.compile(r"^[dol]{1}['‘]{1}[\p{Letter}]+(?:['s]{2})?$", regex.I)
    UC_INITIALS = regex.compile(r"^(?:[\p{Uppercase_Letter}]{1}\.{1}|[\p{Uppercase_Letter}]{1}\.{1}[\p{Uppercase_Letter}]{1})+$")
else:
    INLINE_PERIOD = regex.compile(r'[\w][.][\w]', regex.I)
    UC_ELSEWHERE = regex.compile(r'[%s]*?[a-zA-Z]+[A-Z]+?' % PUNCT)
    CAPFIRST = regex.compile(r"^[%s]*?([\w])" % PUNCT)
    APOS_SECOND = regex.compile(r"^[dol]['‘][\w]+(?:['s]{2})?$", regex.I)
    UC_INITIALS = regex.compile(r"^(?:[A-Z]\.|[A-Z]\.[A-Z])+$")
