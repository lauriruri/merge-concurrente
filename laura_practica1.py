
'''
Implementar un merge concurrente:
- Tenemos NPROD procesos que producen números no negativos de forma
creciente. Cuando un proceso acaba de producir, produce un -1. 
Cada proceso almacena el valor almacenado en una variable compartida con el consumidor,
un -2 indica que el almacén está vacío.

- Hay un proceso merge que debe tomar los números y almacenarlos de
forma creciente en una única lista (o array). El proceso debe esperar a que
los productores tengan listo un elemento e introducir el menor de
ellos.

- Se debe crear listas de semáforos. Cada productor solo maneja los
sus semáforos para sus datos. El proceso merge debe manejar todos los
semáforos.

- OPCIONAL: se puede hacer un búffer de tamaño fijo de forma que
los productores ponen valores en el búffer.

'''

from multiprocessing import Process, Manager
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore
from random import random,randint

COTA = 100
N=5 #numero de procesos
values=[]
procesos=[]
lleno=[]
vacio=[]

def llamar_proceso(proc_id):
    value = 0
    LIMITE = randint(2,10) #con esto hago que cada productor tenga una capacidad distinta y 'aleatoria'
    print(LIMITE, "este es mi limite para el proceso ", proc_id)
    #LIMITE=10
    for i in range(0,LIMITE):
        print("process",proc_id,"wait")
        vacio[proc_id].acquire()
        value = value + randint(0, COTA)
        values[proc_id].value = value
        print("process",proc_id,"produced value",values[proc_id].value)
        lleno[proc_id].release()
        print("process",proc_id,"release")

    #finaliza mi límite, no tengo más que producir
    vacio[proc_id].acquire()
    values[proc_id].value = -1
    lleno[proc_id].release()


def minimum_pos(l):
    aux = l[0]
    pos = 0
    contador = 0
    longitud = len(l)
    for i in range(0,len(l)):
        if (aux == -1 and contador < longitud-1):
            aux = l[i+1]
            pos = i+1
        if (l[i] == -1):
            contador = contador + 1
        if (l[i]<aux and l[i]!=-1):
            aux = l[i]
            pos = i
    return (aux, pos, contador)

def llamar_consumidor(lleno,values,resultado):

    local_values=[]
    for i in range(0,N):       
        print("consumer waiting for", i)
        lleno[i].acquire()
        local_values.append(values[i].value)
        print ("este es el valor: ", values[i].value)
        print("y así queda mi local_values ,", local_values)
    print("initial values are:", local_values)
    
    #j=0
    while True:
        (minimo, posicion, contador)=minimum_pos(local_values)
        if (contador == len(local_values)):
            break
        resultado.append(minimo)
        #j=j+1
        print("consumer releasing", posicion)
        vacio[posicion].release()
        print("consumer waiting", posicion)
        lleno[posicion].acquire()
        local_values[posicion]=values[posicion].value
        print("values are:", local_values)

########################################

def main():
    manager = Manager()
    resultado = manager.list()

    #inicializo los procesos
    for i in range(0,N):
        values.append(Value('i',-2)) #inicializo los valores a -2
        vacio.append(Semaphore(1))
        lleno.append(Semaphore(0))
        procesos.append(Process(target=llamar_proceso, args = (i,)))
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

'''
producer(i)
loop
    empty(i).wait()
    producer
    non_empty(i).signal()

consumer //necesito que haya al menos un valor distinto de -1
//si un proceso esta en -1 ya no produce mas!!!!
for i
    non_empty(i).wait()
loop
    i <- minimo
    almacenamos
    empty(i).signal() //despertamos al que ha producido al mínimo
    non.empty(i).wait() 
'''