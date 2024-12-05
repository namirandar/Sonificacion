import subprocess
import sys

class GestorLibrerias:
    def __init__(self, librerias):
        """
        Inicializa el gestor con una lista de librerías que se instalarán.

        Args:
            librerias (list): Lista de librerías a instalar.
        """
        self.librerias = librerias

    def instalar_librerias(self):
        """
        Recorre la lista de librerías y las instala una por una utilizando pip.
        """
        for libreria in self.librerias:
            self.instalar_libreria(libreria)

    def instalar_libreria(self, libreria):
        """
        Instala una librería utilizando pip.

        Args:
            libreria (str): Nombre de la librería a instalar.
        """
        try:
            print(f"Instalando {libreria}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
            print(f"{libreria} instalada con éxito.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar {libreria}: {e}")
        except Exception as e:
            print(f"Error inesperado al intentar instalar {libreria}: {e}")
