import argparse
import logging
import traceback
from pathlib import Path as LocalPath
from typing import Union

from .core import wipe_free_space

logger = logging.getLogger(__name__)

PathOrStr = Union[LocalPath, str]


def main(args):
    try:
        print()
        print("WARNING/LIMITATIONS: this simple utility performs 3 passes to write and fill")
        print("available free space.  It is not exhaustive.  It does not wipe filenames that were used")
        print("in the past and file and directory names may still be recoverable- and other data might")
        print("be recoverable as well.")
        print()
        print("After filling available space, the temporary file is deleted.")
        print()
        parser = argparse.ArgumentParser(
            description="Simple utility for filling unused disk space to prevent deleted file recovery"
        )
        parser.add_argument(
            "--filename",
            type=str,
            default=None,
            help="Filename/path to create, which also specifies the disk to fill.  Default: temporary file.",
        )
        parser.add_argument("-v", "--v", action="store_true", help="Increase verbosity.")
        args = parser.parse_args(args)

        if args.v:
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.DEBUG)
            logging.getLogger().setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logger.debug(f"Debug-level verbosity enabled.")

        wipe_free_space(args.filename)

    except Exception as ex:
        print(str(ex))
        logger.error(traceback.format_exc())
