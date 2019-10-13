import sys
from mpi4py import MPI

class Aligner:
    def __init__(self):
        try:
            self.fichero = sys.argv[1]
            self.match_value = int(sys.argv[2])
            self.mismatch_value = int(sys.argv[3])
            self.gap_value = int(sys.argv[4])

            self.n_threads = int(sys.argv[5])

        except:
            raise ValueError("> Usage: python alignment-serial.py <strings file> <match value> <mismatch value> <gap value>")

        self.cadenas = []
        self.base_lenght = 0
        self.base_index = 0
        self.n_cadenas = 0

        self.score_total = 0

        try:
            f = open(self.fichero)
            fl = f.readlines()
        except:
            raise ValueError("> Error: could not open file", self.fichero)

        index = 0

        for line in fl:
            if line[len(line)-1] == "\n":
                self.cadenas.append(line[:-1])
                if len(line)-1 > self.base_lenght:
                    self.base_lenght = len(line)-1
                    self.base_index = index
            else:
                self.cadenas.append(line)
                if len(line) > self.base_lenght:
                    self.base_lenght = len(line)
                    self.base_index = index
            index += 1
        self.n_cadenas = len(self.cadenas)

    def fill_matriz(self, inicio, fin):
        for i in range(inicio,fin):
            self.cadenas[i] = self.cadenas[i] + "-"*(self.base_lenght-len(self.cadenas[i]))

    def align(self, inicio, fin):
        for i in range(inicio,fin):
            for j in range(self.base_lenght-1,1,-1):
                if i == self.base_index or self.cadenas[i][j] != "-":
                    break

                ultima_letra = j
                while self.cadenas[i][ultima_letra] == "-":
                    ultima_letra -= 1

                if self.cadenas[i][ultima_letra] == self.cadenas[self.base_index][j]:
                    #Las siguientes 2 lineas simplemente hacen el switch de caracteres
                    self.cadenas[i] = self.cadenas[i][:j]+self.cadenas[i][ultima_letra]+self.cadenas[i][j+1:]
                    self.cadenas[i] = self.cadenas[i][:ultima_letra]+"-"+self.cadenas[i][ultima_letra+1:]

    def calc_score(self, inicio, fin):
        for j in range(inicio,fin):
            score_column = 0
            for i in range(self.n_cadenas-1):
                for k in range(i+1, self.n_cadenas):
                    if self.cadenas[k][j] == self.cadenas[i][j]:
                        if self.cadenas[k][j] == "-":
                            score_column += self.gap_value
                        else:
                            score_column += self.match_value
                    else:
                        score_column += self.mismatch_value

            self.score_total += score_column

    def show(self):
        print(self.cadenas)
        print("Numero de cadenas: ",self.n_cadenas)
        print("Posicion de la base: ",self.base_index)
        print("Longitud de la base: ",self.base_lenght)
        print("Score: ",self.score_total)
        print("Tasa: ",self.score_total/self.n_cadenas)

error = False
try:
    aligner = Aligner()
except ValueError:
    error_type, error_instance, traceback = sys.exc_info()
    print(error_instance)
    error = True

if error == False:
    
    comm = MPI.COMM_WORLD
    rank = comm.rank
    name = MPI.Get_processor_name()
    print(name)
    print(rank)
    n_cadenas_medium = int((aligner.n_cadenas / 2) - ((aligner.n_cadenas / 2) % 1))
    print(n_cadenas_medium)
    base_lenght_medium = int((aligner.base_lenght /2) - ((aligner.base_lenght / 2) % 1))

    #-------------------------------------------------------------------------fill matriz
    if rank == 0:
        aligner.fill_matriz(0,n_cadenas_medium)
        otherRank_cadenas = comm.recv(source=1)
        aligner.cadenas = aligner.cadenas[:n_cadenas_medium] + otherRank_cadenas
        comm.send(aligner.cadenas, dest=1)

    if rank == 1:
        aligner.fill_matriz(n_cadenas_medium,aligner.n_cadenas)
        comm.send(aligner.cadenas[n_cadenas_medium:], dest=0)
        aligner.cadenas = comm.recv(source=0)

    #------------------------------------------------------------------------------------/

    #------------------------------------------------------------------------alineamiento
    if rank == 0:
        aligner.align(0,n_cadenas_medium)
        otherRank_cadenas = comm.recv(source=1)
        aligner.cadenas = aligner.cadenas[:n_cadenas_medium] + otherRank_cadenas
        comm.send(aligner.cadenas, dest=1)

    if rank == 1:
        aligner.align(n_cadenas_medium,aligner.n_cadenas)
        comm.send(aligner.cadenas[n_cadenas_medium:], dest=0)
        aligner.cadenas = comm.recv(source=0)

    #------------------------------------------------------------------------------------/

    #--------------------------------------------------------------calculo de score total

    if rank == 0:
        aligner.calc_score(0,base_lenght_medium)
        otherRank_score = comm.recv(source=1)
        aligner.score_total += otherRank_score
    #---------------------------------------------------------------------salida de datos
        aligner.show()
    #------------------------------------------------------------------------------------/

    if rank == 1:
        aligner.calc_score(base_lenght_medium,aligner.base_lenght)
        comm.send(aligner.score_total, dest=0)

    #------------------------------------------------------------------------------------/
