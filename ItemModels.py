#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 9 juil. 2015

@author: GRENON Loïc
"""

from PyQt4 import QtCore, QtGui

COLOR_ROLE = QtCore.Qt.UserRole


class LogReaderTableModel(QtGui.QStandardItemModel):
    def __init__(self, headerData, parent=None, *args):
        super(QtGui.QStandardItemModel, self).__init__(parent, *args)
        self.headerData = headerData
        
    def data(self, index, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            if role == QtCore.Qt.BackgroundRole:
                return index.data(COLOR_ROLE)
        return QtGui.QStandardItemModel.data(self, index, role)
     
    def headerData(self, col, orientation, role=None):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if len(self.headerData) > col:
                return QtCore.QVariant(self.headerData[col])
            else:
                return QtCore.QVariant()
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(col + 1)
        return QtCore.QVariant()
    
    def addValue(self, index, value):
        self.setData(index, QtCore.QVariant(value))
