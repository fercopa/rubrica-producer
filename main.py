import sys
from PyQt4 import QtCore, QtGui
from FPSeguros import Ui_MainProducer
import Ui_iseguro


class MainPage(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainProducer()
        self.ui.setupUi(self)
        self.form = None

        QtCore.QObject.connect(self.ui.btnOperaciones,
                               QtCore.SIGNAL('clicked()'),
                               self.operaciones)

        QtCore.QObject.connect(self.ui.btnCobranzas,
                               QtCore.SIGNAL('clicked()'),
                               self.cobranzas)

    def operaciones(self):
        self.form = Ui_iseguro.MyForm()
        self.form.ui.show()

    def cobranzas(self):
        pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainPage = MainPage()
    mainPage.show()
    sys.exit(app.exec_())
