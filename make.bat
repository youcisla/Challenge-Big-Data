@echo off
if "%1" == "install" goto install
if "%1" == "run" goto run
if "%1" == "clean" goto clean
goto help

:install
echo Installing requirements...
python -m pip install -r requirements.txt
goto end

:run
echo Running Streamlit app...
python -m streamlit run app.py
goto end

:clean
echo Cleaning up...
rmdir /s /q __pycache__ 2>nul
rmdir /s /q src\__pycache__ 2>nul
goto end

:help
echo Usage: 
echo   make.bat install  - Install dependencies
echo   make.bat run      - Run the application
echo   make.bat clean    - Remove build artifacts
goto end

:end
