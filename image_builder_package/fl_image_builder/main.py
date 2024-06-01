#!/usr/bin/env python3
from args_parser.main import parse_arguments_and_set_context


def main() -> None:
    context = parse_arguments_and_set_context()
    context.trigger_build_plan()


if __name__ == "__main__":
    main()
