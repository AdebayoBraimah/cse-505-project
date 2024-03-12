#!/usr/bin/env python3
"""Renames any file with the corresponding information for file submission.
"""
import os
import sys
import shutil
import argparse

from typing import Any, Dict, List, Optional, Tuple, Union


def main() -> None:
    """Main function

    Raises:
        RuntimeError: Raised if ``file`` is empty or is ``None``.
    """
    parser = arg_parser()
    args = parser.parse_args()

    # Print help message in the case of no arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        args: Dict[str, Any] = vars(args)

    # Get variable names
    file: str = args.get("file")
    first_name: str = args.get("first_name")
    last_name: str = args.get("last_name")
    id_num: int = args.get("id_num")
    extra: Tuple[Union[int, str]] = args.get("extra")
    copy: bool = args.get("copy")

    if (file is None) or (file == ""):
        raise RuntimeError(
            f"'-f', '--file' option must be specified, and cannot be empty."
        )

    # Rename
    rename_file_submission(
        file=file,
        first_name=first_name,
        last_name=last_name,
        id_num=id_num,
        copy=copy,
        extra=extra,
    )
    return None


def file_parts(file: str) -> Tuple[str, str, str]:
    """Similar to MATLAB's ``fileparts`` function.
    Splits a full filename into:
        * file path
        * filename (no file path, no file extension)
        * file extension

    Args:
        file: Input file filename.

    Returns:
        Tuple:
            * file path
            * filename (no file path, no file extension)
            * file extension
    """
    file: str = os.path.abspath(file)

    # Extract and organize strings
    filepath: str
    ext: str
    _filename: str

    filepath, _filename = os.path.split(file)
    _, ext = os.path.splitext(file)
    filename: str = _filename[: -len(ext)]

    return filepath, filename, ext


def rename_file_submission(
    file: str,
    first_name: str,
    last_name: str,
    id_num: int,
    copy: bool = False,
    extra: Optional[Union[str, List[str], Tuple[str, ...]]] = None,
) -> str:
    """Renames file with the input information.

    Args:
        file: Input file name
        first_name: First name
        last_name: Last name
        id_num: Student ID number
        copy: Copies file with the corresponding output filename, rather than renaming input file. Defaults to None.
        extra: Extra information to append to filename, specified as either a string, list or n-tuple. Defaults to None.

    Returns:
        Output filename
    """
    file: str = os.path.abspath(file)

    # Input checks
    id_num: int = int(id_num)

    # Extract filename details
    filepath: str
    ext: str

    filepath, _, ext = file_parts(file=file)

    # Rename or copy file
    filename: str = f"{first_name}_{last_name}_{id_num}"

    if extra is not None:

        if isinstance(extra, str):
            filename: str = f"{filename}_{extra}"

        if (isinstance(extra, tuple)) or (isinstance(extra, list)):
            for item in _flatten(extra):
                filename: str = f"{filename}_{item}"

    outname: str = os.path.join(filepath, filename + ext)

    if copy:
        shutil.copy2(file, outname, follow_symlinks=True)
    else:
        os.rename(file, outname)

    return outname


def _flatten(in_list) -> List[str]:
    """Helper function to flatten nested lists into one list.

    Args:
        in_list: Input nested list.

    Returns:
        Flattened list.
    """
    return [x for xs in in_list for x in xs]


def arg_parser() -> argparse.ArgumentParser:
    """Command line interface (CLI) argument parser.

    Returns:
       Argument parser object.
    """
    # Init parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=55, width=100
        ),
        # , formatter_class=argparse.RawTextHelpFormatter)
    )

    # Parse Arguments
    reqoptions = parser.add_argument_group("Required Arguments")

    reqoptions.add_argument(
        "-f",
        "--file",
        dest="file",
        type=str,
        metavar="<STR>",
        default=None,
        help="REQUIRED: Input file to be renamed.",
    )

    optoptions = parser.add_argument_group("Optional Arguments")

    optoptions.add_argument(
        "--first" "--first-name",
        dest="first_name",
        type=str,
        metavar="<STR>",
        default="Adebayo",
        help="OPTIONAL: First name.",
    )

    optoptions.add_argument(
        "--last" "--last-name",
        dest="last_name",
        type=str,
        metavar="<STR>",
        default="Braimah",
        help="OPTIONAL: Last name.",
    )

    optoptions.add_argument(
        "--ID" "--ID-num",
        dest="id_num",
        type=int,
        metavar="<INT>",
        default=115099306,
        help="OPTIONAL: ID number.",
    )

    optoptions.add_argument(
        "-e",
        "--extra",
        dest="extra",
        default=None,
        action="append",
        nargs="+",
        metavar="<INT or STR> ...",
        help="OPTIONAL: Additional/Extra information to be appended to output filename. \
            \nNOTE: Can be specified multiple times.",
    )

    optoptions.add_argument(
        "-c",
        "--copy",
        dest="copy",
        default=False,
        action="store_true",
        help="OPTIONAL: Copy input file to a new file name, rather than renaming.",
    )

    # args: argparse.ArgumentParser.parse_args = parser.parse_args()

    return parser


if __name__ == "__main__":
    main()
