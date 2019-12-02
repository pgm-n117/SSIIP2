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

