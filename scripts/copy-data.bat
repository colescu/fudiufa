@echo off
rmdir /s /q "app\public\data"
mkdir "app\public\data"
xcopy "data\generated\*" "app\public\data\" /s /y /i /q >nul
xcopy "data\manual\*" "app\public\data\" /s /y /i /q >nul
del /s /q "app\public\data\*.sqlite3" >nul
del /s /q "app\public\data\*.sqbpro" >nul
echo Copy complete!