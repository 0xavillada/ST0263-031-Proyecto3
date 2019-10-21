# Modelo PCAM

## Partición

A partir de la solución serial, podemos definir el algoritmo en cuatro partes:

- Lectura del archivo
- Llenado de la matriz
- Alineamiento de la matriz
- Puntuación

## Comunicación

Cada una de las cuatro partes se debe ejecutar de manera secuencial en el orden descrito en la partición. Es decir, primero la lectura, luego el llenado y así sucesivamente. Esto hace que la paralelización solamente se pueda hacer dentro de cada una de ellas en el momento de su "turno". 
Por lo tanto cada una se debe comunicar con la anterior para recibir su resultado y comenzar su ejecución. 

![Comunicacion](pcam-2.png)

## Aglomeración

## Mapeo

