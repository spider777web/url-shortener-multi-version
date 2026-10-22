#!/bin/bash
# Run a version manually using: ./start.sh v1
VERSION=${1:-v1}
case "$VERSION" in
  v1) cd v1 && python3 app.py ;;
  v2) cd v2 && python3 app.py ;;
  v3) cd v3 && python3 app.py ;;
  *) echo "Usage: ./start.sh [v1|v2|v3]"; exit 1 ;;
esac
