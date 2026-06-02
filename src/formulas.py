from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rig_comm.formulas import *  # noqa: F401,F403
import rig_comm.formulas as _formulas


if __name__ == "__main__":
    _formulas._test_all_formulas()
