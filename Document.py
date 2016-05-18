# -*- coding = utf-8 -*-

from xml.dom import minidom
from minixsv import pyxsval


class DocumentCobranza:
    "Class with methods for creating xml file cobranza."
    def __init__(self, filenameXML, filenameXSD):
        self.doc = pyxsval.parseAndValidate(filenameXML, filenameXSD)
        self.document = self.doc.getTree().document
        self.regs = self.document.getElementsByTagName('Registro')

    def get_header(self):
        "Return a dictionary with matricula, tipoPersona and cantidadRegistros"
        data = {}
        productor = self.document.getElementsByTagName('Productor')[0]
        matricula = productor.getAttribute('Matricula')
        data['matricula'] = matricula
        tipoPersona = productor.getAttribute('TipoPersona')
        data['tipoPersona'] = tipoPersona
        nodeCantReg = self.document.getElementsByTagName('CantidadRegistros')
        cantidadReg = nodeCantReg[0]
        data['cantidadRegistros'] = ''
        if cantidadReg.hasChildNodes():
            data['cantidadRegistros'] = cantidadReg.firstChild.data
        return data

    def is_empty_regs(self):
        "Return True if there is not register otherwise False"
        if self.regs:
            return False
        else:
            return True

    def get_register(self):
        "Return a node register"
        reg = ''
        if self.regs:
            reg = self.regs.pop(0)
        return reg

    def get_data_from_element(self, elem):
        "Return a string data from a element of xml file"
        ret = ''
        if elem.hasChildNodes():
            ret = elem.firstChild.data
        return ret

    def get_data_from_register(self, reg):
        "Return a dictionary data from a element Registro."
        data = {}
        if reg:
            # Tipo Registro
            tipoRegistro = reg.getElementsByTagName('TipoRegistro')[0]
            data['tipoRegistro'] = self.get_data_from_element(tipoRegistro)

            # Fecha Registro
            fechaRegistro = reg.getElementsByTagName('FechaRegistro')[0]
            data['fechaRegistro'] = self.get_data_from_element(fechaRegistro)

            # Concepto
            concepto = reg.getElementsByTagName('Concepto')[0]
            data['concepto'] = self.get_data_from_element(concepto)

            # Polizas
            data['polizas'] = []
            nodePolizas = reg.getElementsByTagName('Polizas')[0]
            polizas = nodePolizas.getElementsByTagName('Poliza')
            for poliza in polizas:
                if poliza.hasChildNodes():
                    data['polizas'].append(poliza.firstChild.data)

            # Compania
            ciaid = reg.getElementsByTagName('CiaID')[0]
            data['ciaId'] = self.get_data_from_element(ciaid)

            # Organizador is a tuple (matricula, tipoPersona)
            organizador = reg.getElementsByTagName('Organizador')
            data['organizador'] = ''
            if organizador:
                element = organizador[0]
                matricula = element.getAttribute('Matricula')
                tipoPersona = element.getAttribute('TipoPersona')
                data['organizador'] = (matricula, tipoPersona)

            # Importe
            importe = reg.getElementsByTagName('Importe')[0]
            data['importe'] = self.get_data_from_element(importe)

            # Importe tipo
            importeTipo = reg.getElementsByTagName('ImporteTipo')[0]
            data['importeTipo'] = self.get_data_from_element(importeTipo)

        return data


