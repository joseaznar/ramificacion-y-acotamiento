from scipy.optimize import linprog
import pandas
import math
import numpy

"""
En este documento se tienen dos funciones: solver_iteration y solver
solver_iteration implementa una iteración del algoritmo de ramificación y acotamiento
para resolver problemas de la forma:

                    min  c^T*x
                    s.a. A*x<=b
                         x>=0, x con entradas enteras

y solver resuelve el problema especificado en los csv's, hay tres archivos:

    - matriz-A.csv
    - vector-b.csv
    - vector-c.csv

Cada uno contiene los coeficientes del elemento especificado en su nombre.
"""
def solver_iteration(A, b, c):
    """
    Este método recursivo resuelve mediante ramificación y acotamiento un problema de programación
    lineal entera, usa el solver de scipy.
    El problema es de la forma:

                    min  c^T*x
                    s.a. A*x<=b
                         x>=0, x con entradas enteras

    :param A: Matriz que contiene las restricciones.
    :param b: Vector que contiene los valores de menor o igual para las restricciones.
    :param c: Vector que contiene los coeficientes de la función objetivo.
    :return: Regresa el estatus de la iteración
    """
    # llamamos a las variables globales
    global min_global
    global x_global

    # primeros resolvemos el problema relajados con las restricciones originales
    resp = linprog(c=c, A_ub=A, b_ub=b)

    # vamos a revisar si todos los valores de la solución son enteros
    flag = True
    index = -1
    var = resp.x

    # si el problema no está bien definido o no está acotado regresamos el estatus
    if resp.status>1:
        return resp.status

    # iteramos para ver si todos son enteros
    for i in var:
        index = index + 1
        if not isinstance(i, int) and int(i) != i:
            print('i no es, i: ' + str(i))
            flag = False
            break

    # en caso de que sean todos enteros, aquí termina la iteración y revisamos si es
    # un valor mejor al mínimo que se tiene; si el mínimo obtenido es mayor al mejor que se tiene,
    # entonces aquí termina la iteración y seguimos a la siguiente

    if resp.fun < min_global:
        if flag:
            min_global = resp.fun
            x_global = var

            return resp.status
    else:
        return resp.status

    # redondeamos hacia arriba y hacia abajo la variable que no es entera
    x_top = math.ceil(list(var)[index])
    x_bot = math.floor(list(var)[index])

    # agregamos la restricción -x_i <= -x_top
    A_top = pandas.DataFrame(data=A)
    zeros = numpy.zeros(len(A_top.columns))
    zeros[index] = -1
    zeros = list(zeros)
    cont = len(A)
    aux = len(A)
    A_top.loc[cont] = [i for i in range(0, len(list(A.columns)))]
    print(str(A_top))
    # agregamos la fila necesaria
    for elem in list(A.columns):
        A_top.loc[cont, elem] = zeros[cont-aux]
        aux = aux - 1
    b_top = b.copy()
    b_top[cont] = int(-x_top)
    # corremos el solver con la nueva restricción
    estatus_top = solver_iteration(A_top, b_top, c)

    # agregamos la restricción x_i <= x_bot
    A_bot = pandas.DataFrame(data=A)
    zeros = numpy.zeros(len(A_bot.columns))
    zeros[index] = 1
    zeros = list(zeros)
    cont = len(A)
    aux = len(A)
    A_bot.loc[cont] = [i for i in range(0, len(list(A.columns)))]
    # agregamos la fila necesaria
    for elem in list(A.columns):
        A_bot.loc[cont, elem] = zeros[cont - aux]
        aux = aux - 1
    b_bot = b.copy()
    b_bot[cont] = int(x_bot)

    # corremos el solver con la nueva restricción
    estatus_bot = solver_iteration(A_bot, b_bot, c)

    # si alguno de los dos corrió adecuadamente, regresamos ese estatus,
    # en caso contrario ponemos el má alto, que es indiferente, pues
    # no llega aquí en la primera iteración si está bien definido el problema
    if estatus_bot==0 or estatus_top==0:
        return 0
    else:
        return max(estatus_top, estatus_bot)


def solver():
    """
    Método que resuelve un problema de programación lineal entera de la forma:

                    min  c^T*x
                    s.a. A*x<=b
                         x>=0, x con entradas enteras
    :return: Regresa el mínimo, los coeficientes que dan el mínimo y el estatus de la función.
    El estatus es 0, si se optimizó correctamente; 1, si se llegó al máximo número de iteraciones
    en la solución; 2, si no está bien definido el problema, y 3, si no está acotado.
    """
    # primero obtenemos los datos de los csv's
    A = pandas.read_csv('matriz-A.csv', sep=',', index_col=False)
    b = pandas.read_csv('vector-b.csv', sep=',', index_col=False)
    c = pandas.read_csv('vector-c.csv', sep=',', index_col=False)

    # ahora definimos las variables globales que tendrán los valores óptimos
    global min_global
    min_global = math.inf

    global x_global
    x_global = numpy.zeros(len(A.columns))

    # finalmente llamamos a la función que ejecuta recursivamente las itercaciones
    # del solver
    estatus = solver_iteration(A[[i for i in list(A.columns)]], b['b'], c['c'])

    return [min_global, x_global, estatus]


if __name__ == '__main__':
    resp = solver()

    print(resp)
