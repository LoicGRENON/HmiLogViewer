#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 9 juil. 2015

@author: GRENON Loïc
"""

from PyQt4 import QtCore, QtGui
from ui.main import Ui_MainWindow
from ItemModels import LogReaderTableModel
from MyAboutDialog import MyAboutDialog
import codecs
import csv
import re
import sys
import os


class HmiLogViewer(QtGui.QMainWindow):
    def __init__(self):
        super(HmiLogViewer, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.aboutDialog = MyAboutDialog(self)

        self.model = None
        self.header = [u"Date",
                       u"Version",
                       u"Status",
                       u"Turntable plate",
                       u"Riveting Depth\n(mm)",
                       u"Riveting low limit\n(mm)",
                       u"Riveting high limit\n(mm)",
                       u"Riveting time\n(s)",
                       u"Riveting pressure\n(bar)",
                       u"Loop 1 - SP\n(°C)",
                       u"Loop 1 - PV\n(°C)",
                       u"Loop 2 - SP\n(°C)",
                       u"Loop 2 - PV\n(°C)",
                       u"Loop 3 - SP\n(°C)",
                       u"Loop 3 - PV\n(°C)",
                       u"Melting time\n(s)"]
        
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
        
    def openFile(self, append=False):
        """
        Ouvrir un fichier CSV
        :param append: Do not close previous file if True
        """
        sFilePath = self.openFileDialog()
        if os.path.isfile(sFilePath):
            if not append:
                self.closeFile()
            self.parseLogFile(str(sFilePath))
            self.ui.actionClose.setEnabled(True)
            self.ui.actionAddFile.setEnabled(True)
            self.ui.toolBtnAppend.setEnabled(True)
            self.ui.actionSaveAs.setEnabled(True)
            self.ui.toolBtnSave.setEnabled(True)
        
    def openFileDialog(self):
        return QtGui.QFileDialog.getOpenFileName(self.ui.centralwidget,
                                                 u"Choose a log file",
                                                 QtCore.QString(),
                                                 "CSV (*.csv)")
            
    def closeFile(self):
        """
        Effacer les données des fichiers ouverts
        """
        self.model = None
        self.setModel()
        self.ui.actionSaveAs.setEnabled(False)
        self.ui.toolBtnSave.setEnabled(False)
        
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
        self.model = LogReaderTableModel(self.header, self.ui.centralwidget)
        self.ui.tableView.setModel(self.model)
        
    def parseLogFile(self, filename):
        """
        Le fichier de journalisation est composé de 3 champs séparés par des tabulations :
        1 : Date au format jj/mm/aaaa
        2 : Heure au format HH:MM:SS
        3 : Le message composé de 15 champs séparés par des points virgules :
            3.1  : Le numéro de version de pièce
            3.2  : L'état de la pièce (0:mauvaise / 1:bonne)
            3.3  : Le posage sur lequel la pièce a été assemblée (1: posage 1 / 2: posage 2)
            3.4  : La profondeur de bouterollage mesurée (0.1mm)
            3.5  : La limite mini de bouterollage (0.1mm)
            3.6  : La limite maxi de bouterollage (0.1mm)
            3.7  : Le temps de bouterollage (0.1s)
            3.8  : La pression de bouterollage (0.1bar)
            3.9  : La consigne de température de la boucle 1 (0.1°C)
            3.10 : La température mesurée de la boucle 1 (0.1°C)
            3.11 : La consigne de température de la boucle 2 (0.1°C)
            3.12 : La température mesurée de la boucle 2 (0.1°C)
            3.13 : La consigne de température de la boucle 3 (0.1°C)
            3.14 : La température mesurée de la boucle 3 (0.1°C)
            3.15 : Le temps de fusion (0.1s)

            :param filename: file to be parsed
        """

        if not self.ui.tableView.model():
            self.setModel()

        try:
            with codecs.open(filename, 'r', 'utf-16') as f:
                for line in f:
                    if line.endswith("\r\n"):
                        line = line[:-2]
                    if line.endswith("\n"):
                        line = line[:-1]
                        
                    lineFields = re.split(r'\t+', line)
                    # On contrôle que la ligne comprend le nombre de champs attendus
                    if len(lineFields) == 3:
                        # Le message est composé de 15 champs séparés par des points-virgule
                        # -> on les extrait et contrôle que le nombre de champs est correct
                        fields = lineFields[2].split(";")
                        if len(fields) == 15:
                            try:
                                items = [QtGui.QStandardItem((unicode(float(field)/10)))
                                         if idx in range(3, 15) else
                                         QtGui.QStandardItem(field)
                                         for idx, field in enumerate(fields)]
                            except (ValueError, UnicodeError):
                                # En cas d'erreur, on ignore la ligne courante et on passe à la suivante
                                continue
                            
                            # On concatène les champs date et heure et on les ajoute en tête de liste
                            items.insert(0, QtGui.QStandardItem(lineFields[0] + " " + lineFields[1]))
                            items.append(QtGui.QStandardItem())
                                
                            self.model.appendRow(items)
        except (IOError, OSError, UnicodeError) as e:
            QtGui.QMessageBox.critical(self.ui.centralwidget,
                                       "Opening failed",
                                       "Failed to open file.\nReturned error is :\n%s" % e,
                                       QtGui.QMessageBox.Ok)
        
        self.updateModel()
            
    def updateModel(self):        
        tv = self.ui.tableView
        tv.setModel(self.model)
        # Redimensionner les lignes et colonnes en fonction du contenu
        tv.resizeColumnsToContents()
        tv.resizeRowsToContents()
                
    def saveFile(self):
        sFilePath = QtGui.QFileDialog.getSaveFileName(self.ui.centralwidget,
                                                      u"Choose a log file",
                                                      QtCore.QString(),
                                                      "CSV (*.csv)")
        if sFilePath:
            try:
                with open(str(sFilePath), "wb") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow([s.encode("cp1255") for s in self.header])
                    for row in range(0, self.model.rowCount()):
                        itemRow = ["%s" % self.model.item(row, col).data(QtCore.Qt.DisplayRole).toString()
                                   if col == 0 else
                                   self.model.item(row, col).data(QtCore.Qt.DisplayRole).toInt()[0]
                                   if col < 4 else
                                   "%s" % self.model.item(row, col).data(QtCore.Qt.DisplayRole).toReal()[0]
                                   for col in range(0, self.model.columnCount() - 1)]
                        writer.writerow(itemRow)
            except (IOError, OSError, UnicodeError) as e:
                QtGui.QMessageBox.critical(self.ui.centralwidget,
                                           "Saving failed",
                                           "Failed to save file.\nReturned error is :\n%s" % e,
                                           QtGui.QMessageBox.Ok)


def main():
    app = QtGui.QApplication(sys.argv)
    w = HmiLogViewer()
    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
