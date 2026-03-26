from parking_lot.models import Car


class ParkingLotFullError(Exception):
    pass


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = {}

    def park(self, reg_no, color):
        for i in range(1, self.capacity + 1):
            if i not in self.slots:
                self.slots[i] = Car(reg_no, color)
                return i
        raise ParkingLotFullError

    def leave(self, slot_no):
        del self.slots[slot_no]

    def get_registration_numbers_by_color(self, color):
        return [car.reg_no for car in self.slots.values() if car.color == color]

    def get_slot_number_by_reg_no(self, reg_no):
        for slot, car in self.slots.items():
            if car.reg_no == reg_no:
                return slot
        return None

    def get_slot_numbers_by_color(self, color):
        return [slot for slot, car in self.slots.items() if car.color == color]
