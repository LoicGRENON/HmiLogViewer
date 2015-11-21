#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 16 juil. 2015

@author: GRENON Loïc
"""

from PyQt4 import QtGui
from ui.aboutDialog import Ui_aboutDialog


class MyAboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self)
