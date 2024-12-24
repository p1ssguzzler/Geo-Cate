@echo off
set "PYTHON_URL=https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"
set "PYTHON_INSTALLER=python-installer.exe"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %PYTHON_INSTALLER%"
    if not exist %PYTHON_INSTALLER% (
        echo Failed to download Python. Please check your internet connection.
        pause
        exit /b
    )

    echo Running Python installer...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Failed to install Python. Please install it manually.
        pause
        exit /b
    )

    echo Cleaning up installer...
    del %PYTHON_INSTALLER%
)

echo Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo Failed to install pip. Please install it manually.
        pause
        exit /b
    )
)

echo Installing required Python packages...
pip install requests >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install required Python packages. Please check your internet connection or pip installation.
    pause
    exit /b
)

python -m venv venv >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to create a virtual environment. Skipping this step.
) else (
    echo Virtual environment created successfully. To activate it, run:
    echo     venv\Scripts\activate
)

echo Installation complete. Run the Python script with:
echo     python main.py
pause
