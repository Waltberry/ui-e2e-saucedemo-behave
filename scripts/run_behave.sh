#!/usr/bin/env bash
set -euo pipefail
export HEADLESS=${HEADLESS:-1}
mkdir -p reports/junit reports/screenshots
behave -f progress -o reports/behave.log -f junit -o reports/junit
echo "Reports saved in ./reports"