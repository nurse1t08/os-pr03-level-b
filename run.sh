#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 ptree.py
python3 runner.py --count 3 -- sleep 1
python3 zombie.py
python3 orphan.py
python3 cow_memory.py --mb 32
