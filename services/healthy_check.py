# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import git


class HealthyCheck:

    def __init__(self):
        self.root_path = self.get_root_path()

    @staticmethod
    def get_root_path() -> str:
        root_path = os.path.dirname(os.path.dirname(__file__))
        return root_path

    def get_commit_it(self):
        repo = git.Repo(self.root_path)
        commit_id = repo.head.object.hexsha
        return commit_id

