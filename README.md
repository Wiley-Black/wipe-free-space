# wipe-free-space
A simple program for filling free disk space with random data to "prevent" recovery of deleted files.

WARNING: this program is not exhaustive!  People have put a lot of thought into data deletion and recovery in the past and this program isn't it.  It's a quick and simple program for "probably" protecting data that
was deleted.

This program writes a temporary file until the disk is full.  The file contains the byte value 0xFF, all ones, throughout the file.  It then deletes the file and does it again with all zeros.  Finally, it writes a third temporary file with random values.

This tool definitely does not protect in that:

- The filenames and directory names that have been deleted would still be recoverable.
- It only wipes free space on the disk.  Existing files aren't touched.

The latest Windows executable is available [here](dist/wipe_free_space.exe).
