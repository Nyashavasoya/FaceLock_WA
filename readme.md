# Face Unlock for WhatsApp on Windows

This Python script enhances security by requiring facial recognition for access to WhatsApp on a Windows system. If the user in front of the system is recognized as a trusted user, they are allowed to use WhatsApp freely.

## Getting Started

Follow the steps below to set up and run the script:

## 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Nyashavasoya/FaceLock_WA.git
cd FaceLock_WA
cd WAScript
mkdir data
```

## 2. Add Trusted User Images

Place 2-3 images of the trusted user in the `data` folder. These images will be used for facial recognition.

## 3. Set Up the Virtual Environment

Make sure you have Python 3.8 installed. Then, set up a virtual environment and activate it:

```bash
python3.8 -m venv .venv
.\.venv\Scripts\activate
```
### if this throws error here is the detailed way to deal with it 
Check for python3.8 is already there in your system or not if it isnot then [click here to download](https://www.python.org/downloads/release/python-380/) <br>
After downloading install python3.8 and try to remember the file of installation <br>
Here is the command to activate venv with most common path <br>
```bash
C:\Users\<UserName>\AppData\Local\Programs\Python\Python38\python.exe -m venv .venv
.\.venv\Scripts\activate
```

## 4. Install Dependencies

Install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## 5. Run the Script

After installing the dependencies,First run encode_faces.py in WAScrpt file then  you can run the `runner.py` script:


```bash
python .\WAScript\encode_faces.py
python runner.py
```

This will start the process, checking periodically if WhatsApp is running and ensuring that only a recognized user can access it.

