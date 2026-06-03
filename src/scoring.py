from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rig_comm.scoring import *  # noqa: F401,F403


if __name__ == "__main__":
    import json

    score = example_sarah_chen()
    gates = GateEngine.check_gates(
        score,
        "Your team is spending 40% of engineering hours on architecture maintenance.",
    )

    print(json.dumps(score.to_dict(), indent=2))
    print("\n=== GATE CHECK ===")
    print(json.dumps(gates, indent=2))
