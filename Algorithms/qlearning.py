from time import time
import math
from Environment.qTableClass import *
from random import *
from Environment.blackboxenvironment import *
from Algorithms.auxMethods import *

#ProbSize:      Tamaño del problema n*n
#Seed:          Semilla para generación de aleatorios
#correctProb:   Probabilidad de elección correcta de la acción
#alpha:         por defecto 0.1, es la preferencia de la nueva solución frente a la anterior
#gamma:         por defecto 1
#iterations:    nº de iteraciones que aplicará el algoritmo para encontrar la política óptima


def qLearning(ProbSize, seed, correctProb, alpha, gamma, iterations):
    global qT


    decaimiento = 0     #--MODIFICABLE--
    alphaValue = alpha
    nIteration = 0

    # Objeto qTable con diccionario de la QTabla para el algoritmo {pareja estado(x,y) : {accion : utilidad}}
    qT = qTableClass()


    environment = BlackBoxEnvironment(ProbSize, seed, correctProb)

    '''
    Algoritmo QLearning
    '''
    learningTime = time()
    while (nIteration < iterations):

        #Obtenemos el estado inicial
        state = (0, environment.getInitialCarColumn())

        while(not environment.isGoal(state[0], state[1])):
            action = None       #Acción que evaluamos en el estado actual
            newAction = None    #Mejor acción del estado siguiente para la evaluación

            #Si el estado no ha sido visitado, lo añadimos, incluido el inicial
            if(state not in qT.qTable.keys()):
                qT.updateStateQtable(environment, state)

            #Si random es menor que probabilidad de exploración (por defecto 0.1), elegimos acción aleatoria
            #Si no: Obtenemos la acción con mejor evaluación en el estado actual
            if(random.random()<0.1):    #Mejora la exploración --MODIFICABLE--
                action = environment.getActions()[random.randint(0,3)]
                #Si la acción no fué explorada, la añadimos a la qtabla
                if(action not in qT.qTable[state].keys()):
                    qT.updateActionQtable(state, action)
            else:
                action = getBestAction(state, environment)[0]

            #Generamos el nuevo estado al que llegamos en función de la acción elegida (aleatorio en función de correctProb)
            newState = environment.applyAction(state[0], state[1], action)

            #Si el nuevo estado no existe en la qTabla, lo añadimos
            if((newState[0], newState[1]) not in qT.qTable.keys()):
                qT.updateStateQtable(environment, (newState[0], newState[1]))


            #Obtenemos la acción con mejor evaluación del estado al que llegamos para recalcular el qValor
            newAction = getBestAction((newState[0], newState[1]), environment)[0]

            #Obtenemos el QValor del siguiente estado al que iremos
            nextQValue = qT.qTable[(newState[0], newState[1])][newAction]

            #Obtenemos la recompensa de movernos al siguiente estado
            reward = environment.getReward(newState[0], newState[1])

            #Alpha con decaimiento. POR DEFECTO 0.1
            if (decaimiento):
                alphaValue = alpha *(pow(0.999, nIteration))

            if(environment.isGoal(newState[0], newState[1])):
                qT.qTable[state][action] = (1 - alphaValue) * qT.qTable[state][action] + alphaValue * (reward)
            else:
                qT.qTable[state][action] = (1 - alphaValue) * qT.qTable[state][action] + alphaValue * (reward + gamma * nextQValue)

            #Actualizamos al siguiente estado para la siguiente iteración
            state = (newState[0], newState[1])

        nIteration += 1

    learningTime = time() - learningTime
    print("Tiempo de aprendizaje: "+ str(learningTime))

    policy = generatePolicy(qT.qTable, ProbSize)
    evaluation = environment.policyEvaluation(policy, 10000)

    return [evaluation, learningTime]


def generatePolicy(qTable, ProbSize):

    policy = dict()     # Diccionario para la política, {pareja estado(x,y) : acción}
    utilities = dict()  # Diccionario de utilidades, {pareja estado(x,y) : utilidad}

    action = None
    for i in range(ProbSize):
        for j in range(ProbSize):
            auxUtil = -math.inf
            #Los valores i,j que estén en la qtabla serán posiciones validas
            if((i,j) in qTable.keys()):
                for a in qTable[(i,j)].items():
                    if(a[1]>auxUtil):
                        auxUtil = a[1]
                        action = a[0]

                policy[(i,j)] = action
                utilities[(i,j)] = auxUtil
            #Los valores que no estén, serán muros (es útil para la representación gráfica)
            else:
                policy[(i,j)] = "WALL"
                utilities[(i,j)] = auxUtil

    printPolicy(policy, ProbSize)
    printUtils(utilities, ProbSize)

    return policy


#Para elegir la mejor acción de manera común entre el nuevo estado y el qu estamos explorando
def getBestAction(state, environment):
    auxUtil = -math.inf
    for a in environment.getActions():
        if (a not in qT.qTable[state].keys()):
            qT.updateActionQtable(state, a)

        if (qT.qTable[state][a] > auxUtil):
            auxUtil = qT.qTable[state][a]
            action = a
    return (action, auxUtil)