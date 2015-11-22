# -*- coding: utf-8 -*-


class ProjectIdError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
