#!/usr/bin/env python3
from image_management import build_images, prepare_new_image_names, push_images
from notification_management import (
    notify_about_failed_build_and_terminate,
    notify_about_successful_build,
)
from repo_management import check_cloned_repo, clone_repo
from utils.arg_parsing import parse_args


def main() -> None:
    parse_args()
    try:
        clone_repo()
        check_cloned_repo()
        prepare_new_image_names()

        build_images()
        push_images()

        notify_about_successful_build()
    except Exception as e:
        notify_about_failed_build_and_terminate(f"Something unexpected went wrong; '{e}'")


if __name__ == "__main__":
    main()
