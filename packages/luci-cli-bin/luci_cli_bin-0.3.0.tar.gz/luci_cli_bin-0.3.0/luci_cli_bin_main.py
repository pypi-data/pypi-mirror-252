import os
import sys
import sysconfig
import pathlib

THISDIR = pathlib.Path(__file__).resolve().parent

def find_bin() -> str:
    bin_name = pathlib.Path(sys.argv[0]).name
    exe = bin_name + sysconfig.get_config_var("EXE")

    path = THISDIR.joinpath("luci_cli_bin", exe)
    if os.path.isfile(path):
        return path

    raise FileNotFoundError(path)


def main():
    bin = os.fsdecode(find_bin())
    if sys.platform == "win32":
        import subprocess

        completed_process = subprocess.run([bin, *sys.argv[1:]])
        sys.exit(completed_process.returncode)
    else:
        os.execvp(bin, [bin, *sys.argv[1:]])


if __name__ == "__main__":
    main()

