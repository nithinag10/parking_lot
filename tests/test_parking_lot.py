import pytest
from parking_lot.parking_lot import ParkingLot, ParkingLotFullError


def test_park_returns_nearest_slot():
    lot = ParkingLot(3)
    assert lot.park("KA-01-HH-1234", "White") == 1
    assert lot.park("KA-01-HH-9999", "White") == 2


def test_park_raises_when_full():
    lot = ParkingLot(1)
    lot.park("KA-01-HH-1234", "White")
    with pytest.raises(ParkingLotFullError):
        lot.park("KA-01-HH-9999", "Black")


def test_leave_frees_slot():
    lot = ParkingLot(3)
    lot.park("KA-01-HH-1234", "White")
    lot.park("KA-01-HH-9999", "Black")
    lot.leave(1)
    assert 1 not in lot.slots


def test_park_reuses_freed_slot():
    lot = ParkingLot(3)
    lot.park("KA-01-HH-1234", "White")
    lot.park("KA-01-HH-9999", "Black")
    lot.leave(1)
    assert lot.park("KA-01-PP-0001", "Red") == 1


def test_get_registration_numbers_by_color():
    lot = ParkingLot(3)
    lot.park("KA-01-HH-1234", "White")
    lot.park("KA-01-HH-9999", "White")
    lot.park("KA-01-PP-0001", "Black")
    assert lot.get_registration_numbers_by_color("White") == ["KA-01-HH-1234", "KA-01-HH-9999"]
    assert lot.get_registration_numbers_by_color("Blue") == []


def test_get_slot_number_by_reg_no():
    lot = ParkingLot(3)
    lot.park("KA-01-HH-1234", "White")
    assert lot.get_slot_number_by_reg_no("KA-01-HH-1234") == 1
    assert lot.get_slot_number_by_reg_no("UNKNOWN") is None


def test_get_slot_numbers_by_color():
    lot = ParkingLot(3)
    lot.park("KA-01-HH-1234", "White")
    lot.park("KA-01-HH-9999", "Black")
    lot.park("KA-01-PP-0001", "White")
    assert lot.get_slot_numbers_by_color("White") == [1, 3]
    assert lot.get_slot_numbers_by_color("Blue") == []
