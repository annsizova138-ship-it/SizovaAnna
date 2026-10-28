@echo off
cd /d "%~dp0.."
echo [1] script without errors
python src\main.py --vfs examples\minimal.json --script examples\script_ok.txt
echo [2] script stops: unknown command
python src\main.py --vfs examples\minimal.json --script examples\script_unknown.txt
echo [3] script stops: wrong arguments
python src\main.py --vfs examples\minimal.json --script examples\script_args.txt
echo [4] script with exit
python src\main.py --vfs examples\minimal.json --script examples\script_exit.txt
echo [5] script file not found
python src\main.py --vfs examples\minimal.json --script examples\no_such_script.txt