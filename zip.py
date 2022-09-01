import os
import zipfile
from zipfile import ZipFile

def __copyInFile(iF, oF, buffersize=1024, tocopy = 0):
    copied = 0
    i = 0
    while True:
        i += 1
        elsetocpy = tocopy - copied
        
        if (elsetocpy - buffersize > 0) or (tocopy == 0):
            tmp = iF.read(buffersize)
            if tmp == b'':
                if i == 1:
                    return False
                else:
                    return True
            else:
                oF.write(tmp)
                copied += buffersize

        else:
            tmp = iF.read(elsetocpy)
            if tmp == b'':
                if i == 1:
                    return False
                else:
                    return True
            else:
                oF.write(tmp)
                return True

"""Comprimiendo Archivos"""
def split(inFileSrc, output, splitIn):
    splitNumber = 1
    try:
        inFile = open(inFileSrc, 'rb');
    except FileNotFoundError:
        print('Error: El Archivo %s No Existe. Saliendo...' % (inFileSrc))
        return False
        exit()
    while True:
        if output == None:
            outFile = open(inFileSrc + '.' + str('%03d' % (splitNumber)), 'wb')
        else:
            outFile = open(os.path.join(output, os.path.basename(inFileSrc)) + '.' + str('%03d' % (splitNumber)), 'wb')
        if not __copyInFile(inFile, outFile, 1024, splitIn):
            outFile.close()
            if output == None:
                os.remove(inFileSrc + '.' + str('%03d' % (splitNumber)))
            else:
                os.remove(os.path.join(output, os.path.basename(inFileSrc)) + '.' + str('%03d' % (splitNumber)))
            break
        else:
            outFile.close()
            splitNumber += 1
    inFile.close()
    os.remove(inFileSrc)
    return True,splitNumber


def getUnitAndValue(inVar):
    inVar = str(inVar)
    number = ''
    unit = ''
    for l in inVar:
        if(l.isdigit() or l == ',' or l == '.'):
            if l == ',':
                l = '.'
            number += l
        else:
            unit += l
    number = float(number)
    return (number, unit)

"""==================Conversion de Unidades===================="""
def getBytes(inVar):
    tmp = getUnitAndValue(inVar)
    number = tmp[0]
    unit = tmp[1]
    del tmp

    if(unit == 'k' or unit == 'K' or unit == 'KB'):
        return int(number * 1000)
    elif(unit == 'm' or unit == 'M' or unit == 'MB'):
        return int(number * 1000000)
    elif(unit == 'g' or unit == 'G' or unit == 'GB'):
        return int(number * 1000000000)
    elif(unit == 't' or unit == 'T' or unit == 'TB'):
        return int(number * 1000000000000)
    elif(unit == 'p' or unit == 'P' or unit == 'PB'):
        return int(number * 1000000000000000)
    elif(unit == 'e' or unit == 'E' or unit == 'EB'):
        return int(number * 1000000000000000000)
    elif(unit == 'z' or unit == 'Z' or unit == 'ZB'):
        return int(number * 1000000000000000000000)
    elif(unit == 'y' or unit == 'Y' or unit == 'YB'):
        return int(number * 1000000000000000000000000)

    elif(unit == 'KiB'):
        return int(number * 1024)
    elif(unit == 'MiB'):
        return int(number * 1048576)
    elif(unit == 'GiB'):
        return int(number * 1073741824)
    elif(unit == 'TiB'):
        return int(number * 1099511627776)
    elif(unit == 'PiB'):
        return int(number * 1125899906842624)
    elif(unit == 'EiB'):
        return int(number * 1152921504606846976)
    elif(unit == 'ZiB'):
        return int(number * 1180591620717411303424)
    elif(unit == 'YiB'):
        return int(number * 1208925819614629174706176)
    elif(unit == '' or unit == 'b' or unit == 'B'):
        return int(number)
    else:
        print('Error durante la conversion de  %s, Seguro q enviaste un valor Correcto? Saliendo...' % (str(inVar)))
        exit()

"""Comprimir Carpeta"""
def compresion(file:str,dir :str): 
    if file != '':
        file = file
    else:
        file = 'nuevo'
    foo = zipfile.ZipFile(file, 'w')
    foo.write(file)
    # Añadiendo archivos al directorio
    for root, dirs, files in os.walk(dir):
        for f in files:
            foo.write(os.path.join(root, f))
    foo.close()
    return './'+ file

def compressionone(file:str,dir:str):
    if file != '':
        file = file
    else:
        file = 'nuevo.zip'
    with ZipFile(file, 'w') as myzip:
        myzip.write(dir)
    return './'+ file
    