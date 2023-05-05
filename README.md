# merge-concurrente
En este repositorio se encuentran las soluciones al siguiente ejercicio:

"Implementar un merge concurrente:
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

- OPCIONAL: mente se puede hacer un búffer de tamaño fijo de forma que
los productores ponen valores en el búffer."

En la carpeta se encuentran diferentes archivos:
1- LICENSE
2- README.md
3-laura_opcional1.py
4-laura_opcional2.py
5-laura_practica1.py
6-practica.py

  -El archivo 1 es la licencia.
  
  -El archivo 2 es este mismo.
  
  -El archivo 6 no debe tenerse en cuenta para la entrega, pues este es una versión anterior del archivo 5, que finalmente es el que funciona.

  -El archivo 5 contiene la parte obligatoria de la práctica. Para resolver este ejercicio se ha seguido el siguiente esquema de manera geneal:

producer(i)
loop
    empty(i).wait()
    producer
    non_empty(i).signal()
    
consumer 
for i
    non_empty(i).wait()
loop
    i <- minimo
    almacenamos
    empty(i).signal() 
    non.empty(i).wait() 
   
Para ejecutar este programa se tiene que llamar a la función main().

Comentario sobre la función minimum_pos(l): esta toma una lista y devuelve su elemento mínimo, su posición en la lista y un contador con el número de -1 que se encuentran en la lista. Esto nos interesa porque cuando nuestro productor deja de producir escribe un -1, y nuestro consumidor dejará de consumir cuando en todas las posiciones de la lista se encuentre un -1, es decir, no haya más productores produciendo.

  - El archivo 3 contiene la solución al ejercicio opcional propuesto por el profesor: en esta ocasión cada productor tiene una lista de valores en lugar de un valor. Se siguen las mismas ideas planteadas en el archivo 5. Para ejecutar este programa se tiene que llamar a la función main().
Para ejecutar este programa se stiene que llamar a la función main().

  -El archivo 4 contiene la solución a otra variación del ejercicio 5 propuesta por la alumna. En este modelo se tienen dos consumidores:
  consumidor1: toma el mínimo de los valores disponibles en ese momento.
  consumidor2: toma el máximo de los valores disponibles en ese momento.
  Se sigue la siguiente idea: produce- consume consumidor1- produce - consume consumidor 2 (recursivamente hasta que todos los valores esten a -1). NOTA: los resultados obtenidos no siguen un orden completo en el caso de consumidor2 ya que se produce de manera creciente).

