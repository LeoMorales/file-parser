# -*- coding: utf-8 -*-
# @Author: leomorales

LONGITUD_VALIDA_DE_LINEA = 162
OFFSET_MATRICULA = 8
OFFSET_CLASE = 4
OFFSET_TIPO_DOCUMENTO = 9
OFFSET_SECCION = 4
OFFSET_CIRCUITO = 4
OFFSET_MESA = 4
OFFSET_SEXO = 1
OFFSET_ORDEN_PADRON = 4

class DataExtractor(object):
    """docstring for DataExtractor"""
    def __init__(self):
        super(DataExtractor, self).__init__()
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
        if len(data) > LONGITUD_VALIDA_DE_LINEA:
            print(len(data))
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
