#!/bin/bash
git config --global user.name "go2coding"

git pull
cd /home/ubuntu/fine_tuning/CatwalkGlimpse-AISelections

python3 Scraper.py
python3 FindNew.py
python3 SendMail.py

git add ./
today=$(date +%Y%m%d)
git commit -m "${today} new update"
git push -u origin main
