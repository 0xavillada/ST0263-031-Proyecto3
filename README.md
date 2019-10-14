# ST0263-031-Proyecto3
Este proyecto corresponde a la unidad numero 2 del curso Topicos especiales en telematica del programa en ingenieria de sistemas de la univeridad EAFIT.

# Correr el programa serial:
python3 aligment-serial.py <fichero con cadenas a alinear> <valor coincidencia> <valor no coincidencia> <valor faltante>

# Correr el programa paralelo:
mpiexec -f ./hosts_mpi -np "<numero de nodos>" /opt/anaconda3/bin/python ./alignment-parallel.py "<fichero con cadenas a alinear>" "<valor coincidencia>" "<valor no coincidencia>" "<valor faltante> <numero threads>"
