"""
A class to create a proem of information for a command line application.
"""
import math
import os
import logging
from typing import List

from colorama import Fore, just_fix_windows_console

just_fix_windows_console()

class Proem:
    """
    A class to create a proem of information for a command line application.

    :param app_nm: The name of the application.
    :param flavor_text: (optional) A short description of the application.
    :param version: (optional) The version of the application.
    :param repo_url: (optional) The URL to the repository for the application.
    :param repo_issues_url: (optional) The URL to the repository issues for the application.
    :param width: (optional) The width of the proem. If set to 0 or below, width will be set to the terminal width. (default is ``80``)
    :param border_char: (optional) The character used to create the border. (default is ``#``)
    :param border_color: (optional) The color of the border. (default is ``magenta``)
    :param description: (optional) A long description of the application. (default is ``None``)
    :param description_align: (optional) The alignment of the description text. Must be ``left``, ``center``, or ``right``. (default is ``left``)
    """

    def __init__(
        self,
        app_nm: str,
        flavor_text: str = None,
        version: str = None,
        repo_url: str = None,
        repo_issues_url: str = None,
        width: int = 80,
        border_char: str = "#",
        border_color: str = "magenta",
        description: str = None,
        description_align: str = 'left'
    ):
        self.app_nm = app_nm
        self.flavor_text = flavor_text
        self.version = version
        self.repo_url = repo_url
        self.repo_issues_url = repo_issues_url
        self.width = width
        self.border_char = border_char
        self.border_color = border_color
        self.description = description
        self.description_align = description_align

    def _str_to_color(self) -> str:
        color_name = self.border_color.lower()

        color_map = {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE
        }

        set_color = color_map.get(color_name, '')

        if set_color == '':
            logging.warning('Color not supported. Setting border color to no color.')

        return set_color
    def _border_char(self) -> str:
        return self._border_color_str + self.border_char + Fore.RESET

    def _border_line(self) -> str:
        return self._border_color_str + self.border_char * self.width + Fore.RESET

    def _empty_line(self) -> str:
        return self._border_char() + ' ' * self._empty_width * len(self.border_char) + self._border_char()

    def _wrap_text_left(self, text: str) -> str:
        return self._border_char() + ' ' + text.ljust(self._empty_width * len(self.border_char) - 1) + self._border_char()

    def _wrap_text_center(self, text: str) -> str:
        return self._border_char() + text.center(self._empty_width * len(self.border_char)) + self._border_char()

    def _wrap_text_right(self, text: str) -> str:
        return self._border_char() + text.rjust(self._empty_width * len(self.border_char) - 1) + ' ' + self._border_char()

    def _text_line(self, text: str, align: str = 'center', nl: bool = True) -> str:
        pad_width = self.width - 4

        _nl = '\n' if nl else ''

        # Calculate the number of chunks the text will be split into.
        chunks = math.ceil(len(text) / pad_width)

        text_line = ''

        # Determine the alignment method to use.
        if align == 'center':
            method = self._wrap_text_center
        elif align == 'left':
            method = self._wrap_text_left
        elif align == 'right':
            method = self._wrap_text_right
        else:
            raise ValueError("align must be 'center', 'left', or 'right'")

        # Split the text into chunks and apply the alignment method to each chunk.
        for x in range(chunks):
            if x == 0:
                text_line += method(text[0:pad_width]) + _nl
            elif x == chunks - 1:
                text_line += method(text[pad_width * x:]) + _nl
            else:
                text_line += method(text[pad_width * x:pad_width * (x + 1)]) + _nl

        return text_line

    def _find_max_width(self) -> int:
        max_width = len(self.app_nm)

        if self.flavor_text:
            max_width = max(max_width, len(self.flavor_text))

        if self.repo_url:
            max_width = max(max_width, len(self.repo_url))

        if self.repo_issues_url:
            max_width = max(max_width, len(self.repo_issues_url))

        if self.version:
            max_width = max(max_width, len(self.version))

        return max_width

    @property
    def width(self) -> int:
        """
        The width of the proem.
        """
        return self._width

    @width.setter
    def width(self, width: int):
        """
        Set the width of the proem.

        :param width: The width of the proem. If set to 0 or below, width will be set to the terminal width.
        """
        max_width = self._find_max_width() + 4

        if width <= 0:
            try:
                self._width = os.get_terminal_size().columns
            except OSError:
                self._width = 80
                logging.warning('Width is less than 0. Setting to default width of 80.')
        elif width < max_width:
            self._width = max_width
            logging.warning('Width is less than proem contents. Setting width to max width of proem contents which is %s.', max_width)
        else:
            try:
                self._width = min(width, os.get_terminal_size().columns)
            except OSError:
                self._width = width

        self._empty_width = self._width - 2

    @property
    def description_align(self) -> str:
        """
        The alignment of the description text.
        """
        return self._description_align

    @description_align.setter
    def description_align(self, description_align: str):
        """
        Set the alignment of the description text.

        :param description_align: The alignment of the description text. Must be ``left``, ``center``, or ``right``.
        """
        if description_align not in ['left', 'center', 'right']:
            raise ValueError("description_align must be 'left', 'center', or 'right'")

        self._description_align = description_align

    @property
    def border_color(self) -> str:
        """
        The color of the border.
        """
        return self._border_color

    @border_color.setter
    def border_color(self, border_color: str):
        """
        Set the color of the border.

        :param border_color: The color of the border.
        """
        self._border_color = border_color
        self._border_color_str = self._str_to_color()

    def build(self) -> str:
        """
        Build the proem text as a string.

        :return: The proem text as a string
        """
        proem_str = self._border_line() + '\n'
        proem_str += self._text_line(self.app_nm)

        if self.flavor_text:
            proem_str += self._text_line(self.flavor_text)

        if self.version:
            proem_str += self._empty_line() + '\n'
            proem_str += self._text_line(self.version)

        if self.repo_url:
            proem_str += self._empty_line() + '\n'
            proem_str += self._text_line(self.repo_url)

        if self.repo_issues_url:
            proem_str += self._empty_line() + '\n'
            proem_str += self._text_line(self.repo_issues_url)

        if self.description:
            proem_str += self._empty_line() + '\n'
            proem_str += self._text_line(text = self.description, align = self.description_align)

        proem_str += self._border_line() + '\n'

        return proem_str

    def build_list(self) -> List[str]:
        """
        Build the proem text as a list of strings.

        :return: The proem text as a list of strings
        """
        proem_list = []

        proem_list.append(self._border_line())
        proem_list.append(self._text_line(self.app_nm, nl=False))

        if self.flavor_text:
            proem_list.append(self._text_line(self.flavor_text, nl=False))

        if self.version:
            proem_list.append(self._empty_line())
            proem_list.append(self._text_line(self.version, nl=False))

        if self.repo_url:
            proem_list.append(self._empty_line())
            proem_list.append(self._text_line(self.repo_url, nl=False))

        if self.repo_issues_url:
            proem_list.append(self._empty_line())
            proem_list.append(self._text_line(self.repo_issues_url, nl=False))

        if self.description:
            proem_list.append(self._empty_line())
            proem_list.append(self._text_line(text = self.description, align = self.description_align, nl=False))

        proem_list.append(self._border_line())

        return proem_list

    def __str__(self):
        return self.build()

    def __iter__(self):
        return iter(self.build_list())
