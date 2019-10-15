# ST0263-031-Proyecto3
Este proyecto corresponde a la unidad numero 2 del curso Topicos especiales en telematica del programa en ingenieria de sistemas de la univeridad EAFIT.

# Variante de alineamiento múltiple para ácidos nucleicos y péptidos

## Contexto:
Un alineamiento múltiple de secuencias  es un alineamiento de tres o más secuencias biológicas, generalmente proteínas, ADN o ARN. En general, se asume que el conjunto de secuencias de consulta que se ingresa como entrada (conjunto problema) tienen una relación evolutiva por la cual comparten un linaje y descienden de un ancestro común, el alineamiento se utiliza para evaluar la conservación de los dominios proteicos, las estructuras terciarias y secundarias, e incluso aminoácidos o nucleótidos individuales.

## Problema:
Como puede ser difícil alinear a mano tres o más secuencias de longitud biológicamente relevante, y casi siempre consume mucho tiempo, se utilizan algoritmos computacionales para producir y analizar los alineamientos. El objetivo principal del alineamiento es cuantificar el grado de similitud de las cadenas superponiendo una cadena sobre la otra con la posibilidad de desplazar caracteres a la derecha o a la izquierda, sin alterar el orden de la cadena original. Para esta variante del alineamiento, se tiene una cadena de referencia para la cuál se supone en términos biológicos, es la que contiene mayor cantidad de material genético (mayor longitud) y las demás cadenas asociadas (menor longitud) serán sobre las cuales se trabajará, modificandolas de tal forma, que se puedan identificar la posible fracción de ADN faltante en esa cadena.

El cálculo del puntaje se lleva a cabo mediante la entrada, dando como penalización un valor entero “K” a cada “Mismatch” y un valor entero “L” a cada “match.

## Ejemplo:

Entrada:
match points= +1
mismatch points= -1
gap points= 0

ATATCCG
TCCG
ATGTACTG
ATGTCTG

Salida:
Puntaje= 4
Tasa= 4/4 = 1

"A T G T A C T G"
"A T -  A T C C G"
"A T G T -  C T G"
"- T - - -  C C G"

#### Aquí el score por ejemplo de la columna 3 es:
G
"-"
G
"-"

score = score(G,-) + score(G, G) + score(G,-) + score(-,G) + score (-,-) + score(G,-)
          =        -1        +         1         +       -1        +        -1        +        0       +       -1
          =  -3


# Correr el programa serial:
python3 aligment-serial.py "fichero con cadenas a alinear" "valor coincidencia" "valor no coincidencia" "valor faltante"

Ejemplo: $ time python alignment-serial.py dna50.txt -1 1 0
(corriendo: archivo:"dna50.txt" con score(1 mach)(-1 missmach)(0 gab) y 2 hilos))

# Correr el programa paralelo:
mpiexec -f ./hosts_mpi -np "numero de nodos" /opt/anaconda3/bin/python ./alignment-parallel.py "fichero con cadenas a alinear" "valor coincidencia" "valor no coincidencia" "valor faltante" "numero threads"

Ejemplo:$ time mpiexec -f ./hosts_mpi -np 2 /opt/anaconda3/bin/python ./alignment-parallel.py dna50.txt 1 -1 0 2 
(corriendo con 2 nodos, el archivo "dna50.txt" con score(1 mach)(-1 missmach)(0 gab) y 2 hilos))
