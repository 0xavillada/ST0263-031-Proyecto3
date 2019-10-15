import sys
from mpi4py import MPI
import threading
import time

class Aligner:
    def __init__(self):
        try:
            self.fichero = sys.argv[1]
            self.match_value = int(sys.argv[2])
            self.mismatch_value = int(sys.argv[3])
            self.gap_value = int(sys.argv[4])

            self.n_threads = int(sys.argv[5])

        except:
            raise ValueError("> Usage: python alignment-serial.py <strings file> <match value> <mismatch value> <gap value> <number of threads>")
        self.cadenas = []
        self.base_lenght = 0
        self.base_index = 0
        self.n_cadenas = 0
        self.cont=0
        
        self.score_total = 0

        try:
            f = open(self.fichero)
            fl = f.readlines()
        except:
            raise ValueError("> Error: could not open file", self.fichero)

        index = 0
        is_windows=0
        for line in fl:
            if line[len(line)-1] == "\n":
                self.cadenas.append(line[:-1-is_windows])
                if len(line)-1 > self.base_lenght:
                    self.base_lenght = len(line)-1-is_windows
                    self.base_index = index
            else:
                self.cadenas.append(line)
                if len(line) > self.base_lenght:
                    self.base_lenght = len(line)-is_windows
                    self.base_index = index
            index += 1
        self.n_cadenas = len(self.cadenas)
        self.base_lenght_segment = int(self.base_lenght / self.n_threads)
        self.n_cadenas_segment = int(self.n_cadenas / self.n_threads)


    def threading_segments(self, inicio, fin, target_thread, segment):
        if segment == 0:
           segment = 1
        inicio_thread = inicio
        for hilo in range(self.n_threads):
            if (inicio_thread + segment) > fin or ((inicio_thread + segment)+segment) > fin:
                if target_thread == 1:
                    t = threading.Thread(target=self.fill_matriz_thread, args=(inicio_thread, fin))
                    t.start()
                elif target_thread == 2:
                    t = threading.Thread(target=self.align_thread, args=(inicio_thread, fin))
                    t.start()
                else:
                    t = threading.Thread(target=self.calc_score_thread, args=(inicio_thread, fin))
                    t.start()
                break
            else:

                if target_thread == 1:
                    t = threading.Thread(target=self.fill_matriz_thread, args=(inicio_thread, (inicio_thread + segment)))
                    t.start()
                elif target_thread == 2:
                    t = threading.Thread(target=self.align_thread, args=(inicio_thread, (inicio_thread + segment)))
                    t.start()
                else:
                    t = threading.Thread(target=self.calc_score_thread, args=(inicio_thread, (inicio_thread + segment)))
                    t.start()
            inicio_thread += segment

    def fill_matriz_thread(self, inicio, fin):
        for i in range(inicio,fin):
            self.cadenas[i] = self.cadenas[i] + "-"*(self.base_lenght-len(self.cadenas[i]))

    def align_thread(self, inicio, fin):
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

    def calc_score_thread(self, inicio, fin):
        score_temp=0
        for j in range(inicio,fin):
            score_column = 0
            for i in range(self.n_cadenas-1):                
                for k in range(i+1, self.n_cadenas):
                    if self.cadenas[k][j] == self.cadenas[i][j]:
                        if self.cadenas[k][j] == "-":
                            score_column += self.gap_value
                            self.cont+=1
                        else:
                            score_column += self.match_value
                            self.cont+=1
                    else:
                        score_column += self.mismatch_value
                        self.cont+=1
                
            score_temp += score_column
        self.score_total += score_temp
        print(self.score_total)


        
    def show(self):
        #print(self.cadenas)
        f = open(self.fichero[:-4]+"_out.txt","w+")
        for x in self.cadenas:
            f.write(x+"\n")

        print("Numero de cadenas: ",self.n_cadenas)
        print("Posicion de la base: ",self.base_index)
        print("Longitud de la base: ",self.base_lenght)
        print("Score: ",self.score_total)
        print("Tasa: ",self.score_total/self.n_cadenas)
        f = open(self.fichero[:-4]+"_out_parallel.txt", "w+")
        for x in self.cadenas:
            f.write(x+"\n")

        
error = False
try:
    aligner = Aligner()
except ValueError:
    error_type, error_instance, traceback = sys.exc_info()
    print(error_instance)
    error = True

if error == False:
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    name = MPI.Get_processor_name()
    n_cadenas_medium = int((aligner.n_cadenas / 2) - ((aligner.n_cadenas / 2) % 1))
    base_lenght_medium = int((aligner.base_lenght /2) - ((aligner.base_lenght / 2) % 1))

    #-------------------------------------------------------------------------fill matriz
    if rank == 0:
        #aligner.fill_matriz(0,n_cadenas_medium)
        
        aligner.threading_segments(0, n_cadenas_medium, 1, aligner.base_lenght_segment)
        
        otherRank_cadenas = comm.recv(source=1)
        aligner.cadenas = aligner.cadenas[:n_cadenas_medium] + otherRank_cadenas
        comm.send(aligner.cadenas, dest=1)

    if rank == 1:
        #aligner.fill_matriz(n_cadenas_medium,aligner.n_cadenas)
        
        aligner.threading_segments(n_cadenas_medium, aligner.n_cadenas, 1, aligner.base_lenght_segment)

        comm.send(aligner.cadenas[n_cadenas_medium:], dest=0)
        aligner.cadenas = comm.recv(source=0)

    #------------------------------------------------------------------------------------/

    #------------------------------------------------------------------------alineamiento
    if rank == 0:
        #aligner.align(0,n_cadenas_medium)

        aligner.threading_segments(0, n_cadenas_medium, 2, aligner.base_lenght_segment)

        otherRank_cadenas = comm.recv(source=1)
        aligner.cadenas = aligner.cadenas[:n_cadenas_medium] + otherRank_cadenas
        comm.send(aligner.cadenas, dest=1)

    if rank == 1:
        #aligner.align(n_cadenas_medium,aligner.n_cadenas)

        aligner.threading_segments(n_cadenas_medium, aligner.n_cadenas, 2, aligner.base_lenght_segment)

        comm.send(aligner.cadenas[n_cadenas_medium:], dest=0)
        aligner.cadenas = comm.recv(source=0)

    #------------------------------------------------------------------------------------/

    #--------------------------------------------------------------calculo de score total
    if rank == 0:
        #aligner.calc_score(0,base_lenght_medium)

        aligner.threading_segments(0, base_lenght_medium, 3, aligner.base_lenght_segment)
        otherRank_score = comm.recv(source=1)
        print(otherRank_score)
        aligner.score_total += otherRank_score
    #---------------------------------------------------------------------salida de datos
        time.sleep(0.5)
        aligner.show()
        comm.Abort()
    #------------------------------------------------------------------------------------/


    if rank == 1:
        #aligner.calc_score(base_lenght_medium,aligner.base_lenght)

        aligner.threading_segments(base_lenght_medium, aligner.base_lenght, 3, aligner.base_lenght_segment)
        print(aligner.score_total)
        comm.send(aligner.score_total, dest=0)
    #------------------------------------------------------------------------------------/
    
