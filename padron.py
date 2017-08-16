# -*- coding: utf-8 -*-
# @Author: leomorales
# @Date:   2017-08-08 15:17:59
# @Last Modified by:   leomorales
# @Last Modified time: 2017-08-09 17:23:52

import argparse
import codecs
from pprint import pprint
import re
import sys
import utiles
from workers import WorkerManager
try:
    from xlsxwriter import Workbook
    IMPOSIBLE_GENERAR_EXCEL_WE = False
except ImportError:
    IMPOSIBLE_GENERAR_EXCEL_WE = True

# reload(sys)
# sys.setdefaultencoding('utf-8')


INICIO_CUENTA = 0
"""
OUTPUT_FILE_NAME_TEMPLATE = '../output/sql/{}.sql'
# FILE_NAME = 'test/cpa_300001_to_end_reg.txt'
DEBUG_FILE_NAME = "debug_lineas_no_procesadas.txt"
LONGITUD_VALIDA_DE_LINEA = 162
OFFSET_MATRICULA = 8
OFFSET_CLASE = 4
OFFSET_TIPO_DOCUMENTO = 9
OFFSET_SECCION = 4
OFFSET_CIRCUITO = 4
OFFSET_MESA = 4
OFFSET_SEXO = 1
OFFSET_ORDEN_PADRON = 4

CLAVES = [
    'matricula',
    'tipo_documento',
    'clase',
    'apellido',
    'nombres',
    'domicilio',
    'seccion',
    'circuito',
    'mesa',
    'sexo',
    'nro_orden_padron',
    'id']
"""

def main_old(data_file_name, output_file_name, line_start):
    # Inicializacion
    lines_ok = line_start
    lines_not_ok = 0
    excel_row = 0
    debug_lineas_no_validas = []
    complete_output_file_name = OUTPUT_FILE_NAME_TEMPLATE.format(output_file_name)
    sql_file = codecs.open(complete_output_file_name, 'w', encoding='utf-8', errors='ignore')
    sql_file.write(SQL_FILE_HEADER)

    print('Leer el archivo {}.'.format(str(data_file_name)))
    # inicializacion excel file
    # Create a workbook and add a worksheet.
    # workbook = xlsxwriter.Workbook('../output/excel/'+output_file_name+'.xlsx')
    # worksheet = workbook.add_worksheet()


    # Main loop
    with codecs.open(data_file_name, "r",encoding='utf-8', errors='ignore') as f:
        for line in f:
            person = extraer_data(line)
            if person:
                person['id'] = lines_ok
                # print_person_to_sql(sql_file, person)
                print_person_to_sql_update_nro_de_orden(sql_file, person)
                #print_person_to_excel(worksheet, person, excel_row)
                lines_ok += 1
                excel_row += 1
                # print("{} OK".format(lines_ok))
            else:
                debug_lineas_no_validas.append(line)
                lines_not_ok += 1
                # print("{} MAL".format(lines_not_ok))
    sql_file.close()
    with open(DEBUG_FILE_NAME, 'w') as f:
        f.write("".join([str(linea) for linea in debug_lineas_no_validas]))
    # workbook.close()

    # Prints finales
    print('Cantidad de lineas del archivo {}.'.format(str(lines_ok+lines_not_ok)))
    print('\tvalidas acumuladas: {}.'.format(str(lines_ok)))
    print('\tno validas acumuladas: {}.'.format(str(lines_not_ok)))
    print('\tarchivo generado: {}.'.format(complete_output_file_name))

    return lines_ok
    
def analize_file(wm, data_file_name, output_file_name, line_start):
    # Inicializacion
    print('Leer el archivo {}.'.format(str(data_file_name)))

    wm.init(output_file_name)

    # Main loop
    with codecs.open(data_file_name, "r",encoding='utf-8', errors='ignore') as f:
        for line in f:
            wm.work(line)
    

    # Prints finales
    wm.finalize()
    return wm.procesed
    

"""
def extraer_data(line):
    '''
        Recibe una linea de 160 caracteres de al forma:
            '999999991900PEREZ                                   JUAN AMALIO                                    AV 9 de JULIO y CORRIENTES        DNI-EA     1   1 0001F 001'

        y retorna un dict con la informacion de la persona tokenizada.
    '''
    if len(line) > LONGITUD_VALIDA_DE_LINEA:
        print(len(line))
        return None
    
    # primera separacion:
    col1 = line[0:52].rstrip() # contiene la matricula la clase y el apellido
    nombres = line[52:99].strip()  # contiene los nombres
    domicilio = line[99:133].strip()  # contiene el domicilio
    col4 = line[133:].strip()  # contien tipo de doc, seccion, circuito, mesa, sexo y nro de orden en el padron
    # existen casos en que viene sin tipo de documento, al stripear nos queda una linea mas chica...
    # entonces ese caso es tenido en cuenta en procesar_cuarta_columna
    
    person = {}
    person = procesar_primer_col(col1, person)
    person['nombres'] = nombres.replace("'", "")
    person['domicilio'] = domicilio.replace("'", "").replace('"', "")
    person = procesar_cuarta_col(col4, person)
    
    return person

def procesar_primer_col(columna, person):
    person ['matricula'] = columna[0:OFFSET_MATRICULA].strip()
    person ['clase'] = columna[OFFSET_MATRICULA: (OFFSET_MATRICULA+OFFSET_CLASE)].strip()
    person ['apellido'] = columna[(OFFSET_MATRICULA+OFFSET_CLASE):].strip().replace("'", "")

    return person
    
def procesar_cuarta_col(columna, person):

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
    
def print_person_to_sql(a_file, a_person):
    # pprint(a_person)
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
    a_file.write(person_values_for_sql)
    
def print_person_to_sql_update_nro_de_orden(a_file, a_person):
    # pprint(a_person)
    person_values_for_sql = SQL_UPDATE_LINE_TEMPLATE.format(
        utiles.validar_nro_de_orden(a_person.get('nro_orden_padron')),
        utiles.validar_id(a_person.get('id')),
        )
    #pprint(person_values_for_sql)
    a_file.write(person_values_for_sql)
    
def print_person_to_excel(sheet, person, row):
    for col_i, clave in enumerate(CLAVES):
        sheet.write(row, col_i, person.get(clave))

"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genera un archivo SQL a partir de un archivo cpa')
    parser.add_argument('archivo', metavar='A', type=str,
                        help='archivo que contiene en cada linea, el nombre del archivo a parsear y el nombre que se le quiere asignar a la salida sql')
    parser.add_argument('--inicio', type=int, default=INICIO_CUENTA,
                        help='desde donde empezar a contar los objetos (default: 0)')

    args = parser.parse_args()

    print("argumentos:")
    print(args.archivo)

    wm = WorkerManager()
    wm.create_sql_worker()
    if not IMPOSIBLE_GENERAR_EXCEL_WE:
        wm.create_excel_worker()

    lines = INICIO_CUENTA
    try:
        archivo = open(args.archivo, 'r')
        for line in archivo:
            data_file_name, output_file_name = list(map(lambda name: name.strip(), line.split(',')))
            lines = analize_file(wm, data_file_name, output_file_name, lines)
    except FileNotFoundError as e:
        print("El archivo que especifico, no existe")
