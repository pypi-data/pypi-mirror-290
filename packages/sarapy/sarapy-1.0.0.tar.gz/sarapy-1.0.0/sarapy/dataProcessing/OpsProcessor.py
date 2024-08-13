###Documentación en https://github.com/lucasbaldezzari/sarapy/blob/main/docs/Docs.md
import warnings
import datetime
from dateutil.tz import tzutc
import numpy as np
import pandas as pd
# from sarapy.mlProcessors import PlantinFMCreator
from sarapy.mlProcessors import PlantinClassifier
from sarapy.preprocessing import TransformInputData, TransformToOutputData

class OpsProcessor():
    """Clase para procesar las operaciones de los operarios. La información se toma de la base de datos
    hostórica y se procesa para obtener un array con las operaciones clasificadas para cada operario.
    
    La clase recibe una muestra desde la base de datos histórica y la procesa para obtener las
    operaciones clasificadas para cada operario. Se clasifican las operaciones desde el punto de vista
    del plantín y del fertilizante. La clasificación del tipo de operación respecto de plantín se hace
    con el pipeline para plantín, idem para el fertilizante.
    """
    
    def __init__(self, **kwargs):
        """Constructor de la clase OpsProcessor.
        
        Args:
            - distanciaMedia: Distancia media entre operaciones.
        """

        plclass_map = {"classifier_file","imputeDistances", "distanciaMedia",
                       "umbral_precision"," dist_mismo_lugar", "max_dist",
                       "umbral_ratio_dCdP", "deltaO_medio"}

        kwargs_plclass = {}
        ##recorro kwargs y usando plclass_map creo un nuevo diccionario con los valores que se pasaron
        for key, value in kwargs.items():
            if key in plclass_map:
                kwargs_plclass[key] = value
        
        self._plantin_classifier = PlantinClassifier.PlantinClassifier(**kwargs_plclass)
        # self._fertilizerFMCreator = FertilizerFMCreator() ## PARA IMPLEMENTAR
        
        self._operationsDict = {} ##diccionario de operarios con sus operaciones
        self._platin_classifiedOperations = np.array([]) ##array con las operaciones clasificadas para plantin
        self._fertilizer_classifiedOperations = np.array([]) ##array con las operaciones clasificadas para plantin
        self._last_row_db = 0 ##indicador de la última fila de los datos extraidos de la base de datos histórica
        self.transformInputData = TransformInputData.TransformInputData()
        self.transformToOutputData = TransformToOutputData.TransformToOutputData()
        
    def processOperations(self, data):
        """Método para procesar las operaciones de los operarios.

        Se toma una nueva muestra y se procesa la información para clasificar las operaciones considerando el
        plantín y por otro lado el fertilizante.
        Se retorna un array con las clasificaciones concatenadas, manteniendo el orden de las operaciones por operario.
        
        Args:
            data: Es una lista de diccionario. Cada diccionario tiene los siguientes keys.
            
            Ejemplo:
            
            {
                "id_db_h":1, #int
                "ID_NPDP":"XXAA123", #string
                "FR": 1, #int
                "TLM_NPDP": b'\xfc\x01\t\t\x00\x00\x00\x98', #bytes
                "date_oprc":datetime.datetime(2024, 2, 16, 21, 2, 2, tzinfo=tzutc()),#datetime
                "Latitud":-32.145564789, #float
                "Longitud":-55.145564789, #float
                "Precision": 1000,
                "id_db_dw": 1 #int
            }
            
        Returns:
            Lista de diccionarios con las clasificaciones. Cada diccionario tiene la forma
            {"id_db_h": 10, "id_db_dw": 10, "tag_seedling": 1, "tag_fertilizer": 1}
        """
        
        ##chqueo que newSample no esté vacío
        if len(data) != 0:
            newSample = self.transformInputData.fit_transform(data)
            #Si tenemos nuevas operaciones, actualizamos el diccionario de operaciones
            self.updateOperationsDict(newSample) #actualizamos diccionario interno de la clase
            pl_clas = self.classifyForPlantin() #clasificamos las operaciones para plantín
            ft_clas = newSample[:,7].astype(int) #clasificamos las operaciones para fertilizante
            id_db_h_nums, id_db_dw_nums = self.getActualOperationsNumbers() #obtenemos los números de operaciones desde el diccionario de operaciones
            date_oprc = newSample[:,3]
            return self.transformToOutputData.fit_transform(np.column_stack((id_db_h_nums,
                                                                             id_db_dw_nums,
                                                                             pl_clas,
                                                                             ft_clas,
                                                                             date_oprc)))
        else:
            self.resetAllNewSamplesValues()
            return None
        
    def updateOperationsDict(self, newSample):
        """Actualiza el diccionario de operaciones.
        
        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            
            - 0: id_db_h
            - 1: ID_NPDP
            - 2: TLM_NPDP
            - 3: date_oprc
            - 4: latitud
            - 5: longitud
            - 6: Precision
            - 7: FR
            - 8: id_db_dw
                
        Returns:
            - None
            NOTA: PENSAR SI SE DEVUELVE ALGO COMO UN TRUE O FALSE PARA SABER SI SE ACTUALIZÓ O NO EL DICCIONARIO
            DE MANERA CORRECTA O HUBO ALGÚN PROBLEMA Y ASÍ VER QUÉ HACER EN EL MAIN
        """
        
        ID_NPDPs_newOperations = np.unique(newSample[:,1]) ##identificadores de operarios con nuevas operaciones en la muestra
        
        ##chqueo si estos ID_NPDPs ya están en el diccionario, sino los agrego
        for ID_NPDP in ID_NPDPs_newOperations:
            if ID_NPDP not in self._operationsDict:
                #El diccionario contiene la siguiente información:
                #sample_ops: np.array con las columnas de TLM_NPDP, date_oprc, lat, lon, precision
                #last_oprc: np.array de la última operación con las columnas de TLM_NPDP, date_oprc, lat, lon, precision
                #first_day_op_classified: booleano para saber si es la primera operación del día fue clasificada
                self._operationsDict[ID_NPDP] = {"sample_ops": None,
                                                 "last_oprc": None, 
                                                 "first_day_op_classified": False,
                                                 "new_sample": False,
                                                 "id_db_h": None,
                                                 "id_db_dw": None} #inicio del diccionario anidado para el nuevo operario
                
        ##actualizo el diccionario con las operaciones nuevas para aquellos operarios que correspondan
        for ID_NPDP in ID_NPDPs_newOperations:
            sample_ops = newSample[newSample[:,1] == ID_NPDP][:,2:] #me quedo con las columnas de TLM_NPDP, date_oprc, lat, lon, precision
            id_db_h = newSample[newSample[:,1] == ID_NPDP][:,0]
            id_db_dw = newSample[newSample[:,1] == ID_NPDP][:,8]
            ##actualizo el diccionario
            self._operationsDict[ID_NPDP]["sample_ops"] = sample_ops
            self._operationsDict[ID_NPDP]["id_db_h"] = id_db_h
            self._operationsDict[ID_NPDP]["id_db_dw"] = id_db_dw
            ##chequeo si tenemos última operación, si es así, asignamos dicha operación en la primera fila de sample_ops
            last_op = self._operationsDict[ID_NPDP]["last_oprc"]
            ###si last_op es not None y last_op no está vacía, entonces concatenamos last_op con sample_ops
            if last_op is not None and last_op.size != 0:
                self._operationsDict[ID_NPDP]["sample_ops"] = np.vstack((last_op, sample_ops))
                
        self.updateNewSamplesValues(ID_NPDPs_newOperations) #actualizo el estado de 'new_sample' en el diccionario de operaciones
        self.updateLastOperations(ID_NPDPs_newOperations) #actualizo la última operación de una muestra de operaciones en el diccionario de operaciones

    def classifyForPlantin(self):
        """Método para clasificar las operaciones para plantín.
        Se recorre el diccionario de operaciones y se clasifican las operaciones para plantín.

        Returns:
            - plantinClassifications: np.array con las clasificaciones de las operaciones para plantín.
        """

        ##creamos/reiniciamos el array con las clasificaciones de las operaciones para plantín
        plantinClassifications = None
        
        ##me quedo con los ID_NPDPs que tengan _operationsDict[ID_NPDP]["new_sample"] iguales a True
        ops_with_new_sample = [ID_NPDP for ID_NPDP in self.operationsDict.keys() if self.operationsDict[ID_NPDP]["new_sample"]]

        for ID_NPDP in ops_with_new_sample:#self.operationsDict.keys():
            ##clasificamos las operaciones para plantín
            operations = self.operationsDict[ID_NPDP]["sample_ops"]
            classified_ops = self._plantin_classifier.classify(operations)
            
            ##chequeo si first_day_op_classified es True, si es así, no se considera la primera fila de las classified_ops
            if self.operationsDict[ID_NPDP]["first_day_op_classified"]:
                classified_ops = classified_ops[1:]
                
            # plantinClassifications = np.vstack((plantinClassifications, classified_ops)) if plantinClassifications is not None else classified_ops
            plantinClassifications = np.concatenate((plantinClassifications, classified_ops)) if plantinClassifications is not None else classified_ops
            
            self.operationsDict[ID_NPDP]["first_day_op_classified"] = True

        return plantinClassifications
            
    def updateLastOperations(self, ID_NPDPs_newOperations):
        """Método para actualizar la última operación de una muestra de operaciones en el diccionario de operaciones

        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            La forma de cada dato dentro de la lista newSample es (n,6). Las columnas de newSample son,
            
                - 0: id_db_h
                - 1: ID_NPDP
                - 2: TLM_NPDP
                - 3: date_oprc
                - 4: latitud
                - 5: longitud
                - 6: Precision
                - 7: FR
                - 8: id_db_dw
        """
        
        for ID_NPDP in ID_NPDPs_newOperations:
            self._operationsDict[ID_NPDP]["last_oprc"] = self._operationsDict[ID_NPDP]["sample_ops"][-1]
    
    def updateNewSamplesValues(self, ID_NPDPs_newOperations):
        """Método para actualizar el estado de 'new_sample' del diccionario de operaciones.

        Args:
            - ID_NPDPs_newOperations: lista con los ID_NPDPs que tienen nuevas operaciones.
        """

        ##recorro el diccionario de operaciones y actualizo el estado de 'new_sample' a
        ##True para los ID_NPDPs que tienen nuevas operaciones y a False para los que no tienen nuevas operaciones
        for ID_NPDP in self.operationsDict.keys():
            if ID_NPDP in ID_NPDPs_newOperations:
                self._operationsDict[ID_NPDP]["new_sample"] = True
            else:
                self._operationsDict[ID_NPDP]["new_sample"] = False
    
    def resetAllNewSamplesValues(self):
        """Método para resetar todos los valores de new_sample en el diccionario de operaciones.
        """
        
        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["new_sample"] = False

    def getActualOperationsNumbers(self):
        """Método para obtener los números de operaciones desde el diccionario de operaciones para aquellos operarios que
        tienen nuevas operaciones en la muestra."""

        id_db_h_list = np.array([])
        id_db_dw_list = np.array([])
        for ID_NPDP in self.operationsDict.keys():
            if self.operationsDict[ID_NPDP]["new_sample"]:
                id_db_h_list = np.append(id_db_h_list, self.operationsDict[ID_NPDP]["id_db_h"].flatten())
                id_db_dw_list = np.append(id_db_dw_list, self.operationsDict[ID_NPDP]["id_db_dw"].flatten())

        return id_db_h_list.astype(int), id_db_dw_list.astype(int)
    
    def updateFirstDayOp(self):
        """Método para actualizar el indicador de si es la primera operación del día para cada operario en el diccionario de operaciones.
        """

        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["first_day_op_classified"] = False
    
    def cleanSamplesOperations(self):
        """Método para limpiar las operaciones de un operario en el diccionario de operaciones.

        Args:
            - newSample: lista con los datos (numpy.array de strings) de las operaciones.
            La forma de cada dato dentro de la lista newSample es (n,6). Las columnas de newSample son,
            
                - 0: id_db_h
                - 1: ID_NPDP
                - 2: TLM_NPDP
                - 3: date_oprc
                - 4: latitud
                - 5: longitud
                - 6: Precision
        """

        for ID_NPDP in self.operationsDict.keys():
            self._operationsDict[ID_NPDP]["sample_ops"] = None
            
    @property
    def operationsDict(self):
        return self._operationsDict
    
    
if __name__ == "__main__":
    #cargo archivo examples\volcado_17112023_NODE_processed.csv
    import pandas as pd
    import numpy as np
    import os
    from sarapy.utils.getRawOperations import getRawOperations

    data_df_raw = getRawOperations("examples\\2024-05-30\\UPM007N\\data.json", "examples\\2024-05-30\\UPM007N\\historical-data.json")

    import time
    start_time = time.time()
    op = OpsProcessor(classifier_file="examples\\pip_lda_imp.pkl", imputeDistances = False)
    classifcations = op.processOperations(data_df_raw)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    
    print(len(classifcations))
    classifcations[:10]