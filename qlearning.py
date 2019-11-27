from time import time
from blackboxenvironment import *
from auxMethods import *




def qLearning(ProbSize, seed, correctProb, alpha, gamma, iterations):
    nIteration = 0

    policy = dict()     # Diccionario para la política, {pareja estado(x,y) : acción}
    utilities = dict()  # Diccionario de utilidades, {pareja estado(x,y) : utilidad}
    qTable = dict()     # Diccionario de la QTabla para el algoritmo {pareja estado(x,y) : {accion : utilidad}}

    qTable = {}

    environment = BlackBoxEnvironment(ProbSize, seed, correctProb)
    qTable = environment.initQTable()
    '''
    Algoritmo QLearning
    '''
    learningTime = time()
    while (nIteration < iterations):

        state = (0, environment.getInitialCarColumn())

        while(not environment.isGoal(state[0], state[1])):
            action = None
            newAction = None
            auxUtil = -math.inf
            newAuxUtil = -math.inf

            #Obtenemos la acción con mejor evaluación en el estado actual
            for a in qTable[state].items():
                if(a[1]>auxUtil):
                    auxUtil = a[1]
                    action = a[0]

            #Generamos el nuevo estado al que llegamos en función de la acción elegida (aleatorio en función de correctProb)
            newState = environment.applyAction(state[0], state[1], action)

            #Obtenemos la acción con mejor evaluación del estado al que llegamos para recalcular el qValor
            for a in qTable[(newState[0], newState[1])].items():
                if(a[1]>newAuxUtil):
                    newAuxUtil = a[1]
                    newAction = a[0]

            nextQValue = qTable[(newState[0],newState[1])][newAction]

            reward = environment.getReward(state[0], state[1])

            #Alpha con decaimiento. POR DEFECTO 0.1
            #alphaValue = alpha*(pow(0.999, nIteration))
            qTable[state][action] = (1 - alpha) * qTable[state][action] + alpha * (reward + gamma * nextQValue)

            state = (newState[0], newState[1])

        nIteration += 1

    learningTime = time() - learningTime
    print("Tiempo de aprendizaje: "+ str(learningTime))

    policy = generatePolicy(qTable, ProbSize)
    environment.policyEvaluation(policy, 10000)

    return 0


def generatePolicy(qTable, ProbSize):

    policy = dict()
    utilities = dict()

    action = None
    for i in range(ProbSize):
        for j in range(ProbSize):
            auxUtil = -math.inf
            for a in qTable[(i,j)].items():
                if(a[1]>auxUtil):
                    auxUtil = a[1]
                    action = a[0]


            policy[(i,j)] = action
            utilities[(i,j)] = auxUtil

    printPolicy(policy, ProbSize)
    printUtils(utilities, ProbSize)

    return policy