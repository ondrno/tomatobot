import time
from enum import IntEnum


class RelaisStatus(IntEnum):
    OFF = 0
    ON = 1


class Relais:
    def __init__(self, device):
        self._device = device
        self._status = RelaisStatus.OFF
        self._device.off()

        self._on_time = 0
        self._total_on_time = 0
        self._on_count = 0
        self.__timer_start = 0

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def on_count(self):
        return self._on_count

    @on_count.setter
    def on_count(self, value):
        self._on_count = value

    @property
    def total_on_time(self):
        return self._total_on_time

    @property
    def on_time(self):
        return self._on_time

    @on_time.setter
    def on_time(self, value):
        self._on_time = value

    @property
    def status(self):
        return self._status

    def reset_total_on_time(self):
        if self.status == RelaisStatus.OFF:
            self._total_on_time = 0

    def reset_on_count(self):
        if self.status == RelaisStatus.OFF:
            self.on_count = 0

    def on(self, duration: int = 0):
        if self.status == RelaisStatus.OFF:
            self.on_count += 1
            self.__timer_start = time.time()
            self._status = RelaisStatus.ON
            self._device.on()
            if duration:
                time.sleep(duration)

    def off(self, duration: int = 0):
        if self.status == RelaisStatus.ON:
            delta_seconds = time.time() - self.__timer_start
            self._device.off()
            self._status = RelaisStatus.OFF
            self.on_time = delta_seconds
            self._total_on_time += delta_seconds
            self.__timer_start = 0
            if duration:
                time.sleep(duration)
