"""Clase para la QTabla, en la que almacenamos un diccionario para la qTabla:
    {pareja estado(x,y) : {accion : utilidad}}

Y dos métodos para insertar nuevos estados y acciones que no hayan sido exploradas
"""

class qTableClass:
    def __init__(self):
        self.qTable = dict()


    def updateStateQtable(self, environment, state):
        self.qTable.setdefault(state,{})
        if (environment.isGoal(state[0], state[1])):
            self.qTable[state].update({"GOAL": environment.getReward(state[0], state[1])})
        return

    def updateActionQtable(self, state, action):
        self.qTable[state].update({action:0.0})
        return