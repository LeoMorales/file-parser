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
from DataExtractor import DataExtractor




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
        self.personDataExtractor = DataExtractor()
        
    def create_sql_worker(self):
        self.workers.append(SQLWorker(self.personDataExtractor))

    def create_excel_worker(self):
        self.workers.append(ExcelWorker(self.personDataExtractor))
        
    def init(self, working_file_name):
        for worker in self.workers:
            worker.init(working_file_name)

    def work_old(self, data):
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

    def work(self, data):
        """
            En nuestro caso, data va a ser una linea de archivo.
            Cada worker trabaja con ella como lo crea necesario.
        """
        self.counter += 1
        for worker in self.workers:
            worker.work(data)
        self.procesed +=1
        
    def finalize(self):
        """
            Finalizar los workers e imprimir la cantitdad de registros
            procesados hasta el momento
        """
        for worker in self.workers:
            worker.finalize()
        print("\nFINALIZADO: {}\n\n".format(self.counter))


class SQLWorker(object):
    """
        SQLWorker:
        Procesa diccionarios con la informacion de la persona
        y genera un archivo con el script SQL correspondiente
        a la carga de dicho lote de registros.
    """
    def __init__(self, dataExtractor):
        super(SQLWorker, self).__init__()
        self.dataExtractor = dataExtractor
    
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

    def work(self, data):
        """
            Acciones de procesamiento:
                - Llenar el template de linea SQL con los valores del
                diccionario de persona recibido.
                - Escribirlo en el archivo.
                - Incrementar contador de lineas escritas.
        """
        a_person = self.dataExtractor.process_person(data)
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
    def __init__(self, dataExtractor):
        super(ExcelWorker, self).__init__()
        self.workbook = None
        self.worksheet = None
        self.row_count = 0
        self.dataExtractor = dataExtractor


    def init(self, output_file_name):
        """
            Acciones de inicializacion:
                - Crear el archivo de trabajo con el nombre recibido.
                - Inicializar la hoja con la que vamos a trabajar.
        """
        self.complete_output_file_name = '../output/excel/'+output_file_name+'.xlsx'
        self.workbook = Workbook(self.complete_output_file_name)
        self.worksheet = workbook.add_worksheet()

    def work(self, data):
        """
            Acciones de procesamiento:
                - Escribir en cada columna de la fila actual, los valores
                de las claves del diccionario de persona recibido
                - Incrementar contador de lineas escritas.
        """
        person = self.dataExtractor.process_person(data)
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