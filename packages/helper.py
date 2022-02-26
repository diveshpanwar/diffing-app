#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""

import logging
from os import path, makedirs
from config import DIRS


def make_dirs():
    """
    make the necessary dirs
    """
    for folder_key in DIRS:
        makedirs(path.join(DIRS[folder_key]), exist_ok=True)


def set_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s ==> %(message)s'
    )