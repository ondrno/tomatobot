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
    def on_time(self):
        return self._on_time

    @on_time.setter
    def on_time(self, value):
        self._on_time = value

    @property
    def status(self):
        return self._status

    def reset_on_time(self):
        if self.status == RelaisStatus.OFF:
            self.on_time = 0

    def reset_on_count(self):
        if self.status == RelaisStatus.OFF:
            self.on_count = 0

    def on(self):
        if self.status == RelaisStatus.OFF:
            self.on_count += 1
            self.__timer_start = time.time()
            self._status = RelaisStatus.ON
            self._device.on()

    def off(self):
        if self.status == RelaisStatus.ON:
            delta_seconds = time.time() - self.__timer_start
            self._device.off()
            self._status = RelaisStatus.OFF
            self.on_time += delta_seconds
            self.__timer_start = 0


if __name__ == "__main__":
    def play_sequence(switch_times: list):
        next_relais_status = RelaisStatus.ON
        for delay in switch_times:
            if next_relais_status % 2 == RelaisStatus.ON:
                print(f"Switch gpio at pin={args.io} ON for {delay} seconds.")
                s.on()
            else:
                s.off()
                print(f"On for {s.on_time} seconds. Switch it OFF for {delay} seconds.")
            time.sleep(delay)
            next_relais_status += 1
        s.off()

    import mock
    import argparse
    # https://gpiozero.readthedocs.io/en/stable/
    # from gpiozero import OutputDevice

    parser = argparse.ArgumentParser(
        description="Switch on/off a relais controlled by raspberry pi gpio"
    )
    parser.add_argument("--io", help="raspberry gpio to switch", type=int, default=17)
    parser.add_argument("--on_seq", help="a sequence of on/off times in seconds, e.g. 2;5;2;10 would switch it on "
                                         "for 2 seconds, off for 5 seconds, on for 2 seconds, off for 10 seconds",
                        type=str, default="1")
    parser.add_argument("--loop", help="if set to True the on_seq is played in a continuous loop", type=bool,
                        default=False)
    args = parser.parse_args()

    switch_times = []
    if args.on_seq:
        switch_times = [int(x) for x in str(args.on_seq).strip(";").split(";")]
        if len(switch_times) % 2 == 1:
            parser.exit(status=-1, message="Wrong number of arguments")

    # gpio_pin = OutputDevice(args.io)
    gpio_pin = mock.MagicMock()
    s = Relais(gpio_pin)

    if args.loop:
        loop_counter = 1
        while True:
            print(f"## play sequence #{loop_counter}")
            play_sequence(switch_times)
            loop_counter += 1
    else:
        play_sequence(switch_times)

    print(f"## summary: gpio at pin={args.io} was ON for {s.on_time} seconds.")