class NewDocumentOperacion:
    """
    Class with methods for creating xml file Operacion.
    """
    def __init__(self):
        self.doc = minidom.Document()
        # Tag <SSN>
        self.root = self.doc.createElement("SSN")
        self.doc.appendChild(self.root)
        # Tag <Cabecera>
        self.header = self.doc.createElement("Cabecera")
        self.root.appendChild(self.header)
        # Tag <Detalle>
        self.detail = self.doc.createElement("Detalle")
        self.root.appendChild(self.detail)

    def format_date(self, fecha):
        """Formats the date.
        Input:
            Date as a string.
        Return:
            A date as a string with this format: yyyy-mm-dd
        """
        s = fecha.replace('/', '-')
        res = ''
        if s.count('-') == 2 and s.replace('-', '').isdigit():
            str1, str2, str3 = s.split('-')
            if len(str1) == 4:  # yyyy-mm-dd
                res = s
            elif len(str3) == 4:  # dd-mm-yyyy
                res = '-'.join((str3, str2, str1))
        return res

    def create_header(self, data):
        """
        Building a structure like:
            <Cabecera>
                <Productor TipoPersona='' Matricula=''/>
                <CantidadRegistros></CantidadRegistros>
            </Cabecera>
        Create a header from a data dictionary
        The key=value of data dictionary are:
            tipoPersona = <string>
            matricula = <string>
            cantidadRegistros = <string>
        """
        productor = self.doc.createElement("Productor")
        if data['tipoPersona']:
            productor.setAttribute("TipoPersona", str(data['tipoPersona']))
        if data['matricula']:
            productor.setAttribute("Matricula", str(data['matricula']))
        self.header.appendChild(productor)
        cantReg = self.doc.createElement("CantidadRegistros")
        value_cant = str(data['cantidadRegistros'])
        cantReg.appendChild(self.doc.createTextNode(value_cant))
        self.header.appendChild(cantReg)

    def create_register(self, data):
        """
        Build an XML structure as:
        <Registro>
            <FechaRegistro></FechaRegistro>
            <Asegurados>
                <Asegurado TipoAsegurado='' TipoDoc='' NroDoc='' Nombre=''>
                </Asegurado>
            </Asegurados>
            <CPAProponente></CPAProponente>
            <ObsProponente></ObsProponente>
            <CPACantidad></CPACantidad>
            <CodigosPostales>
                <CPA></CPA>
            </CodigoPostales>
            <CiaID></CiaID>
            <Organizador TipoPersona='' Matricula=''/>
            <BienAsegurado></BienAsegurado>
            <Ramo></Ramo>
            <SumaAsegurada></SumaAsegurada>
            <SumaAseguradaTipo></SumaAseguradaTipo>
            <CoberturaFechaDesde></CoberturaFechaDesde>
            <CoberturaFechaHasta></CoberturaFechaHasta>
            <TipoOperacion></TipoOperacion>
            <Poliza></Poliza>
            <Flota></Flota>
            <TipoContacto></TipoContacto>
        </Registro>

        The key=value of data dictionary are:
            fechaRegistros = <string>
            asegurados = [(Nombre1, TipoDoc1, NroDoc1, TipoAsegurado1),
                         (Nombre2, TipoDoc2, NroDoc2, TipoAsegurado2), ...]
            cpaProponente = <string>
            obsProponente = <string>
            cpaCantidad = <string>
            codigosPostales = [<string1>, <string2>, ...]
            ciaId = <string>
            bienAsegurado = <string>
            ramo = <string>
            sumaAsegurada = <string>
            sumaAseguradaTipo = <string>
            fechaDesde = <string>
            fechaHasta = <string>
            tipoOperacion = <string>
            poliza = <string>
            flota = <string>
            tipoContacto = <string>
        """
        reg = self.doc.createElement("Registro")
        fechaReg = self.doc.createElement("FechaRegistro")
        value_fr = self.format_date(data['fechaRegistro'])
        fechaReg.appendChild(self.doc.createTextNode(value_fr))
        reg.appendChild(fechaReg)
        asegurados = self.doc.createElement("Asegurados")
        for n, td, nd, ta in data['asegurados']:
            asegurado = self.doc.createElement("Asegurado")
            if ta:
                asegurado.setAttribute('TipoAsegurado', ta)
            if td:
                asegurado.setAttribute('TipoDoc', td)
            if nd:
                asegurado.setAttribute('NroDoc', nd)
            if n:
                asegurado.setAttribute('Nombre', n)
            asegurados.appendChild(asegurado)
        reg.appendChild(asegurados)

        cpaProp = self.doc.createElement("CPAProponente")
        value_cpap = unicode(data['cpaProponente'])
        cpaProp.appendChild(self.doc.createTextNode(value_cpap))
        reg.appendChild(cpaProp)

        obsProp = self.doc.createElement("ObsProponente")
        value_obsp = unicode(data['obsProponente'])
        obsProp.appendChild(self.doc.createTextNode(value_obsp))
        reg.appendChild(obsProp)

        cpaCant = self.doc.createElement("CPACantidad")
        cpaCant.appendChild(self.doc.createTextNode(str(data['cpaCantidad'])))
        reg.appendChild(cpaCant)
        codigosPostales = self.doc.createElement("CodigosPostales")
        for cp in data['codigosPostales']:
            codPost = self.doc.createElement("CPA")
            codPost.appendChild(self.doc.createTextNode(str(cp)))
            codigosPostales.appendChild(codPost)
        reg.appendChild(codigosPostales)
        ciaId = self.doc.createElement("CiaID")
        ciaId.appendChild(self.doc.createTextNode(str(data['ciaId'])))
        reg.appendChild(ciaId)

        if data['organizador']:
            organizador = self.doc.createElement('Organizador')
            m, tp = data['organizador']
            organizador.setAttribute('TipoPersona', tp)
            organizador.setAttribute('Matricula', m)
            reg.appendChild(organizador)

        bienAseg = self.doc.createElement("BienAsegurado")
        value_ba = unicode(data['bienAsegurado'])
        bienAseg.appendChild(self.doc.createTextNode(value_ba))
        reg.appendChild(bienAseg)

        ramo = self.doc.createElement("Ramo")
        ramo.appendChild(self.doc.createTextNode(str(data['ramo'])))
        reg.appendChild(ramo)

        sumAseg = self.doc.createElement("SumaAsegurada")
        value_sa = unicode(data['sumaAsegurada'])
        sumAseg.appendChild(self.doc.createTextNode(value_sa))
        reg.appendChild(sumAseg)

        sumAsegT = self.doc.createElement("SumaAseguradaTipo")
        value_sat = str(data['sumaAseguradaTipo'])
        sumAsegT.appendChild(self.doc.createTextNode(value_sat))
        reg.appendChild(sumAsegT)

        if data['coberturaFechaDesde']:
            cobertura_fd = self.doc.createElement("CoberturaFechaDesde")
            value_fd = self.format_date(data['coberturaFechaDesde'])
            cobertura_fd.appendChild(self.doc.createTextNode(value_fd))
            reg.appendChild(cobertura_fd)

        if data['coberturaFechaHasta']:
            cobertura_fh = self.doc.createElement('CoberturaFechaHasta')
            value_fh = self.format_date(data['coberturaFechaHasta'])
            cobertura_fh.appendChild(self.doc.createTextNode(value_fh))
            reg.appendChild(cobertura_fh)

        tipo_operacion = self.doc.createElement("TipoOperacion")
        value_tp = str(data['tipoOperacion'])
        tipo_operacion.appendChild(self.doc.createTextNode(value_tp))
        reg.appendChild(tipo_operacion)

        if data['poliza']:
            poliza = self.doc.createElement('Poliza')
            poliza.appendChild(self.doc.createTextNode(str(data['poliza'])))
            reg.appendChild(poliza)

        flota = self.doc.createElement("Flota")
        flota.appendChild(self.doc.createTextNode(str(data['flota'])))
        reg.appendChild(flota)

        tipo_cont = self.doc.createElement("TipoContacto")
        value_tc = str(data['tipoContacto'])
        tipo_cont.appendChild(self.doc.createTextNode(value_tc))
        reg.appendChild(tipo_cont)
        self.detail.appendChild(reg)

    def save(self, filename):
        "Save the xml with filename"
        xml_str = self.doc.toprettyxml(indent="  ", encoding="utf-8")
        with open(filename, 'w') as f:
            f.write(xml_str)


