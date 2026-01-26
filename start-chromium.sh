#!/usr/bin/bash
sleep 5

DISPLAY=:0 chromium --kiosk --incognito --disk-cache-dir=/dev/null --media-cache-size=1 http://localhost:8000/ --password-store=basic
