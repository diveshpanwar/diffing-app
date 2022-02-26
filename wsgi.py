#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""


from flask import Flask, jsonify
from packages.helper import make_dirs
from config import DEBUG
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

make_dirs()


@app.route("/health", methods=["GET", "POST", "PUT", "DELETE"])
def health():
    """
    Health Endpoint
    """
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
        debug=DEBUG
    )
