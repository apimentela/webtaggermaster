import re
import nltk
from django.conf import settings
'''
class Settings(object):
    def __init__(self):
        self.DICCIONARIOS_PATH = "/nums_para_editar_txt.dat"
settings = Settings()
'''
patterns = [r"R\W*?E\W*?S\W*?U\W*?L\W*?T\W*?A\W*?N\W*?D\W*?O\W*?\n$",
            r"C\W*?O\W*?N\W*?S\W*?I\W*?D\W*?E\W*?R\W*?A\W*?N\W*?D\W*?O\W*?\n$",
            r"R\W*?E\W*?S\W*?U\W*?E\W*?L\W*?V\W*?E\W*?\n$"]
textPATTERNS = []
dicc_textREPLACE = {}
chars1 = [':', ',', ';', '.', '!', '?', '<', '>',
          '+', '%', '$', ' ', '/', '=', '@', '*',
          '(', ')', '[', ']', '{', '}', '-']
chars2 = ['\xc3\xb1', '\xc3\x91', '\xc3\xa1', '\xc3\xa9', '\xc3\xad',
          '\xc3\xb3', '\xc3\xba', '\xc3\x81', '\xc3\x89', '\xc3\x8d',
          '\xc3\x93', '\xc3\x9a', '\xc3\xbc', '\xc3\x9c']
chars3 = ['\xe2\x80\x9c', '\xe2\x80\x9d', '\xe2\x80\x99']
charsTOreplace = {'\xc2\xa1': " -! ", '\xc2\xbf': " -? ", '\xc2\x91': ' " '}
simbolox = ['\xc2', '\xc3', '\xe2']
def buscarSaltoLinea(considerandoTexto, inicioResolutivos):
    while inicioResolutivos > 0:
        if considerandoTexto[inicioResolutivos] == '\n':
            break
        inicioResolutivos -= 1
    return inicioResolutivos
def buscaResolutivosAUX2 (considerandoTexto, inicioResolutivos):
    considerando  = considerandoTexto[:inicioResolutivos]
    resolutivo    = considerandoTexto[inicioResolutivos:]
    considerando += "\n\n%=%FIN_CONSIDERANDOS%=%\n\n"
    resolutivo    = resolutivo.replace("E%=%", "E%=%\n\n")
    return (considerando, resolutivo)
def buscaResolutivosAUX (considerandoTexto, pattern):
    i = len(considerandoTexto)-1 
    while i > 0:
        inicioResolutivos = considerandoTexto[i].rfind(pattern)
        if inicioResolutivos >= 0:
            break
        i -= 1
    if i < 0:
        return (considerandoTexto, None)
    else:
        inicioResolutivos = buscarSaltoLinea(considerandoTexto[i], inicioResolutivos) 
        considerandos     = considerandoTexto[:i]
        resolutivos       = considerandoTexto[i+1:]
        ultimoConsi, primerRes = buscaResolutivosAUX2 (considerandoTexto[i], inicioResolutivos)
        considerandos.append(ultimoConsi)
        resolutivos = [primerRes] + resolutivos
        resolutivos=encadena(resolutivos)
        return (considerandos, resolutivos)
def buscaResolutivos(considerandoTexto):
    global textPATTERNS
    inicioResolutivos = -1
    if textPATTERNS:
        pattern   = textPATTERNS[-1]
        if re.search(r"R\W*?E\W*?S\W*?U\W*?E\W*?L\W*?V\W*?E\W*?$", pattern, re.IGNORECASE):
            return buscaResolutivosAUX(considerandoTexto, pattern)
    return (considerandoTexto, None)
def traerConsiderandos(text):
    text, resolutivos  = buscaResolutivos(text) 
    considerandos      = []
    considerandoTexto  = ""
    considerandoNumber = 0
    for line in text:
        line = line.split('\n')
        for l in line:
            numero = re.search(r"%\=%\d+%\=%", l) 
            if numero:
                number = numero.group() 
                numero = re.search(r"\d+", number).group()
                numero = int(numero)
                if numero-1 == considerandoNumber:
                    considerandoNumber += 1
                    considerandos.append(considerandoTexto)
                    considerandoTexto = "\n\n%%=%%CONSIDERANDO_" + str(numero) + "%%=%%\n\n"
                else:
                    considerandoTexto += "\n" + number + "\n"
            else:
                considerandoTexto += l
        considerandoTexto += "\n\n"
    considerandos.append(considerandoTexto) 
    if resolutivos:
        considerandos.append(resolutivos) 
    return considerandos
