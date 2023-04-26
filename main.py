import os
import sys
from pathlib import Path


def rename_folders():
    home_path = Path.home()
    dirs_file_path = home_path / ".config" / "user-dirs.dirs"
    dirs_file_back = home_path / ".config" / "user-dirs.back"
    locale_file_path = home_path / ".config" / "user-dirs.locale"

    with open(dirs_file_path, "r") as dirs_file:
        lines = dirs_file.readlines()
    os.rename(dirs_file_path, dirs_file_back)
    for line in lines:
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
            with open(dirs_file_path, "a") as dirs_file:
                dirs_file.write(new_line + "\n")

    with open(locale_file_path, "w") as locale_file:
        locale_file.write("en_US\n")


if __name__ == '__main__':
    if sys.platform != 'linux':
        raise SystemExit("Incorrect system platform. You need Linux.")
    rename_folders()
