import sys

matriz = []


def load_cero_in_matriz(filas, columnas):
    """
        Crea una matriz de ceros con el tamaño indicado por parámetros.
        La matriz se almacena en la variable global 'matriz'.
    """
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(0)
        matriz.append(fila)

def load_table(arch_name):
    """
        El formato del archivo es el siguiente: la primera línea contiene el número de filas y columnas, 
        separadas por una coma. El resto de las líneas contienen la fila, la columna y el valor de cada 
        celda del tablero, separados por comas. Los índices de fila y columna se basan en 1.

        Por ejemplo, un archivo con el siguiente texto crearía un tablero de 3x3 con los valores 1 en la 
        posición (1,1), 2 en la posición (2,2) y 3 en la posición (3,3):
        3,3
        1,1,1
        2,2,2
        3,3,3
    """
    
    with open(arch_name, 'r') as f:
        linea_dimensiones = f.readline().strip().replace(" ", "")
        filas = int(linea_dimensiones.split(",")[0])
        columnas = int(linea_dimensiones.split(",")[1])

        #Inicializar la matrz con ceros 
        load_cero_in_matriz(filas, columnas)

        for line in f:
                line = line.strip().replace(" ", "")
                fila = int(line.split(",")[0])-1
                colu = int(line.split(",")[1])-1
                data = int(line.split(",")[2])

                matriz[fila][colu] = data
                #print(fila, colu, data)

def mostrar_matriz():
    """
        Muestra el tablero de juego actual con los índices de fila y columna.

        La función imprime la matriz del tablero de juego, donde se muestra el valor de cada celda.
        Las filas y columnas se indexan a partir de 1. Las celdas con valor 0 se muestran como 
        guiones bajos ('_'), mientras que los demás valores se muestran tal cual.
    """

    print("\nTablero de juego:")

    # Encabezado de columnas
    encabezado = "     "  # Espacio para el índice de filas
    for j in range(len(matriz[0])):
        encabezado += f"{j+1:^3}"
    print(encabezado)

    # Contenido de la matriz con índice de fila
    for i, fila in enumerate(matriz):
        linea = f"{i+1:^5}"  # Índice de fila centrado
        for valor in fila:
            if valor == 0:
                linea += " _ "
            else:
                linea += f"{valor:^3}"
        print(linea)

def coordenadas():
    valido = True
    while valido:
        print("Ingresa las coordenadas:")
        fila = int(input("Fila: ")) - 1
        column = int(input("Columna: ")) - 1

        if matriz[fila][column] == 0:
            print("Esta casilla no es válida.")
            valido = True
        else:
            valido = False

    return fila, column

def revisar_moviento(fila, col, dir):
    if dir == "w":
        if matriz[fila+1][col] == 0:
            return True
    if dir == "s":
        if matriz[fila-1][col] == 0:
            return True
    if dir == "a":
        if matriz[fila][col-1] == 0:
            return True
    if dir == "d":
        if matriz[fila][col+1] == 0:
            return True
    return False

def juego():
    estado_juego = True
    while estado_juego:
        mostrar_matriz()
        print("Juega tu turno.")

        print(coordenadas())

if __name__ == '__main__':

    entrada = sys.argv
    if len(entrada) == 0:
        print("Recuerde: python interfaz.py <archivo de entrada>")
    else:
        load_table(entrada[1])
        juego()
    