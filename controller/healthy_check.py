# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import json
from flask import Blueprint
from flask import Response

from services import HealthyCheck

healthy_check_bp = Blueprint("healthy_check", __name__)


@healthy_check_bp.get("/whoami")
def healthy_check():
    app_env = os.environ.get("APP_ENV", "development")
    hc = HealthyCheck()
    msg = {
        "msg": "Hello Mist Rain",
        "env": app_env,
        "commit_id": hc.get_commit_it()
    }
    return Response(json.dumps(msg), status=200, mimetype="application/json")