class DocumentOperacion:
    def __init__(self, filenameXML, filenameXSD):
        self.fileout = filenameXML
        self.doc = pyxsval.parseAndValidate(filenameXML, filenameXSD)
        self.tree = self.doc.getTree()
        self.regs = self.tree.document.getElementsByTagName('Registro')

    def is_empty_regs(self):
        if self.regs:
            return False
        else:
            return True

    def get_register(self):
        ret = ''
        if self.regs:
            ret = self.regs.pop(0)
        return ret

    def get_header(self):
        data = {}
        header = self.tree.document.getElementsByTagName('Cabecera')[0]
        prod = header.getElementsByTagName('Productor')[0]
        data['matricula'] = prod.getAttribute('Matricula')
        data['tipoPersona'] = prod.getAttribute('TipoPersona')
        cantReg = header.getElementsByTagName('CantidadRegistros')[0]
        data['cantidadRegistros'] = self.get_data_from_element(cantReg)
        return data

    def get_data_from_element(self, elem):
        res = ''
        if elem.hasChildNodes():
            res = elem.firstChild.data
        return res

    def format_date(self, fecha):
        """Formats the date.
        Input:
            Date as a string.
        Return:
            A date as a string with this format: yyyy-mm-dd
        """
        s = fecha.replace('/', '-')
        res = ''
        if s.count('-') == 2 and s.replace('-', '').isdigit():
            str1, str2, str3 = s.split('-')
            if len(str1) == 4:  # yyyy-mm-dd
                res = s
            elif len(str3) == 4:  # dd-mm-yyyy
                res = '-'.join((str3, str2, str1))
        return res

    def get_data_register(self, reg):
        """Return the dates from a register
        Input:
            A node register from a xml file Operacion
        Return:
            A data dictionary
        """
        data = {}
        nodeFechaReg = reg.getElementsByTagName('FechaRegistro')[0]
        fechaReg = self.get_data_from_element(nodeFechaReg)
        data['fechaRegistro'] = self.format_date(fechaReg)

        asegurados = reg.getElementsByTagName('Asegurados')[0]
        asegurado_list = asegurados.getElementsByTagName('Asegurado')
        valor = []
        for e in asegurado_list:
            n = e.getAttribute('Nombre')
            td = e.getAttribute('TipoDoc')
            nd = e.getAttribute('NroDoc')
            ta = e.getAttribute('TipoAsegurado')
            valor.append((n, td, nd, ta))
        data['asegurados'] = valor

        cpaProp = reg.getElementsByTagName('CPAProponente')[0]
        data['cpaProponente'] = self.get_data_from_element(cpaProp)

        obsProp = reg.getElementsByTagName('ObsProponente')[0]
        data['obsProponente'] = self.get_data_from_element(obsProp)

        cpaCant = reg.getElementsByTagName('CPACantidad')[0]
        data['cpaCantidad'] = self.get_data_from_element(cpaCant)

        codPost = reg.getElementsByTagName('CodigosPostales')[0]
        cod_list = codPost.getElementsByTagName('CPA')
        valor = []
        for e in cod_list:
            cp = self.get_data_from_element(e)
            valor.append(cp)
        data['codigosPostales'] = valor

        ciaid = reg.getElementsByTagName('CiaID')[0]
        data['ciaId'] = self.get_data_from_element(ciaid)

        organs = reg.getElementsByTagName('Organizador')
        data['organizador'] = ''
        if organs:
            organ = organs[0]
            tp = organ.getAttribute('TipoPersona')
            value = (organ.getAttribute('Matricula'), tp)
            data['organizador'] = value

        bienAseg = reg.getElementsByTagName('BienAsegurado')[0]
        data['bienAsegurado'] = self.get_data_from_element(bienAseg)

        ramo = reg.getElementsByTagName('Ramo')[0]
        data['ramo'] = self.get_data_from_element(ramo)

        sumaAseg = reg.getElementsByTagName('SumaAsegurada')[0]
        data['sumaAsegurada'] = self.get_data_from_element(sumaAseg)

        sumaAsegT = reg.getElementsByTagName('SumaAseguradaTipo')[0]
        data['sumaAseguradaTipo'] = self.get_data_from_element(sumaAsegT)

        cobDesde = reg.getElementsByTagName('CoberturaFechaDesde')[0]
        data['coberturaFechaDesde'] = self.get_data_from_element(cobDesde)

        cobHasta = reg.getElementsByTagName('CoberturaFechaHasta')[0]
        data['coberturaFechaHasta'] = self.get_data_from_element(cobHasta)

        tipoOp = reg.getElementsByTagName('TipoOperacion')[0]
        data['tipoOperacion'] = self.get_data_from_element(tipoOp)

        p = reg.getElementsByTagName('Poliza')
        if not p:
            data['poliza'] = ''
        else:
            poliza = p[0]
            data['poliza'] = self.get_data_from_element(poliza)

        flota = reg.getElementsByTagName('Flota')[0]
        data['flota'] = self.get_data_from_element(flota)

        tipoCont = reg.getElementsByTagName('TipoContacto')[0]
        data['tipoContacto'] = self.get_data_from_element(tipoCont)

        return data

    def change_date_register(self, reg, newdate):
        """
        Modifies the field: FechaRegistro
        Input:
            - reg: a register
            - newdate: a date as a string
        """
        a = ''
        d = ''
        m = ''
        fecha = reg.getElementsByTagName('FechaRegistro')[0]
        if '-' in newdate:
            d, m, a = newdate.split('-')
        elif '/' in newdate:
            d, m, a = newdate.split('/')
        if a:
            fecha.firstChild.replaceWholeText('-'.join([a, m, d]))

    def save(self, fileoutput):
        """Save the document as xml file
        Input:
            fileoutput: a path or name file output
        """
        with open(fileoutput, 'w') as f:
            f.write(self.tree.document.toxml(encoding='UTF-8'))
