import sys
from parking_lot.command_processor import CommandProcessor


def main():
    processor = CommandProcessor()
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            for line in f:
                output = processor.process(line)
                if output:
                    print(output)
    else:
        print("Parking Lot System. Type 'exit' to quit.")
        while True:
            try:
                line = input("> ")
                if line.strip() == "exit":
                    print("Exiting.")
                    break
                output = processor.process(line)
                if output:
                    print(output)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break


if __name__ == "__main__":
    main()
