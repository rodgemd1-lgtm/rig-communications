{
  "name": "comm-pipeline",
  "version": "1.0",
  "description": "Signal → Tournament → Ensemble Draft → Score → Swarm → Gate → Ship/Learn",
  "steps": [
    {"name": "signal", "action": "set", "values": {"signal_card": "SignalCard"}},
    {"name": "tournament", "action": "set", "values": {"angle_card": "AngleCard"}},
    {"name": "ensemble_draft", "action": "set", "values": {"draft": "Draft"}},
    {"name": "score", "action": "evaluate", "input": "draft", "channel": "email", "output": "score"},
    {"name": "swarm", "action": "set", "values": {"swarm_verdict": "Consensus"}},
    {"name": "gate", "action": "guard", "input": "draft", "channel": "email", "output": "verdict", "max_attempts": 2},
    {"name": "human_approval", "action": "human_approval", "input": "approved"}
  ]
}
