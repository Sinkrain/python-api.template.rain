# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Flask
from controller import healthy_check_bp


def register_route(app: Flask):
    """
    注册路由
    """
    app.register_blueprint(healthy_check_bp)

