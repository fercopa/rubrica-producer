import sys
import datetime
import json
from docx import Document as Docx
from PyQt4.QtGui import QFileDialog, QMessageBox
from Ui_mainTable import QtGui, QtCore, Ui_MainWindow
from Ui_updateDate import Ui_DialogModificar
from Ui_addRegister import Ui_DialogAdd
from Document import DocumentOperacion
from Document import NewDocumentOperacion


T_ID = 0
T_FECHREG = 1
T_ASEG = 2
T_CPAP = 3
T_CPAOBS = 4
T_CPACANT = 5
T_CPAPS = 6
T_CIAID = 7
T_ORG = 8
T_BASEG = 9
T_RAMO = 10
T_SASEG = 11
T_VIGE = 12
T_TOP = 13
T_FLOTA = 14
T_TCONT = 15

RAMO_ID = '36'

# For docx document
T_FREG = 1          # Fecha registro
T_NYA = 2           # Nombre y apellido
T_DIR = 3           # Direccion
T_UBIC = 4          # Ubicacion del riesgo
T_CIA = 5           # Compania (Entidad Aseguradora)
T_BIEN = 6          # Bien asegurado
T_RIESGO = 7        # Riesgo a cubrir
T_SUMASEG = 8       # Suma asegurada
T_VIGENCIA = 9      # Vigencia seguro