def separaConsiderando(bloqueTexto, pattern):
    aux         = re.search(pattern, bloqueTexto, re.IGNORECASE)
    aux         = aux.group()
    inicioConsi = bloqueTexto.find(aux) 
    inicio   = bloqueTexto[:inicioConsi] + "\n\n" 
    consider = bloqueTexto[inicioConsi:]
    consider = consider.replace(aux, aux+"\n\n")
    return (inicio, consider)
def marcarConsiderandos (text):
    global textPATTERNS
    if len(textPATTERNS) > 1: 
        pattern = textPATTERNS[1]
        newText = ""
        i       = 0
        lim     = len(text)
        while text: 
            if re.search(pattern, text[0]):
                inicio, text[0] = separaConsiderando(text[0], pattern)
                newText += inicio 
                break
            else:
                newText += text[0]
                del text[0]
            i += 1
        considerandos = traerConsiderandos(text) 
        for c in considerandos:
            newText += c
        return newText
    else:
        return encadena(text)
def encadena (text):
    cad = ""
    for line in text:
        cad += line
        cad += "\n"
    return cad
def buscarEncabezados (text):
    inicioPags = []
    nextLines  = []
    repeticion = 0
    next       = 1
    i          = 0
    lim        = len(text)
    while i < lim:
        if re.match("^\x0c.*\n$", text[i]):
            if text[i] in inicioPags: 
                repeticion += 1
                if i+next < lim:
                    if text[i+next] in nextLines:
                        next += 1
                    else:
                        del nextLines[next-1]
                    nextLines.append(text[i+next])
            else:
                inicioPags.append(text[i])
                if i+next < lim:
                    nextLines.append(text[i+next])
        if len(inicioPags) > 4: 
            return []
        elif repeticion > 5:    
            if len(inicioPags) > 1:
                return inicioPags[1:] + nextLines[:-1]
            else: 
                return inicioPags + nextLines[:-1]
        i += 1
    return []
def ersteAcomodaTexto (text):
    newtext    = []
    ecabezados = buscarEncabezados(text)
    i   = 0
    lim = len(text)
    while i < lim:
        if re.match("^\W*?\d+\W*?\n$", text[i]): 
            if i+1 == lim: 	
                break
            if (i+2<lim) and text[i] == text[i+1] and (text[i+2].find("\x0c")>=0):
                i += 1
                continue
            nextLine = re.match("^\x0c.*\n$", text[i+1])
            if nextLine:    
                nextLine = nextLine.group(0)
                if nextLine in ecabezados: 
                    i += 2 
                    continue
                else:			   
                    text[i+1] = text[i+1].replace("\x0c", "")
                    i += 1 
                    continue
            else:
                if re.match("^\x0c", text[i]):
                    i += 1
                    continue
                newtext.append(text[i])
        elif text[i] in ecabezados: 
            if (i+1<lim) and (re.match("^\W*?\d+\W*?\n$", text[i+1])):
                i += 2
                continue
            i += 1
            continue
        elif re.match("^\x0c.*\n$", text[i]):
            text[i] = text[i].replace("\x0c", "") 
            newtext.append(text[i])
        else:	
            newtext.append(text[i])
        i += 1
    return newtext
def findImpirtantThings(line):
    global patterns
    if (len(patterns)>1) and (re.search(patterns[0], line, re.IGNORECASE)):
        aux = re.search(patterns[0], line, re.IGNORECASE)
        del patterns[0]
        return aux
    elif re.search(patterns[0], line, re.IGNORECASE):
        aux = re.search(patterns[0], line, re.IGNORECASE)
        return aux
    else:
        return None
def isImportantLine(line):
    global textPATTERNS
    aux = findImpirtantThings(line)
    if aux:
        aux  = aux.group()       
        xua  = specialStrip(aux) 
        line = line.replace(aux, "\n\n%=%"+xua+"%=%\n\n")
        textPATTERNS.append("%=%"+xua+"%=%")
        return line
    else:
        return line
