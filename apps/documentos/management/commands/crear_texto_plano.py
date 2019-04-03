import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from apps.documentos.models import Anotacion
import json
from apps.documentos.utils.funciones import (acomodaTexto, marcarConsiderandos,
                                             limpiarTexto, restaurarNumeros,
                                             convertir_texto_a_bd, dar_formato_a_texto)
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
        print(args)
        print(options)
        anotaciones = Anotacion.objects.all()
        print(os.getcwd())
        root_path = os.getcwd()
        for anotacion in anotaciones:
            print(anotacion)
            filepath = anotacion.get_url_file()
            filepath_prov = "{0}.prov".format(filepath.split('/')[-1])
            command = ["pdftotext", "-layout", "-raw", "-q",
                       root_path + filepath, filepath_prov
                       ]
            print(" ".join(command))
            proceso = subprocess.Popen(command, stdout=subprocess.PIPE)
            exit_code = proceso.wait()
            print(exit_code)
            texto = dar_formato_a_texto(filepath_prov, new_path=None)
            print("termino de dar formato...")
            all_words = convertir_texto_a_bd(texto)
            anotacion.set_texto(json.dumps(all_words))
            anotacion.save_documento()
            return 0
            i=0
            for line in _file.readlines():
                print(line)
                all_lines.append(line)
                all_words += line.split(' ')
                for word in line.split(' '):
                    dict_words[i] = word
                    i+=1
            anotacion.set_texto(json.dumps(all_words))
            anotacion.save_documento()
            print("TOTAL DE LINEAS: ")
            print(len(all_lines))
            print("TOTAL DE PALABRAS: ")
            print(len(all_words))
            print("TOTAL Longitud texto(array): ")
            print(len(str(all_words)))
            print("TOTAL PALABRAS(dict): ")
            print(len(dict_words))
            print("LEN PALABRAS(dict): ")
            print(len(str(dict_words)))
            anotacion.set_texto(json.dumps(all_words))
            anotacion.save_documento()
        try:
            self.stdout.write(self.style.SUCCESS('Comando custom by "%s"' % 'METALLICA GREEN'))
        except Exception as e:
            raise CommandError('Error " %s " ' % str(e))
