from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from sheenroo_algs.file import split


def test_happy_case_1():
    with NamedTemporaryFile() as test_input:
        # setup test input file
        test_input.write(b"line1\n")
        test_input.write(b"line2\n")
        test_input.write(b"line3")
        test_input.flush()

        # execute the function
        output_paths = split(file=Path(test_input.name), max_lines=1)

        # verify correctness
        assert len(output_paths) == 3
        assert open(output_paths[0], 'rb').read() == b"line1"
        assert open(output_paths[1], 'rb').read() == b"line2"
        assert open(output_paths[2], 'rb').read() == b"line3"

        for


def test_happy_case_2():
    with NamedTemporaryFile() as test_input:
        # setup test input file
        test_input.write(b"line1\n")
        test_input.write(b"line2\n")
        test_input.write(b"line3")
        test_input.flush()

        # execute the function
        output_paths = split(file=Path(test_input.name), max_lines=2)

        # verify correctness
        assert len(output_paths) == 2


def test_even_split():
    with NamedTemporaryFile() as test_input:
        # setup test input file
        test_input.write(b"line1\n")
        test_input.write(b"line2\n")
        test_input.write(b"line3\n")
        test_input.write(b"line4")
        test_input.flush()

        # execute the function
        output_paths = split(file=Path(test_input.name), max_lines=2)

        # verify correctness
        assert len(output_paths) == 2
