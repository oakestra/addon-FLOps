import argparse

from args_parser.common import Subparsers
from flops_utils.types import MLModelFlavor

DEVEL_HELP_TXT = """
Reuses special base images that already include the ML repo dependencies.
Intended for the development of the image builder.
Helps skip/reuse lengthy dependency resolutions, etc.
Only works if the provided repo_url has a matching dependency base image in Github.
"""


def prepare_fl_actors_argparsers(subparsers: Subparsers) -> None:
    fl_actors_parser = subparsers.add_parser(
        "fl_actors",
        help="command for FL actors image builds (e.g. learner, aggregator)",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    fl_actors_parser.add_argument(
        "repo_url", type=str, help="The URL of the GitHub repository."
    )
    fl_actors_parser.add_argument("ml_model_flavor", type=MLModelFlavor)
    fl_actors_parser.add_argument(
        "--use-devel-base-images",
        action="store_true",
        default=False,
        help=DEVEL_HELP_TXT,
    )
