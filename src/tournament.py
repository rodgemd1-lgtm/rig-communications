from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rig_comm.tournament import *  # noqa: F401,F403
import rig_comm.tournament as _tournament


if __name__ == "__main__":
    _tournament._test_tournament()
