#!/usr/bin/env python3
from args_parser.main import parse_arguments_and_execute
from context.main import get_context
from image_management import build_images, prepare_new_image_names, push_images
from notification_management import (
    notify_about_failed_build_and_terminate,
    notify_about_successful_builder_process,
)
from repo_management import check_cloned_repo, clone_repo
from utils.timeframes import BUILD_PREPARATION_TIMEFRAME, FULL_BUILDER_PROCESS_TIMEFRAME


def main() -> None:
    parse_arguments_and_execute()
    builder_context = get_context()
    builder_context.timer.start_new_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    try:
        builder_context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
        clone_repo()
        check_cloned_repo()
        prepare_new_image_names()
        builder_context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
        build_images()
        push_images()
        builder_context.timer.end_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
        notify_about_successful_builder_process()
    except Exception as e:
        notify_about_failed_build_and_terminate(
            f"Something unexpected went wrong; '{e}'"
        )


if __name__ == "__main__":
    main()
