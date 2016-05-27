# Cobranzas

import sys
import datetime
import json
from Ui_mainTable import QtGui, QtCore, Ui_MainWindow
from PyQt4.QtGui import QFileDialog, QMessageBox
from Ui_updateDate import Ui_DialogModificar
from Ui_addRegisterCobranza import Ui_Cobranzas
from Document import DocumentCobranzas
from Document import NewDocumentCobranzas


T_ID = 0
T_TIPOREG = 1
T_FECHREG = 2
T_CONCEPT = 3
T_POLIZAS = 4
T_ORG = 5
T_CIAID = 6
T_IMPORTE = 7


class AddReg(Ui_Cobranzas):
    def __init__(self):
        self.dial = QtGui.QDialog()
        Ui_Cobranzas.setupUi(self, self.dial)

        # Type of Register
        tipoRegistro = self.strings_from_file('files/tipoRegistro.json')
        self.comboBoxTipoRegistro.addItems(tipoRegistro)

        # Organizer
        organizador = self.strings_from_file('files/tipoPersona.json')
        organizador.insert(0, '0-Ninguno')
        self.comboBoxOrganizador.addItems(organizador)

        # Company
        ciaId = self.strings_from_file('files/TablaCompania.json')
        self.comboBoxCiaId.addItems(ciaId)

        # Type of currency
        importeTipo = self.strings_from_file('files/tiposMonedas.json')
        self.comboBoxImporteTipo.addItems(importeTipo)

        # Button add Polizas
        QtCore.QObject.connect(self.btnPolizas, QtCore.SIGNAL('clicked()'),
                               self.add_polizas)

        # Button Ok
        QtCore.QObject.connect(self.btnAceptar, QtCore.SIGNAL('clicked()'),
                               self.add_accept)

        # Button Cancel
        QtCore.QObject.connect(self.btnCancelar, QtCore.SIGNAL('clicked()'),
                               self.add_reject)

    def add_accept(self):
        """
        Verify that the fields are good and if there is an error
        not close the dialog
        """
        # Clear message error
        self.clear_labels_errors()
        res = self.validate_form()
        if res:
            self.dial.accept()

    def add_reject(self):
        "Cancel the form"
        self.dial.reject()

    def add_polizas(self):
        "Add an poliza to the field Plain Text"
        # Clear message error
        self.label_Poliza.clear()
        poliza = self.cmpPoliza.text()
        if not poliza:
            self.label_Poliza.setText('Requerido')
            self.label_Poliza.setStyleSheet('QLabel {color: red;}')
        if poliza:
            self.cmpPlainTextPolizas.appendPlainText(poliza)
            self.cmpPoliza.clear()

    def strings_from_file(self, filename):
        """
        Get a list of string with your key from a file.
        Argument:
            Path of a file. The file is a .json and its contents is
            {<Key>: {<Key1>: <Value1>, <Key2>: <Value2> ... }}
        Return:
            A list of string like: ['<Key>-<ValueX>', '<Key>-<ValueX>, ...]
        """
        with open(filename) as f:
            data = json.load(f)
            try:  # Most files contain the value='Descripcion'
                res = [str(k)+'-'+data[k]['Descripcion'] for k in data.keys()]
                res.sort(key=lambda e: int(e.split('-')[0]))
            except KeyError:
                # There is a file containing the value='Denominacion'
                res = [str(k)+'-'+data[k]['Denominacion']
                       for k in data.keys()]
                res.sort(key=lambda e: int(e.split('-')[0]))
            return res

    def clear_labels_errors(self):
        "Clear error messages ocurred"
        self.label_FechaRegistro.clear()
        self.label_Concepto.clear()
        self.label_Poliza.clear()
        self.label_Matricula.clear()
        self.label_Importe.clear()

    def validate_form(self):
        """
        Check that all fields are correct
        Return:
            True if all fields are correct otherwise False and print error
            messages
        """
        res = True
        # Check Fecha registro
        fecha = self.cmpFechaRegistro.text()
        v = self.is_valid_date(fecha)[0]  # (Bool, Date)
        if fecha and not v:
            self.label_FechaRegistro.setText('Fecha invalida')
            self.label_FechaRegistro.setStyleSheet('QLabel {color: red;}')
            res = False
        elif not fecha:
            self.label_FechaRegistro.setText('Requerido')
            self.label_FechaRegistro.setStyleSheet('QLabel {color: red;}')
            res = False

        # Check Concepto
        campo = self.cmpConcepto.text()
        if not campo:
            self.label_Concepto.setText('Requerido')
            self.label_Concepto.setStyleSheet('QLabel {color:red;}')
            res = False

        # Check Polizas
        campo = self.cmpPlainTextPolizas.toPlainText()
        if not campo:
            self.label_Poliza.setText('Debe agregar al menos 1 poliza')
            self.label_Poliza.setStyleSheet('QLabel {color: red;}')
            res = False

        # Check Organizador
        currentText = self.comboBoxOrganizador.currentText()
        id_item = currentText.split('-')[0]
        campo = self.cmpMatricula.text()
        if id_item != '0' and not campo:
            # A Organizador have a Matricula
            self.label_Matricula.setText('Requerido')
            self.label_Matricula.setStyleSheet('QLabel {color: red;}')
            res = False
        elif id_item == '0' and campo:
            # A Matricula belongs to a Organizador
            self.label_Matricula.setText('Seleccione organizador')
            self.label_Matricula.setStyleSheet('QLabel {color: red;}')
            res = False

        # Check Importe
        campo = str(self.cmpImporte.text())
        if not campo or not campo.isdigit():
            self.label_Importe.setText('Requerido')
            self.label_Importe.setStyleSheet('QLabel {color: red;}')
            res = False

        return res

    def is_valid_date(self, date):
        """
        Check that the date is correct
        Return:
            A tuple (True, <Date>) if the date is correct otherwise (False, '')
        """
        res = (False, '',)
        fecha = date.replace('/', '-')
        if fecha and fecha.count('-') == 2:
            d, m, a = fecha.split('-')
            try:  # fecha = dd-mm-yyyy
                dato = datetime.date(int(a), int(m), int(d))
                res = (True, dato,)
            except ValueError:
                try:  # fecha = yyyy-mm-dd
                    dato = datetime.date(int(d), int(m), int(a))
                    res = (True, dato,)
                except ValueError:  # fehca = other format
                    pass
        return res


