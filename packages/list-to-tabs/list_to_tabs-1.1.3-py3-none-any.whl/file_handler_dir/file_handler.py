from pathlib import Path


class file_handler_class:
    def __init__(
        self, src_file: Path, dest_dir: Path, output_file_name: str, batch_size: int
    ):
        self.i_src_file = src_file
        self.i_dest_dir = dest_dir
        self.i_output_file_name = output_file_name
        self.i_batch_size = batch_size

    def file_to_dict(self) -> dict:
        temp_dict = dict()
        with open(self.i_src_file, "r") as file:
            for line_num, line_content in enumerate(file):
                temp_dict[line_num] = str(line_content).strip()
        return temp_dict

    def create_new_file(self) -> Path:
        if not self.i_src_file.exists() and not self.i_dest_dir.is_dir():
            open(self.i_src_file, "a")
        else:
            pass
        return Path(
            "/home/simsjo/"
        )  # TODO: make this into a recursive function so that if filename exists, subfix w/ num

    def insert_into_file(self, insert_text: str):
        with open(f"{self.i_dest_dir}/{self.i_output_file_name}", "a") as file:
            file.write(insert_text)

    def text_transform(self, insert_host: str, insert_command: str) -> str:
        return f"title: {insert_host};; command: {insert_command} {insert_host}\n"

    # def get_subdirs(file_path: Path):
    #     list_of_dirs = [x for x in file_path.iterdir() if x.is_dir()]
    #     print(list_of_dirs)
