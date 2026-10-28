@echo off
cd /d "%~dp0.."
echo [1] minimal VFS
python src\main.py --vfs examples\minimal.json --script examples\test_all.txt
echo [2] VFS with several files
python src\main.py --vfs examples\several_files.json --script examples\test_all.txt
echo [3] VFS with 3+ levels
python src\main.py --vfs examples\deep.json --script examples\test_all.txt
