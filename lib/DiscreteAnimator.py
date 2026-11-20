import random

from typing import Any, Callable, List
from enum import Enum


class Repeat_Mode(Enum):
    """Enumeration of available repeat modes."""
    ONCE = 0
    REPEAT = 1


class DiscreteAnimator:
    """Animates through a sequence of discrete values over time."""

    def __init__(
        self,
        values: List[Any],
        interval: float,  # Time interval (e.g., 3 seconds)
        repeat_mode: Repeat_Mode,
        value_update_callback: Callable[[Any], None] = None,
    ):
        """
        Args:
            values (List[Any]): The list of discrete values (e.g., [True, False]).
            interval (float): The time interval in seconds before switching values.
            repeat_mode (Repeat_Mode): Whether to repeat indefinitely or stop after one cycle.
            value_update_callback (Callable[[Any], None]): Function to call when value updates.
        """
        self._values = values
        self._interval = interval  # Time to wait before picking a new random value
        self._repeat_mode = repeat_mode
        self._value_update_callback = value_update_callback
        self._anim_time = 0.0
        self._done = False

        self._current_value = random.choice(self._values)  # Pick first random value

        if self._value_update_callback:
            self._value_update_callback(self._current_value)

    def tick(self, delta_time: float):
        """Advances time and selects a new random value every `interval` seconds."""
        if self._done:
            return

        self._anim_time += delta_time

        if self._anim_time >= self._interval:
            self._anim_time = 0  # Reset timer
            new_value = random.choice(self._values)  # Pick a new random value

            # Only update if the new value is different
            if new_value != self._current_value:
                self._current_value = new_value
                if self._value_update_callback:
                    self._value_update_callback(self._current_value)

        # Stop after one cycle if Repeat_Mode is ONCE
        if self._repeat_mode == Repeat_Mode.ONCE:
            self._done = True

    def is_done(self) -> bool:
        """Returns True if animation is finished."""
        return self._done

    def get_value(self):
        """Returns the current value."""
        return self._current_value
