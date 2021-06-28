from tomatobot import Relais, RelaisStatus, NoWaterExc


class WaterPump(Relais):
    """Implements a water pump controlled by a relay which is controlled by a gpio pin of a raspberry pi"""
    def __init__(self, device, buck_size: float, min_level: float = 0):
        super().__init__(device)

        self._bucket_size = buck_size   # in liter
        self._fill_level = buck_size    # remaining water in the bucket
        self._min_level = min_level     # if minimum level of water is reached pump will switch off
        if min_level > buck_size:
            raise ValueError("Min level must be smaller than the bucket size.")

        if not self._min_level:         # set default to 10% of the bucket size
            self._min_level = self._bucket_size * 0.1
        self._water_out = 0             # pumped water in liter after the latest pump interval
        self._total_water_out = 0       # total sum of pumped water in liter
        self._water_throughput = 0.05   # in liter per second

    @property
    def bucket_size(self):
        return self._bucket_size

    @property
    def water_out(self):
        return self._water_out

    @property
    def total_water_out(self):
        return self._total_water_out

    @property
    def fill_level(self):
        return self._fill_level

    @fill_level.setter
    def fill_level(self, value):
        self._fill_level = value

    def reset_fill_level(self) -> float:
        """
        Resets the fill level using the size of the bucket.

        :return: the value of the fill level
        """
        self._fill_level = self._bucket_size
        return self._fill_level

    def on(self, duration: int) -> None:
        """
        Switches the water pump on and wait afterwards for a certain duration.

        Before, it will checked if the bucket contains enough water to avoid
        that the pump runs dry.

        :param duration: time in seconds to wait after switching the pump on
        :return: None
        """
        expected_water_out = self._water_throughput * duration
        if self._fill_level - expected_water_out < self._min_level:
            raise NoWaterExc("Run out of water. Fill the bucket again.")
        super().on(duration)

    def off(self, duration: int) -> None:
        """
        Switches the water pump off and wait afterwards for a certain duration.
        After switching off the remaining water in the bucket in liter,
        the pumped water (in liter), and the total pumped water (in liter) is calculated.

        :param duration: time in seconds to wait after switching the pump off
        :return: None
        """
        if self.status == RelaisStatus.ON:
            super().off(duration)
            self._water_out = self._water_throughput * self.on_time
            self._total_water_out += self._water_out
            self._fill_level -= self._water_out


if __name__ == "__main__":
    import platform
    import argparse

    def play_sequence(switch_times: list):
        next_relais_status = RelaisStatus.ON
        for delay in switch_times:
            if next_relais_status % 2 == RelaisStatus.ON:
                print(f"Switch gpio at pin={args.io} ON for {delay} seconds.")
                s.on(delay)
            else:
                s.off(delay)
                print(f"Pump was on for {s.on_time:.2f} seconds, pumped {s.water_out:.2f}l of water. "
                      f"Switch it OFF for {delay} seconds.")
            next_relais_status += 1
        s.off(0)

    parser = argparse.ArgumentParser(
        description="Switch on/off a relais controlled by raspberry pi gpio"
    )
    parser.add_argument("--io", help="raspberry gpio to switch", type=int, default=17)
    parser.add_argument("--on_seq", help="a sequence of on/off times in seconds, e.g. 2;5;2;10 would switch it on "
                                         "for 2 seconds, off for 5 seconds, on for 2 seconds, off for 10 seconds",
                        type=str, default="5;1")
    parser.add_argument("--loop", help="if set to True the on_seq is played in a continuous loop", type=bool,
                        default=False)
    args = parser.parse_args()

    switch_times = []
    if args.on_seq:
        switch_times = [int(x) for x in str(args.on_seq).strip(";").split(";")]
        if len(switch_times) % 2 == 1:
            parser.exit(status=1, message="Wrong number of arguments")

    if platform.platform().find('armv6l'):
        # https://gpiozero.readthedocs.io/en/stable/
        from gpiozero import OutputDevice

        gpio_pin = OutputDevice(f"GPIO{args.io}", active_high=False)
    else:
        import mock
        gpio_pin = mock.MagicMock()

    s = WaterPump(gpio_pin, buck_size=2, min_level=1.5)

    if args.loop:
        loop_counter = 1
        while True:
            print(f"## play sequence #{loop_counter}")
            play_sequence(switch_times)
            loop_counter += 1
    else:
        play_sequence(switch_times)

    print(f"## summary: gpio at pin={args.io} was ON for {s.total_on_time:.2f} seconds.")
    print(f"## bucket size={s.bucket_size:.2f}l")
    print(f"## total water out={s.total_water_out:.2f}l")
    print(f"## remaining water={s.fill_level:.2f}l")
