from pathlib import Path


class file_handler_class:

    @staticmethod
    def file_to_dict(input_file: Path) -> dict:
        temp_dict = dict()
        with open(input_file, "r") as file:
            for line_num, line_content in enumerate(file):
                temp_dict[line_num] = str(line_content).strip()
        return temp_dict

    @staticmethod
    def create_new_file(input_file: Path, dest_dir: Path) -> Path:
        if not input_file.exists() and not dest_dir.is_dir():
            open(input_file, "a")
        else:
            pass
        return Path(
            ""
        )  # TODO: make this into a recursive function so that if filename exists, subfix w/ num

    @staticmethod
    def insert_into_file(dest_dir: Path, output_file: str, insert_text: str):
        with open(f"{dest_dir}/{output_file}", "a") as file:
            file.write(insert_text)

    @staticmethod
    def text_transform(insert_host: str, insert_command: str) -> str:
        return f"title: {insert_host};; command: {insert_command} {insert_host}\n"

    # def get_subdirs(file_path: Path):
    #     list_of_dirs = [x for x in file_path.iterdir() if x.is_dir()]
    #     print(list_of_dirs)
