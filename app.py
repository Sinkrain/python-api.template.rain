# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Flask

from models import local_session
import route


def create_app():
    app = Flask(__name__)
    app.session = local_session
    route.register_route(app)

    @app.teardown_appcontext
    def remove_session(*args, **kwargs):
        app.session.remove()

    return app


if __name__ == "__main__":

    my_app = create_app()
    my_app.run(host="127.0.0.1", port=8080)
