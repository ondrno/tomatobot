from tomatobot import RelaisStatus, Relais
import pytest
import time
from mock import MagicMock


@pytest.fixture(scope="function")
def device():
    dev = MagicMock()
    yield dev


@pytest.fixture(scope="function")
def relais(device):
    r = Relais(device)
    yield r


class TestRelaisStatus:
    def test_relais_status_has_two_states(self):
        s = RelaisStatus
        assert s.OFF == 0
        assert s.ON == 1


class TestRelais:
    def test_init_sets_relais_to_off(self, device):
        s = Relais(device)
        assert s.status == RelaisStatus.OFF
        assert s.on_time == 0
        assert s.on_count == 0
        device.off.assert_called_once()

    def test_on(self, relais):
        relais.on()
        assert relais.status == RelaisStatus.ON
        assert relais.on_count == 1
        assert relais.on_time == 0

    def test_on_after_on(self, relais):
        relais.on()
        assert relais.status == RelaisStatus.ON
        assert relais.on_count == 1
        assert relais.on_time == 0
        relais.on()
        assert relais.status == RelaisStatus.ON
        assert relais.on_count == 1
        assert relais.on_time == 0

    def test_off_without_on(self, relais):
        relais.off()
        assert relais.status == RelaisStatus.OFF
        assert relais.on_count == 0
        assert relais.on_time == 0

    def test_off_after_on(self, relais):
        relais.on()
        time.sleep(0.1)
        relais.off()
        assert relais.status == RelaisStatus.OFF
        assert relais.on_count == 1
        assert relais.on_time > 0

    def test_reset_on_time_in_status_off_resets_counter(self, relais):
        relais.on_time = 10
        relais.reset_on_time()
        assert relais.on_time == 0

    def test_reset_on_time_in_status_on_does_nothing(self, relais):
        relais.on_time = 10
        relais.on()
        relais.reset_on_time()
        assert relais.on_time == 10

    def test_reset_on_count_in_status_off_resets_counter(self, relais):
        relais.on_count = 10
        relais.reset_on_count()
        assert relais.on_count == 0

    def test_reset_on_count_in_status_off_resets_counter(self, relais):
        relais.on()
        relais.on_count = 10
        relais.reset_on_count()
        assert relais.on_count == 10

