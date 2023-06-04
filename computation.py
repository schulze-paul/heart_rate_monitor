
import time

class ButtonPress:
    """Class for button press event"""

    def __init__(self, time, button):
        self.time = time
        self.button = button

class HeartRateComputation:
    """Class for heart rate monitor"""

    def __init__(self):
        self._button_presses = []
        self._heart_rate = 0
        self._heart_rate_list = []

    def add_button_press(self, button_press):
        """Add button press event"""
        self._button_presses.append(button_press)

    def get_heart_rate(self):
        """Calculate heart rate"""
        if len(self._button_presses) < 2:
            return 0
        else:
            self._heart_rate = 60 / (self._button_presses[-1].time - self._button_presses[-2].time)
            self._heart_rate_list.append(self._heart_rate)
            return self._heart_rate

    def get_average_heart_rate(self):
        """Calculate average heart rate"""
        if len(self._heart_rate_list) == 0:
            return 0
        else:
            # compute the average hearth rate with earlier measurements
            # having less weight
            weights = [0.5 ** i for i in range(len(self._heart_rate_list))]
            return sum([weight * heart_rate for weight, heart_rate in zip(weights, self._heart_rate_list)]) / sum(weights)
    
    def step(self):
        self.add_button_press(ButtonPress(time.time(), "space"))