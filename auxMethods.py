import math
from blackboxenvironment import *

"""Métodos auxiliares para la implemetnación de iteración de valores y QLearning"""

def printPolicy(policy, ProbSize):

    for i in range(ProbSize):
        line = ""
        for j in range(ProbSize):
            line = line + " \t|" +policy.get((i,j))
        print(line)



def printUtils(utilities, ProbSize):
    for i in range(ProbSize):
        line = ""
        for j in range(ProbSize):
            line = line + "\t %.2f" % (utilities.get((i,j)))
        print(line)


def evalTotalUtilities(utilities, auxUtilities):
    utility = 0.0
    auxUtility = 0.0
    for s in dict(utilities).values():
        utility += s

    for s in dict(auxUtilities).values():
        auxUtility += s

    return abs(auxUtility - utility)

