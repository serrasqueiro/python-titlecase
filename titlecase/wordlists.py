# -*- coding: utf-8 -*-

""" Word(s) lists
"""

import os
import logging
logger = logging.getLogger(__name__)

ENCODING_IN = "UTF-8"


def create_wordlist_filter_from_file(file_path):
    """ Load a list of abbreviations from the file with the provided path,
    reading one abbreviation from each line, and return a callback to
    be passed to the `titlecase` function for preserving their given
    canonical capitalization during title-casing.
    """
    if file_path is None:
        logger.debug('No abbreviations file path given')
        return lambda word, **kwargs: None
    file_path_str = str(file_path)
    if not os.path.isfile(file_path_str):
        logger.debug('No abbreviations file found at: %s', file_path_str)
        return lambda word, **kwargs: None
    with open(file_path_str, encoding=ENCODING_IN) as fd_in:
        logger.debug('Reading abbreviations from file: %s', file_path_str)
        abbrevs_gen = (
            line.strip()
            for line in fd_in.read().splitlines() if line
        )
        abbrevs = {
            abbr.upper(): abbr
            for abbr in abbrevs_gen
        }
        if logger.isEnabledFor(logging.DEBUG):
            for abbr in abbrevs.values():
                logger.debug('Registered abbreviation: [%s]', abbr)
        return lambda word, **kwargs: abbrevs.get(word.upper())


def cmd():
    """ Handler for command line invocation.

    Try to handle any reasonable thing thrown at this.
    Consume '-f' and '-o' as input/output, allow '-' for stdin/stdout
    and treat any subsequent arguments as a space separated string to
    be titlecased (so it still works if people forget quotes).
    """
    parser = argparse.ArgumentParser(allow_abbrev=False)
    in_group = parser.add_mutually_exclusive_group()
    in_group.add_argument('string', nargs='*', default=[],
            help='String to titlecase')
    in_group.add_argument('-f', '--input-file',
            help='File to read from to titlecase')
    parser.add_argument('-o', '--output-file',
            help='File to write titlecased output to')
    parser.add_argument('-w', '--wordlist',
            help='Wordlist for acronyms')
    parser.add_argument('--preserve-blank-lines', action='store_true',
            help='Do not skip blank lines in input')

    args = parser.parse_args()

    if args.input_file is not None:
        if args.input_file == '-':
            ifile = sys.stdin
        else:
            ifile = open(args.input_file, encoding="UTF-8")
    else:
        ifile = sys.stdin

    if args.output_file is not None:
        if args.output_file == '-':
            ofile = sys.stdout
        else:
            ofile = open(args.output_file, 'w')
    else:
        ofile = sys.stdout

    if len(args.string) > 0:
        in_string = ' '.join(args.string)
    else:
        with ifile:
            in_string = ifile.read()

    if args.wordlist is not None:
        wordlist_file = args.wordlist
    else:
        wordlist_file = os.path.join(os.path.expanduser('~'), '.titlecase.txt')
    wordlist_filter = create_wordlist_filter_from_file(wordlist_file)

    with ofile:
        ofile.write(maincase(in_string, callback=wordlist_filter,
            preserve_blank_lines=args.preserve_blank_lines))
