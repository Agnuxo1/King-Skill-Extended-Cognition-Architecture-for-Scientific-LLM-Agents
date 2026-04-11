---
name: skill-14-git-operations
description: >
  Git operations: commit, push, branch, merge, diff, status for OpenCLAW repos
  and GitHub Actions workflows. Use bash_tool directly.
  Triggers: "git commit", "push to GitHub", "branch", "merge", "diff",
  "GitHub Actions", "gist", "pull request", "clone repo".
token_savings: 3/5
dependencies: git, gh (GitHub CLI)
---

## Common patterns (bash_tool)

```bash
# Status and diff
git status && git diff --stat

# Stage and commit
git add -A && git commit -m "feat: description"

# Push
git push origin main

# Create gist (OpenCLAW state persistence)
gh gist create state.json --public --desc "OpenCLAW agent state"

# Update gist
gh gist edit GIST_ID state.json

# GitHub Actions: trigger workflow
gh workflow run paper-pipeline.yml --ref main

# Clone OpenCLAW repo
git clone https://github.com/Agnuxo1/OpenCLAW-P2P.git

# Check Actions status
gh run list --limit 5
gh run view RUN_ID
```

## OpenCLAW gist state persistence

```python
import subprocess, json

def save_state(state: dict, gist_id: str):
    with open("/tmp/state.json", "w") as f:
        json.dump(state, f)
    subprocess.run(["gh", "gist", "edit", gist_id, "/tmp/state.json"])

def load_state(gist_id: str) -> dict:
    result = subprocess.run(["gh", "gist", "view", gist_id, "--raw"],
                           capture_output=True, text=True)
    return json.loads(result.stdout)
```
