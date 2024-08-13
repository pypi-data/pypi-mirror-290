"""Defines the OBIS objects."""


class Obis:
    def to_bytes(code):
        return bytes([int(a) for a in code.split(".")])

    VoltageL1 = to_bytes("01.0.32.7.0.255")
    VoltageL2 = to_bytes("01.0.52.7.0.255")
    VoltageL3 = to_bytes("01.0.72.7.0.255")
    CurrentL1 = to_bytes("1.0.31.7.0.255")
    CurrentL2 = to_bytes("1.0.51.7.0.255")
    CurrentL3 = to_bytes("1.0.71.7.0.255")
    RealPowerIn = to_bytes("1.0.1.7.0.255")
    RealPowerOut = to_bytes("1.0.2.7.0.255")
    RealEnergyIn = to_bytes("1.0.1.8.0.255")
    RealEnergyOut = to_bytes("1.0.2.8.0.255")
    ReactiveEnergyIn = to_bytes("1.0.3.8.0.255")
    ReactiveEnergyOut = to_bytes("1.0.4.8.0.255")
    Factor = to_bytes("01.0.13.7.0.255")
    DeviceNumber = to_bytes("0.0.96.1.0.255")
    LogicalDeviceNumber = to_bytes("0.0.42.0.0.255")
