#!/usr/bin/python3

import argparse
import pathlib
import sys
import pkg_resources
from file_handler_dir.file_handler import file_handler_class


def main():

    # Dynamically get version from setup
    __version__ = pkg_resources.require("list-to-tabs")[0].version


    parser = argparse.ArgumentParser(
        description="Splits single newline seperated host "
        "file into Konsole tab batches",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v", "--version",
        help="get current package version",
        action='version',
        version='%(prog)s ' + __version__
    )
    parser.add_argument(
        "src",
        help="fully qualified path to host list - /path/to/list",
        type=pathlib.Path
    )
    parser.add_argument(
        "dest",
        help="fully qualified path to output dir - /path/to/output_dir",
        type=pathlib.Path
    )
    parser.add_argument(
        "-b", "--batch",
        default=(sys.maxsize / 2),
        help="set number of hosts per batch - default is entire file",
        type=int
    )
    parser.add_argument(
        "-n", "--name",
        default="batch",
        help="set name of batches - default is batch",
        type=str
    )

    passed_args = vars(parser.parse_args())

    src_file_path = passed_args["src"]
    dest_dir_path = passed_args["dest"]
    output_name = passed_args["name"]

    # Currently unimplemented
    # batch_size = passed_args["batch"]

    if not (src_file_path.is_file()) or not (dest_dir_path.is_dir()):
        print("Source or Destination not reachable")
        sys.exit()

    file_obj = file_handler_class()
    file_dict = file_obj.file_to_dict(src_file_path)

    # TODO: this prints will need to be removed
    print(file_dict.values())

    file_dict = {
        host: file_obj.text_transform(file_dict[host], "ssh") for host in file_dict
    }

    for item in file_dict.values():
        file_obj.insert_into_file(dest_dir_path, output_name, item)

    for item in file_dict.items():
        print(item)
    # TODO: need to check this prior to appending to file so that it can be incremented
    # print(file_handler_dir.check_if_file(des_file))


if __name__ == "__main__":
    main()
