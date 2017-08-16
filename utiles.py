# -*- coding: utf-8 -*-
# @Author: leomorales
# @Date:   2017-08-08 15:17:59
# @Last Modified by:   leomorales
# @Last Modified time: 2017-08-09 14:47:53

TIPOS_DE_DOC = {
    'DNI': 1,   
    'DNIT': 10,  
    'DNIC': 11,  
    'L': 12,  
    'DNID': 13,  
    'DNI-EC': 13535,   
    'DNI5': 13536,   
    'DNI6': 13537,   
    'LT': 13538,   
    'DNI-ED': 13539,   
    'DDRECT': 13540,   
    'DNI8': 13541,   
    'ESTUD': 13542,   
    'ESTUDIA': 13543,   
    'DT.REP.': 13544,   
    'A/CAS': 13545,   
    'DNI-EE': 13546,   
    'EST': 13547,   
    'DNI-ES': 13548,   
    'ADC': 13549,   
    'DNI7': 13550,   
    'EMP': 13551,   
    'DCS': 13552,   
    'A.D': 13553,   
    'DD RECT': 13554,   
    'DNI.REC': 13555,   
    'DS': 13556,   
    'DCT': 13557,   
    'DNIREC': 13558,   
    'A.DE CA': 13559,   
    'DNI13': 13560,   
    'EMP.DOM': 13561,   
    'A DE C': 13562,   
    'REFLEXO': 13563,   
    'Q D': 13564,   
    'DMI': 13565,   
    'DOC': 13566,   
    'DNI9': 13567,   
    'QS DS': 13568,   
    'EMPL': 13569,   
    'A.DE C.': 13570,   
    'DTO.203': 13571,   
    'M.DE RO': 13572,   
    'DD REC': 13573,   
    'AMA DE': 13574,   
    'DDS': 13575,   
    'ALB': 13576,   
    'DD REP.': 13577,   
    'DE C': 13578,   
    'TEC ADM': 13579,   
    'QS': 13580,   
    'AMA': 13581,   
    'SEPT': 13582,   
    'LOTE11': 13583,   
    'DNI10': 13584,   
    'A.DE.C.': 13585,   
    'EMP.': 13586,   
    'S': 13587,   
    'P.B. A': 13588,   
    'VEND': 13589,   
    'A DE C.': 13590,   
    'DNI CAN': 13591,   
    'DOMEST': 13592,   
    'NO': 13593,   
    'S/PROF': 13594,   
    'DNI-EF': 13595,   
    'ALBAÑIL': 13596,   
    'DNI-ER': 13597,   
    'ARTES.': 13598,   
    'F. 05': 13599,   
    'DTRECT': 13600,   
    'DNI11': 13601,   
    'DOCT': 13602,   
    'DDF': 13603,   
    'DD (REP': 13604,   
    'PENS.': 13605,   
    'PENSION': 13606,   
    'DT REP.': 13607,   
    'DNI OD': 13608,   
    'DT REP': 13609,   
    'GANADER': 13610,   
    'PEO': 13611,   
    'ROCA': 13612,   
    'JORNALE': 13613,   
    'ESTUD.': 13614,   
    'DN': 13615,   
    'PEON': 13616,   
    'JOR': 13617,   
    'GAN': 13618,   
    'C04': 13619,   
    'COM': 13620,   
    '40 VIV': 13621,   
    'COMERCI': 13622,   
    'DSEPUP.': 13623,   
    'DNI .': 13624,   
    'JUB': 13625,   
    'CHO': 13626,   
    'MIL': 13627,   
    'DT RECT': 13628,   
    'AY': 13629,   
    'TRANSP': 13630,   
    'EMP.DT.': 13631,   
    'EMPL.DD': 13632,   
    'A/C DD': 13633,   
    'DOCENTE': 13634,   
    'S/P': 13635,   
    'DD.REP': 13636,   
    'AUT': 13637,   
    'EMPLEAD': 13638,   
    'DTO C': 13639,   
    'ING': 13640,   
    'EST.': 13641,   
    'L.T.': 13642,   
    'EMPL.': 13643,   
    'A.D.C.': 13644,   
    'MEC': 13645,   
    'DSET': 13646,   
    'DS.': 13647,   
    'DC RECT': 13648,   
    'D.': 13649,   
    'DST': 13650,   
    'EMP. DC': 13651,   
    'DDQS': 13652,   
    'L.T': 13653,   
    'AGRICUL': 13654,   
    'DTP': 13655,   
    'LETRIST': 13656,   
    'A.DE C': 13657,   
    'DD.RECF': 13658,   
    'S/PROFE': 13659,   
    'M.M.DE': 13660,   
    'DD REP': 13661,   
    'DDI': 13662,   
    'EMPL.PO': 13663,   
    'LOT 16': 13664,   
    'DD]': 13665,   
    'D.C.': 13666,   
    'DDST': 13667,   
    'ALBAÑIL': 13668,   
    '15': 13669,   
    'DNI-EG': 13670,   
    'DNI-EH': 13671,   
    'DNIT': 15,  
    'LD': 16,  
    'LC': 2,   
    'LE': 3,   
    'PASAPORTE': 4,   
    'CUIL': 5,   
    'CI': 6,   
    'DNI-EA': 7,   
    'DNID': 8,   
    'DNI-EB': 9,   
}

def validar_matricula(valor):
    """ TIPO: int"""
    return valor

def validar_tipo_documento(valor):
    """ TIPO: int"""
    return TIPOS_DE_DOC.get(valor, 1)

def validar_clase(valor):
    """ TIPO: smallint """
    if len(valor) == 0:
        return 'NULL'
    return valor


def validar_apellido(valor):
    """ TIPO: varchar 40"""
    return valor


def validar_nombres(valor):
    """ TIPO: varchar 47"""
    return valor


def validar_domicilio(valor):
    """ TIPO: varchar 35"""
    return valor


def validar_seccion(valor):
    """ TIPO: smailint"""
    return valor


def validar_circuito(valor):
    """ TIPO: varchar 4"""
    return valor


def validar_mesa(valor):
    """ TIPO: int"""
    return valor


def validar_sexo(valor):
    """ TIPO: char 1"""
    if valor not in 'fFmM':
        return '-'
    return valor


def validar_nro_de_orden(valor):
    """ TIPO: int """
    try:
        return int(valor)
    except Exception as e:
        return 0


def validar_id(valor):
    """ TIPO: int"""
    return valor

