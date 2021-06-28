class WaterPumpException(Exception):
    """Generic water pump exception"""
    pass


class NoWaterExc(WaterPumpException):
    """Raised when the pump run out of water, i.e. the bucket is empty """
    pass
