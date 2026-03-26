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
        while True:
            try:
                line = input()
                output = processor.process(line)
                if output:
                    print(output)
            except (EOFError, KeyboardInterrupt):
                break


if __name__ == "__main__":
    main()
