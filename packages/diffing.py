#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""


import logging
from os import path
from flask import request
from config import DIRS
from difflib import HtmlDiff, unified_diff


def read_file_from_storage(location, filename):
    try:
        data = None
        with open(path.join(location, filename), 'r') as file:
            data = file.read()
        return data
    except Exception as ex:
        logging.exception(ex)
        raise Exception(f"Unable to read {filename} from location {location}")


def write_file_to_storage(location, filename, data):
    try:
        with open(path.join(location, filename), 'w') as file:
            file.writelines(data)
        return True
    except Exception as ex:
        logging.exception(ex)
        raise Exception(f"Unable to write {filename} to location {location}")


def start_diffing(files):
    result = []
    for source_file, destination_file, filename in files:
        try:
            output_file = f"{filename}.html"
            res = create_diff(source_file, destination_file,
                              filename, output_file)
            base_arr = request.base_url.split("/")[:3]
            base_arr.append(output_file)
            result.append({
                "filename": filename,
                "status": "Processed" if res else "Not Processed",
                "file_path": "/".join(base_arr) if res else ""
            })
        except Exception as ex:
            logging.exception(ex)
            raise Exception("Error occured in Start diffing")


def create_diff(old_file, new_file, filename, output_file=None):
    try:
        file_1 = open(
            path.join(DIRS["source_files"], old_file)
        ).readlines()
        file_2 = open(
            path.join(DIRS["destination_files"], new_file)
        ).readlines()

        if output_file:
            delta = HtmlDiff(wrapcolumn=67).make_file(
                file_1, file_2, old_file, new_file
            )
            with open(path.join(DIRS["html_files"], output_file), 'w') as opfile:
                opfile.write(delta)
            return (True, delta)
        else:
            delta = unified_diff(file_1, file_2, old_file, new_file)
            return delta
    except Exception as ex:
        logging.exception(ex)
        raise Exception(f"Unable to compute the diff for file {filename}")
