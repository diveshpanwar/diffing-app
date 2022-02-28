#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""


import logging
from flask import Flask, jsonify, redirect, render_template
from packages.helper import make_dirs, set_logging
from flask_sslify import SSLify
from config import DEBUG, DIRS, TEMPLATE_FOLDER
from flask_cors import CORS
from api.blueprints.diff_blueprint import diff_blueprint
from api.blueprints.home import home_blueprint
from os import path, walk
from os.path import getmtime
from datetime import datetime, timezone

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
SSLify(app)
CORS(app)

set_logging()
make_dirs()


# Register Blueprints
app.register_blueprint(diff_blueprint, url_prefix="/api/v1/diff")
app.register_blueprint(home_blueprint, url_prefix="/")



@app.route("/<path:text>", methods=["GET", "POST"])
def all_routes(text):
    if text.endswith(".js") or text.endswith("json") or text.endswith(".ico") or text.endswith(".css"):
        return app.send_static_file(text)
    else:
        return "", 404


@app.route("/html/<html_file_name>", methods=["GET"])
def send_html(html_file_name):
    if path.exists(path.join(DIRS["html_files"], html_file_name)):
        return render_template(html_file_name)
    else:
        return f"<h4 align='center'> File <i>{html_file_name}</i> does not exist.</h4>"


@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def root():
    root_redirection = "/"
    logging.info(f"Redirecting to {root_redirection}")
    return redirect(root_redirection)


@app.route("/health", methods=["GET", "POST", "PUT", "DELETE"])
def health():
    """
    Health Endpoint
    """
    logging.info("Health EP Accessed")
    return jsonify({
        "name": "DIFFING APP",
        "live": True,
        "ready": True,
        "endpoints": {
                "/": "redirection to /api/v1/diff",
                "/health": "Health API",
                "/api/v1/diff": "Difffing API"
        }
    })


@app.route("/files", methods=["GET"])
def files():
    title = "Files On Server"
    data = []

    def get_time(timestamp): return str(
        datetime.fromtimestamp(
            timestamp,
            datetime.now(timezone.utc).astimezone().tzinfo
        ).strftime('%d %D, %Y %I:%M:%S %p, %A')
    )

    try:
        for dirpath, dirroot, filenames in walk(path.join(DIRS["html_files"])):
            for filename in filenames:
                if (filename != "files.html"):
                    timestamp = getmtime(path.join(dirpath, filename))
                    data.append({
                        "filename": filename,
                        "date_created": get_time(timestamp)
                    })
    except Exception as ex:
        logging.exception(ex)
        return jsonify({
            "error": "Unable to Fetch the List of Files on the Server"
        }), 500
    if len(data) == 0:
        return jsonify({
            "message": "No Files Present on Server"
        })
    return render_template("files.html", title=title, data=data)


if __name__ == "__main__":
    app.run(
        debug=DEBUG,
        ssl_context=("ssl/cert.pem", "ssl/key.pem")
    )
