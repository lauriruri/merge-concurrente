from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from random import random

'''
Implementar un merge concurrente:
- Tenemos NPROD procesos que producen números no negativos de forma
creciente. Cuando un proceso acaba de producir, produce un -1
- Hay un proceso merge que debe tomar los números y almacenarlos de
forma creciente en una única lista (o array). El proceso debe esperar a que
los productores tengan listo un elemento e introducir el menor de
ellos.
- Se debe crear listas de semáforos. Cada productor solo maneja los
sus semáforos para sus datos. El proceso merge debe manejar todos los
semáforos.
- OPCIONAL: mente se puede hacer un búffer de tamaño fijo de forma que
los productores ponen valores en el búffer.

PRIMERA VERSIÓN:
para poder elegir el mínimo tienen que haber producido un valor todos los consumidores

luego el consumidor va cogiendo los numeros y ordenandolos de menor a mayor

el prodeso acaba cuando algún productor esta  -1, ponemos un numero aleatorio de vueltas.

fijamos n numero de vueltas y cada proceso crea 

idea es que la lista de C sea una lista ordenada y con todos los numeros positivos.

SEGUNDA VERSIÓN:
cada productor tiene una lista! en vez de un valor. 
Se controla con semáforos. Si en un proceso encuentra el -1 se acaba.
'''

from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from random import random