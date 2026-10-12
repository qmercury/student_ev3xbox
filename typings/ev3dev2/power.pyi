class PowerSupply:
    measured_volts: float
    measured_amps: float
    measured_voltage: int
    measured_current: int
    def __init__(self, address = ..., name_pattern: str = ..., name_exact: bool = ..., **kwargs) -> None: ...