class MyForm(Ui_MainWindow):

    def __init__(self):
        self.ui = QtGui.QMainWindow()
        Ui_MainWindow.setupUi(self, self.ui)

        self.menuVer.removeAction(self.actionResponsabilidad_civil)
        # Name of the columns
        tipoRegistro = 'Tipo de Registro'
        fechaRegistro = 'Fecha Registro'
        concepto = 'Concepto'
        polizas = 'Polizas'
        organizador = 'Organizador\nMatricula-T.Persona'
        compania = 'Compania'
        importe = 'Importe'
        li = ['ID', tipoRegistro, fechaRegistro, concepto, polizas,
              organizador, compania, importe]

        # Setup the header of columns
        self.tabla.setColumnCount(len(li))
        self.tabla.setHorizontalHeaderLabels(li)
        self.tabla.resizeColumnsToContents()
        self.tabla.resizeRowsToContents()
        self.tabla.setSortingEnabled(True)

        self.doc = ''  # Current document loaded
        # This dictionary contains (date: register) for future modification
        # { <Key1>: (date1, reg1), <Key2>: (date2, reg2), ... }
        self.registers = {}
        # Keys of dictionary registers that were eliminated
        self.delete_list = []

        # Functions for the buttons
        # Update Register
        QtCore.QObject.connect(self.btnUpdateReg,
                               QtCore.SIGNAL('clicked()'),
                               self.dialog_modificar_date)
        # Delete Register
        QtCore.QObject.connect(self.btnDelete,
                               QtCore.SIGNAL('clicked()'),
                               self.delete_reg)

        self.actionAbrir_archivo.triggered.connect(self.loadFile)
        self.actionGuardar_como.triggered.connect(self.saveFile)
        self.actionAgregar_archivo_xml.triggered.connect(self.add_file)
        self.actionAgregar_registro.triggered.connect(self.dialog_add_reg)
        self.actionTodos_los_registros.triggered.connect(
            self.show_all_registers)

    def saveFile(self):
        """Save a xml file as <filename>.xml"""
        if self.tabla.rowCount() > 0:
            doc = NewDocumentCobranzas()
            data_header = self.doc.get_header()
            for elem in self.delete_list:
                del(self.registers[elem])
            cantReg = str(len(self.registers))
            data_header['cantidadRegistros'] = cantReg
            doc.create_header(data_header)
            regs = self.registers.values()
            # Order for date
            regs.sort(key=lambda t: t[0])
            for e in regs:
                doc.create_register(e[1])
            # Save the doc
            name = QFileDialog.getSaveFileName(self.ui, 'Guardar como...',
                                               filter='*.xml')
            if unicode(name).endswith('.xml'):
                doc.save(unicode(name))
            else:
                doc.save(unicode(name)+'.xml')

    def dialog_add_reg(self):
        "Open a windows to fill a form"
        if self.doc:
            ui = AddReg()
            ui.dial.exec_()

            if ui.dial.result():
                reg = {}
                box = unicode(ui.comboBoxTipoRegistro.currentText())
                reg['tipoRegistro'] = box.split('-')[0]
                reg['concepto'] = unicode(ui.cmpConcepto.text())
                # Polizas
                currentText = ui.cmpPlainTextPolizas.toPlainText()
                list_p = currentText.split('\n')
                polizas = []
                for p in list_p:
                    polizas.append(unicode(p))
                reg['polizas'] = polizas
                org = str(ui.comboBoxOrganizador.currentText())
                mat = str(ui.cmpMatricula.text())
                reg['organizador'] = (mat, org.split('-')[0])
                cid = unicode(ui.comboBoxCiaId.currentText())
                reg['ciaId'] = cid.split('-')[0]
                reg['importe'] = unicode(ui.cmpImporte.text())
                it = unicode(ui.comboBoxImporteTipo.currentText())
                reg['importeTipo'] = it.split('-')[0]

                row = len(self.registers)
                dato = str(ui.cmpFechaRegistro.text())
                if dato:
                    dato = dato.replace('/', '-')
                    d, m, a = dato.split('-')
                    newDate = datetime.date(int(a), int(m), int(d))
                    reg['fechaRegistro'] = newDate.isoformat()
                    self.registers[str(row+1)] = (newDate, reg)
                    self.show_register(str(row+1), reg)
                    self.refresh_header()
        else:
            QMessageBox.critical(self.ui, 'Advertencia',
                                 'No hay ningun xml cargado')

    def dialog_modificar_date(self):
        """Modify the date (Fecha Registro) of current row"""
        if self.tabla.rowCount() > 0:
            row = self.tabla.currentRow()
            item = self.tabla.item(row, T_FECHREG)

            dial = QtGui.QDialog()
            ui = Ui_DialogModificar()
            ui.setupUi(dial)
            dial.exec_()

            if dial.result():  # If press OK
                # Get the id of register
                item_id = self.tabla.item(row, 0)
                item_id = str(item_id.text())

                # Get the new date. Should be dd/mm/yyyy or dd-mm-yyyy
                dato = unicode(ui.cmpFecha.text())
                d, m, a = '', '', ''
                if dato and ('-' in dato or '/' in dato):
                    dato = dato.replace('/', '-')
                    d, m, a = dato.split('-')  # EXCEPTION
                    # Get the register
                    reg = self.registers[item_id][1]
                    newDate = datetime.date(int(a), int(m), int(d))
                    # Update the current table
                    item.setText(newDate.isoformat())
                    if self.doc:
                        reg['fechaRegistro'] = newDate.isoformat()
                        self.registers[item_id] = (newDate, reg)

    def add_file(self):
        """Add more register from a file to the table"""
        if self.registers:
            obj_file = QtGui.QFileDialog.getOpenFileName(self.ui,
                                                         'Abrir archivo',
                                                         filter='*.xml')
            filename = unicode(obj_file)
            if filename:
                try:
                    doc = DocumentCobranzas(filename,
                                            'files/SchemaCobranza.xsd')
                    row = len(self.registers)
                    while not doc.is_empty_regs():
                        reg = doc.get_register()
                        data = doc.get_data_from_register(reg)
                        fechaReg = data['fechaRegistro']
                        # Store a list of (date, reg)
                        # fechaReg = 'yyyy-mm-dd'
                        y, m, d = fechaReg.split('-')
                        date = datetime.date(int(y), int(m), int(d))
                        self.registers[str(row+1)] = (date, data)
                        row += 1
                    self.show_all_registers()
                    self.refresh_header()
                except Exception as e:
                    msg = 'Archivo no valido.\nDetalles:\n' + e.message
                    QMessageBox.critical(self.ui, 'Error', msg)
        else:
            self.loadFile()

    def clear_table(self):
        """Clean the table"""
        for i in range(0, self.tabla.rowCount()):
            self.tabla.removeRow(0)

    def loadFile(self):
        """Open a dialog file for choise a xml file"""
        self.clear_table()
        self.registers = {}
        self.delete_list = []
        # Get the name of xml file
        namef = QtGui.QFileDialog.getOpenFileName(self.ui,
                                                  'Abrir archivo',
                                                  filter='*.xml')
        # Get the absolute path of xml file as a string
        filename = unicode(namef)
        if filename:
            try:
                self.doc = DocumentCobranzas(filename,
                                             'files/SchemaCobranza.xsd')
                header_data = self.doc.get_header()
                tp = self.get_dataFromFile('files/tipoPersona.json')
                value = tp[header_data['tipoPersona']]['Descripcion']
                self.label_TipoPersona.setText(value)
                self.label_Matricula.setText(header_data['matricula'])
                self.label_CantReg.setText(header_data['cantidadRegistros'])

                row = 0
                while(not self.doc.is_empty_regs()):
                    reg = self.doc.get_register()
                    data = self.doc.get_data_from_register(reg)
                    fechaReg = data['fechaRegistro']
                    # Store a list of (date, reg)
                    # fechaReg = 'yyyy-mm-dd'
                    y, m, d = fechaReg.split('-')
                    date = datetime.date(int(y), int(m), int(d))
                    self.registers[str(row+1)] = (date, data)
                    row += 1
                self.show_all_registers()
                self.refresh_header()
            except Exception as e:
                msg = 'Archivo no valido.\nDetalles:\n' + e.message
                QMessageBox.critical(self.ui, 'Error', msg)

    def get_dataFromFile(self, filename):
        """
        Get the datas from a file json
        Argument:
            A path of file json
        Return:
            A dict from a file json
        """
        data = ''
        with open(filename) as f:
            data = json.load(f)
        return data

    def format_date(self, ddmmyy):
        """Format the date like: yyyy-mm-dd
        Argument:
            A string "dd/mm/yyyy" or "yyyy-mm-dd"
        Return:
            A date string "yyyy-mm-dd
        """
        date = ddmmyy.replace('/', '-')
        d, m, y = date.split('-')
        if len(y) == 4:
            date = '-'.join((y, m, d))
        return date

    def show_register(self, key, reg):
        """Show the register in a row fo table"""
        row = self.tabla.rowCount()
        # data = self.doc.get_data_register(reg)
        self.tabla.insertRow(row)
        self.tabla.setItem(row, T_ID, QtGui.QTableWidgetItem(key))

        tipoRegistro = self.get_dataFromFile('files/tipoRegistro.json')
        value = tipoRegistro[reg['tipoRegistro']]['Descripcion']
        self.tabla.setItem(row, T_TIPOREG, QtGui.QTableWidgetItem(value))

        fechaReg = self.format_date(reg['fechaRegistro'])
        self.tabla.setItem(row, T_FECHREG, QtGui.QTableWidgetItem(fechaReg))

        concepto = reg['concepto']
        self.tabla.setItem(row, T_CONCEPT, QtGui.QTableWidgetItem(concepto))

        polizas = '\n'.join(reg['polizas'])
        self.tabla.setItem(row, T_POLIZAS, QtGui.QTableWidgetItem(polizas))

        # Organizador
        tipoPersona = self.get_dataFromFile('files/tipoPersona.json')
        if reg['organizador']:
            matricula, tp_org = reg['organizador']
            tp_org = tipoPersona[tp_org]['Descripcion']
            organizador = '-'.join((matricula, tp_org))
            self.tabla.setItem(row, T_ORG, QtGui.QTableWidgetItem(organizador))

        # Compania
        tablaCompania = self.get_dataFromFile('files/TablaCompania.json')
        compania = reg['ciaId']
        compania = tablaCompania[compania]['DenominacionCorta']
        self.tabla.setItem(row, T_CIAID, QtGui.QTableWidgetItem(compania))

        # Suma asegurada y su tipo
        monedas = self.get_dataFromFile('files/tiposMonedas.json')
        id_tipo = reg['importeTipo']
        moneda = monedas[id_tipo]['Signo']
        importe = moneda + ' ' + reg['importe']
        self.tabla.setItem(row, T_IMPORTE, QtGui.QTableWidgetItem(importe))

        self.tabla.resizeRowToContents(row)

    def show_all_registers(self):
        """Show the registers in a table"""
        if self.registers:
            self.clear_table()
            list_regs = [(k, self.registers[k][0], self.registers[k][1])
                         for k in self.registers.keys()
                         if k not in self.delete_list]
            list_regs.sort(key=lambda t: t[1])
            for t in list_regs:
                reg = t[2]
                k = t[0]
                self.show_register(k, reg)
            self.refresh_header()

    def delete_reg(self):
        "Delete a register of current row selected"
        row = self.tabla.currentRow()
        if row >= 0:
            msg = 'Esta seguro que quiere borrar el registro?'
            dial = QMessageBox.question(self.ui, 'Advertencia', msg,
                                        QMessageBox.Ok | QMessageBox.Cancel)
            if dial == QMessageBox.Ok:
                item = self.tabla.item(row, T_ID)
                if item is not None:
                    self.delete_list.append(unicode(item.text()))
                    self.tabla.removeRow(row)
                    self.refresh_header()

    def refresh_header(self):
        "Update the len of registers"
        cantReg = str(len(self.registers) - len(self.delete_list))
        self.label_CantReg.setText(cantReg)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.ui.show()
    sys.exit(app.exec_())
