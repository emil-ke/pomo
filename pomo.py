#!/usr/bin/env python3
import curses
import time


def get_user_input(screen):
    screen.clear()
    screen.addstr("For how many minutes do you want to study?\n> ")
    minutes = int(screen.getstr().decode())
    screen.clear()
    screen.addstr("How long should your break be?\n> ")
    break_time = int(screen.getstr().decode())
    screen.clear()
    screen.addstr("How many breaks do you want to take?\n> ")
    break_count = int(screen.getstr().decode())
    return minutes, break_time, break_count


def get_user_confirmation(screen):
    while True:
        screen.clear()
        screen.addstr("Do you want to rerun the program? (Answer with either 'yes' or 'no')\n> ")
        choice = screen.getstr().decode().lower()
        if choice in ["yes", "no"]:
            return choice
        else:
            screen.addstr("Invalid input. Please enter either 'yes' or 'no'.")
            screen.refresh()
            time.sleep(2)


def run_pomodoro(screen, minutes, break_time, break_count):
    curses.curs_set(0)

    for i in range(break_count):
        seconds = minutes * 60

        while seconds > 0:
            rem_min, _ = divmod(seconds, 60)

            # Calculate progress
            progress = (minutes * 60 - seconds) / (minutes * 60)
            bar_width = 20
            filled_width = int(progress * bar_width)
            empty_width = bar_width - filled_width
            bar = "[" + filled_width * "#" + empty_width * " " + "]"

            # Display progress and clock
            screen.clear()
            screen.addstr(f"Pomodoro {i+1} of {break_count}\n")
            screen.addstr(f"Time remaining: {rem_min} minutes\n")  # Updated line
            screen.addstr(f"{bar}")
            screen.refresh()
            curses.doupdate()

            time.sleep(1)
            seconds -= 1

        screen.clear()
        screen.addstr(f"\nTime's up! Take a break for {break_time} minutes.")
        screen.refresh()
        time.sleep(break_time * 60)

        screen.clear()
        screen.addstr(f"Pomodoro {i+1} of {break_count}\n")
        screen.addstr("Break's over. Back to work!")
        screen.refresh()
        time.sleep(3)

    screen.clear()
    screen.refresh()


def main():
    while True:
        try:
            # Initialize a curses screen
            screen = curses.initscr()

            # Enable input echoing
            curses.echo()

            # Prompt the user for input to determine Pomodoro duration, break length, and number of breaks
            minutes, break_time, break_count = get_user_input(screen)

            # Run the Pomodoro timer
            run_pomodoro(screen, minutes, break_time, break_count)

            # Prompt the user for confirmation to run the program again
            choice = get_user_confirmation(screen)

            # If the user chooses not to run the program again, exit the loop
            if choice == "no":
                break

        except KeyboardInterrupt:
            # If the user interrupts the program with a keyboard interrupt, exit the loop
            break

        finally:
            # Reset the curses settings and close the screen
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    main()
