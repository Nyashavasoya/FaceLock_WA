import psutil
import time
import os
import subprocess
from dotenv import load_dotenv
import pygetwindow as gw
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
PROCESS_NAME = os.getenv('PROCESS_NAME')
SCRIPT_TO_RUN = os.getenv('SCRIPT_TO_RUN')
VENV_PATH = os.getenv('VENV_PATH')

# Set up logging to use the same file as encode_faces.py and main.py
logging.basicConfig(filename='runner_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Add a separator to indicate a new session
logging.info("------------------New logging session for runner ------------------")

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

def hide_whatsapp_window():
    """Hide the WhatsApp window."""
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        window = windows[0]
        window.minimize()  # Minimize the window to hide it
        logging.info("WhatsApp window minimized.")

def show_whatsapp_window():
    """Show the WhatsApp window."""
    windows = gw.getWindowsWithTitle("WhatsApp")
    if windows:
        window = windows[0]
        window.restore()  # Restore the window to make it visible
        logging.info("WhatsApp window restored.")
        window.maximize()
        logging.info("WhatsApp window maximized.")

def main():
    logging.info("Monitoring started.")
    while True:
        if is_process_running(PROCESS_NAME):
            hide_whatsapp_window()  # Hide WhatsApp window before verification
            logging.info(f"{PROCESS_NAME} is running. Verifying user...")
            run_face_recognition_script()
            # Wait a bit before showing the window again
            logging.info("returning to monitoring")
            if not is_process_running(PROCESS_NAME):
                logging.info(f"{PROCESS_NAME} is no longer running.")
                continue
            show_whatsapp_window()  # Show WhatsApp window only if face is verified
            logging.info("waiting for 30 minutes")
            time.sleep(30*60)  # Check every 30 minutes
        else:
            logging.info(f"{PROCESS_NAME} is not running.")
            time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
