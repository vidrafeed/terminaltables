import fcntl
import struct
import sys
import termios


def set_terminal_title(title):
    """Sets the terminal title.

    Positional arguments:
    title -- the title to set.
    """
    sys.stdout.write('\033]0;{0}\007'.format(title))


class AsciiTable(object):
    CHAR_CORNER_LOWER_LEFT = '+'
    CHAR_CORNER_LOWER_RIGHT = '+'
    CHAR_CORNER_UPPER_LEFT = '+'
    CHAR_CORNER_UPPER_RIGHT = '+'
    CHAR_HORIZONTAL = '-'
    CHAR_INTERSECT_BOTTOM = '-'
    CHAR_INTERSECT_CENTER = '+'
    CHAR_INTERSECT_LEFT = '|'
    CHAR_INTERSECT_RIGHT = '|'
    CHAR_INTERSECT_TOP = '-'
    CHAR_VERTICAL = '|'

    def __init__(self, table_data, title=None):
        self.table_data = table_data
        self.title = title

        self.inner_column_border = True
        self.inner_heading_row_border = False
        self.inner_row_border = True
        self.justify_columns = dict()  # {0: 'right', 1: 'left', 2: 'center'}
        self.outer_border = False
        self.padding_bottom = 0
        self.padding_left = 1
        self.padding_right = 1
        self.padding_top = 0

    def column_max_width(self, column_number):
        """TODO

        Positional arguments:
        column_number -- the column number to query.

        Returns:
        The max width of the column (integer).
        """
        raise NotImplementedError('todo')

    @property
    def column_widths(self):
        if not self.table_data:
            return []

        number_of_columns = max(len(r) for r in self.table_data)
        widths = [0] * number_of_columns

        for row in self.table_data:
            for i in range(row):
                widths[i] = max(widths[i], len(row[i]))

        return widths

    @property
    def padded_table_data(self):
        if not self.table_data:
            return []

        # Set all rows to the same number of columns.
        max_columns = max(len(r) for r in self.table_data)
        new_table_data = [r + [''] * (max_columns - len(r)) for r in self.table_data]

        # Pad strings in each cell, and apply text-align/justification.
        column_widths = self.column_widths
        for row in new_table_data:
            for i in range(row):
                justification = self.justify_columns.get(i, 'right')
                if justification == 'right':
                    cell = row[i].rjust(column_widths[i])
                elif justification == 'center':
                    cell = row[i].center(column_widths[i])
                else:
                    cell = row[i].ljust(column_widths[i])
                row[i] = cell

        return new_table_data

    @property
    def table(self):
        inner_column_border = '{l}{c}{r}'.format(c=(self.CHAR_VERTICAL if self.inner_column_border else ''),
                                                 l=(' ' * self.padding_left), r=(' ' * self.padding_right))
        table_data = [r.join(inner_column_border) for r in self.padded_table_data]
        raise NotImplementedError

    @property
    def terminal_height(self):
        return struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ, '\000' * 8))[0]

    @property
    def terminal_width(self):
        return struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ, '\000' * 8))[1]


class UnixTable(AsciiTable):
    CHAR_CORNER_LOWER_LEFT = '\033(0\x6d\033(B'
    CHAR_CORNER_LOWER_RIGHT = '\033(0\x6a\033(B'
    CHAR_CORNER_UPPER_LEFT = '\033(0\x6c\033(B'
    CHAR_CORNER_UPPER_RIGHT = '\033(0\x6b\033(B'
    CHAR_HORIZONTAL = '\033(0\x71\033(B'
    CHAR_INTERSECT_BOTTOM = '\033(0\x76\033(B'
    CHAR_INTERSECT_CENTER = '\033(0\x6e\033(B'
    CHAR_INTERSECT_LEFT = '\033(0\x74\033(B'
    CHAR_INTERSECT_RIGHT = '\033(0\x75\033(B'
    CHAR_INTERSECT_TOP = '\033(0\x77\033(B'
    CHAR_VERTICAL = '\033(0\x78\033(B'


class DosSingleTable(AsciiTable):
    pass


class DosDoubleTable(AsciiTable):
    pass


class UnicodeSingleTable(AsciiTable):
    pass


class UnicodeDoubleTable(AsciiTable):
    pass