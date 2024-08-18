from fire import Fire

from rpyt import (
    create_crowdin_inputs,
    read_common,
    read_dialogue,
)


class PyTools:
    read_common = staticmethod(read_common)
    read_dialogue = staticmethod(read_dialogue)
    create_crowdin_inputs = staticmethod(create_crowdin_inputs)


def main():
    Fire(PyTools)


if __name__ == "__main__":
    main()
