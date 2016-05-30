# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowProgress.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_WindowProgress(object):
    def setupUi(self, WindowProgress):
        WindowProgress.setObjectName(_fromUtf8("WindowProgress"))
        WindowProgress.setEnabled(True)
        WindowProgress.resize(300, 200)
        WindowProgress.setMinimumSize(QtCore.QSize(300, 200))
        WindowProgress.setMaximumSize(QtCore.QSize(300, 200))
        self.verticalLayout = QtGui.QVBoxLayout(WindowProgress)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(279, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.label_info = QtGui.QLabel(WindowProgress)
        self.label_info.setObjectName(_fromUtf8("label_info"))
        self.verticalLayout.addWidget(self.label_info)
        self.progressBar = QtGui.QProgressBar(WindowProgress)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        spacerItem1 = QtGui.QSpacerItem(279, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(WindowProgress)
        QtCore.QMetaObject.connectSlotsByName(WindowProgress)

    def retranslateUi(self, WindowProgress):
        WindowProgress.setWindowTitle(_translate("WindowProgress", "Dialog", None))
        self.label_info.setText(_translate("WindowProgress", "Creando documento docx...", None))

