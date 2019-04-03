import sys
import funciones
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('BASIC')
logging.basicConfig(level=logging.DEBUG)
print("HOLA SCRIPT")
if __name__ == '__main__':
	try:
		print("INICIO SCRIPT")
		logger.debug("INICIO SCRIPT debug")
		if len(sys.argv) == 4:
			arch = open (sys.argv[1], "r")
			text =arch.readlines()
			arch.close()
			ruta  = sys.argv[3]
			ruta  = ruta
			texto = funciones.acomodaTexto(text, ruta)
			texto = funciones.marcarConsiderandos(texto)
			texto = funciones.limpiarTexto(texto)
			texto = funciones.restaurarNumeros(texto)
			arch = open (sys.argv[2], "w")
			arch.write(texto)
			arch.close()
		else:
			print ("Error al tratar el archivo x")
	except Exception as e:
		print("Error al procesar {0}".format(e))
