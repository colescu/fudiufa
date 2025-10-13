@echo off
python "%~dp0update_date.py"
echo -----
call npx tsx "%~dp0export_strata.ts"
python "%~dp0update_reflex.py"
echo -----
python "%~dp0update_ipa.py"
echo -----
python "%~dp0export_syllables.py"
python "%~dp0export_mc.py"
echo -----
python "%~dp0export_lang.py"
echo -----
call "%~dp0copy-data.bat"
pause