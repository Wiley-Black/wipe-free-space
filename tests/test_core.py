import errno
from unittest.mock import patch

import wipe_free_space.core


def test_core():

    write_history = []
    write_count = 0

    def update_write_count(*args, **kwargs):
        nonlocal write_history, write_count
        write_count += 1
        write_history.append(write_count)
        if write_count == 3:
            write_count = 0
            raise OSError(errno.ENOSPC, "ENOSPC")

    with patch("wipe_free_space.core.file_write") as mocked:
        mocked.side_effect = update_write_count
        wipe_free_space.core.wipe_free_space(None)

    assert write_history == [1, 2, 3, 1, 2, 3, 1, 2, 3]
