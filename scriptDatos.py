from time import time
import os
import random
from Algorithms import qlearning, valueiteration

tiempoInicio = None
tiempoFin = None
#solucion = Solucion(None, None, None, None, None, None, None)
Npruebas = 25 #numero de pruebas que se haran para cada caso

problemSizes = [5, 10, 15, 20, 25, 30]

seeds = []
random.seed(2019)
for i in range(len(problemSizes)):
    seeds.append([])
    for n in range(Npruebas):
        seeds[i].append(random.random())

'''
Formato del fichero csv para Iteracion de valores:
Tamaño del laberinto, Iteraciones necesarias, Utilidad de la política encontrada, Tiempo de aprendizaje, Tiempo de ejec.
'''

if(not(os.path.exists("./Datos"))):
    os.mkdir('./Datos', 0o777)

'''
Pruebas variando el tamaño y manteniendo el resto de valores 
'''

#Iteración de valores: [correctProb = 0.7, gamma = 1, limite para delta = 0.001]
cabecera = "Tamaño, Utilidad de la Politica, Iteraciones, Tiempo de aprendizaje, Tiempo de ejecucion\n"
fd = open("./Datos/ValueItDefaultParam.csv", "w")
fd.writelines(cabecera)
solucion = None
for i in range(len(problemSizes)):
    for n in range(Npruebas):
        tiempoInicio = time()
        solucion = valueiteration.valueIteration(problemSizes[i], seeds[i][n], 0.7, 1, 0.001)
        tiempoFin = time() - tiempoInicio
        fd.writelines(problemSizes[i].__str__() + "," + str(solucion[0]) + "," + str(solucion[1]) + "," + str(solucion[2]) + "," + str(tiempoFin) + "\n")

fd.close()


#QLearning[correctProb = 0.7, gamma = 1, alpha= 0.1, 10000 iteraciones]
cabecera = "Tamaño, Utilidad de la Politica, Tiempo de aprendizaje, Tiempo de ejecucion, Iteraciones\n"
fd = open("./Datos/QLearningDefaultParam.csv", "w")
fd.writelines(cabecera)
solucion = None
for i in range(len(problemSizes)):
    for n in range(Npruebas):
        tiempoInicio = time()
        solucion = qlearning.qLearning(problemSizes[i], seeds[i][n], 0.7, 0.5, 1, 10000)
        tiempoFin = time() - tiempoInicio
        fd.writelines(problemSizes[i].__str__() + "," + str(solucion[0]) + "," + str(solucion[1]) + "," + str(tiempoFin) + "," + str(10000) + "\n")

fd.close()