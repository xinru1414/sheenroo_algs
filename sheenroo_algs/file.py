from io import TextIOWrapper
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List


def split(file: Path, max_lines: int) -> List[Path]:
    """
    This function split a file into multiple smaller ones.
    Args:
        file: a path to the file that needs to be split
        max_lines: max number of lines in each split file
    Returns:
        a list of paths to the split files
    """
    split_file_paths = []
    with open(file, 'rb') as fp_in:
        count = max_lines
        fp_out = None
        for line in fp_in:
            if count == max_lines:
                count = 0
                if fp_out:
                    fp_out.close()
                    split_file_paths.append(fp_out.name)
                fp_out = NamedTemporaryFile(delete=False)
            if count + 1 == max_lines and line[-1:] == b'\n':
                fp_out.write(line[:-1])
            else:
                fp_out.write(line)
            count += 1
    if fp_out:
        fp_out.close()
        split_file_paths.append(fp_out.name)

    return split_file_paths


# class Shuffler:
#     def __init__(self, fp: TextIOWrapper, sep=b'\n'):
#         self.fp = fp
#         self.sep = sep
#
#     def __iter__(self):
#         pass
#
#     def __index_file(self):
#         pass