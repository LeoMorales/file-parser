# -*- coding: utf-8 -*-
# @Author: leomorales
# @Date:   2017-08-08 15:17:59
# @Last Modified by:   leomorales
# @Last Modified time: 2017-08-09 17:23:52

import argparse
import codecs
import sys
import utiles
from workers import WorkerManager
try:
    from xlsxwriter import Workbook
    IMPOSIBLE_GENERAR_EXCEL_WE = False
except ImportError:
    IMPOSIBLE_GENERAR_EXCEL_WE = True

# Para Linux, descomentar las siguientes lineas
# reload(sys)
# sys.setdefaultencoding('utf-8')


INICIO_CUENTA = 900000

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

def parsear_argumentos():
    parser = argparse.ArgumentParser(description='Genera un archivo SQL a partir de un archivo cpa')
    parser.add_argument('archivo', metavar='A', type=str,
                        help='archivo que contiene en cada linea, el nombre del archivo a parsear y el nombre que se le quiere asignar a la salida sql')
    parser.add_argument('--inicio', type=int, default=INICIO_CUENTA,
                        help='desde donde empezar a contar los objetos (default: 0)')

    args = parser.parse_args()

    print("argumentos:")
    print(args.archivo)

    return args.archivo

if __name__ == '__main__':
    # Obtener el nombre del archivo que contiene los nombres de los archivos a analizar:
    input_file_names = parsear_argumentos()
    
    # Inicializar el worker manager y los workers:
    wm = WorkerManager(INICIO_CUENTA)
    wm.create_sql_worker()
    # wm.create_mesa_worker()
    if not IMPOSIBLE_GENERAR_EXCEL_WE:
        wm.create_excel_worker()

    # main loop:
    lines = INICIO_CUENTA
    try:
        archivo = open(input_file_names, 'r')
        for line in archivo:
            data_file_name, output_file_name = list(map(lambda name: name.strip(), line.split(',')))
            lines = analize_file(wm, data_file_name, output_file_name, lines)
    except FileNotFoundError as e:
        print("El archivo que especifico, no existe")
