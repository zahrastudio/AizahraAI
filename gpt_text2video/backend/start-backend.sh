#!/usr/bin/env bash
set -e
BASEDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASEDIR"
pip install --prefer-binary -r requirements.txt
python3 main.py