def isImportantLineII(diccNums, line):
    global textREPLACE
    if len(line)>0 and diccNums.has_key(line[0].lower()):
        finDeNumero, numero = buscaNumero(line, 0, len(line),  diccNums[line[0].lower()]) 
        if numero:
            textOri = line[:finDeNumero]	      
            textNew = "\n\n" + numero + "\n\n"    
            lineEND = line[finDeNumero:]	      
            line    = textNew + lineEND       	  
            key                   = (textNew, lineEND)
            dicc_textREPLACE[key] = textOri
    return line
def zweiteAcomodaTexto(text, ruta=settings.DICCIONARIOS_PATH):
    diccNums  = importarNumeros(ruta)
    parrafos  = []
    parrafo   = ""
    for line in text:
        line = isImportantLine(line)
        if re.search(r".*[.:]\n$", line): 
            line = line.strip()
            line = isImportantLineII(diccNums, line)
            parrafo += line
            parrafo += "\n"
            parrafos.append(parrafo)
            parrafo = ""
        else:
            line = line.strip()
            line = isImportantLineII(diccNums, line)
            line += " "
            parrafo += line
    parrafos.append(parrafo)
    return parrafos
def acomodaTexto (text, ruta=settings.DICCIONARIOS_PATH):
    text = ersteAcomodaTexto(text)
    text = zweiteAcomodaTexto(text, ruta)
    return text
def specialStrip(aux):
    cad = ""
    for letra in aux:
        if re.match("\w", letra):
            cad += letra
    return cad
def importarNumeros(ruta=settings.DICCIONARIOS_PATH):
    try:
        numeros = {}
        archivo = open(ruta, "U")
        for num in archivo:
            num = num.replace('\n', '')
            num = num.split("#@%")
            diccionariza(numeros, num[1], num[0])
        archivo.close()
        return numeros
    except Exception as e:
        print("Error importarNumeros: {0}".format(e))
def diccionariza (diccionario, identificador, lista):
    if len(lista) == 1:
        diccionario[lista[0]]={}
        diccionario[lista[0]]["<<fin>>"]="%=%"+identificador+"%=%"
        return
    elif re.match("\W", lista[0]):
        diccionariza(diccionario, identificador, lista[1:])
    elif diccionario.has_key(lista[0]):
        diccionariza(diccionario[lista[0]], identificador, lista[1:])
    else:
        diccionario[lista[0]]={}
        diccionariza(diccionario[lista[0]], identificador, lista[1:])
def buscaNumero(texto, i, tam,  diccionario):
    i = i+1
    if i < tam:
        if re.match("\w", texto[i]): 
            if diccionario.has_key(texto[i].lower()): 
                return buscaNumero(texto, i, tam,  diccionario[texto[i].lower()])
            elif diccionario.has_key("<<fin>>"): 
                return (i, diccionario["<<fin>>"])
            else:
                return (None, None)
        else: 
            return buscaNumero(texto, i, tam,  diccionario)
    else:
        if diccionario.has_key("<<fin>>"):
            return (i, diccionario["<<fin>>"])
        else:
            return (None, None)
def cambiarCadena(line, patron, sustit=''):  
    trash = re.findall(patron, line)
    for t in trash:
        line = line.replace(t, sustit, 1)
    return line
def juntarAsteris(line):
    trash = re.search(r"\*\s+?\*", line)
    while trash:
        trash = trash.group()
        line  = line.replace(trash, "**")
        trash = re.search(r"\*\s+?\*", line)
    return line
def limpiarTexto(texto):
    cadena = ""
    texto  = texto.split('\n')
    for line in texto:
        line = line.strip()
        line = line.lstrip('.')
        line = line.lstrip('-')
        line = line.lstrip(',')
        line = line.lstrip(':')
        if line == "":
            continue
        line = cambiarCadena(line, r"&")
        line = cambiarCadena(line, r"&..;", "--")
        if re.match(r".*[.:]$", line): 
            line = eliminasimbolos(line)
            line = line.strip()
            line+='\n\n'
        elif re.match(r".*%=%\W?$", line): 
            if re.match(r"^%%?=%%?.*%%?=%%?\W?$", line):
                line = "\n\n" + line + "\n\n"
            else:
                line = eliminasimbolos(line)
                line = line.strip()
                line+='\n\n'
        else:
            line = eliminasimbolos(line)
            line = line.strip()
        line = cambiarCadena(line, r" {2,}", ' ') 
        line = juntarAsteris(line)                
        line = cambiarCadena(line, r"\*{2,}", '****') 
        cadena += line
    return cadena
