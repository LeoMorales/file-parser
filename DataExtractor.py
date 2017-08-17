# -*- coding: utf-8 -*-
# @Author: leomorales
#
#   Los extractores de datos, saben como tratar (parsear) un string
#   para generar un objeto de salida (en estos casos trabajamos con
#   diccionarios, pero podrian ser un objeto tambien).
#   Este objeto de salida va a poder ser correctamente utilizado
#   por el worker que utiliza este data esxtractor.

LONGITUD_VALIDA_DE_LINEA = 162
OFFSET_MATRICULA = 8
OFFSET_CLASE = 4
OFFSET_TIPO_DOCUMENTO = 9
OFFSET_SECCION = 4
OFFSET_CIRCUITO = 4
OFFSET_MESA = 4
OFFSET_SEXO = 1
OFFSET_ORDEN_PADRON = 4

#Constantes para process_escuela:
CELDA_A0 = "Nombre"
COLUMNA_NOMBRE = 0
COLUMNA_DOMICILIO = 1
COLUMNA_MESA_DESDE = 5
COLUMNA_MESA_HASTA = 6

class DataExtractor(object):
    """docstring for DataExtractor"""
    def __init__(self):
        super(DataExtractor, self).__init__()
        self.last_data_received = None
        self.last_data_processed = None

    def process_person(self, data):
        """
            Recibe una linea de 160 caracteres de al forma:
                '999999991900PEREZ                                   JUAN AMALIO                                    AV 9 de JULIO y CORRIENTES        DNI-EA     1   1 0001F 001'

            que respeta el siguiente formato:
                matricula (8)
                clase(4)
                apellido(40)
                nombres(47)
                domicilio(35)
                tipo documento(9)
                seccion(4)
                circuito(4)
                mesa(4)
                sexo(1)
                nro orden padron(4)  
            y retorna un dict con la informacion de la persona tokenizada.
        """
        if data == self.last_data_received:
            print("it founded in cache :P")
            return self.last_data_processed

        if len(data) > LONGITUD_VALIDA_DE_LINEA:
            print("Error: line to long: {}".format(len(data)))
            return None
        
        # primera separacion:
        col1 = data[0:52].rstrip() # contiene la matricula la clase y el apellido
        nombres = data[52:99].strip()  # contiene los nombres
        domicilio = data[99:133].strip()  # contiene el domicilio
        col4 = data[133:].strip()  # contien tipo de doc, seccion, circuito, mesa, sexo y nro de orden en el padron
        # existen casos en que viene sin tipo de documento, al stripear nos queda una linea mas chica...
        # entonces ese caso es tenido en cuenta en procesar_cuarta_columna y se da por hecho que el dato faltante es
        # el tipo de documento.
        
        person = {}
        person = self.procesar_primer_col(col1, person)
        person['nombres'] = nombres.replace("'", "")
        person['domicilio'] = domicilio.replace("'", "").replace('"', "")
        person = self.procesar_cuarta_col(col4, person)
        
        self.last_data_received = data
        self.last_data_processed = person
        return person

    def procesar_primer_col(self, columna, person):
        person ['matricula'] = columna[0:OFFSET_MATRICULA].strip()
        person ['clase'] = columna[OFFSET_MATRICULA: (OFFSET_MATRICULA+OFFSET_CLASE)].strip()
        person ['apellido'] = columna[(OFFSET_MATRICULA+OFFSET_CLASE):].strip().replace("'", "")
        return person
        
    def procesar_cuarta_col(self, columna, person):
        if len(columna) < 24:
            # es el caso en el que viene sin tipo de doc
            # es el unico caso que se descubrio en 10k registros
            person ['tipo_documento'] = ""
            person ['nro_orden_padron'] = columna[-4:].strip()
            person ['sexo'] = columna[-5:-4].strip()
            person ['mesa'] = columna[-9:-5].strip()
            person ['circuito'] = columna[-13: -9].strip()
            person ['seccion'] = columna[:-13].strip()
            return person

        person ['tipo_documento'] = columna[0:OFFSET_TIPO_DOCUMENTO].strip()
        person ['seccion'] = columna[9: 9+OFFSET_SECCION].strip()
        person ['circuito'] = columna[13: 13+OFFSET_CIRCUITO].strip()
        person ['mesa'] = columna[17: 17+OFFSET_MESA].strip()
        person ['sexo'] = columna[21: 21+OFFSET_SEXO].strip()
        person ['nro_orden_padron'] = columna[22:].strip()

        return person

    def process_escuela(self, data):
        """
            Recibe una linea con el formato:
            ESCUELA N° 9999    ANTARTIDA ARGENTINA 9999 RAWSON    1    1    1    4    4    9999

            Retorna un dict <<escuela>> con la informacion que nos importa:
            >>pprint(escuela)
            >> {
                    'nombre': 'ESCUELA N° 9999'
                    'domicilio': 'ANTARTIDA ARGENTINA 9999 RAWSON'
                    'mesa-desde': 1
                    'mesa-hasta': 4
                }
            Si la linea no respeta el formato, retorna dict vacio.

        """
        # return "".join(map(lambda s: "{} ||| ".format(s), data.split(";")))
        columnas = data.split(";")
        if len(columnas) > 10:
            return {}
        if columnas[0] == CELDA_A0:
            return {}
        
        escuela = {}
        escuela['nombre'] = columnas[COLUMNA_NOMBRE]
        escuela['domicilio'] = columnas[COLUMNA_DOMICILIO]
        escuela['mesa-desde'] = columnas[COLUMNA_MESA_DESDE]
        escuela['mesa-hasta'] = columnas[COLUMNA_MESA_HASTA]
        return escuela
