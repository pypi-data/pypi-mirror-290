"""Tests the obisvalue classes."""

import math

from src.smartmeter_austria_energy.constants import PhysicalUnits
from src.smartmeter_austria_energy.obisvalue import ObisValueFloat, ObisValueString


def test_ObisvalueFloat():
    """Test the ObisValueFloat class."""
    # arrange
    my_raw_value : float = 12345

    my_Wh = 0x1E
    my_unit = PhysicalUnits(my_Wh)
    my_scale = -3

    # act
    my_obisvalue = ObisValueFloat(raw_value=my_raw_value, unit=my_unit, scale=my_scale)

    # assert
    assert my_obisvalue.RawValue == my_raw_value
    assert my_obisvalue.Scale == my_scale
    assert my_obisvalue.Unit == my_unit

    assert my_obisvalue.Value == my_raw_value * 10**my_scale
    assert my_obisvalue.ValueString == f"{my_obisvalue.Value} {my_obisvalue.Unit.name}"


def test_ObisvalueFloat_add_matching_unit():
    """Test the ObisValueFloat class add method."""
    # arrange
    my_raw_value1 : float = 1.1
    my_raw_value2 : float = 2.1

    my_Wh = 0x1E
    my_unit = PhysicalUnits(my_Wh)
    my_scale1 = 3
    my_scale2 = -1

    my_obisvalue1 = ObisValueFloat(raw_value=my_raw_value1, unit=my_unit, scale=my_scale1)
    my_obisvalue2 = ObisValueFloat(raw_value=my_raw_value2, unit=my_unit, scale=my_scale2)

    # act
    my_obisvalue = my_obisvalue1 + my_obisvalue2

    # assert
    assert my_obisvalue.Unit == my_unit

    assert my_obisvalue.Value == my_raw_value1 * 10**my_scale1 + my_raw_value2 * 10**my_scale2
    assert my_obisvalue.ValueString == f"{my_obisvalue.Value} {my_obisvalue.Unit.name}"


def test_ObisvalueFloat_sub_matching_unit():
    """Test the ObisValueFloat class subtract method."""
    # arrange
    my_raw_value1 : float = 1.1
    my_raw_value2 : float = 2.1

    my_Wh = 0x1E
    my_unit = PhysicalUnits(my_Wh)
    my_scale1 = 3
    my_scale2 = -1

    my_obisvalue1 = ObisValueFloat(raw_value=my_raw_value1, unit=my_unit, scale=my_scale1)
    my_obisvalue2 = ObisValueFloat(raw_value=my_raw_value2, unit=my_unit, scale=my_scale2)

    # act
    my_obisvalue = my_obisvalue1 - my_obisvalue2

    # assert
    assert my_obisvalue.Unit == my_unit

    assert my_obisvalue.Value == my_raw_value1 * 10**my_scale1 - my_raw_value2 * 10**my_scale2
    assert my_obisvalue.ValueString == f"{my_obisvalue.Value} {my_obisvalue.Unit.name}"


def test_ObisvalueFloat_add_not_matching_unit():
    """Test the ObisValueFloat class add method."""
    # arrange
    my_raw_value1 : float = 0.7
    my_raw_value2 : float = 6.23

    my_Wh = 0x1E
    my_W = 0x1B
    my_unit1 = PhysicalUnits(my_Wh)
    my_unit2 = PhysicalUnits(my_W)

    my_scale1 = -1
    my_scale2 = 4

    my_obisvalue1 = ObisValueFloat(raw_value=my_raw_value1, unit=my_unit1, scale=my_scale1)
    my_obisvalue2 = ObisValueFloat(raw_value=my_raw_value2, unit=my_unit2, scale=my_scale2)

    # act
    my_obisvalue = my_obisvalue1 + my_obisvalue2

    # assert
    assert my_obisvalue.Unit == PhysicalUnits.Undef
    assert math.isnan(my_obisvalue.Value)
    assert my_obisvalue.ValueString == f"{my_obisvalue.Value} {my_obisvalue.Unit.name}"


def test_ObisvalueFloat_sub_not_matching_unit():
    """Test the ObisValueFloat class subtract method."""
    # arrange
    my_raw_value1 : float = 1.1
    my_raw_value2 : float = 2.1

    my_Wh = 0x1E
    my_W = 0x1B
    my_unit1 = PhysicalUnits(my_Wh)
    my_unit2 = PhysicalUnits(my_W)

    my_scale1 = 1
    my_scale2 = 0

    my_obisvalue1 = ObisValueFloat(raw_value=my_raw_value1, unit=my_unit1, scale=my_scale1)
    my_obisvalue2 = ObisValueFloat(raw_value=my_raw_value2, unit=my_unit2, scale=my_scale2)

    # act
    my_obisvalue = my_obisvalue1 - my_obisvalue2

    # assert
    assert my_obisvalue.Unit == PhysicalUnits.Undef
    assert math.isnan(my_obisvalue.Value)
    assert my_obisvalue.ValueString == f"{my_obisvalue.Value} {my_obisvalue.Unit.name}"


def test_ObisvalueString():
    """Test the ObisValueString class."""
    # arrange
    my_raw_value : str = "Test_me"

    # act
    my_obisvalue = ObisValueString(raw_value=my_raw_value)

    # assert
    assert my_obisvalue.RawValue == my_raw_value
