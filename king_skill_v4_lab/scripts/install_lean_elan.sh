#!/usr/bin/env bash
# EXP-03 — non-interactive elan + Lean stable (run in Docker or CI).
set -euo pipefail
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain stable
# shellcheck disable=SC1090
source "$HOME/.elan/env"
lean --version
echo "Lean OK. Run project-specific lake test for 53/53 when test suite is vendored."
