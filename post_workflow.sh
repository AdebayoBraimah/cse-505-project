#!/usr/bin/env bash

echo "Changing file permissions"
chmod 755 file_sub.py

echo "Changing PDF name"
python ./file_sub.py -f main.pdf -e project

echo "Uploading to GitHub"
git add Adebayo_Braimah_115099306_project.pdf
git commit -m "[skip actions] Auto WF: Document upload"
git push origin main
