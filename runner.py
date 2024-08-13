import psutil
import time
import os
import subprocess
from dotenv import load_dotenv
import pygetwindow as gw

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
PROCESS_NAME = os.getenv('PROCESS_NAME')
SCRIPT_TO_RUN = os.getenv('SCRIPT_TO_RUN')
VENV_PATH = os.getenv('VENV_PATH')

def is_process_running(process_name):
    """Check if a process with the given name is running."""
    for proc in psutil.process_iter(['name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def activate_venv(venv_path):
    """Prepare command to activate the virtual environment using PowerShell."""
    activate_script = os.path.join(venv_path, 'Scripts', 'Activate.ps1')
    return f'powershell -Command ". \'{activate_script}\'; python"'

def run_face_recognition_script():
    """Run the face recognition script to verify the user."""
    os.chdir(os.path.dirname(SCRIPT_TO_RUN))  # Change to directory of the script
    activation_command = activate_venv(VENV_PATH)
    full_command = f'{activation_command} "{SCRIPT_TO_RUN}"'
    subprocess.run(full_command, shell=True, check=True)

def hide_whatsapp_window():
    """Hide the WhatsApp window."""
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        window = windows[0]
        window.minimize()  # Minimize the window to hide it

def show_whatsapp_window():
    """Show the WhatsApp window."""
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        window = windows[0]
        window.restore()  # Restore the window to make it visible

def main():
    while True:
        if is_process_running(PROCESS_NAME):
            hide_whatsapp_window()  # Hide WhatsApp window before verification
            print(f"{PROCESS_NAME} is running. Verifying user...")
            run_face_recognition_script()
            # Wait a bit before showing the window again
            time.sleep(10)
            if not is_process_running(PROCESS_NAME):
                continue
            show_whatsapp_window()  # Show WhatsApp window only if face is verified
        else:
            time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
