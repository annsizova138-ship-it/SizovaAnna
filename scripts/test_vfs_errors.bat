@echo off
cd /d "%~dp0.."
echo [1] VFS file not found
python src\main.py --vfs examples\no_such_vfs.json --script examples\script_ok.txt
echo [2] broken JSON
python src\main.py --vfs examples\broken.json --script examples\script_ok.txt