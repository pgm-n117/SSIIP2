import math
from time import time
from Environment.blackboxenvironment import *
from Algorithms.auxMethods import *

#ProbSize:      Tamaño del problema n*n
#Seed:          Semilla para generación de aleatorios
#correctProb:   Probabilidad de elección correcta de la acción
#gamma:         por defecto 1
#convergencia:  valor de convergencia de delta para la condición de parada


def valueIteration(ProbSize, seed, correctProb, gamma, convergencia):

    policy = dict()     # Diccionario para la política, {pareja estado(x,y) : acción}
    utilities = dict()  # Diccionario de utilidades, {pareja estado(x,y) : utilidad}

    nIteration = 0

    '''
    Inicializamos la politica inicial (aleatoria) y las utilidades iniciales 
    (0.0 para todos los casos excepto los estados finales, que tienen su recompensa)
    '''
    environment = BlackBoxEnvironment(ProbSize, seed, correctProb)

    for i in range(ProbSize):
        for j in range(ProbSize):
            if(environment.maze[i][j] == -1):
                policy.update({(i, j): "WALL"})
                utilities.update({(i, j): 0.0})
            else:
                if (environment.isGoal(i,j)):
                    policy.update({(i, j): "GOAL"})
                    utilities.update({(i, j): environment.getReward(i, j)})
                else:
                    policy.update({(i, j): environment.getActions()[random.randrange(4)]})
                    utilities.update({(i, j): 0.0})

    #Imprime el estado inicial del problema
    #printPolicy(policy, ProbSize)
    #printUtils(utilities, ProbSize)

    '''
    Algoritmo de iteración de valores
    '''
    learningTime = time()
    delta = math.inf
    stop = False
    while (not stop):

        auxPolicy = policy.copy()
        auxUtilities = utilities.copy()
        diff=0.0
        #Para cada estado:
        for s in utilities.keys():
            #Si no es pared y no es un estado final
            if (environment.maze[s[0]][s[1]] != -1 and not(environment.isGoal(s[0],s[1]))):
                #Variables auxiliares para cada iteración
                auxAction = ""
                auxUtil = -math.inf

                #Obtenemos los posibles estados a los que se puede llegar
                possibleStates = environment._getNextPositionsByDeterministicAction(s[0], s[1])

                #Para cada acción, si el siguiente estado es el que resulta de nuestra acción -> probabilidad de moverse a la posición correcta * utilidad del destino
                #Si no, probabilidad de moverse a cualquier otra posición * utilidad del destino
                for action in environment.getActions():
                    auxEval = 0.0
                    for pS in range(len(possibleStates)):
                        if(pS == environment._getActionIndex(action)):
                            aux = environment.probCorrectMove * utilities[possibleStates[pS][0], possibleStates[pS][1]]
                        else:
                            aux = environment.probWrongMove * utilities[possibleStates[pS][0], possibleStates[pS][1]]

                        auxEval+=aux

                    if(auxEval > auxUtil):
                        auxUtil = auxEval
                        auxAction = action

                auxUtil = environment.getReward(s[0], s[1]) + gamma*auxUtil

                auxPolicy[s] = auxAction
                auxUtilities[s] = auxUtil

                # Condición de parada
                auxdiff = abs(auxUtilities[s] - utilities[s])
                if (auxdiff > diff):
                    diff = auxdiff

        #Cuando el cambio entre la iateración actual y la anterior sea menor que convergencia (por defecto 0.001), paramos
        if(abs(delta - diff)<convergencia):
            stop=True

        delta = diff
        print("Delta: %.5f" % (diff))

        nIteration +=1

        policy = auxPolicy.copy()
        utilities = auxUtilities.copy()

    learningTime = time() - learningTime

    print("Numero de iteraciones: "+ str(nIteration))
    print("Tiempo de aprendizaje: "+ str(learningTime))
    printPolicy(policy, ProbSize)
    printUtils(utilities, ProbSize)


    #Final Policy Evaluation:
    evaluation = environment.policyEvaluation(policy, 10000)


    return [evaluation, nIteration, learningTime]


