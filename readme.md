# Diffing API

## Starting Dev Application

* Generating SSL Certificates `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
* Setup Virtual ENV `python -m venv .venv`
* Installing dependencies `.venv\Scripts\pip install -r requirements.txt`
* Starting Server `.venv\Scripts\python ./wsgi.py`
