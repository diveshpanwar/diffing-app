#!/usr/bin/env python
"""
Author: Divesh Panwar
Email: divesh.panwar@gmail.com
"""

from flask import Blueprint
from flask_restx import Api


diff_blueprint = Blueprint("diff_blueprint", __name__)
diff_api = Api(
    title="DIFF API",
    description="This API helps in finding the difference between files."
)

diff_api.init_app(diff_blueprint)


from api.namespaces.diff_namespace import diff_namespace
diff_api.add_namespace(diff_namespace)