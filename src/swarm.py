from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rig_comm.swarm import *  # noqa: F401,F403


if __name__ == "__main__":
    swarm = example_swarm()
    print(f"Predicted Success: {swarm.predicted_success():.3f}")
    print(f"Swarm Consensus: {swarm.swarm_consensus():.3f}")
    print(f"Trust Decay: {swarm.has_trust_decay()}")
