"""Setup Script. Run before deploy"""
import subprocess
from os import getcwd, path, remove

def execute_command(command):
    """Excecute CMD commands"""
    cmd = " ".join(command) if isinstance(command, list) else command
    print(f"Executing command: {cmd}")
    result = subprocess.run(command if isinstance(
        command, list) else f"{command}", check=False)
    print(
        f"Command result code: {result.returncode}. {
            'Excecuted successfully' if result.returncode == 0 else 'Error: '+str(result.stderr)}."
    )


WD = getcwd()
VENV_DIR = path.join(WD, "venv")
print(f"Current working directory: {WD}")
print(f"Current virtual enviroment directory: {VENV_DIR}")
if not path.exists(VENV_DIR):
    execute_command(["python", "-m", "venv", VENV_DIR])
requirements_path = path.join(WD, "requirements.txt")
if path.isfile(requirements_path) and path.exists(requirements_path):
    requirements_bat = path.join(WD, "install_requirements.bat")
    with open(requirements_bat, "w+", encoding="utf-8") as setup_bat_script:
        setup_bat_script.write(
            f"""@echo off
    set original_dir=%CD%
    set venv_root_dir="{VENV_DIR}"
    set app_root_dir="{WD}"
    call %venv_root_dir%\\Scripts\\activate.bat
    cd %app_root_dir%
    pip install --upgrade -r "{requirements_path}"
    if %errorlevel% == 0 (
       call :rollback_setting
       echo 'Requirementes installed successfully.'
       exit /b 0
    ) else (
       call :rollback_setting
       echo 'Requirementes installation failed.'
       exit /b 1
    )
    :rollback_setting
            call %venv_root_dir%\\Scripts\\deactivate.bat
            cd %original_dir%
            exit /b 0
          """
        )
    setup_bat_script.close()
    execute_command(requirements_bat)
    remove(requirements_bat)


with open(path.join(WD, "run_app.bat"), "w", encoding="utf-8") as bat_script:
    bat_script.write(
        f"""@echo off
    REM remember the initial folder location
    set original_dir=%CD%
    REM the location of the virtual environment
    set venv_root_dir="{VENV_DIR}"
    REM the location of the Python script
    set app_root_dir="{WD}"
    REM activate the virtual environment
    call %venv_root_dir%\\Scripts\\activate.bat
    REM run the python script and pass the config file path as argument
    python %app_root_dir%\\main.py %app_root_dir%\\app.conf
    REM handling exit code from Python script
    if %errorlevel% == 0 (
       call :rollback_setting
       echo "Python script execution succeeded."
       REM terminate the current script,
       REM but leaves the parent window/script/calling label open.
       exit /b 0
    ) else (
       call :rollback_setting
       echo "Python script execution failed."
       REM terminate the current script,
       REM but leaves the parent window/script/calling label open.
       exit /b 1
    )

    REM define a function
    :rollback_setting
        REM deactivate the virtual environment
        call %venv_root_dir%\\Scripts\\deactivate.bat
        REM change to the initial folder location
        cd %original_dir%
        REM ensure that the function exits properly.
        exit /b 0
    """
    )
    bat_script.close()
