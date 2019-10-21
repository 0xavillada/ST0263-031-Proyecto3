# ST0263-031-Proyecto3
Este proyecto corresponde a la unidad numero 2 del curso Topicos especiales en telematica del programa en ingenieria de sistemas de la univeridad EAFIT.

# Variante de alineamiento múltiple para ácidos nucleicos y péptidos

## Contexto:
Un alineamiento múltiple de secuencias  es un alineamiento de tres o más secuencias biológicas, generalmente proteínas, ADN o ARN. En general, se asume que el conjunto de secuencias de consulta que se ingresa como entrada (conjunto problema) tienen una relación evolutiva por la cual comparten un linaje y descienden de un ancestro común, el alineamiento se utiliza para evaluar la conservación de los dominios proteicos, las estructuras terciarias y secundarias, e incluso aminoácidos o nucleótidos individuales.

## Problema:
Como puede ser difícil alinear a mano tres o más secuencias de longitud biológicamente relevante, y casi siempre consume mucho tiempo, se utilizan algoritmos computacionales para producir y analizar los alineamientos. El objetivo principal del alineamiento es cuantificar el grado de similitud de las cadenas superponiendo una cadena sobre la otra con la posibilidad de desplazar caracteres a la derecha o a la izquierda, sin alterar el orden de la cadena original. Para esta variante del alineamiento, se tiene una cadena de referencia para la cuál se supone en términos biológicos, es la que contiene mayor cantidad de material genético (mayor longitud) y las demás cadenas asociadas (menor longitud) serán sobre las cuales se trabajará, modificandolas de tal forma, que se puedan identificar la posible fracción de ADN faltante en esa cadena.

El cálculo del puntaje se lleva a cabo mediante la entrada, dando como penalización un valor entero “K” a cada “Mismatch” y un valor entero “L” a cada “match.

## Ejemplo:

#### Entrada:

match points= +1

mismatch points= -1

gap points= 0

ATATCCG

TCCG

ATGTACTG

ATGTCTG

#### Salida:

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
# Desarrollo:

## Modulos:
El problema se divide en 4 puntos importantes, los cuales son :
- Lectura de archivo: Leer las cadenas de adn y transferirlas a una matriz.
- Rellenado de adn incompletos: Rellenar los dna con "-" para que queden de igual tamaño a la secuencia de adn mas completa.
- Alineamiento de los dna: Alinear los adn de tal forma que quede lo mas similar al adn mas completo.
- Score: Adquirir score de la matriz formada de adn y determinar por un puntaje que el usuario determina.

## Implementacion:
Para este problema se utilizo el lenguaje python acompañada de:
- mpi4py para el uso de mpi.
- threading para el uso manual de open mp.

### Que no se paralelizo?
- Lectura de archivo: ya que la libreria que maneja python solo permite leer linea por linea, impidiendo una lectura mas agil

### Que se paralelizo?
-Relleno de adn incompletos:Adquirido la matriz, esta es fragmentada dependiendo de la cantidad de hilos que se haya determinado, añadiendo"-", a las cadenas faltantes de caracteres
- Alineamiento de los dna:Adquirido la matriz, esta es comparada caracter por caracter con la cadena "maestra"(mas completa), y adquiere una forma funcional
- Score :Adquirida la matriz y una vez fragmentada, esta se compara con la matriz madre , que viene siendo un apuntador para compararse y sacar su puntaje, es decir entonces que cada fila es comparada con sus otras filas determinadas por una columna y una vez hecho esta es sumada con sus otros hilos y finalmente sumadas por los nodos.
#### NOTA:El programa se ejecuta con 2 nodos(mpi),cada nodo adquiere la mitad de la matriz (cortada de forma horizontal),que a medida se van dando las situaciones el nodo maestro y los trabajadores van compartiendo informacion y como caracter principal .

# Correr el programa serial:
          python3 aligment-serial.py "fichero con cadenas a alinear" "valor coincidencia" "valor no coincidencia" "valor faltante"

Ejemplo: 
          $ time python alignment-serial.py dna50.txt -1 1 0
(corriendo: archivo:"dna50.txt" con score(1 mach)(-1 missmach)(0 gab) y 2 hilos))

# Correr el programa paralelo:
          mpiexec -f ./hosts_mpi -np "numero de nodos" /opt/anaconda3/bin/python ./alignment-parallel.py "fichero con cadenas a alinear" "valor coincidencia" "valor no coincidencia" "valor faltante" "numero threads"

Ejemplo:
          $ time mpiexec -f ./hosts_mpi -np 2 /opt/anaconda3/bin/python ./alignment-parallel.py dna50.txt 1 -1 0 2 
(corriendo con 2 nodos, el archivo "dna50.txt" con score(1 mach)(-1 missmach)(0 gab) y 2 hilos))

# Test
## (Test (Dna50.txt))

Test (Dna50.txt): Este test contiene 50 secuencias de dna y cada secuencia contiene de (5000mil a 11mil nucleótidos)

En este test se evidencia la gran mejora de tiempo, trar aplicar un poco de paralelismo tanto de openmp(1-32 hilos) y mpi(1-2 nodos).
viendo una mejora de hasta 2 veces, en comparativa del serial al paralelo.

![alt text](https://i.ibb.co/3Nf8mBL/Untitled.png)

Tabla #1 (Grafica Speedup y eficiencia) y datos del serial
Se determina que una de las opciones mas optimas es la utilizacion de 4 hilos,2 nodos), ya que desde este punto en adelante la mejora en el tiempo va siendo reducida,ademas de la eficiencia.

![alt text](https://i.ibb.co/kGWV6kS/Capture.png)

Tabla #2(comparativa del tiempo de la mejor speedup-eficiencia con respecto al serial )
Evidencia de que puede lograrse una velocidad 2 veces mejor aplicando MPI(2 nodos) y open mp(4 hilos) que la serial

# Sustentacion

- https://youtu.be/-VSynlhlvDQ - Andres Felipe Villada: Alineamiento

