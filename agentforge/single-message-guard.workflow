{
  "name": "single-message-guard",
  "version": "1.0",
  "description": "draft → gate → revise loop → ship",
  "steps": [
    {"name": "guard", "action": "guard", "input": "draft", "channel": "email", "output": "verdict", "max_attempts": 3},
    {"name": "human_approval", "action": "human_approval", "input": "approved"}
  ]
}
