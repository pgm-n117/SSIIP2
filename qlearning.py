
from blackboxenvironment import *
from auxMethods import *




def qLearning(ProbSize, seed, correctProb, alpha, gamma, iterations):
    nIteration = 0

    global policy  # Diccionario para la política, {pareja estado(x,y) : acción}
    global utilities  # Diccionario de utilidades, {pareja estado(x,y) : utilidad}
    global qTable  # Diccionario de la QTabla para el algoritmo {pareja estado(x,y) : {accion : utilidad}}

    qTable = {}

    environment = BlackBoxEnvironment(ProbSize, seed, correctProb)
    qTable = environment.initQTable()
    '''
    Algoritmo QLearning
    '''
    while (nIteration < iterations):


        state = (0, environment.getInitialCarColumn())

        while(not environment.isGoal(state[0], state[1])):
            action = None
            newAction = None
            auxUtil = -math.inf
            newAuxUtil = -math.inf

            for a in qTable[state].items():
                if(a[1]>auxUtil):
                    auxUtil = a[1]
                    action = a[0]

            newState = environment.applyAction(state[0], state[1], action)

            for a in qTable[(newState[0], newState[1])].items():
                if(a[1]>newAuxUtil):
                    newAuxUtil = a[1]
                    newAction = a[0]

            nextQValue = qTable[(newState[0],newState[1])][newAction]

            reward = environment.getReward(state[0], state[1])

            qTable[state][action] = (1-alpha)*qTable[state][action]+alpha*(reward + gamma*nextQValue)

            state = (newState[0],newState[1])

        nIteration+=1


    generatePolicy(ProbSize)


    return 0


def generatePolicy(ProbSize):

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