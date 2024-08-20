import errno
import logging
import tempfile
from pathlib import Path as LocalPath
from typing import Any, BinaryIO, Optional, Union

import numpy as np
import psutil
from tqdm import tqdm

logger = logging.getLogger(__name__)

PathOrStr = Union[LocalPath, str]
FileHandleType = Union[tempfile.NamedTemporaryFile, BinaryIO]


class WipeFile:
    def __init__(self, fn: Optional[PathOrStr]):
        self.filename = LocalPath(fn) if fn is not None else None

    def exists(self) -> bool:
        if self.filename is None:
            return False
        else:
            return self.filename.exists()

    def unlink(self) -> None:
        if self.filename is not None:
            self.filename.unlink()

    def approx_path(self) -> LocalPath:
        if self.filename is None:
            return LocalPath(tempfile.TemporaryDirectory().name).parent
        else:
            return self.filename.parent

    def open(self, mode: str):
        if self.filename is None:
            temp_file = tempfile.NamedTemporaryFile(mode)
            return temp_file.__enter__()
        else:
            return self.filename.open(mode)

    def __str__(self):
        return "[Temporary file]" if self.filename is None else str(self.filename)


# A little wrapper to make mock testing easier...
def file_write(fh: Any, data: Any) -> None:
    fh.write(data)


def wipe_free_space(fn: Optional[PathOrStr]):
    fn = WipeFile(fn)
    if fn.exists():
        raise RuntimeError(f"The requested filename '{fn}' already exists.")

    fill_value_1 = 0xFF
    fill_value_2 = 0x00

    MiB = 1048576
    block_size = 64 * MiB
    data1 = np.full((block_size,), fill_value_1, dtype=np.uint8).tobytes()
    data2 = np.full((block_size,), fill_value_2, dtype=np.uint8).tobytes()
    data3 = np.random.randint(0, 0x100, size=(block_size,), dtype=np.uint8).tobytes()
    data = [data1, data2, data3]

    for i_pass in range(3):
        pass_data = data[i_pass]
        print(f"\nStarting pass #{i_pass+1} out of 3...")
        initial_free_space = psutil.disk_usage(str(fn.approx_path())).free
        # print(f"Initial free space = {initial_free_space / MiB} MiB")
        pbar = tqdm(total=initial_free_space, unit="B", unit_scale=True)
        if fn.exists():
            fn.unlink()
        try:
            with fn.open("wb") as fh:
                while True:
                    try:
                        file_write(fh, pass_data)
                        pbar.update(block_size)
                    except OSError as e:
                        if e.errno == errno.ENOSPC:
                            break
                        else:
                            raise

        finally:
            if fn.exists():
                fn.unlink()

    print(f"\nCompleted!")
