#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""


import logging
from flask import Flask, jsonify, redirect
from packages.helper import make_dirs, set_logging
from config import DEBUG
from flask_cors import CORS
from api.blueprints.diff_blueprint import diff_blueprint

app = Flask(__name__)
cors = CORS(app)

set_logging()
make_dirs()


# Register Blueprints
app.register_blueprint(diff_blueprint, url_prefix="/api/v1/diff")


@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def root():
    root_redirection = "/api/v1/diff"
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


if __name__ == "__main__":
    app.run(
        debug=DEBUG,
        ssl_context="adhoc"
    )
