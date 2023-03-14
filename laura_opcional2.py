'''
- OPCIONAL: intento hacer dos consumidores: uno que tome el maximo y otro el minimo y se vayan turnando.
'''

from multiprocessing import Process, Manager
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore
from random import random,randint

COTA = 100
N=5 #numero de procesos
CAP_PROCESO = 3
values = []
procesos=[]
lleno=[]
vacio=[]


def llamar_proceso(proc_id, values):
    value = 0
    LIMITE = 5

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
        if (l[i][0] < aux and l[i][0]!=-1):
            aux = l[i][0]
            pos_values = i
            proceso = l[i][1]
            pos_array = l[i][2]
    return (aux, pos_values, proceso, pos_array, contador)

def maximun_pos(l): #l = [(1,2,3)] donde 1-> valor; 2-> proceso; 3-> posicion dentro del array
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
        if (l[i][0] > aux and l[i][0]!=-1):
            aux = l[i][0]
            pos_values = i
            proceso = l[i][1]
            pos_array = l[i][2]
    return (aux, pos_values, proceso, pos_array, contador)


################################
def llamar_consumidor1(lleno,values,resultado1, paso_turno_1, paso_turno_2, local_values):
    #print("estoy en el cosumidor 1 y estos son mis values : ", values)
    print("ENTRO EN COSUMIDOR 1")
    
    while True:
        paso_turno_1.acquire()
        (minimo, pos_values, proceso, pos_array, contador) = minimum_pos(local_values)
        if (contador == len(local_values)):
            paso_turno_2.release()
            break
        resultado1.append(minimo)
        values[proceso][pos_array] = -2
        print("consumer releasing", proceso)
        vacio[proceso].release()
        print("consumer waiting", proceso)
        lleno[proceso].acquire()
        local_values[pos_values] = (values[proceso][pos_array], proceso, pos_array)
        print("values are:", local_values)
        print("RESULTADO 1: ", resultado1)
        paso_turno_2.release()

def llamar_consumidor2(lleno,values,resultado2, paso_turno_1, paso_turno_2, local_values):
    #print("estoy en el cosumidor 2 y estos son mis values : ", values)
    print("ENTRO EN COSUMIDOR 2")
   
    while True:
        paso_turno_2.acquire()
        (minimo, pos_values, proceso, pos_array, contador) = maximun_pos(local_values)
        if (contador == len(local_values)):
            paso_turno_1.release()
            break
        resultado2.append(minimo)
        values[proceso][pos_array] = -2
        print("consumer releasing", proceso)
        vacio[proceso].release()
        print("consumer waiting", proceso)
        lleno[proceso].acquire()
        local_values[pos_values] = (values[proceso][pos_array], proceso, pos_array)
        print("values are:", local_values)
        print("RESULTADO 2: ", resultado2)
        paso_turno_1.release()

########################################

def main():

    manager = Manager()
    resultado1 = manager.list()
    resultado2 = manager.list()

    paso_turno_1 = Semaphore(1)
    paso_turno_2 = Semaphore(0)

    local_values = manager.list()

    #inicializo los procesos
    for i in range(0,N):
        values.append(Manager().list([-2 for x in range(0, CAP_PROCESO)]))

        vacio.append(Semaphore(1))
        lleno.append(Semaphore(0))
        procesos.append(Process(target=llamar_proceso, args = (i, values,)))

    for proceso in procesos:
        proceso.start()

    #inicio local_values
    for i in range(0,N):       
                print("consumer waiting for", i)
                lleno[i].acquire()
                for j in range(0,CAP_PROCESO):
                    local_values.append((values[i][j],i,j)) #almaceno su proceso y su indice dentro del array
    print("initial values are:", local_values)


    #llamada al consumidor
    consumidor1 = Process(target=llamar_consumidor1, args=(lleno,values,resultado1, paso_turno_1, paso_turno_2,local_values,))
    consumidor2 = Process(target=llamar_consumidor2, args=(lleno,values,resultado2, paso_turno_1, paso_turno_2,local_values,))

    consumidor1.start()
    consumidor2.start()

    consumidor1.join()
    consumidor2.join()

    for proceso in procesos:
        proceso.join()

    print("\n")
    print(resultado1, "en el main")
    print(resultado2, "en el main")
    print('Ha terminado')

if __name__ == "__main__" :
    main()
    print("fin")