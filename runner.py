import psutil
import time
import os
import subprocess
from dotenv import load_dotenv
import pygetwindow as gw
import logging
import ctypes

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
PROCESS_NAME = os.getenv('PROCESS_NAME')  # Should be "WhatsApp.exe"
SCRIPT_TO_RUN = os.getenv('SCRIPT_TO_RUN')  # Path to face recognition script
VENV_PATH = os.getenv('VENV_PATH')  # Path to the virtual environment

# Set up logging
logging.basicConfig(filename='runner.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("------------------New logging session ------------------")

def is_process_running(process_name):
    """Check if a process with the given name is running."""
    for proc in psutil.process_iter(['name']):
        if process_name.lower() in proc.info['name'].lower():
            logging.info(f"{process_name} is running.")
            return True
    return False

def activate_venv(venv_path):
    """Prepare command to activate the virtual environment using PowerShell."""
    activate_script = os.path.join(venv_path, 'Scripts', 'Activate.ps1')
    logging.info(f"Activating virtual environment using {activate_script}.")
    return f'powershell -Command ". \'{activate_script}\'; python"'

def run_face_recognition_script():
    """Run the face recognition script to verify the user."""
    os.chdir(os.path.dirname(SCRIPT_TO_RUN))  # Change to directory of the script
    activation_command = activate_venv(VENV_PATH)
    full_command = f'{activation_command} "{SCRIPT_TO_RUN}"'
    logging.info("Running face recognition script.")
    subprocess.run(full_command, shell=True, check=True)

def hide_window(hwnd):
    """Hide the window using hwnd."""
    ctypes.windll.user32.ShowWindow(hwnd, 0)  # Hide the window

def show_window(hwnd):
    """Restore the window using hwnd."""
    ctypes.windll.user32.ShowWindow(hwnd, 1)  # Restore the window

def check_whatsapp_running():
    """Check if WhatsApp is running and return its window handle."""
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        hwnd = windows[0]._hWnd
        return hwnd
    return None

def main():
    logging.info("Monitoring started.")
    while True:
        hwnd = check_whatsapp_running()
        if hwnd:
            hide_window(hwnd)  # Hide WhatsApp window before verification
            logging.info("WhatsApp is running. Verifying user...")
            run_face_recognition_script()  # Run face recognition

            # After face recognition, if WhatsApp is still running, restore the window
            if is_process_running(PROCESS_NAME):
                logging.info("Face recognized! Restoring WhatsApp window.")
                show_window(hwnd)  # Show WhatsApp window if face is verified
                logging.info("Waiting for 30 minutes before re-verification.")
                time.sleep(30 * 60)  # Check every 30 minutes
            else:
                logging.info("WhatsApp is no longer running.")
        else:
            logging.info(f"{PROCESS_NAME} is not running.")
            time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()