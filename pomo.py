#!/usr/bin/env python3
import curses
import time


def get_user_input(screen):
    """Get user input for study duration, break time, and break count.

    Args:
        screen (curses.window): The window to display the input prompt on.

    Returns:
        A tuple containing the study duration (in minutes), break time (in minutes), and break count.
    """
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
    """Get user confirmation to rerun the program.

    Args:
        screen (curses.window): The window to display the input prompt on.

    Returns:
        A string containing the user's choice (either 'yes' or 'no').
    """
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
    """Run the Pomodoro timer.

    Args:
        screen (curses.window): The window to display the timer on.
        minutes (int): The duration of each study session (in minutes).
        break_time (int): The duration of each break (in minutes).
        break_count (int): The number of study/break cycles to complete.
    """
    curses.curs_set(0)

    for i in range(break_count):
        seconds = minutes * 60

        while seconds > 0:
            rem_min, rem_sec = divmod(seconds, 60)

            # Calculate progress
            progress = (minutes * 60 - seconds) / (minutes * 60)
            bar_width = 20
            filled_width = int(progress * bar_width)
            empty_width = bar_width - filled_width
            bar = "[" + filled_width * "#" + empty_width * " " + "]"

            # Display progress and clock
            screen.clear()
            screen.addstr(f"Pomodoro {i+1} of {break_count}\n")
            screen.addstr(f"Time remaining: {rem_min:02d}:{rem_sec:02d}\n")
            screen.addstr(f"{bar} {progress * 100:.1f}%")
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

    screen.clear()  # clear the screen after the final break
    screen.refresh()


def main():
    """
    The main function of the Pomodoro timer program.

    The function initializes a curses screen and then repeatedly prompts the user for input to determine the
    duration of each Pomodoro, the length of each break, and the number of breaks. It then runs the Pomodoro timer,
    waits for the user's confirmation to run the program again, and then exits.

    :return: None
    """
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
