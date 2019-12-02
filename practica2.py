from argparse import ArgumentParser
from time import time


if __name__ == "__main__":

    # ArgumentParser con una descripción de la aplicación
    parser = ArgumentParser(description='%(prog)s es un simulador de aprendizaje por refuerzo e iteración de valores')
    # Argumento posicional con descripción
    parser.add_argument('n', type=int, help='tamaño del problema')
    parser.add_argument('seed', type=int, help='semilla para funcion random')
    parser.add_argument('pCorrect', type=float, help='probabilidad de elegir la acción correcta')
    parser.add_argument('gamma', type=float, help='factor de descuento (recompensas depreciativas)', default=1)
    parser.add_argument('algoritmo', choices=['valueiteration', 'qlearning'], help='Algoritmo con el que se abordará el ejercicio')

    '''
    Alpha representa la preferencia de valores q nuevos frente a los antiguos 
        (Alpha = 1 prefiere los nuevos, Alpha = 0 prefiere los antiguos siempre, por lo que no actualiza)
        El valor por defecto de las practicas es 0.1
        
    Delta representa la condición de parada, (cuanto mas cercano a 0 sea, más precisión) parará cuando la
        diferencia entre la utilidad de la nueva politica y la anterior sea menor que delta 
        El valor por defecto empleado en las prácticas es 0.001
    '''
    parser.add_argument('alphaDelta', type=float, help='alpha para qLearning / delta para iteración de valores', default=1)
    parser.add_argument('--nIteraciones', type=int, help='iteraciones de qLearning')

    args = parser.parse_args()

    print(args)

    #Para medir el tiempo de ejecución
    global tiempoInicio
    tiempoInicio = time()


    if(args.algoritmo=='valueiteration'):
        from Algorithms.valueiteration import *
        solucion = valueIteration(args.n, args.seed, args.pCorrect, args.gamma, args.alphaDelta)
    elif(args.algoritmo=='qlearning'):
        from Algorithms.qlearning import *
        solucion = qLearning(args.n, args.seed, args.pCorrect, args.alphaDelta, args.gamma, args.nIteraciones)


    tiempoFin = str(time()- tiempoInicio)


    print("Tiempo de ejecución: " + tiempoFin)