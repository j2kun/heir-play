from pathlib import Path
import os
import shlex
import subprocess

from IPython.core.magic import Magics
from IPython.core.magic import cell_magic
from IPython.core.magic import magics_class


HEIR_OPT_URL = "https://github.com/google/heir/releases/download/nightly/heir-opt"


def abort_cleanup():
    cwd = Path(dir=os.getcwd())
    tmpfile = cwd / "heir-opt"
    os.remove(tmpfile)


def load_nightly() -> Path:
    """Fetches the nightly heir-opt binary from GitHub and returns the path to it."""
    print("Loading heir-opt nightly binary")
    # TODO: how to clean up the tmpdir after ipython closes?
    # At worst, the user will see this in their heir_play dir and delete it.
    cwd = Path(dir=os.getcwd())
    tmpfile = cwd / "heir-opt"
    if os.path.isfile(tmpfile):
        print("Using existing local heir-opt")
        return tmpfile

    # -L follows redirects, necessary for GH asset downloads
    proc = subprocess.run(["curl", "-L", "-o", tmpfile, HEIR_OPT_URL])
    if proc.returncode != 0:
        print("Error downloading heir-opt")
        print(proc.stderr)
        return None

    proc = subprocess.run(["chmod", "a+x", tmpfile])
    if proc.returncode != 0:
        print("Error modifying permissions on heir-opt")
        print(proc.stderr)
        abort_cleanup()
        return None

    return tmpfile


@magics_class
class HeirOptMagic(Magics):
    def __init__(self, shell, binary_path="heir-opt"):
        """
        Initialize heir-opt with a path to the heir-opt binary.
        If not specified, will assume heir-opt is on the path.
        """
        super(HeirOptMagic, self).__init__(shell)
        self.binary_path = binary_path

    @cell_magic
    def heir_opt(self, line, cell):
        """
        Run heir-opt on the input cell.

        Args:
            line: The options to pass to heir-opt.
            cell: The input to pass to heir-opt.
        """
        print("Running heir-opt...")
        completed_process = subprocess.run(
            [self.binary_path] + shlex.split(line), input=cell, text=True
        )
        if completed_process.returncode != 0:
            print("Error running heir-opt")
            print(completed_process.stderr)
            return
        output = completed_process.stdout
        print(output)
