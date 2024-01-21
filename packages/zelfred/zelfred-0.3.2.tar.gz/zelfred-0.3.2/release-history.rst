.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.3.2 (2023-01-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Forget to add the following public API in 0.3.1, now they are available:
    - ``zelfred.api.open_url_or_print``
    - ``zelfred.api.open_file_or_print``
    - ``zelfred.api.copy_or_print``


0.3.1 (2023-01-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Allow user to custom ``UIRender`` and use it in ``UI``.
- Add ``open_url_or_print``, ``copy_or_print`` actions.

**Minor Improvements**

- Add the following sample app to app gallery:
    - refresh_cache_v1
    - refresh_cache_v2
    - refresh_cache_v3
    - json_formatter

**Miscellaneous**

- Add "Maintainer Guide" document.


0.2.4 (2023-11-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that user has to tap CTRL + C multiple times to jump out of the sub session.
- Fix a bug that the debug log should write to ``${HOME}/.zelfred-log.txt``.


0.2.3 (2023-10-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Add the missing CTRL + U keyboard shortcut.


0.2.2 (2023-10-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Allow user to custom the following shortcut keys's behavior:
    - ``Ctrl + T``
    - ``Ctrl + G``
    - ``Ctrl + B``
    - ``Ctrl + N``


0.2.1 (2023-10-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Allow user to customize the "key pressed" event processing logics.
- Allow user to delete word forward and backward.
- Remove the ``Ctrl + G`` and ``Ctrl + H`` keyboard shortcut.
- Add the ``Alt + Left`` and ``Alt + Right`` keyboard shortcut to move cursor to the previous or next word.
- Add the ``Ctrl + U`` user action.
- Add the ``repaint`` method, allow user to print some helper information before running the user defined handler.
- Add the ``run_sub_session`` method, allow user to implement a custom handler that can enter a custom sub session.
- Add ``post_enter_handler``, ``post_ctrl_a_handler``, ``post_ctrl_w_handler``, ``post_ctrl_u_handler``, ``post_ctrl_p_handler`` methods, allow user to custom the behavior after user action. The default behavior is to exit the UI.

**Minor Improvements**

- Add the following sample app to app gallery:
    - random_password_generator
    - calculate_file_checksum
    - search_google_chrome_bookmark
    - password_book


0.1.5 (2023-10-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Allow user to stay in the session after user action (Enter, Ctrl + A, Ctrl + W, Ctrl + P).


0.1.4 (2023-10-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Allow the ``F1`` key to recover the previous user input.


0.1.3 (2023-10-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Print ``🔴 keyboard interrupt, exit.`` message when user press ``Ctrl+C``.


0.1.2 (2023-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- Fix license. It should be GPL.
- Add ``folder_and_file_search`` app to gallery.


0.1.1 (2023-10-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
