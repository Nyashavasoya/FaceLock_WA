# Face Unlock for WhatsApp on Windows

This Python script enhances security by requiring facial recognition for access to WhatsApp on a Windows system. If the user in front of the system is recognized as a trusted user, they are allowed to use WhatsApp freely.

## Getting Started

Follow the steps below to set up and run the script:

## 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Nyashavasoya/FaceLock_WA.git
cd FaceLock_WA
cd WAscript
mkdir data
```

## 2. Add Trusted User Images

Place 2-3 images of the trusted user in the `data` folder. These images will be used for facial recognition.

## 3. Set Up the Virtual Environment

Make sure you have Python 3.8 installed. Then, set up a virtual environment and activate it:

```bash
python3.8 -m venv venv
source venv/Scripts/activate  # On Windows
```

## 4. Install Dependencies

Install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 5. Run the Script

After installing the dependencies, you can run the `runner.py` script:

```bash
python runner.py
```

This will start the process, checking periodically if WhatsApp is running and ensuring that only a recognized user can access it.

