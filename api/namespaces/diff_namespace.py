#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""

from ast import Compare
from email import message
import logging

from flask import jsonify
from api.blueprints.diff_blueprint import diff_api
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage
from time import perf_counter

diff_post_endpoint = reqparse.RequestParser()
diff_post_endpoint.add_argument(
    "old_file",
    type=FileStorage,
    location="files",
    required=True,
    help="Old FIle can be a .txt, .json or .yaml"
)
diff_post_endpoint.add_argument(
    "new_file",
    type=FileStorage,
    location="files",
    required=True,
    help="New FIle can be a .txt, .json or .yaml"
)


diff_namespace = diff_api.namespace(
    "diff_namespace",
    description="Diffing Operations on the files."
)

@diff_namespace.route("/compare")
class Compare(Resource):
    @diff_api.expect(diff_post_endpoint)
    @diff_api.response(200, "Success", headers={'Content-Type': 'application/json'})
    def post(self):
        start_time = perf_counter()
        args = diff_post_endpoint.parse_args()
        error_message = "Error while comparing files"
        try:
            return jsonify({
                "message": "I will do the Diffig"
            })
        except Exception as ex:
            logging.error(ex)
            return jsonify({
                "status": "Error",
                "message": error_message
            }), 500
        finally:
            logging.info(
                f"Time take from file comparison is {str(perf_counter() - start_time)} Seconds"
            )
