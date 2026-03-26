from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Static, Input, Button
from textual.reactive import reactive

from parking_lot.parking_lot import ParkingLot, ParkingLotFullError, DuplicateCarError, InvalidSlotError


class SlotWidget(Static):
    def __init__(self, slot_no, **kwargs):
        super().__init__(**kwargs)
        self.slot_no = slot_no
        self.car = None

    def update_slot(self, car=None):
        self.car = car
        if car:
            self.update(f"[b]{self.slot_no}[/b]\n{car.reg_no}\n{car.color}")
            self.add_class("occupied")
            self.remove_class("empty")
        else:
            self.update(f"[b]{self.slot_no}[/b]\n\nEMPTY")
            self.add_class("empty")
            self.remove_class("occupied")


class ParkingGrid(Container):
    pass


class MessageBar(Static):
    pass


class ParkingLotApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #top {
        height: auto;
        padding: 1 2;
    }

    #actions {
        height: auto;
        padding: 1 2;
    }

    Button {
        margin: 0 1;
        min-width: 20;
    }

    #input-area {
        height: auto;
        padding: 1 2;
    }

    Input {
        width: 100%;
    }

    ParkingGrid {
        layout: grid;
        grid-size: 4;
        grid-gutter: 1;
        padding: 1 2;
        height: 1fr;
    }

    SlotWidget {
        height: 5;
        content-align: center middle;
        text-align: center;
        border: solid $secondary;
    }

    SlotWidget.empty {
        background: $surface;
        color: $text-muted;
    }

    SlotWidget.occupied {
        background: $success 30%;
        color: $text;
        border: solid $success;
    }

    MessageBar {
        height: 3;
        padding: 1 2;
        background: $surface;
        color: $text;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    lot = reactive(None)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Create a parking lot to get started", id="top")
        yield Horizontal(
            Button("Create Lot", id="btn-create", variant="primary"),
            Button("Park Car", id="btn-park", variant="success"),
            Button("Remove Car", id="btn-leave", variant="error"),
            Button("Search", id="btn-search", variant="warning"),
            id="actions",
        )
        yield Input(placeholder="Enter command...", id="cmd-input")
        yield ParkingGrid(id="grid")
        yield MessageBar("Welcome! Click 'Create Lot' or type: create_parking_lot <n>", id="message")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_widget = self.query_one("#cmd-input", Input)
        if event.button.id == "btn-create":
            input_widget.value = "create_parking_lot "
            input_widget.focus()
        elif event.button.id == "btn-park":
            input_widget.value = "park "
            input_widget.focus()
        elif event.button.id == "btn-leave":
            input_widget.value = "leave "
            input_widget.focus()
        elif event.button.id == "btn-search":
            input_widget.value = "slot_numbers_for_cars_with_colour "
            input_widget.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value.strip()
        event.input.value = ""
        if not line:
            return
        self.run_command(line)

    def run_command(self, line):
        parts = line.split()
        command = parts[0]
        msg = self.query_one("#message", MessageBar)

        if command == "create_parking_lot":
            if len(parts) < 2:
                msg.update("Usage: create_parking_lot <capacity>")
                return
            n = int(parts[1])
            self.lot = ParkingLot(n)
            self.build_grid()
            msg.update(f"Created parking lot with {n} slots")
            self.query_one("#top").update(f"Parking Lot  —  {len(self.lot.slots)}/{self.lot.capacity} occupied")
        elif command == "park":
            if self.lot is None:
                msg.update("Create a parking lot first!")
                return
            if len(parts) < 3:
                msg.update("Usage: park <reg_no> <color>")
                return
            try:
                slot = self.lot.park(parts[1], parts[2])
                self.refresh_slot(slot)
                msg.update(f"Parked {parts[1]} ({parts[2]}) at slot {slot}")
            except ParkingLotFullError:
                msg.update("Sorry, parking lot is full!")
            except DuplicateCarError:
                msg.update(f"Car {parts[1]} is already parked!")
        elif command == "leave":
            if self.lot is None:
                msg.update("Create a parking lot first!")
                return
            if len(parts) < 2:
                msg.update("Usage: leave <slot_no>")
                return
            try:
                slot_no = int(parts[1])
                self.lot.leave(slot_no)
                self.refresh_slot(slot_no)
                msg.update(f"Slot {slot_no} is now free")
            except InvalidSlotError:
                msg.update(f"Slot {parts[1]} is already empty!")
        elif command == "registration_numbers_for_cars_with_colour":
            result = self.lot.get_registration_numbers_by_color(parts[1])
            msg.update(", ".join(result) if result else "Not found")
        elif command == "slot_number_for_registration_number":
            slot = self.lot.get_slot_number_by_reg_no(parts[1])
            msg.update(f"Slot {slot}" if slot is not None else "Not found")
        elif command == "slot_numbers_for_cars_with_colour":
            result = self.lot.get_slot_numbers_by_color(parts[1])
            msg.update(", ".join(str(s) for s in result) if result else "Not found")
        elif command in ("exit", "q", "quit"):
            self.exit()
            return
        else:
            msg.update(f"Unknown command: {command}")
            return

        if self.lot:
            self.query_one("#top").update(f"Parking Lot  —  {len(self.lot.slots)}/{self.lot.capacity} occupied")

    def build_grid(self):
        grid = self.query_one("#grid", ParkingGrid)
        grid.remove_children()
        for i in range(1, self.lot.capacity + 1):
            slot = SlotWidget(i)
            grid.mount(slot)
            slot.update_slot()

    def refresh_slot(self, slot_no):
        grid = self.query_one("#grid", ParkingGrid)
        for widget in grid.children:
            if isinstance(widget, SlotWidget) and widget.slot_no == slot_no:
                widget.update_slot(self.lot.slots.get(slot_no))
                break


def run():
    app = ParkingLotApp()
    app.run()


if __name__ == "__main__":
    run()
