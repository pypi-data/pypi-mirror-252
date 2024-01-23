from argparse import Namespace
from pathlib import Path
from pprint import pformat

import tomli
from loguru import logger


def install(args: Namespace) -> None:
    link_defs_file = Path(args.INPUT_FILE)
    logger.info("Reading link definitions from {}", link_defs_file)
    with link_defs_file.open("rb") as inp:
        d = tomli.load(inp)
    logger.debug("d={}", pformat(d))
    dest_root: Path = args.destination.expanduser()
    logger.info("Will install the symlinks under {}", dest_root)
    for folder, _files in d.items():
        if isinstance(_files, dict):
            dest_subfolder, files = _files["dest"], _files["files"]
        else:
            dest_subfolder, files = "", _files
        if not files:
            files = ["."]

        logger.debug("folder:         {}", folder)
        logger.debug("files:          {}", files)
        logger.debug("dest_subfolder: {!r}", dest_subfolder)

        logger.info("Installing from folder {!r}", folder)
        for f in files:
            source: Path = (link_defs_file.parent / folder / f).resolve()
            dest = dest_root / dest_subfolder / (source.name if source.is_dir() else f)
            logger.debug("source:  {}", source)
            logger.debug("symlink: {}", dest)
            if args.include and not (args.include.search(str(source)) or args.include.search(str(dest))):
                logger.debug("source/dest does not match {}", args.include)
                continue
            logger.info("Checking if to create {}", dest)
            if dest.exists():
                if not dest.is_symlink():
                    logger.error(
                        ("{0} is not a symlink, will not touch; to compare, run:\n" "code --diff {1} {0}"),
                        dest,
                        source,
                    )
                    continue
                if not args.force:
                    logger.warning(
                        ("{} already exists (and points to {}), skipping " "(use --force to recreate)"),
                        dest,
                        dest.resolve(),
                    )
                    continue
                dest.unlink()
            dest.parent.mkdir(exist_ok=True, parents=True)
            dest.symlink_to(source)
            logger.success("Created {} -> {}", dest, source)
