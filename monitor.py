from time import monotonic
from textual import events
from textual._types import WatchCallbackType

from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.dom import DOMNode
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Header, Footer, Static, Label

class RateDisplay(Static):
    
    count = reactive(0)
    times = []

    def _on_mount(self) -> None:
        """Event handler when the widget is added."""
        self.update("Current: 0\nAverage: 0")

    def add_press(self) -> None:
        self.count += 1
        self.times.append(monotonic())
        current_rate = 60 / (self.times[-1] - self.times[-2]) if len(self.times) > 1 else 0
        average_rate = sum([60 / (self.times[i] - self.times[i-1]) for i in range(1, len(self.times))]) / (len(self.times) - 1) if len(self.times) > 1 else 0 
        self.update(f"Current: {round(current_rate)} bpm \nAverage: {round(average_rate)} bpm")

    def reset(self) -> None:
        self.count = 0
        self.times = []
        self.update("Current: 0 bpm\nAverage: 0 bpm")

class HeartRateMonitor(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler when button is pressed."""
        id = event.button.id
        counter = self.query_one(RateDisplay)

        if id == "beat":
            counter.add_press()
            self.add_class("started")
        elif id == "reset":
            counter.reset()
            self.remove_class("started")

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Button("Beat", id="beat", variant="default")
        yield Button("Reset", id="reset", variant="error")
        yield RateDisplay()

    
    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""

        key = event.key
        if key == "space":
            counter = self.query_one(RateDisplay)
            counter.add_press()
            self.add_class("started")
        elif key == "r":
            counter = self.query_one(RateDisplay)
            counter.reset()
            self.remove_class("started")


class HeartrateApp(App):

    CSS_PATH = "monitor.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        """Create child widget for the app."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(HeartRateMonitor())
        
    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = HeartrateApp()
    app.run()