@echo off

setlocal enabledelayedexpansion

virtualenv virtualenv
call virtualenv/Scripts/activate.bat
pip install -r requirements.txt
call virtualenv/Scripts/deactivate.bat
