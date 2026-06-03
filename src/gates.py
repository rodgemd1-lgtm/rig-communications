from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rig_comm.gates import *  # noqa: F401,F403
import rig_comm.gates as _gates


if __name__ == "__main__":
    _gates._test_gates()
