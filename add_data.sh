#!/usr/bin/env bash
PS4="#:"
set -x
for i in {1..68}
do
    python main.py PIE/s$i fliph noise_0.001 rot_5 rot_-5 blur_1.0 blur_2.0
done