# DICOM VIEWER

## About this app

This app aims to provide a functional tool for DICOM images visualization, allowing to annotate and store data.
Three diferent MRI techniques are shown simultaneously for each patient in the database, in order to analyse a complete prostate study.



## How to run this app locally

(The following instructions are for unix-like shells)

Clone this repository and navigate to the directory containing this `README` in
a terminal.

Make sure you have installed the latest version of pip to install the files

```bash
python3 -m pip install --upgrade pip
```

Create and activate a virtual environment (recommended):

```bash
python -m venv myvenv
source myvenv/bin/activate
```

Install the requirements

```bash
pip install -r requirements.txt
```

Run the app. An IP address where you can view the app in your browser will be
displayed in the terminal.

```bash
python app.py
```

