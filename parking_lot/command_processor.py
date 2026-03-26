from parking_lot.parking_lot import ParkingLot, ParkingLotFullError


class CommandProcessor:
    def __init__(self):
        self.lot = None

    def process(self, line):
        parts = line.strip().split()
        if not parts:
            return None
        command = parts[0]

        if command == "create_parking_lot":
            self.lot = ParkingLot(int(parts[1]))
            return f"Created a parking lot with {parts[1]} slots"
        elif command == "park":
            try:
                slot = self.lot.park(parts[1], parts[2])
                return f"Allocated slot number: {slot}"
            except ParkingLotFullError:
                return "Sorry, parking lot is full"
        elif command == "leave":
            self.lot.leave(int(parts[1]))
            return f"Slot number {parts[1]} is free"
        elif command == "registration_numbers_for_cars_with_colour":
            result = self.lot.get_registration_numbers_by_color(parts[1])
            return ", ".join(result) if result else "Not found"
        elif command == "slot_number_for_registration_number":
            slot = self.lot.get_slot_number_by_reg_no(parts[1])
            return str(slot) if slot is not None else "Not found"
        elif command == "slot_numbers_for_cars_with_colour":
            result = self.lot.get_slot_numbers_by_color(parts[1])
            return ", ".join(str(s) for s in result) if result else "Not found"
        elif command == "exit":
            return None
        else:
            return "Unknown command"
