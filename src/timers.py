import math
import styles
from datetime import datetime, timedelta


def _create_timer_values(json):
    expiration = datetime.strptime(json["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
    remaining_time = expiration - datetime.utcnow()
    remaining_seconds = remaining_time.total_seconds()
    return expiration, remaining_time, remaining_seconds


class Timer:
    def __init__(self, timer, state, root, loop):
        self.timer = timer
        self.state = state
        self._root = root
        self._loop = loop

    def set_state(self, json):
        expiration, remaining_time, remaining_seconds = _create_timer_values(json)
        if remaining_seconds < 0:
            self.timer.set(str('00:00:00'))
            retry = 120000
        else:
            self.timer.set(str(remaining_time))
            retry = remaining_seconds * 1000.0 + 120000
        self.state.set(json['state'].capitalize())
        return round(retry), remaining_time

    def update_timer(self, remaining_time):
        remaining_time -= timedelta(seconds=1)
        seconds = remaining_time.total_seconds()
        if seconds <= 0:
            return
        else:
            self.timer.set(str(remaining_time).split(".")[0])
        self._root.after(1000, lambda: self.update_timer(remaining_time))
        self._root.after(1000, lambda: styles.enable_clickthrough(self._root))  # Required to maintain transparency

