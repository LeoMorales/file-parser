# File Parser

Script python que parsea un archivo txt que contiene el padrón en el
siguiente formato:
- matricula (8)
- clase(4)
- apellido(40)
- nombres(47)
- domicilio(35)
- tipo documento(9)
- seccion(4)
- circuito(4)
- mesa(4)
- sexo(1)
- nro orden padron(4)

La gracia es que nosotros conocemos como esta almacenado esto en una
base de datos, por lo cual podemos generar el script sql que cargue la base
a partir de la información de los archivos recibidos.
De yapa, queremos pasar estos registros a un archivo excel.

## Run:

>> python parser.py convertir.txt

Las líneas de convertir.txt tiene el siguiente formato:

  <nombre_del_archivo_a_parsear>, <nombre_para_los_archivos_de_salida>

donde <nombre_para_los_archivos_de_salida> no tiene extensión.

Desafíos en el camino:
- Como evito tocar el código para cambiar el comportamiento segun desee
  generar el archivo sql, o el archivo excel, o ambos. Parametrizar
- Como hacer para que cambie la forma de parsear el archivo interpretándolo
  de distintas formas segun se desee para luego realizar diferentes acciones
  pertinentes (escribir en un archivo, escribir en una BD, etc).
- Y si en lugar de generar los archivos sql, directamente nos conectamos
  a la base?.
- etc...
