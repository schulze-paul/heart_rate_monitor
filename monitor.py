"""
Heart rate monitor
------------------
The program relies on the user to press the space bar and displays the measured heart rate.
"""

import keyboard
import os
import numpy as np
import curses # for terminal display

from computation import HeartRateComputation

class HeartRateDisplay:
    """Display the heart rate as a graph in the terminal."""

    def __init__(self):
        self._heart_rate = 0
        self.terminal_width = os.get_terminal_size().columns
        self.terminal_height = os.get_terminal_size().lines

    def set_heart_rate(self, heart_rate):
        """Set the heart rate."""
        self._heart_rate = heart_rate

    def get_rate_line(self, label: str, rate: float) -> str:
        """Get the line to display the heart rate."""
        
        # display the heart rate as a graph
        # the heart rate is displayed as a number of asterisks
        # the heart rate is rounded to the nearest integer
        
        
        label = "Average rate"
        rate = self._heart_rate

        print_line = ""
        # show heart rate
        print_line += label + ":"
        number_spaces = 3 - int(np.log10(rate))  if rate != 0 else 3
        print_line += " " * number_spaces
        print_line += f"{round(rate)} bpm "

        # show bar
        bar_area = self.terminal_width - len(label) - 13 
        bar_width = min(round(rate), bar_area)
        white_space_width = bar_area - bar_width
        print_line += "["
        print_line += "*" * bar_width 
        print_line += " " * white_space_width
        print_line += "] "

        return print_line
    
    def display(self):
        """Display the heart rate."""
        # clear the screen
        # initialize curses
        stdscr = curses.initscr()

        # clear the screen
        stdscr.clear()

        # display the heart rate
        print(self.get_rate_line("Current rate", self._heart_rate))
        print(self.get_rate_line("Average rate", self._heart_rate))

        # refresh the screen
        
        # end curses
        curses.endwin()





        

def main():
    """Main function"""
    computer = HeartRateComputation()
    display = HeartRateDisplay()


    
    keyboard.add_hotkey("space", computer.step)
    while True:
        # continually update the screen with the heart rate and average heart rate
        # every 0.1 seconds
        # update the screen in the same line and overwrite the previous line
        display.set_heart_rate(computer.get_heart_rate())
        display.display()




if __name__ == "__main__":
    main()