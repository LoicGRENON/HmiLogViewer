#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 9 juil. 2015

@author: GRENON Loïc
"""

from PyQt4 import QtCore, QtGui
from ui.main import Ui_MainWindow
from ItemModels import COLOR_ROLE, LogReaderTableModel
from MyAboutDialog import MyAboutDialog
from MyExceptions import *
import codecs
import csv
import sys
import os
import yaml
import ast
import shutil


class HmiLogViewer(QtGui.QMainWindow):
    def __init__(self):
        super(HmiLogViewer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.aboutDialog = MyAboutDialog(self)

        self.model = None
        self.parserConfig = {'headers': None,
                             'cols': None}
        self.projectId = ""

        # Menu entries actions
        QtCore.QObject.connect(self.ui.actionOpen,
                               QtCore.SIGNAL("triggered()"),
                               self.openFile)
        QtCore.QObject.connect(self.ui.actionAddFile,
                               QtCore.SIGNAL("triggered()"),
                               lambda: self.openFile(True))
        QtCore.QObject.connect(self.ui.actionClose,
                               QtCore.SIGNAL("triggered()"),
                               self.closeFile)
        QtCore.QObject.connect(self.ui.actionSaveAs,
                               QtCore.SIGNAL("triggered()"),
                               self.saveFile)
        QtCore.QObject.connect(self.ui.actionImportConfigFile,
                               QtCore.SIGNAL("triggered()"),
                               self.importConfigFile)
        QtCore.QObject.connect(self.ui.actionAbout,
                               QtCore.SIGNAL("triggered()"),
                               self.aboutDialog.open)
        # Tool buttons actions
        QtCore.QObject.connect(self.ui.toolBtnOpen,
                               QtCore.SIGNAL("clicked()"),
                               self.openFile)
        QtCore.QObject.connect(self.ui.toolBtnAppend,
                               QtCore.SIGNAL("clicked()"),
                               lambda: self.openFile(True))
        QtCore.QObject.connect(self.ui.toolBtnSave,
                               QtCore.SIGNAL("clicked()"),
                               self.saveFile)

    def getItemParserConfig(self, projectId=""):
        """

        :param projectId: str
        :return: dict
        """
        projectId = projectId.strip()
        try:
            # First open the config file which is in the same directory than the executable
            with open("HmiLogViewer.yaml", "r") as f:
                return self.parseConfig(f, projectId)
        except (IOError, OSError):
            try:
                with open(os.path.join(self.getConfigPath(), "HmiLogViewer.yaml"), "r") as f:
                    return self.parseConfig(f, projectId)
            except (IOError, OSError) as e:
                QtGui.QMessageBox.critical(self.ui.centralwidget,
                                           u"Config loading failed",
                                           u"Unable to read config file.\nReturned error is :\n%s" % e,
                                           QtGui.QMessageBox.Ok)
                return {'headers': {},
                        'cols': {'decimals': 0,
                                 'values': {},
                                 'color': {},
                                 'visible': True}}

    def parseConfig(self, fp, projectId):
        """
        Parse config file for the projectId
        :param fp: file object
        :param projectId: str
        :return: dict
        """
        data = yaml.safe_load(fp)
        for d in data['LogData']:
            if projectId == d['projectId']:
                headers = ['Date']
                cols = []
                for item in d['items']:
                    headers.append(u"{}\n({})".format(item['name'], item['unit'])
                                   if item['unit'] else
                                   u"{}".format(item['name']))

                    try:
                        decimals = item['decimals']
                    except KeyError:
                        decimals = 0

                    try:
                        values = ast.literal_eval(item['values'])
                    except (KeyError, ValueError, SyntaxError):
                        values = {}

                    try:
                        color = ast.literal_eval(item['color'])
                    except (KeyError, ValueError, SyntaxError):
                        color = {}

                    try:
                        visible = item['visible']
                    except KeyError:
                        visible = True

                    cols.append({'decimals': decimals,
                                 'values': values,
                                 'color': color,
                                 'visible': visible})
                return {'headers': headers,
                        'cols': cols}
        # Raise exception if project is not found
        raise ProjectIdError()

    def getConfigPath(self):
        dirname = os.path.join("EriVallon", "HmiLogViewer")
        if 'ALLUSERSPROFILE' in os.environ:
            try:
                from win32com.shell import shellcon, shell
                appdata_path = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_APPDATA, 0, 0)
            except ImportError:
                appdata_path = os.environ['ALLUSERSPROFILE']
            return os.path.join(appdata_path, dirname)
        elif 'XDG_CONFIG_HOME' in os.environ:
            return os.path.join(os.environ['XDG_CONFIG_HOME'], dirname)
        else:
            return os.path.join(os.environ['HOME'], '.config', dirname)

    def importConfigFile(self):
        sFilePath = QtGui.QFileDialog.getOpenFileName(self.ui.centralwidget,
                                                      u"Choose a config file to import",
                                                      QtCore.QString(),
                                                      "YAML config file (*.yaml)")
        if os.path.isfile(sFilePath):
            r = QtGui.QMessageBox.warning(self.ui.centralwidget,
                                          u"Load config file",
                                          u"You are about to load a new config file located at : %s\n\n"
                                          u"Make sure you have selected a correct config file, "
                                          u"incorrect file may result in a non-functional application." % sFilePath,
                                          QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                          QtGui.QMessageBox.Cancel)
            if r == QtGui.QMessageBox.Ok:
                configPath = self.getConfigPath()
                if not os.path.exists(configPath):
                    os.makedirs(configPath)
                shutil.copy(sFilePath, os.path.join(configPath, "HmiLogViewer.yaml"))

    def openFile(self, append=False):
        """
        Open a csv file
        :param append: Do not close previous file if True
        """
        sFilePath = QtGui.QFileDialog.getOpenFileName(self.ui.centralwidget,
                                                      u"Choose a log file",
                                                      QtCore.QString(),
                                                      "CSV (*.csv)")
        if os.path.isfile(sFilePath):
            if not append:
                self.closeFile()
            self.parseLogFile(str(sFilePath))
            self.ui.actionClose.setEnabled(True)
            self.ui.actionAddFile.setEnabled(True)
            self.ui.toolBtnAppend.setEnabled(True)
            self.ui.actionSaveAs.setEnabled(True)
            self.ui.toolBtnSave.setEnabled(True)
            
    def closeFile(self):
        """
        Effacer les données des fichiers ouverts
        """
        self.model = None
        self.projectId = ""
        self.setModel()
        self.ui.actionSaveAs.setEnabled(False)
        self.ui.toolBtnSave.setEnabled(False)
        self.ui.actionAddFile.setEnabled(False)
        self.ui.toolBtnAppend.setEnabled(False)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile().toLocal8Bit().data()
            if os.path.isfile(path):
                self.parseLogFile(path)
                self.ui.actionClose.setEnabled(True)
                self.ui.actionAddFile.setEnabled(True)
                self.ui.toolBtnAppend.setEnabled(True)
                self.ui.actionSaveAs.setEnabled(True)
                self.ui.toolBtnSave.setEnabled(True)

    def setModel(self):
        self.model = LogReaderTableModel(self.parserConfig['headers'], self.ui.centralwidget)
        self.ui.tableView.setModel(self.model)
        
    def parseLogFile(self, filename):
        """
        Le fichier de journalisation est composé de 3 champs séparés par des tabulations :
        1 : Date au format jj/mm/aaaa
        2 : Heure au format HH:MM:SS
        3 : Le message composé de N champs séparés par des points virgules

            :param filename: file to be parsed
        """

        if not self.ui.tableView.model():
            self.setModel()

        try:
            with codecs.open(filename, "r", "utf-16") as f:
                for lineIdx, line in enumerate(f):
                    if line.endswith("\r\n"):
                        line = line[:-2]
                    if line.endswith("\n"):
                        line = line[:-1]

                    # Check for projectId value
                    if lineIdx == 0:
                        if self.projectId == "":
                            self.projectId = line
                            try:
                                self.parserConfig = self.getItemParserConfig(self.projectId)
                            except ProjectIdError:
                                QtGui.QMessageBox.warning(self.ui.centralwidget,
                                                          u"Config cannot be found",
                                                          u"A proper config cannot be found for this file",
                                                          QtGui.QMessageBox.Ok)
                                break
                            self.setModel()
                        elif line != self.projectId:
                            QtGui.QMessageBox.warning(self.ui.centralwidget,
                                                      u"Wrong log file",
                                                      u"The log file you are trying to open seems to be from "
                                                      u"a different project than the last opened file.\n"
                                                      u"Please close it before opening another.",
                                                      QtGui.QMessageBox.Ok)
                            break

                    lineFields = line.split()
                    # Check if lineField has correct field number : 1: Date / 2: Time / 3: Message
                    if len(lineFields) == 3:
                        # Le message est composé de N champs séparés par des points-virgule
                        # -> on les extrait et contrôle que le nombre de champs est correct par rapport au header
                        msgFields = lineFields[2].strip(";").split(";")
                        if len(msgFields) == len(self.parserConfig['headers']) - 1:
                            items = []
                            for field, fieldConfig in zip(msgFields, self.parserConfig['cols']):
                                decimals = fieldConfig['decimals']
                                values = fieldConfig['values']
                                color = fieldConfig['color']
                                visible = fieldConfig['visible']

                                try:
                                    evalField = ast.literal_eval(field)
                                except ValueError:
                                    evalField = field

                                try:
                                    if decimals != 0:
                                        item = QtGui.QStandardItem((unicode(float(field)/10.0**decimals)))
                                    else:
                                        item = QtGui.QStandardItem(unicode(values[evalField]))
                                except (ValueError, KeyError):
                                    item = QtGui.QStandardItem(unicode(field))

                                try:
                                    item.setData(QtGui.QColor(color[evalField]), COLOR_ROLE)
                                except (ValueError, KeyError):
                                    pass

                                items.append(item)
                            # Add date and time values on the top of the list
                            items.insert(0, QtGui.QStandardItem(" ".join(lineFields[:-1])))
                            # Add extra row for aesthetic reasons
                            items.append(QtGui.QStandardItem())

                            self.model.appendRow(items)
        except (IOError, OSError, UnicodeError) as e:
            QtGui.QMessageBox.critical(self.ui.centralwidget,
                                       u"Opening failed",
                                       u"Failed to open file.\nReturned error is :\n%s" % e,
                                       QtGui.QMessageBox.Ok)
        self.updateModel()
            
    def updateModel(self):        
        tv = self.ui.tableView
        tv.setModel(self.model)
        # Hide the last column to not resize it
        tv.setColumnHidden(self.model.columnCount(), True)
        # Resize cells to contents
        tv.resizeColumnsToContents()
        tv.resizeRowsToContents()
        # Unhide the last column previously hidden
        tv.setColumnHidden(self.model.columnCount(), False)

    def saveFile(self):
        sFilePath = QtGui.QFileDialog.getSaveFileName(self.ui.centralwidget,
                                                      u"Choose a log file",
                                                      QtCore.QString(),
                                                      "CSV (*.csv)")
        if sFilePath:
            try:
                with open(str(sFilePath), "wb") as f:
                    writer = csv.writer(f, delimiter=";")
                    # Write headers
                    writer.writerow([s.encode("cp1255") for s in self.parserConfig['headers']])
                    for row in xrange(self.model.rowCount()):
                        itemRow = ["%s" % self.model.item(row, col).data(QtCore.Qt.DisplayRole).toString()
                                   if col == 0 else
                                   self.model.item(row, col).data(QtCore.Qt.DisplayRole).toInt()[0]
                                   if col < 4 else
                                   "%s" % self.model.item(row, col).data(QtCore.Qt.DisplayRole).toReal()[0]
                                   for col in xrange(self.model.columnCount())]
                        writer.writerow(itemRow)
            except (IOError, OSError, UnicodeError) as e:
                QtGui.QMessageBox.critical(self.ui.centralwidget,
                                           u"Saving failed",
                                           u"Failed to save file.\nReturned error is :\n%s" % e,
                                           QtGui.QMessageBox.Ok)


def main():
    app = QtGui.QApplication(sys.argv)
    w = HmiLogViewer()
    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
