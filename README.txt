En el archivo utils.py se tiene la funcionalidad para resolver un problema de programación lineal 
de la forma:

                    min  c^T*x
                    s.a. A*x<=b
                         x>=0, x con entradas enteras
                         
Se ejecuta simplemente poniendo python utils.py en la consola o poniendo utils.py en una consola de python. 

En el archivo requirements.txt vienen los requerimientos de paquetes.

Los valores de A, b y c deben estar especificados en sus respectivos archivos .csv localizados en esta carpeta. 

El resultado aparecerá en la consola como una lista cuyo primer valor es el mínimo, el segundo es una lista con los coeficientes que generan ese mínimo y el tercero el estatus resultante.
