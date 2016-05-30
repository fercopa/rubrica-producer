# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogmodificar.ui'
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

class Ui_DialogModificar(object):
    def setupUi(self, DialogModificar):
        DialogModificar.setObjectName(_fromUtf8("DialogModificar"))
        DialogModificar.resize(400, 300)
        DialogModificar.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(DialogModificar)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(DialogModificar)
        self.widget.setGeometry(QtCore.QRect(80, 90, 242, 71))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cmpFecha = QtGui.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cmpFecha.setFont(font)
        self.cmpFecha.setObjectName(_fromUtf8("cmpFecha"))
        self.horizontalLayout.addWidget(self.cmpFecha)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogModificar)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogModificar.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogModificar.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogModificar)

    def retranslateUi(self, DialogModificar):
        DialogModificar.setWindowTitle(_translate("DialogModificar", "Dialog", None))
        self.label.setText(_translate("DialogModificar", "Actualizar Fecha", None))
        self.cmpFecha.setPlaceholderText(_translate("DialogModificar", "02/12/2016", None))
        self.label_2.setText(_translate("DialogModificar", "dia/mes/año", None))

