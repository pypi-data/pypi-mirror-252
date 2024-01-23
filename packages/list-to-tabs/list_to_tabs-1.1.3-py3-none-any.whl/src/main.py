#!/usr/bin/python3

import argparse
import sys
from pathlib import Path
from file_handler_dir.file_handler import file_handler_class


def main():
    parser = argparse.ArgumentParser(
        description="Splits single newline seperated host "
        "file into Konsole tab batches",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("src", help="fully qualified path to host list - /path/to/list")
    parser.add_argument(
        "dest", help="fully qualified path to output dir - /path/to/output_dir"
    )
    parser.add_argument(
        "-b", "--batch", default=6, help="set number of hosts per batch - default is 6"
    )
    parser.add_argument(
        "-n", "--name", default="batch", help="set name of batches - default is batch"
    )

    passed_args = vars(parser.parse_args())

    src_file_path = Path(passed_args["src"])
    dest_dir_path = Path(passed_args["dest"])
    output_name = str(passed_args["name"])
    batch_size = int(passed_args["batch"])

    # TESTING
    # src_file_path = Path("/home/simsjo/server.list")
    # dest_dir_path = Path("/home/simsjo")
    # output_name = str("batch")
    # batch_size = int(6)

    # TODO: refactor this to utilize "Path" from pathlib
    if not (src_file_path.is_file()) or not (dest_dir_path.is_dir()):
        print("Source or Destination not reachable")
        sys.exit()

    file_obj = file_handler_class(src_file_path, dest_dir_path, output_name, batch_size)
    file_dict = file_obj.file_to_dict()

    print(file_dict.values())
    print(len(file_dict))

    file_dict = {
        host: file_obj.text_transform(file_dict[host], "ssh") for host in file_dict
    }

    for item in file_dict.values():
        file_obj.insert_into_file(item)

    for item in file_dict.items():
        print(item)
    # TODO: need to check this prior to appending to file so that it can be incremented
    # print(file_handler_dir.check_if_file(des_file))


if __name__ == "__main__":
    main()
