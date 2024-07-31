from IPython.core.magic import StatefulMagics
from IPython.core.magic import cell_magic
from IPython.core.magic import magics_class


@magics_class
class HeirOptMagic(StatefulMagics):
    def __init__(self, shell, binary_path = "heir-opt"):
        """
        Initialize heir-opt with a path to the heir-opt binary.
        If not specified, will assume heir-opt is on the path.
        """
        super(StatefulMagics, self).__init__(shell)
        self.binary_path = binary_path

    @cell_magic
    def heir_opt(self, line):
        print("Running heir-opt")
        return line
