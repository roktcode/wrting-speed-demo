import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing text!")
    stdscr.addstr("\nPress any keyto begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(f"{target}")
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i,  char, color)


def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)

        # 5 is the average word length
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        # in case the entered key is left/right arrow or whatever else...
        # avoid the exception and continue the app
        try:
            if ord(key) == 27:
                break

            if key in ("KEY_BACKSPACE", '\b', "\x7f"):
                if len(current_text) > 0:
                    current_text.pop()
            elif len(current_text) < len(target_text):
                current_text.append(key)
        except:
            continue


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(
            2, 0, "You completed the test! Pres any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
