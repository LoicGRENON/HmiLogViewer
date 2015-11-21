#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 16 juil. 2015

@author: GRENON Loïc
"""

from PyQt4 import QtGui


class MyTableView(QtGui.QTableView):
    def __init__(self, *args):
        super(MyTableView, self).__init__(*args)
