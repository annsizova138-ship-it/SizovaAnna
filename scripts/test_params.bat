@echo off
cd /d "%~dp0.."
echo [1] no parameters
python src\main.py
echo [2] only --vfs
python src\main.py --vfs examples\minimal.json
echo [3] only --script
python src\main.py --script examples\script_ok.txt
echo [4] both parameters
python src\main.py --vfs examples\minimal.json --script examples\script_ok.txt
