# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sat Nov 21 13:30:41 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(789, 608)
        MainWindow.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/HmiLogViewer_256.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.toolBtnOpen = QtGui.QToolButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBtnOpen.sizePolicy().hasHeightForWidth())
        self.toolBtnOpen.setSizePolicy(sizePolicy)
        self.toolBtnOpen.setAutoFillBackground(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/Oxygen-Icons.org-Oxygen-Actions-document-open-folder.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBtnOpen.setIcon(icon1)
        self.toolBtnOpen.setIconSize(QtCore.QSize(32, 32))
        self.toolBtnOpen.setArrowType(QtCore.Qt.NoArrow)
        self.toolBtnOpen.setObjectName(_fromUtf8("toolBtnOpen"))
        self.horizontalLayout.addWidget(self.toolBtnOpen)
        self.toolBtnAppend = QtGui.QToolButton(self.centralwidget)
        self.toolBtnAppend.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/Oxygen-Icons.org-Oxygen-Actions-document-new.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBtnAppend.setIcon(icon2)
        self.toolBtnAppend.setIconSize(QtCore.QSize(32, 32))
        self.toolBtnAppend.setObjectName(_fromUtf8("toolBtnAppend"))
        self.horizontalLayout.addWidget(self.toolBtnAppend)
        self.toolBtnRevert = QtGui.QToolButton(self.centralwidget)
        self.toolBtnRevert.setEnabled(False)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/Oxygen-Icons.org-Oxygen-Actions-document-revert.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBtnRevert.setIcon(icon3)
        self.toolBtnRevert.setIconSize(QtCore.QSize(32, 32))
        self.toolBtnRevert.setObjectName(_fromUtf8("toolBtnRevert"))
        self.horizontalLayout.addWidget(self.toolBtnRevert)
        self.toolBtnSave = QtGui.QToolButton(self.centralwidget)
        self.toolBtnSave.setEnabled(False)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/Oxygen-Icons.org-Oxygen-Actions-document-save.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBtnSave.setIcon(icon4)
        self.toolBtnSave.setIconSize(QtCore.QSize(32, 32))
        self.toolBtnSave.setObjectName(_fromUtf8("toolBtnSave"))
        self.horizontalLayout.addWidget(self.toolBtnSave)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/ressources/LogoEriEurosonics.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tableView = MyTableView(self.centralwidget)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setEnabled(False)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setEnabled(False)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionAddFile = QtGui.QAction(MainWindow)
        self.actionAddFile.setEnabled(False)
        self.actionAddFile.setObjectName(_fromUtf8("actionAddFile"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionAddFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "HmiLogViewer", None))
        self.toolBtnOpen.setText(_translate("MainWindow", "...", None))
        self.toolBtnAppend.setText(_translate("MainWindow", "...", None))
        self.toolBtnRevert.setText(_translate("MainWindow", "...", None))
        self.toolBtnSave.setText(_translate("MainWindow", "...", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionSaveAs.setText(_translate("MainWindow", "Save as", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionAddFile.setText(_translate("MainWindow", "Add file", None))

from MyTableView import MyTableView
import HmiLogViewer_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

