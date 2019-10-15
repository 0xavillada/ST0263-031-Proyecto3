import sys
import time

try:
    fichero = sys.argv[1]
    match_value = int(sys.argv[2])
    mismatch_value = int(sys.argv[3])
    gap_value = int(sys.argv[4])

    cadenas = []
    base_lenght = 0
    base_index = 0
    n_cadenas = 0

    score_total = 0

except:
    print("> Usage: python alignment-serial.py <strings file> <match value> <mismatch value> <gap value>")

def main():
    #-----------------------------------------------------------read file and load matriz
    try:
        f = open(fichero)
        fl = f.readlines()
    except:
        print("> Error: could not open file", fichero)
        return 1

    index = 0

    base_lenght_temp = 0
    base_index_temp = 0
    for line in fl:
        if line[len(line)-1] == "\n":
            cadenas.append(line[:-1])
            if len(line)-1 > base_lenght_temp:
                base_lenght_temp = len(line.replace(" ", ""))-1
                base_index_temp = index
        else:
            cadenas.append(line)
            if len(line) > base_lenght_temp:
                base_lenght_temp = len(line)
                base_index = index
        index += 1
    
    n_cadenas = len(cadenas)
    base_lenght = base_lenght_temp
    base_index = base_index_temp
    print("Numero de cadenas: ",n_cadenas)
    print("Longitud de la base: ",base_lenght)
    #-----------------------------------------------------------------------------------/

    #-------------------------------------------------------------------------fill matriz
    for i in range(n_cadenas):
        cadenas[i] = cadenas[i] + "-"*(base_lenght-len(cadenas[i]))
    #------------------------------------------------------------------------------------/

    #------------------------------------------------------------------------alineamiento
    for i in range(n_cadenas):
        for j in range(base_lenght-1,1,-1):
            if i == base_index or cadenas[i][j] != "-":
                break

            ultima_letra = j
            while cadenas[i][ultima_letra] == "-":
                ultima_letra -= 1

            if cadenas[i][ultima_letra] == cadenas[base_index][j]:
                #Las siguientes 2 lineas simplemente hacen el switch de caracteres
                cadenas[i] = cadenas[i][:j]+cadenas[i][ultima_letra]+cadenas[i][j+1:]
                cadenas[i] = cadenas[i][:ultima_letra]+"-"+cadenas[i][ultima_letra+1:]

    #------------------------------------------------------------------------------------/

    #--------------------------------------------------------------calculo de score total
    score_total_temp = 0
    for j in range(base_lenght):
        score_column = 0
        for i in range(n_cadenas-1):
            for k in range(i+1, n_cadenas):
                if cadenas[k][j] == cadenas[i][j]:
                    if cadenas[k][j] == "-":
                        score_column += gap_value
                    else:
                        score_column += match_value
                else:
                    score_column += mismatch_value

        score_total_temp += score_column
    score_total = score_total_temp
    #------------------------------------------------------------------------------------/

    #---------------------------------------------------------------------salida de datos
    #print(cadenas)
    print("Numero de cadenas: ",n_cadenas)
    print("Posicion de la base: ",base_index)
    print("Longitud de la base: ",base_lenght)
    print("Score: ",score_total)
    print("Tasa: ",score_total/n_cadenas)
    f = open(fichero[:-4]+"_out.txt", "w+")
    for x in cadenas:
        f.write(x+"\n")
    #------------------------------------------------------------------------------------/

main()
