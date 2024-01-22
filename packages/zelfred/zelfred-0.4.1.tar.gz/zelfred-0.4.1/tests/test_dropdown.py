# -*- coding: utf-8 -*-

import pytest

from zelfred.dropdown import Dropdown
from zelfred.exc import NoItemToSelectError


def get_items(menu) -> str:
    return "".join([item for item, flag in menu])


def get_selected_item(menu) -> str:
    for item, flag in menu:
        if flag:
            return item


def _test_high_amount_of_items():
    dd = Dropdown(items=list("abcdefghijklmnopqrstuvwxyz"), show_items_limit=10)
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    dd.press_up()
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    dd.scroll_up(2)
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    menu = dd.menu
    assert get_items(menu) == "abcdefghij"
    assert get_selected_item(menu) == "a"

    dd.press_down(5)
    assert dd.selected_item_index == 5
    assert dd.cursor_position == 5

    menu = dd.menu
    assert get_items(menu) == "abcdefghij"
    assert get_selected_item(menu) == "f"

    dd.press_up(2)
    assert dd.selected_item_index == 3
    assert dd.cursor_position == 3

    menu = dd.menu
    assert get_items(menu) == "abcdefghij"
    assert get_selected_item(menu) == "d"

    dd.scroll_down(2)
    assert dd.selected_item_index == 13
    assert dd.cursor_position == 9

    menu = dd.menu
    assert get_items(menu) == "efghijklmn"
    assert get_selected_item(menu) == "n"

    dd.press_up(2)
    assert dd.selected_item_index == 11
    assert dd.cursor_position == 7

    menu = dd.menu
    assert get_items(menu) == "efghijklmn"
    assert get_selected_item(menu) == "l"

    dd.scroll_down(2)
    assert dd.selected_item_index == 21
    assert dd.cursor_position == 9

    menu = dd.menu
    assert get_items(menu) == "mnopqrstuv"
    assert get_selected_item(menu) == "v"

    dd.scroll_down(2)
    assert dd.selected_item_index == 25
    assert dd.cursor_position == 9

    menu = dd.menu
    assert get_items(menu) == "qrstuvwxyz"
    assert get_selected_item(menu) == "z"

    dd.press_down(2)
    assert dd.selected_item_index == 25
    assert dd.cursor_position == 9

    menu = dd.menu
    assert get_items(menu) == "qrstuvwxyz"
    assert get_selected_item(menu) == "z"

    dd.press_up(3)
    assert dd.selected_item_index == 22
    assert dd.cursor_position == 6

    menu = dd.menu
    assert get_items(menu) == "qrstuvwxyz"
    assert get_selected_item(menu) == "w"


def _test_low_amount_of_items():
    dd = Dropdown(items=list("abc"))
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    dd.press_up()
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    dd.scroll_up(2)
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "a"

    dd.press_down(2)
    assert dd.selected_item_index == 2
    assert dd.cursor_position == 2

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "c"

    dd.press_up(1)
    assert dd.selected_item_index == 1
    assert dd.cursor_position == 1

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "b"

    dd.scroll_down(2)
    assert dd.selected_item_index == 2
    assert dd.cursor_position == 2

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "c"

    dd.press_up(2)
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "a"

    dd.scroll_down(2)
    assert dd.selected_item_index == 2
    assert dd.cursor_position == 2

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "c"

    dd.press_down(2)
    assert dd.selected_item_index == 2
    assert dd.cursor_position == 2

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "c"

    dd.press_up(1)
    assert dd.selected_item_index == 1
    assert dd.cursor_position == 1

    menu = dd.menu
    assert get_items(menu) == "abc"
    assert get_selected_item(menu) == "b"


def _test_press_up_and_down():
    dd = Dropdown(items=list("abc"))
    dd._press_up()
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0
    assert dd.selected_item == "a"

    dd.press_down(3)
    dd._press_down()
    assert dd.selected_item_index == 2
    assert dd.cursor_position == 2
    assert dd.selected_item == "c"


def _test_update():
    dd = Dropdown(items=list("abc"))
    dd._press_down()
    dd.update(items=list("mn"))
    assert dd.items == list("mn")
    assert dd.n_items == 2
    assert dd.selected_item_index == 0
    assert dd.cursor_position == 0
    assert dd.show_items_limit == 2


def _test_selected_item():
    dd = Dropdown(items=[])
    with pytest.raises(NoItemToSelectError):
        _ = dd.selected_item


def test():
    _test_high_amount_of_items()
    _test_low_amount_of_items()
    _test_press_up_and_down()
    _test_update()
    _test_selected_item()


if __name__ == "__main__":
    from zelfred.tests import run_cov_test

    run_cov_test(__file__, "zelfred.dropdown", preview=False)
