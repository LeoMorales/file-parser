# -*- coding: utf-8 -*-
# @Author: leomorales
# @Date:   2017-08-14 15:17:59
# @Last Modified by:   leomorales
# @Last Modified time: 2017-08-09 17:23:52
try:
    from xlsxwriter import Workbook
except ImportError:
    imposible_generar_excel = True

import codecs
from pprint import pprint
import utiles
from constants import (
    OUTPUT_FILE_NAME_TEMPLATE,
    SQL_FILE_HEADER,
    SQL_VALUE_LINE_TEMPLATE,
    SQL_UPDATE_LINE_TEMPLATE,
    CLAVES)

LONGITUD_VALIDA_DE_LINEA = 162
OFFSET_MATRICULA = 8
OFFSET_CLASE = 4
OFFSET_TIPO_DOCUMENTO = 9
OFFSET_SECCION = 4
OFFSET_CIRCUITO = 4
OFFSET_MESA = 4
OFFSET_SEXO = 1
OFFSET_ORDEN_PADRON = 4


class WorkerManager(object):
    """
        Para evitar estar presuntanto si tengo que generar los archivos
        SQL, o los excels, o ambos...dejamos que una clase se encargue
        de toda esta logica mientras evitamos preguntarnos:
            - debo generar solo los sql?
            - debo generar solo los excels?
            - debo generar ambos?
        asi, por cada accion que hagamos (inicializacion, acciones
        principales o cierre)
    """
    def __init__(self):
        super(WorkerManager, self).__init__()
        self.workers = []
        self.procesed = 0
        self.not_valids = []
        self.counter = 0
        
    def create_sql_worker(self):
        self.workers.append(SQLWorker())

    def create_excel_worker(self):
        self.workers.append(ExcelWorker())
        
    def init(self, working_file_name):
        for worker in self.workers:
            worker.init(working_file_name)

    def work(self, data):
        """
            En nuestro caso, data va a ser una linea de archivo.
            Cada worker trabaja con ella como lo crea necesario.
        """
        self.counter += 1
        person = self.extraer_data(data)
        if person:
            person['id'] = self.procesed
            for worker in self.workers:
                worker.work(person)
            self.procesed +=1
        else:
            # debug_lineas_no_validas.append(line)
            self.not_valids.append(procesed)

    def finalize(self):
        """
            Finalizar los workers e imprimir la cantitdad de registros
            procesados hasta el momento
        """
        for worker in self.workers:
            worker.finalize()
        print("\nFINALIZADO: {}\n\n".format(self.counter))

    def extraer_data(self, line):
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
        if len(line) > LONGITUD_VALIDA_DE_LINEA:
            print(len(line))
            return None
        
        # primera separacion:
        col1 = line[0:52].rstrip() # contiene la matricula la clase y el apellido
        nombres = line[52:99].strip()  # contiene los nombres
        domicilio = line[99:133].strip()  # contiene el domicilio
        col4 = line[133:].strip()  # contien tipo de doc, seccion, circuito, mesa, sexo y nro de orden en el padron
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
    

class SQLWorker(object):
    """
        SQLWorker:
        Procesa diccionarios con la informacion de la persona
        y genera un archivo con el script SQL correspondiente
        a la carga de dicho lote de registros.
    """
    def __init__(self):
        super(SQLWorker, self).__init__()
    
    def init(self, working_file_name):
        """
            Acciones de inicializacion:
                - Crea el archivo de trabajo.
                - Escribir el HEADER.
                - Inicializar en 0 el contador de lineas.
        """
        # guardamos el nombre para mostrarlo al finalizar:
        self.complete_output_file_name = OUTPUT_FILE_NAME_TEMPLATE.format(working_file_name)
        self.working_file = codecs.open(self.complete_output_file_name, 'w', encoding='utf-8', errors='ignore')
        self.working_file.write(SQL_FILE_HEADER)
        self.lines_writed = 0

    def work(self, a_person):
        """
            Acciones de procesamiento:
                - Llenar el template de linea SQL con los valores del
                diccionario de persona recibido.
                - Escribirlo en el archivo.
                - Incrementar contador de lineas escritas.
        """
        person_values_for_sql = SQL_VALUE_LINE_TEMPLATE.format(
            utiles.validar_matricula(a_person.get('matricula')),
            utiles.validar_tipo_documento(a_person.get('tipo_documento')),
            utiles.validar_clase(a_person.get('clase')),
            utiles.validar_apellido(a_person.get('apellido')),
            utiles.validar_nombres(a_person.get('nombres')),
            utiles.validar_domicilio(a_person.get('domicilio')),
            utiles.validar_seccion(a_person.get('seccion')),
            utiles.validar_circuito(a_person.get('circuito')),
            utiles.validar_mesa(a_person.get('mesa')),
            utiles.validar_sexo(a_person.get('sexo')),
            utiles.validar_nro_de_orden(a_person.get('nro_orden_padron')),
            utiles.validar_id(a_person.get('id')),
            )
        #pprint(person_values_for_sql)
        self.working_file.write(person_values_for_sql)
        self.lines_writed += 1


    def finalize(self):
        """
            Acciones de finalizacion:
                - Cerrar el archivo de trabajo
                - Mostrar el nombre del archivo que se genero.
                - Y la cantidad de lineas escritas
        """
        self.working_file.close()
        print("######## FIN SQL FILE GENERATOR ###########")
        print('\tarchivo generado: {}.'.format(self.complete_output_file_name))
        print('\tcantidad de lineas del archivo {}.'.format(str(self.lines_writed)))



class ExcelWorker(object):
    """
        ExcelWorker
        Procesa diccionarios con la informacion de la persona
        y genera un archivo excel con los registros en filas.
    """
    def __init__(self):
        super(ExcelWorker, self).__init__()
        self.workbook = None
        self.worksheet = None
        self.row_count = 0


    def init(self, output_file_name):
        """
            Acciones de inicializacion:
                - Crear el archivo de trabajo con el nombre recibido.
                - Inicializar la hoja con la que vamos a trabajar.
        """
        self.complete_output_file_name = '../output/excel/'+output_file_name+'.xlsx'
        self.workbook = Workbook(self.complete_output_file_name)
        self.worksheet = workbook.add_worksheet()

    def work(self, person):
        """
            Acciones de procesamiento:
                - Escribir en cada columna de la fila actual, los valores
                de las claves del diccionario de persona recibido
                - Incrementar contador de lineas escritas.
        """

        for col_i, clave in enumerate(CLAVES):
            self.worksheet.write(self.row_count, col_i, person.get(clave))
        self.row_count += 1

    def finalize(self):
        """
            Acciones de finalizacion:
                - Cerrar el archivo de trabajo
                - Mostrar el nombre del archivo que se genero.
                - Y la cantidad de lineas escritas
        """
        self.workbook.close()
        print("######## FIN EXCEL FILE GENERATOR ###########")
        print('\tarchivo generado: {}.'.format(self.complete_output_file_name))
        print('\tcantidad de lineas del archivo {}.'.format(str(self.row_count)))