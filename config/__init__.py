#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""

from os import environ


HOST: str = environ.get("HOST", "0,0,0,0")
PORT: int = environ.get("PORT", 5000)
DEBUG: bool = environ.get("DEBUG", True)

DIRS = {
    "main": "data",
    "source_files": "data/source_files",
    "destination_files": "data/destination_files",
    "html_files": "data/html_files"
}

ALLOWED_FILES = ["xml", "json", "yaml", "txt"]