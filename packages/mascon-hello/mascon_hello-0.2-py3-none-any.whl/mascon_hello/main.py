def hello():
    print("Hello from Pixegami")

import comtypes.client
import sys
import time

import pandas as pd
import numpy as np

class ETABSAPI:

    def __init__(self, program_path):
        self.SapModel = None
        self.myETABSObject = None
        self.helper = None

        #Establezca el siguiente indicador en Verdadero para adjuntarlo a una instancia existente del programa.
        #de lo contrario se iniciará una nueva instancia del programa.
        self.attach_to_instance = False

        #Establezca el siguiente indicador en Verdadero para especificar manualmente la ruta a ETABS.exe.
        #esto permite una conexión a una versión de ETABS distinta a la última instalación
        #de lo contrario, se iniciará la última versión instalada de ETABS
        self.specify_path = False    

        #Si el indicador anterior está configurado en Verdadero, especifique la ruta a ETABS a continuación
        self.program_path = "C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"  
    
    # Conectar a un modelo existente           
    def connect_to_etabs(self):
        try:
            self.helper = comtypes.client.CreateObject('ETABSv1.Helper')
            time.sleep(2)  # Pausa para asegurar que el objeto se cree correctamente
            self.helper = self.helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)
        except (OSError, comtypes.COMError):
            print("Failed to create helper object.")
            sys.exit(-1)
        
        try:
            self.myETABSObject = self.helper.GetObject("CSI.ETABS.API.ETABSObject")
            time.sleep(2)  # Pausa para asegurar que la conexión se establezca correctamente
            self.SapModel = self.myETABSObject.SapModel
            print("Connected to ETABS model") 
        except (OSError, comtypes.COMError):
            print("No running instance of the program found or failed to attach.")
            sys.exit(-1)

        return self.SapModel, self.myETABSObject, self.helper
    