class AddReg(Ui_DialogAdd):
    def __init__(self):
        self.dial = QtGui.QDialog()
        Ui_DialogAdd.setupUi(self, self.dial)

        tipoPersona = self.strings_from_file('files/tipoPersona.json')
        self.comboBoxTipoPersona.addItems(tipoPersona)

        tipoDoc = self.strings_from_file('files/tiposDocumentos.json')
        self.comboBoxTipoDoc.addItems(tipoDoc)

        organizador = tipoPersona
        organizador.insert(0, '0-Ninguno')
        self.comboBoxOrganizador.addItems(organizador)

        ciaId = self.strings_from_file('files/TablaCompania.json')
        self.comboBoxCiaId.addItems(ciaId)

        ramo = self.strings_from_file('files/ramos.json')
        self.comboBoxRamo.addItems(ramo)

        sumaAsegT = self.strings_from_file('files/tiposMonedas.json')
        self.comboBoxSumaTipo.addItems(sumaAsegT)

        tipoOp = self.strings_from_file('files/tipoOperacion.json')
        self.comboBoxTipoOp.addItems(tipoOp)

        contacto = self.strings_from_file('files/tipoContacto.json')
        self.comboBoxContacto.addItems(contacto)

        QtCore.QObject.connect(self.btnAsegurado, QtCore.SIGNAL('clicked()'),
                               self.add_asegurados)

        QtCore.QObject.connect(self.btnCodigo, QtCore.SIGNAL('clicked()'),
                               self.add_codigosPostales)
        QtCore.QObject.connect(self.btnAceptar, QtCore.SIGNAL('clicked()'),
                               self.add_accept)

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

    def add_asegurados(self):
        "Add an insured to the field Plain Text"
        # Clear message error
        self.label_NroDoc.clear()
        self.label_Nombre.clear()
        tp = self.comboBoxTipoPersona.currentText()
        td = self.comboBoxTipoDoc.currentText()
        nd = self.cmpNroDoc.text()
        if not nd:
            self.label_NroDoc.setText('Requerido')
            self.label_NroDoc.setStyleSheet('QLabel {color: red;}')
        n = self.cmpNombre.text()
        if not n:
            self.label_Nombre.setText('Requerido')
            self.label_Nombre.setStyleSheet('QLabel {color: red;}')
        if nd and n:
            aseg = ','.join((str(tp), str(td), str(nd), str(n)))
            self.cmpAsegurados.appendPlainText(aseg)
            self.cmpNroDoc.clear()
            self.cmpNombre.clear()

    def add_codigosPostales(self):
        "Add a postal code to the field Plain Text"
        c = self.cmpCodPos.text()
        if str(c):
            self.cmpCodigos.append(c)
            self.cmpCodPos.clear()

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
        self.label_Asegurados.clear()
        self.label_CPAP.clear()
        self.label_CPACant.clear()
        self.label_Codigos.clear()
        self.label_Matricula.clear()
        self.label_BienAseg.clear()
        self.label_SumaAseg.clear()
        self.label_FechaDes.clear()
        self.label_FechaHas.clear()

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
        # Check Asegurados
        campo = self.cmpAsegurados.toPlainText()
        if not campo:
            self.label_Asegurados.setText('Debe agregar al menos 1 asegurado')
            self.label_Asegurados.setStyleSheet('QLabel {color: red;}')
            res = False
        # Check CPA Proponente
        campo = self.cmpCPAP.text()
        if not campo:
            self.label_CPAP.setText('Requerido')
            self.label_CPAP.setStyleSheet('QLabel {color:red;}')
            res = False
        # Check Obs Proponente
        """campo = self.cmpObsProp.toPlainText()
        if not campo:
            self.label_ObsProp.setText('Requerido')
            self.label_ObsProp.setStyleSheet('QLabel {color: red;}')
            res = False"""
        # Check Codigos Postales
        # Cantidad
        campo = unicode(self.cmpCPACant.text())
        if not campo:
            self.label_CPACant.setText('Requerido')
            self.label_CPACant.setStyleSheet('QLabel {color: red;}')
            res = False
        elif not campo.isdigit():
            self.label_CPACant.setText('Cantidad invalida')
            self.label_CPACant.setStyleSheet('QLabel {color: red;}')
            res = False
        # Check Consistencia
        campo = self.cmpCodigos.toPlainText()
        if not campo:
            self.label_Codigos.setText('Debe agregar al menos 1 codigo postal')
            self.label_Codigos.setStyleSheet('QLabel {color: red;}')
            res = False
        elif campo:
            cant = int(self.cmpCPACant.text())
            res = cant == len(campo.split('\n'))
            if not res:
                self.label_CPACant.setText('Cantidad no coincide')
                self.label_CPACant.setStyleSheet('QLabel {color: red;}')
                res = False
        # Check Organizador
        currentText = self.comboBoxOrganizador.currentText()
        id_item = currentText.split('-')[0]
        campo = self.cmpMatriculaOrg.text()
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
        # Check Bien asegurado
        campo = self.cmpBienAseg.text()
        if not campo:
            self.label_BienAseg.setText('Requerido')
            self.label_BienAseg.setStyleSheet('QLabel {color: red;}')
            res = False
        # Check Suma asegurada
        campo = str(self.cmpSumaAseg.text())
        if not campo or not campo.isdigit():
            self.label_SumaAseg.setText('Requerido')
            self.label_SumaAseg.setStyleSheet('QLabel {color: red;}')
            res = False

        """
        Fechas
        fecha desde  | fecha hasta   | Resultado
        vacia        | vacia         | OK
        vacia        | fecha valida  | Error
        fecha valida | vacia         | OK
        fecha valida | fecha valida  | fechaDesde <= fechaHasta? OK: Error
        """
        # Check Cobertura Fecha Desde
        fechaD = self.cmpFechaDes.text()
        fechaH = self.cmpFechaHas.text()
        a = self.is_valid_date(fechaD)  # (Bool, Date)
        if fechaD and not a[0]:  # Hay algo en fechaD pero no es una fecha
            self.label_FechaDes.setText('Fecha no valida')
            self.label_FechaDes.setStyleSheet('QLabel {color: red;}')
            res = False
        b = self.is_valid_date(fechaH)  # (Bool, Date)
        if fechaH and not b[0]:  # Hay algo en fechaH pero no es una fecha
            self.label_FechaHas.setText('Fecha no valida')
            self.label_FechaHas.setStyleSheet('QLabel {color: red;}')
            res = False
        if not fechaD and b[0]:  # FechaDesde=empty and FechaHasta=Date
            self.label_FechaDes.setText('Requerido')
            self.label_FechaDes.setStyleSheet('QLabel {color: red;}')
            res = False
        elif a[0] and b[0] and a[1] > b[1]:
            # Check that date 'a' is less than date 'b'
            self.label_FechaHas.setText('Debe ser mayor que Fecha Desde')
            self.label_FechaHas.setStyleSheet('QLabel {color: red;}')
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

        # Name of the columns
        fechaRegistro = 'Fecha Registro'
        asegurados = 'Asegurados o proponentes\nNombre-TipoDoc-Doc-T.Aseg'
        cpa_prop = 'CPA/CP Prop.'
        cpa_obs = 'Observaciones\nCPA/CP'
        cpa_cant = 'CPA/CP Cant.'
        cpas = 'CPAS.'
        compania = 'Compania'
        organizador = 'Organizador\nMatricula-T.Persona'
        bien_aseg = 'Bien a asegurar'
        ramo = 'Ramo'
        suma_aseg = 'Suma a asegurar'
        vigencia = 'Vigencia\nDesde-Hasta'
        tipo_op = 'Tipo operacion\nTipo-Poliza'
        flota = 'Flota'
        tipo_contacto = 'Tipo Contacto'
        li = ['ID', fechaRegistro, asegurados, cpa_prop, cpa_obs, cpa_cant,
              cpas, compania, organizador, bien_aseg, ramo, suma_aseg,
              vigencia, tipo_op, flota, tipo_contacto]

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
                               self.save_as_docx)

        self.actionAbrir_archivo.triggered.connect(self.loadFile)
        self.actionGuardar_como.triggered.connect(self.saveFile)
        self.actionAgregar_archivo_xml.triggered.connect(self.add_file)
        self.actionAgregar_registro.triggered.connect(self.dialog_add_reg)
        self.actionTodos_los_registros.triggered.connect(
            self.show_all_registers)
        # Filter for Responsabilidad Civil
        mapper = QtCore.QSignalMapper(self.ui)
        mapper.setMapping(self.actionResponsabilidad_civil, RAMO_ID)
        self.actionResponsabilidad_civil.triggered.connect(mapper.map)
        mapper.mapped['QString'].connect(self.register_filter)

    def save_as_docx(self):
        "Save a document for Microsoft Windows >= 2007"
        if self.tabla.rowCount() > 0:
            doc = Docx('files/operaciones.docx')
            table = doc.tables[0]
            for elem in self.delete_list:
                del(self.registers[elem])
            regs = self.registers.values()
            # Order for date
            regs.sort(key=lambda t: t[0])
            i = 1
            ca = self.get_dataFromFile('files/TablaCompania.json')
            ramo = self.get_dataFromFile('files/ramos.json')
            monedas = self.get_dataFromFile('files/tiposMonedas.json')
            rows = table.row_cells(0)
            for e in regs:
                fechaRegistro = e[1]['fechaRegistro']
                nombres = []
                direcciones = []
                ubicaciones = []
                for elem in e[1]['asegurados']:
                    n = elem[0]
                    nombre = n[:n.find('-')]
                    direccion = n[n.find('-')+1:n.rfind('-')]
                    ubicacion = n[n.rfind('-')+1:]
                    nombres.append(unicode(nombre.strip()))
                    direcciones.append(unicode(direccion.strip()))
                    ubicaciones.append(unicode(ubicacion.strip()))
                ciaId = e[1]['ciaId']
                aseguradora = ca[ciaId]['Denominacion']
                bienAsegurado = e[1]['bienAsegurado']
                riesgo = ramo[e[1]['ramo']]['Descripcion']
                moneda = monedas[e[1]['sumaAseguradaTipo']]['Signo']
                sumaAseg = moneda + ' ' + e[1]['sumaAsegurada']
                vigencia = e[1]['coberturaFechaDesde'] + '\n' + \
                    e[1]['coberturaFechaHasta']
                # Fill table
                rows[0].text = str(i)
                rows[T_FREG].text = fechaRegistro
                rows[T_NYA].text = '\n'.join(nombres)
                rows[T_DIR].text = '\n'.join(direcciones)
                rows[T_UBIC].text = '\n'.join(ubicaciones)
                rows[T_CIA].text = unicode(aseguradora)
                rows[T_BIEN].text = unicode(bienAsegurado)
                rows[T_RIESGO].text = unicode(riesgo)
                rows[T_SUMASEG].text = unicode(sumaAseg)
                rows[T_VIGENCIA].text = vigencia
                rows = table.add_row().cells
                i += 1
            name = QFileDialog.getSaveFileName(self.ui, 'Guardar como...',
                                               filter='*.docx')
            if unicode(name).endswith('.docx'):
                doc.save(unicode(name))
            else:
                doc.save(unicode(name)+'.docx')

    def saveFile(self):
        """Save a xml file as <filename>.xml"""
        if self.tabla.rowCount() > 0:
            doc = NewDocumentOperacion()
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
                reg['fechaRegistro'] = str(ui.cmpFechaRegistro.text())
                # Asegurados
                currentText = ui.cmpAsegurados.toPlainText()
                list_aseg = currentText.split('\n')
                t = []
                for a in list_aseg:
                    elem = a.split(',')
                    tp = unicode(elem[0].split('-')[0])
                    td = unicode(elem[1].split('-')[0])
                    nd = unicode(elem[2])
                    n = unicode(elem[3])
                    t.append((n, td, nd, tp))
                reg['asegurados'] = t
                reg['cpaProponente'] = unicode(ui.cmpCPAP.text())
                reg['obsProponente'] = unicode(ui.cmpObsProp.toPlainText())
                reg['cpaCantidad'] = unicode(ui.cmpCPACant.text())
                # Codigos Postales
                currentText = ui.cmpCodigos.toPlainText()
                list_cp = currentText.split('\n')
                cps = []
                for c in list_cp:
                    cps.append(unicode(c))
                reg['codigosPostales'] = cps
                cid = unicode(ui.comboBoxCiaId.currentText())
                reg['ciaId'] = cid.split('-')[0]
                org = str(ui.comboBoxOrganizador.currentText())
                mat = str(ui.cmpMatriculaOrg.text())
                reg['organizador'] = (mat, org.split('-')[0])
                reg['bienAsegurado'] = unicode(ui.cmpBienAseg.text())
                r = unicode(ui.comboBoxRamo.currentText()).split('-')[0]
                reg['ramo'] = r
                reg['sumaAsegurada'] = unicode(ui.cmpSumaAseg.text())
                sa = unicode(ui.comboBoxSumaTipo.currentText())
                reg['sumaAseguradaTipo'] = sa.split('-')[0]
                reg['coberturaFechaDesde'] = unicode(ui.cmpFechaDes.text())
                reg['coberturaFechaHasta'] = unicode(ui.cmpFechaHas.text())
                tipOp = unicode(ui.comboBoxTipoOp.currentText())
                reg['tipoOperacion'] = tipOp.split('-')[0]
                reg['poliza'] = unicode(ui.cmpPoliza.text())
                checkFlota = ui.checkBoxFlota.checkState()
                if checkFlota:
                    reg['flota'] = '1'
                else:
                    reg['flota'] = '0'
                contact = unicode(ui.comboBoxContacto.currentText())
                reg['tipoContacto'] = contact.split('-')[0]

                row = len(self.registers)
                dato = reg['fechaRegistro']
                if dato:
                    dato = dato.replace('/', '-')
                    d, m, a = dato.split('-')
                    newDate = datetime.date(int(a), int(m), int(d))
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
                item_id = item_id.text().toUtf8().data()

                # Get the new date. Should be dd/mm/yyyy or dd-mm-yyyy
                dato = ui.cmpFecha.text().toUtf8().data()
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
                        # self.doc.change_date_register(reg, dato)
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
                    doc = DocumentOperacion(filename,
                                            'files/SchemaOperacion.xsd')
                    row = len(self.registers)
                    while not doc.is_empty_regs():
                        reg = doc.get_register()
                        data = doc.get_data_register(reg)
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
                self.doc = DocumentOperacion(filename,
                                             'files/SchemaOperacion.xsd')
                header_data = self.doc.get_header()
                tp = self.get_dataFromFile('files/tipoPersona.json')
                value = tp[header_data['tipoPersona']]['Descripcion']
                self.label_TipoPersona.setText(value)
                self.label_Matricula.setText(header_data['matricula'])
                self.label_CantReg.setText(header_data['cantidadRegistros'])

                row = 0
                while(not self.doc.is_empty_regs()):
                    reg = self.doc.get_register()
                    data = self.doc.get_data_register(reg)
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
        fechaReg = self.format_date(reg['fechaRegistro'])
        self.tabla.setItem(row, T_FECHREG, QtGui.QTableWidgetItem(fechaReg))

        # Asegurados
        # n = Nombre, td = TipoDoc, nd = NroDoc, ta = TipoAsegurado
        tipoAsegurado = self.get_dataFromFile('files/tipoPersona.json')
        tipoDoc = self.get_dataFromFile('files/tiposDocumentos.json')
        list_aseg = []
        for n, td, nd, ta in reg['asegurados']:
            ta = tipoAsegurado[ta]['Descripcion']
            td = tipoDoc[td]['Descripcion']
            list_aseg.append('-'.join((n, td, nd, ta)))
        asegurados = '\n'.join(list_aseg)
        self.tabla.setItem(row, 2, QtGui.QTableWidgetItem(asegurados))

        cpa_p = reg['cpaProponente']
        self.tabla.setItem(row, 3, QtGui.QTableWidgetItem(cpa_p))

        cpa_obs = reg['obsProponente']
        self.tabla.setItem(row, 4, QtGui.QTableWidgetItem(cpa_obs))

        cpa_cant = reg['cpaCantidad']
        self.tabla.setItem(row, 5, QtGui.QTableWidgetItem(cpa_cant))

        cpas = '\n'.join(reg['codigosPostales'])
        self.tabla.setItem(row, 6, QtGui.QTableWidgetItem(cpas))

        # Compania
        tablaCompania = self.get_dataFromFile('files/TablaCompania.json')
        compania = reg['ciaId']
        compania = tablaCompania[compania]['DenominacionCorta']
        self.tabla.setItem(row, 7, QtGui.QTableWidgetItem(compania))

        # Organizador
        if reg['organizador']:
            matricula, tp_org = reg['organizador']
            tp_org = tipoAsegurado[tp_org]['Descripcion']
            organizador = '-'.join((matricula, tp_org))
            self.tabla.setItem(row, 8, QtGui.QTableWidgetItem(organizador))

        bien = reg['bienAsegurado']
        self.tabla.setItem(row, 9, QtGui.QTableWidgetItem(bien))

        # Ramo
        tablaRamo = self.get_dataFromFile('files/ramos.json')
        r = reg['ramo']
        if r in tablaRamo.keys():
            ramo = tablaRamo[r]['Descripcion']
        else:
            ramo = r
        self.tabla.setItem(row, 10, QtGui.QTableWidgetItem(ramo))

        # Suma asegurada y su tipo
        monedas = self.get_dataFromFile('files/tiposMonedas.json')
        id_tipo = reg['sumaAseguradaTipo']
        moneda = monedas[id_tipo]['Signo']
        suma_aseg = moneda + ' ' + reg['sumaAsegurada']
        self.tabla.setItem(row, 11, QtGui.QTableWidgetItem(suma_aseg))

        vigencia = '\n'.join((self.format_date(reg['coberturaFechaDesde']),
                              self.format_date(reg['coberturaFechaHasta'])))
        self.tabla.setItem(row, 12, QtGui.QTableWidgetItem(vigencia))

        # Tipo operacion y poliza
        tipoOperacion = self.get_dataFromFile('files/tipoOperacion.json')
        poliza = reg['poliza']
        id_top = reg['tipoOperacion']
        tipo_op = tipoOperacion[id_top]['Descripcion'] + '\n' + poliza
        self.tabla.setItem(row, 13, QtGui.QTableWidgetItem(tipo_op))

        num_flota = reg['flota']
        flota = 'No'
        if num_flota == '1':
            flota = 'Si'
        self.tabla.setItem(row, 14, QtGui.QTableWidgetItem(flota))

        # Tipo Contacto
        tipoContacto = self.get_dataFromFile('files/tipoContacto.json')
        id_tc = reg['tipoContacto']
        tipo_cont = tipoContacto[id_tc]['Descripcion']
        self.tabla.setItem(row, 15, QtGui.QTableWidgetItem(tipo_cont))

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

    def register_filter(self, campo):
        """
        Show a table filtering with the element campo
        Argument:
            A int representing a field
        """
        if self.registers:
            self.clear_table()
            # registers[k][0] is the date, registers[k][1] is the register
            # and register is a dict
            list_regs = [(k, self.registers[k][0], self.registers[k][1])
                         for k in self.registers.keys()
                         if self.registers[k][1]['ramo'] == campo]
            list_regs.sort(key=lambda t: t[1])
            for t in list_regs:
                reg = t[2]
                k = t[0]
                self.show_register(k, reg)

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
