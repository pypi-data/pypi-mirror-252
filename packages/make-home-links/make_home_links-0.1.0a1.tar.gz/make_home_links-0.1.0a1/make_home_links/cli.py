import re
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, BooleanOptionalAction, Namespace
from functools import partial
from pathlib import Path

from loguru import logger

from . import __version__ as VERSION
from .install import install
from .log import setup_logging

HELP_FORMATTER = ArgumentDefaultsHelpFormatter


def parse_args() -> Namespace:
    parser = ArgumentParser("make-home-links", formatter_class=HELP_FORMATTER)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("-q", "--quiet", action="store_true", help="Log less")
    parser.add_argument("-d", "--debug", action="store_true", help="Log more")
    parser.add_argument(
        "-l",
        "--log-root",
        help="Log root path (specify '' to suppress logging to a file)",
        type=lambda s: Path(s) if s else None,
        metavar="PATH",
        default="",
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Recreate links",
        action=BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "-t",
        "--destination",
        help="Link destination folder",
        type=Path,
        metavar="PATH",
        default="~",
    )
    parser.add_argument(
        "-i",
        "--include",
        help="Consider only paths matching only this regex",
        type=partial(re.compile, flags=re.IGNORECASE),
        metavar="REGEX",
    )
    parser.add_argument(
        "INPUT_FILE",
        help="Link definitions file",
        type=Path,
        metavar="PATH",
        default="link_defs.toml",
        nargs="?",
    )

    return parser.parse_args()


def cli() -> None:
    args = parse_args()
    setup_logging(args)
    logger.debug("args={}", args)
    install(args)
