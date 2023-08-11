import os
import sys
from pathlib import Path
from typing import List
from urllib.parse import unquote

### CONSTANTS
home_path: Path = Path.home()
config_path: Path = Path.joinpath(home_path, ".config")

dirs_file_path: str = str(Path.joinpath(config_path, "user-dirs.dirs"))
locale_file_path: str = str(Path.joinpath(config_path, "user-dirs.locale"))
bookmarks_path: str = str(Path.joinpath(config_path, "gtk-3.0", "bookmarks"))


def read_from_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        array = file.readlines()
        return [x for x in array if x != "\n"]


def write_to_file(filename: str, data: str, perm: str='a') -> None:
    with open(filename, perm) as file:
        file.write(data)


BOOKMARKS: List[str] = [unquote(x) for x in read_from_file(bookmarks_path)]
FOLDERS: List[str] = [x for x in read_from_file(dirs_file_path)]
NEW_BOOKMARKS: List[str] = []

os.rename(bookmarks_path, bookmarks_path + ".bak")
os.rename(dirs_file_path, dirs_file_path + ".bak")



def rename_folders():
    for line in FOLDERS:
        if not line.startswith("#"):
            params, value = line.split("=")
            rus_name = value.split("/")[1].replace('"', '').rstrip()
            eng_name = params.split("_")[1].strip().lower()
            if eng_name == "publicshare":
                eng_name = "share"
            new_line = f'{params}="$HOME/{eng_name}"'
            if os.path.exists(home_path / rus_name):
                os.rename(home_path / rus_name, home_path / eng_name)
            else:
                os.mkdir(home_path / eng_name)
            fix_bookmarks(rus_name, eng_name)
            write_to_file(dirs_file_path, new_line + "\n", "a")


def fix_bookmarks(rus, eng):
    for line in BOOKMARKS:
        if line.split("/")[-1].replace("\n", "") == rus: 
            new_line = line.replace(rus, eng)
            NEW_BOOKMARKS.append(new_line)
            


if __name__ == '__main__':
    if sys.platform != 'linux':
        raise SystemExit("Incorrect system platform. You need Linux.")
    rename_folders()

    write_to_file(locale_file_path, "en_US", "w")
    write_to_file(bookmarks_path, "".join(NEW_BOOKMARKS), "w")
