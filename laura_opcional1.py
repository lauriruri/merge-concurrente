'''
SEGUNDA VERSIÓN:
cada productor tiene una lista! en vez de un valor. 
Se controla con semáforos. Si en un proceso encuentra el -1 se acaba.
'''

from multiprocessing import Process, Manager
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore
#from multiprocessing import Manager
from random import random,randint

##randint(1,30) me genera un numero entre 1 y 30 -> 14
##randint(14,30*2) etc.
COTA = 100
N=5 #numero de procesos
CAP_PROCESO = 3
#sem = Semaphore(0) #numero es numero de procesos que pueden entrar
#values = Manager().list(range(0, N)) #será una lista de arrays
values = [] #Manager().list()
#values = Array('i',range(N))
procesos=[]
lleno=[]
vacio=[]
#resultado = [] #usar algo compartido mejor
#resultado = Array('i',range(N*100))

def llamar_proceso(proc_id, values):
    value = 0
    LIMITE = 5
    #lista_act = values[proc_id]
    for i in range(0,LIMITE):
        print("process",proc_id,"wait")
        vacio[proc_id].acquire()
        for j in range(0,CAP_PROCESO):
            print(values[proc_id])
            if values[proc_id][j] == -2:
                value = value + randint(0, COTA)
                values[proc_id][j] = value
            print("process",proc_id,"produced value", values[proc_id], "in ", j)
        lleno[proc_id].release()
        print("process",proc_id,"release")

#entramos aquí cuando llegamos al fin del límite. tenemos que 'comernos' cada uno de los elementos del array
    for i in range(0, CAP_PROCESO):
        vacio[proc_id].acquire()
        for j in range(0, CAP_PROCESO):
            if values[proc_id][j] == -2:
                values[proc_id][j] = -1
        lleno[proc_id].release()


def minimum_pos(l): #l = [(1,2,3)] donde 1-> valor; 2-> proceso; 3-> posicion dentro del array
    #puedo acceder a las posiciones haciendo: l[0][1] = 2
    aux = l[0][0]
    proceso = l[0][1]
    pos_values = 0
    contador = 0
    pos_array = l[0][2]
    longitud = len(l)
    for i in range(0,len(l)):
        if (aux == -1 and contador < longitud-1):
            aux = l[i+1][0]
            pos_values = i+1
            proceso = l[i+1][1]
            pos_array = l[i+1][2]
        if (l[i][0] == -1):
            contador = contador + 1
            #proceso = l[i][1]
            #pos_array = l[i][2]
        if (l[i][0] < aux and l[i][0]!=-1):
            aux = l[i][0]
            pos_values = i
            proceso = l[i][1]
            pos_array = l[i][2]
    return (aux, pos_values, proceso, pos_array, contador)

################################3
def llamar_consumidor(lleno,values,resultado):
    print("estoy en el cosumidor y estos son mis values : ", values)
#NECESITO UNA VARIABLE COMPARTIDA!!!!!

    local_values=[]
    for i in range(0,N):       
        print("consumer waiting for", i)
        lleno[i].acquire()
        for j in range(0,CAP_PROCESO):
            local_values.append((values[i][j],i,j)) #almaceno su proceso y su indice dentro del array
            #print ("este es un valor de ", i, "este proceso: " , values[i][j])
            #print("y así queda mi local_values ,", local_values)
    print("initial values are:", local_values)
    
    #j=0
    while True:
        (minimo, pos_values, proceso, pos_array, contador) = minimum_pos(local_values)
        if (contador == len(local_values)):
            break
        resultado.append(minimo)
        #j=j+1
        values[proceso][pos_array] = -2
        print("consumer releasing", proceso)
        vacio[proceso].release()
        print("consumer waiting", proceso)
        lleno[proceso].acquire()
        local_values[pos_values] = (values[proceso][pos_array], proceso, pos_array)
        print("values are:", local_values)

    #print(resultado, "EN EL CONSUMIDOR")
########################################

def main():

    manager = Manager()
    resultado = manager.list()

    #values = manager.list()

    #inicializo los procesos
    for i in range(0,N):
        #values.append(Array('i',range(CAP_PROCESO))) #inicializo los valores a -2
        #value.append([])
        #values.append(Manager().list(range(CAP_PROCESO)))
        values.append(Manager().list([-2 for x in range(0, CAP_PROCESO)]))
        #for j in range(0,CAP_PROCESO):
        #    values[i].append(-2)

        vacio.append(Semaphore(1))
        lleno.append(Semaphore(0))
        procesos.append(Process(target=llamar_proceso, args = (i, values,)))

    for proceso in procesos:
        proceso.start()

#llamada al consumidor
    consumidor = Process(target=llamar_consumidor, args=(lleno,values,resultado,))
    consumidor.start()
    consumidor.join()
    for proceso in procesos:
        proceso.join()

    print("\n")
    print(resultado, "en el main")
    print('Ha terminado')

if __name__ == "__main__" :
    main()
    print("fin")