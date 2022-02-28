#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""
from flask import Blueprint, render_template

home_blueprint = Blueprint("home_blueprint", __name__, template_folder="templates", static_folder="static")


@home_blueprint.route("/")
def home():
    return render_template("index.html")