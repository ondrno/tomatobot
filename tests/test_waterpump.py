from tomatobot import WaterPump
import pytest
from mock import MagicMock


@pytest.fixture(scope="function")
def device():
    dev = MagicMock()
    yield dev


@pytest.fixture(scope="function")
def wp(device):
    r = WaterPump(device, 5.0)
    yield r


class TestWaterPump:
    def test_init_calculates_min_level(self, device):
        buck_size = 5
        wp = WaterPump(device, 5.0)
        assert wp.bucket_size == buck_size
        assert wp.fill_level == buck_size
        assert wp._min_level == 0.5
        assert wp.water_out == 0
        assert wp.total_water_out == 0
        assert wp._water_throughput == 0.05

    def test_init_takes_min_level(self, device):
        buck_size = 5
        wp = WaterPump(device, 5.0, min_level=1.25)
        assert wp.bucket_size == buck_size
        assert wp.fill_level == buck_size
        assert wp._min_level == 1.25
        assert wp.water_out == 0
        assert wp.total_water_out == 0
        assert wp._water_throughput == 0.05

    def test_init_raises_exception_if_min_value_too_large(self, device):
        with pytest.raises(ValueError):
            WaterPump(device, 5.0, min_level=5.01)
