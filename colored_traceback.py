import sys
import re
from typing import Iterable, AnyStr


class Colors:
    def __init__(self):
        self.pref: str = "\033["
        self.reset = f"{self.pref}0m"

        self.red = "31m"
        self.blue = "34m"

    def color_string(self, text: AnyStr, color: str = "white", is_bold: bool = False):
        return f'{self.pref}{1 if is_bold else 0};{getattr(self, color)}' + text + self.reset


class Charmify(object):
    def colorize_traceback(self, exception, value, tb) -> None:
        import traceback
        tb_text: str = "".join(traceback.format_exception(exception, value, tb))
        self.stream.write(self.restructure_colored_segments(tb_text))

    @staticmethod
    def split_tokenize(delimiters: Iterable, string: AnyStr) -> list[AnyStr]:
        """
        Tokenizes between File references and Traceback Descriptions,
        later Half of the function performs a check disregaurding any
        redundant double-quotes from non File references
        and ensures full validity of File references.
        :param delimiters: Iterable - pre-detected File References.
        :param string: AnyStr - full Traceback value.
        :return: list[AnyStr] - Tokenized
        """
        import re
        regex_pattern: str = '(' + '|'.join(map(re.escape, delimiters)) + ')'
        split_keeping_delimiter_list: list[AnyStr] = re.split(pattern=regex_pattern, string=string, maxsplit=0)
        for index, s in enumerate(split_keeping_delimiter_list):

            if s[0:5] == r'File ':
                split_keeping_delimiter_list[index - 1] = split_keeping_delimiter_list[index - 1] + s[0:5]
                split_keeping_delimiter_list[index] = s[5:]
        return split_keeping_delimiter_list

    def restructure_colored_segments(self, string: AnyStr) -> str:
        """
        Applies tokenization, then color tagging.
        :param string: : AnyStr - full Traceback value.
        :return: AnyStr - ANSI Compatible string individually colored by token.
        """
        color_tool = Colors()
        quoted_sub_strings = re.findall(r'"(.+?)"', string)
        split_string = self.split_tokenize(
            delimiters=list(map(lambda i: f'File "{i}"', quoted_sub_strings)), string=string)
        return "".join(
            [
                (
                    color_tool.color_string(text=i, color='blue', is_bold=True) if [r'"', r'"'] == [i[0], i[-1]]
                    else color_tool.color_string(text=i, color='red')
                ) for i in split_string
            ]
        )

    @property
    def stream(self):
        try:
            import colorama
            return colorama.AnsiToWin32(sys.stderr)
        except ImportError:
            return sys.stderr


def add_hook(always: bool = False ) -> None:
    """
    Apply hook to tracebacks, applying Jetbrains style Traceback Highlighting,
    providing much easier debugging and log searching.
    :param always: bool
    :return: None
    """
    isatty = getattr(sys.stderr, 'isatty', lambda: False)
    if always or isatty():
        charmer = Charmify()
        sys.excepthook = charmer.colorize_traceback
