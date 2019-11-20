
from blackboxenvironment import *
from auxMethods import *

global policy         #Diccionario para la política, {pareja estado(x,y), acción}
global utilities      #Diccionario de utilidades, {pareja estado(x,y), utilidad}




def valueIteration(ProbSize, seed, correctProb, gamma, convergencia):
    nIteration = 0
    policy = dict()
    utilities = dict()


    environment = BlackBoxEnvironment(ProbSize, seed, correctProb)
    delta = math.inf
    for i in range(ProbSize):
        for j in range(ProbSize):
            if(i==ProbSize-1):
                utilities.update({(i, j): environment.getReward(i,j)})
            else:
                utilities.update({(i, j): 0.0})

            if(environment.maze[i][j] == -1):
                policy.update({(i, j): "WALL"})
            else:
                if (environment.isGoal(i,j)):
                    policy.update({(i, j): "GOAL"})
                else:
                    policy.update({(i, j): environment.getActions()[random.randrange(4)]})

    printPolicy(policy, ProbSize)
    printUtils(utilities, ProbSize)

    while (delta > convergencia):


        auxPolicy = policy.copy()
        auxUtilities = utilities.copy();



        #Para cada estado
        for key in utilities.keys():
            if (environment.maze[key[0]][key[1]] != -1 and not(environment.isGoal(key[0],key[1]))):
                # Auxiliares para cada iteración
                auxAction = ""
                auxUtil = -math.inf
                possibleStates = environment._getNextPositionsByDeterministicAction(key[0], key[1])

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



                auxUtil = environment.getReward(key[0], key[1]) + gamma*auxUtil

                #Condición de parada
                if(abs(auxUtil-utilities[key]) < delta):
                    delta = abs(auxUtil-utilities[key])
                    print("Delta: %.5f" % (delta))

                auxPolicy[key] = auxAction
                auxUtilities[key] = auxUtil

        nIteration +=1

        policy = auxPolicy.copy()
        utilities = auxUtilities.copy()


    environment.printSolution(policy)

    print("Numero de iteraciones: "+ str(nIteration))
    printPolicy(policy, ProbSize)
    printUtils(utilities, ProbSize)

    return 0


