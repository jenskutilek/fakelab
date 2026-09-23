import curses
import textwrap


def dlg_ask_ok_cancel(
    stdscr,
    message: str,
    question: str = "",
    okstring: str = "OK",
    cancelstring: str = "Cancel",
    title: str = "FakeLab",
):
    """
    Display a simple modal dialog using curses.

    Args:
        stdscr (curses.window): The main screen returned by curses.wrapper().
        message (str): The main message shown in the dialog.
        question (str, optional): Text displayed just above the buttons (e.g. "Do you
            want to continue?").. Defaults to an empty string.
        okstring (str, optional): The label of the "OK" button. Defaults to "OK".
        cancelstring (str, optional): The label of the "Cancel" button. Defaults to
            "Cancel".
        title (str, optional): Title to display at the top of the dialog. Defaults to
            "FakeLab".

    Returns:
        int: 1 if the OK button was clicked, 2 if the Cancel button was clicked or the
            window has been closed.
    """
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.refresh()

    # ---- 1. Calculate dialog size ----------------------------------------
    # Use a fixed width (or compute from longest line)
    max_width = min(curses.COLS - 4, 80)  # leave a margin on both sides
    wrapped_msg = textwrap.wrap(message, width=max_width - 2)

    # Height: title(1) + empty(1) + message(lines) + empty(1) +
    #          question(1) + empty(1) + buttons(1)
    height = 1 + 1 + len(wrapped_msg) + 1 + 1 + 1 + 1
    width = max(max_width, len(title) + 4)

    # Center the dialog
    start_y = (curses.LINES - height) // 2
    start_x = (curses.COLS - width) // 2

    win = curses.newwin(height, width, start_y, start_x)
    win.keypad(True)

    # ---- 2. Draw static parts --------------------------------------------
    # Title bar
    win.attron(curses.A_REVERSE)
    win.addstr(0, 1, f" {title} ")
    win.attroff(curses.A_REVERSE)

    # Message area
    y = 2
    for line in wrapped_msg:
        win.addstr(y, 1, line)
        y += 1

    # Empty line before question
    y += 0

    # Question
    if question:
        win.addstr(y + 1, 1, question)

    # ---- 3. Buttons -------------------------------------------------------
    buttons = [okstring, cancelstring]
    selected = 0  # index of the currently highlighted button

    def draw_buttons():
        """Redraws the button row."""
        btn_y = height - 2
        win.attron(curses.A_BOLD)
        x_offset = (
            width - sum(len(b) + 4 for b in buttons) - (len(buttons) - 1) * 2
        ) // 2

        for idx, txt in enumerate(buttons):
            if idx == selected:
                # Highlighted button
                win.attron(curses.A_REVERSE)
            else:
                win.attroff(curses.A_REVERSE)

            btn_text = f"[ {txt} ]"
            win.addstr(btn_y, x_offset, btn_text)
            x_offset += len(btn_text) + 2

        win.attroff(curses.A_BOLD)
        win.refresh()

    draw_buttons()

    # ---- 4. Event loop ----------------------------------------------------
    while True:
        key = win.getch()
        if key in (curses.KEY_LEFT, curses.KEY_BTAB):  # Shift+Tab
            selected = (selected - 1) % len(buttons)
            draw_buttons()
        elif key in (curses.KEY_RIGHT, ord("\t")):  # Tab
            selected = (selected + 1) % len(buttons)
            draw_buttons()
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter
            return 1 if buttons[selected] == okstring else 2
        elif key in (27,):  # ESC
            return 2


# ---------------------------------------------------------------------------


def ask_ok_cancel(
    message: str,
    question: str = "",
    okstring: str = "OK",
    cancelstring: str = "Cancel",
    title: str = "FakeLab",
):
    return curses.wrapper(
        dlg_ask_ok_cancel, message, question, okstring, cancelstring, title
    )
