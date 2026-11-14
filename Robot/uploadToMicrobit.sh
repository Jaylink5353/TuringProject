#!/usr/bin/env bash

ROBOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

source "$ROBOT_DIR/../.venv/bin/activate"

cp "$ROBOT_DIR/microbitMain.py" "$ROBOT_DIR/main.py"
ufs put "$ROBOT_DIR/main.py"
rm "$ROBOT_DIR/main.py"
ufs put "$ROBOT_DIR/piSerialLibmk3.py"
ufs put "$ROBOT_DIR/keyes_mecanum_car_v2.py"
ufs ls
deactivate