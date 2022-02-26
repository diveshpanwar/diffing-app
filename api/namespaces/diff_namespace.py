#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""

import logging

from flask import jsonify, request
from api.blueprints.diff_blueprint import diff_api
from flask_restx import Resource, reqparse
from werkzeug.datastructures import FileStorage
from time import perf_counter
from config import DIRS, ALLOWED_FILES
from os import path
from packages.diffing import create_diff


diff_post_endpoint = reqparse.RequestParser()
diff_post_endpoint.add_argument(
    "old_file",
    type=FileStorage,
    location="files",
    required=True,
    help=f"Old FIle can be a {', '.join(ALLOWED_FILES)} file."
)
diff_post_endpoint.add_argument(
    "new_file",
    type=FileStorage,
    location="files",
    required=True,
    help=f"New FIle can be a {', '.join(ALLOWED_FILES)} file."
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
            old_file = args["old_file"]
            new_file = args["new_file"]

            old_filename = old_file.filename
            new_filename = new_file.filename

            if old_filename.split(".")[-1].lower() not in ALLOWED_FILES or new_filename.split(".")[-1].lower() not in ALLOWED_FILES:
                return jsonify({
                    "error": f"Only files of type {', '.join(ALLOWED_FILES)} are allowed"
                })

            try:
                old_file.save(
                    path.join(DIRS["source_files"], old_filename)
                )
                new_file.save(
                    path.join(DIRS["destination_files"], new_filename)
                )
            except Exception as fileException:
                logging.exception(fileException)
                message = "Unable to Save Files"
                raise Exception(message)
            try:
                output_filename = f"{new_filename}.html"
                result, diff = create_diff(
                    old_filename, new_filename, new_filename, output_filename)
                base_arr = request.base_url.split("/")[:3]
                base_arr.append("html")
                base_arr.append(output_filename)
                response = {
                    "status": "Processed" if result else "Not Processed",
                    "file": "/".join(base_arr) if result else ""
                }
                return jsonify(response)
            except Exception as processException:
                logging.exception(processException)
                message = "Unable to Process Files"
                raise Exception(message)
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
