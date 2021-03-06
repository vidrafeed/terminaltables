from textwrap import dedent

import pytest

import terminaltables
from terminaltables import AsciiTable, UnixTable


@pytest.mark.parametrize('cls', [AsciiTable, UnixTable])
def test_empty(cls):
    table = cls([])
    assert 2 == table.table_width
    assert table.ok is True

    table = cls([[]])
    assert 2 == table.table_width
    assert table.ok is True

    table = cls([['']])
    assert 4 == table.table_width
    assert table.ok is True

    table = cls([[' ']])
    assert 5 == table.table_width
    assert table.ok is True


@pytest.mark.parametrize('cls', [AsciiTable, UnixTable])
def test_simple(cls):
    table_data = [
        ['Name', 'Color', 'Type'],
        ['Avocado', 'green', 'nut'],
        ['Tomato', 'red', 'fruit'],
        ['Lettuce', 'green', 'vegetable'],
    ]
    table = cls(table_data)

    assert 31 == table.table_width
    assert table.ok is True

    table_data.append(['Watermelon', 'green', 'fruit'])
    assert 34 == table.table_width
    assert table.ok is True

    old_func = terminaltables.terminal_width
    terminaltables.terminal_width = lambda: 34
    assert table.ok is True

    terminaltables.terminal_width = lambda: 33
    assert table.ok is False
    terminaltables.terminal_width = old_func


@pytest.mark.parametrize('cls', [AsciiTable, UnixTable])
def test_multi_line(cls):
    old_func = terminaltables.terminal_width
    terminaltables.terminal_width = lambda: 100
    table_data = [
        ['Show', 'Characters'],
        ['Rugrats', dedent('Tommy Pickles, Chuckie Finster, Phillip DeVille, Lillian DeVille, Angelica Pickles,\n'
                           'Susie Carmichael, Dil Pickles, Kimi Finster, Spike')],
        ['South Park', 'Stan Marsh, Kyle Broflovski, Eric Cartman, Kenny McCormick']
    ]
    table = cls(table_data)
    assert 100 == table.table_width
    assert table.ok is True
    terminaltables.terminal_width = old_func


def test_attributes():
    table_data = [
        ['Name', 'Color', 'Type'],
        ['Avocado', 'green', 'nut'],
        ['Tomato', 'red', 'fruit'],
        ['Lettuce', 'green', 'vegetable'],
    ]
    table = AsciiTable(table_data)

    assert 31 == max(len(r) for r in table.table.splitlines())
    assert 31 == table.table_width

    table.outer_border = False
    assert 29 == max(len(r) for r in table.table.splitlines())
    assert 29 == table.table_width

    table.inner_column_border = False
    assert 27 == max(len(r) for r in table.table.splitlines())
    assert 27 == table.table_width

    table.padding_left = 0
    assert 24 == max(len(r) for r in table.table.splitlines())
    assert 24 == table.table_width

    table.padding_right = 0
    assert 21 == max(len(r) for r in table.table.splitlines())
    assert 21 == table.table_width
