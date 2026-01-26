#!/usr/bin/bash
sleep 2

DISPLAY=:0 chromium --kiosk --incognito --disk-cache-dir=/dev/null --media-cache-size=1 http://localhost:8000/ --password-store=basic
