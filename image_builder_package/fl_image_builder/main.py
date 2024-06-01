#!/usr/bin/env python3
from args_parser.main import parse_arguments_and_set_context
from flops_utils.logging import logger
from notification_management import (
    notify_about_failed_build_and_terminate,
    notify_about_successful_builder_process,
)
from utils.timeframes import FULL_BUILDER_PROCESS_TIMEFRAME


def main() -> None:
    context = parse_arguments_and_set_context()
    context.timer.start_new_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    try:
        context.trigger_build_plan()
        notify_about_successful_builder_process()
        context.timer.end_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    except Exception as e:
        msg = "Something unexpected went wrong"
        logger.exception(msg)
        notify_about_failed_build_and_terminate(f"{msg}; '{e}'")


if __name__ == "__main__":
    main()
