# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FPSeguros.ui'
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

class Ui_MainProducer(object):
    def setupUi(self, MainProducer):
        MainProducer.setObjectName(_fromUtf8("MainProducer"))
        MainProducer.resize(290, 270)
        MainProducer.move(400, 200)
        self.centralwidget = QtGui.QWidget(MainProducer)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(42, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.btnOperaciones = QtGui.QPushButton(self.centralwidget)
        self.btnOperaciones.setObjectName(_fromUtf8("btnOperaciones"))
        self.verticalLayout.addWidget(self.btnOperaciones)
        self.btnCobranzas = QtGui.QPushButton(self.centralwidget)
        self.btnCobranzas.setObjectName(_fromUtf8("btnCobranzas"))
        self.verticalLayout.addWidget(self.btnCobranzas)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(41, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        MainProducer.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainProducer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 290, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainProducer.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainProducer)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainProducer.setStatusBar(self.statusbar)

        self.retranslateUi(MainProducer)
        QtCore.QMetaObject.connectSlotsByName(MainProducer)

    def retranslateUi(self, MainProducer):
        MainProducer.setWindowTitle(_translate("MainProducer", "FPSeguros", None))
        self.label.setText(_translate("MainProducer", "Rúbrica digital", None))
        self.btnOperaciones.setText(_translate("MainProducer", "Operaciones", None))
        self.btnCobranzas.setText(_translate("MainProducer", "Cobranzas", None))