def eliminasimbolos (linea):
    global chars1, chars2, chars3, charsTOreplace, simbolox
    limite=len(linea)
    actual=""
    i=0
    while i<limite:
        if linea[i] in chars1: 
            actual += ' ' + linea[i] + ' '
            i += 1
        elif linea[i] in simbolox: 
            if i+1 < limite:
                aux = linea[i]+linea[i+1] 
                if aux in chars2:       
                    actual += linea[i] + linea[i+1]
                    i += 2
                elif charsTOreplace.has_key(aux): 
                    actual +=  charsTOreplace[aux]
                    i += 2
                elif i+2 < limite:
                    aux += linea[i+2] 
                    if aux in chars3:  
                        actual += ' " '
                        i += 3
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        else:
            valorAscii = ord(linea[i])
            if 47 < valorAscii and valorAscii < 58:
                if i+1 < limite:
                    valorAscii = ord(linea[i+1])
                    if 47 < valorAscii and valorAscii < 58:
                        actual += linea[i]
                        i += 1
                    else:
                        actual +=  linea[i] + ' '
                        i += 1
                else:
                    actual += linea[i]
                    i += 1
            elif (64 < valorAscii and valorAscii < 91) or (96 < valorAscii and valorAscii < 123):
                if i+1 < limite:
                    valorAscii = ord(linea[i+1])
                    if (64 < valorAscii and valorAscii < 91) or (96 < valorAscii and valorAscii < 123):
                        actual += linea[i]
                        i += 1
                    elif linea[i+1] in simbolox:
                        actual += linea[i]
                        i += 1
                    else:
                        actual +=  linea[i] + ' '
                        i += 1
                else:
                    actual += linea[i]
                    i += 1
            else:
                i+=1
    return actual
def restaurarNumeros(texto):
    global dicc_textREPLACE
    for k, textOri in dicc_textREPLACE.items():
        textNew, lineEND = k
        lineEND       = limpiarTexto(lineEND)
        textToRestore = textNew + lineEND
        if texto.find(textToRestore) >= 0:
            textOri = ' ' + limpiarTexto(textOri) + ' ' + lineEND
            texto   = texto.replace(textToRestore, textOri)
    return texto
def dar_formato_a_texto(archivo, new_path=None):
    arch = open(archivo, "r")
    text = arch.readlines()
    arch.close()
    texto = acomodaTexto(text)
    texto = marcarConsiderandos(texto)
    texto = limpiarTexto(texto)
    texto = restaurarNumeros(texto)
    if new_path:
        arch = open (new_path, "w")
    else:
        arch = open('{0}_formated.txt'.format(archivo), "w")
        arch.write(texto)
        arch.close()
    return texto
def manejar_considerando(line):
    inicio_considerando = False
    termino_considerando = False
def guardar_parrafo(parrafos, ):
    pass
def convertir_texto_a_bd(texto, modelo=None):
    partes = {0:'inicio',
              1:'considerandos',
              2:'resuelve',
              }
    print("imprimir lineas ya con formato")
    all_lines = list()
    all_words = list()
    dict_words = dict()
    numero_inicial=0
    numero_final=0
    posicion_actual = 0
    considerandos_enumerados = 0
    parrafos = list()
    parrafo_actual = {}
    contador_palabras=0
    for line in texto.split('\n'):
        if '%=%' in line:
            print("EMPIEZAN CONSIDERANDOS")
            posicion_actual=1
            considerandos_enumerados = 0
            print(numero_inicial, contador_palabras)
            if not parrafo_actual:
                print("No habia informacion en este parrafo!!!!!!")
                continue
            modelo.crear_parrafo(numero_inicial=numero_inicial, numero_final=contador_palabras, parrafo_actual=parrafo_actual)
            numero_inicial = contador_palabras+1
            parrafos.append(parrafo_actual)
            parrafo_actual = {}
        else:
            for palabra in line.strip().split():
                if '\n' == palabra:
                    continue
                parrafo_actual[contador_palabras]=palabra
                contador_palabras+=1
    if parrafo_actual:
        print(numero_inicial, contador_palabras)
        modelo.crear_parrafo(numero_inicial=numero_inicial,
                             numero_final=contador_palabras,
                             parrafo_actual=parrafo_actual)
        numero_inicial = numero_final+1
        parrafos.append(parrafo_actual)
        parrafo_actual = ""
    return parrafos
