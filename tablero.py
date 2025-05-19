from colorama import Fore, Style, init

init(autoreset=True)

matriz = []
coordenadas_usdadas = []
num_conectados = 0
num_iniciales = 0
terminado = False

colores_neg = {
    -1: Fore.BLUE,
    -2: Fore.RED,
    -3: Fore.GREEN,
    -4: Fore.CYAN,
    -5: Fore.MAGENTA,
    -6: Fore.YELLOW,
}

colores_pos = {
    1: Fore.BLUE,
    2: Fore.RED,
    3: Fore.GREEN,
    4: Fore.CYAN,
    5: Fore.MAGENTA,
    6: Fore.YELLOW,
}


def dato_seleccionado(fila, col):
    return matriz[fila][col]

def numero_conectados():
    return num_conectados

def aumentar_conectados(fila, col):
    global num_conectados
    num_conectados += 1
    coordenadas_usdadas.append((fila, col))


def get_num_iniciales():
    return num_iniciales

def get_coordenadas_usdadas():
    return coordenadas_usdadas

def get_terminado():
    return terminado

def check_terminado():
    global terminado
    if num_conectados == num_iniciales and revisar_tablero_vacio():
        terminado = True 
    return terminado


def revisar_moviento(fila, col, dir, dato_selec):
    """
        Revisa si el movimiento en la dirección dada es válido. Si lo es, actualiza la
        matriz con el valor de la celda seleccionada y devuelve True y las nuevas
        coordenadas. Si no lo es, devuelve False y las coordenadas no cambian.

        Parámetros:
            fila (int): Fila de la celda actual
            col (int): Columna de la celda actual
            dir (str): Dirección del movimiento (w, a, s, d)
            dato_selec (int): Valor de la celda seleccionada

        Retorna:
            tuple: (bool, int, int), donde el primer elemento es un booleano que indica
            si se ha llegado al otro elemento, y los otros dos elementos son las nuevas
            coordenadas
    """
    nueva_fila, nueva_col = fila, col

    if dir == "w":
        nueva_fila -= 1
    elif dir == "s":
        nueva_fila += 1
    elif dir == "a":
        nueva_col -= 1
    elif dir == "d":
        nueva_col += 1
    else:
        print("Dirección no válida.")
        return True, fila, col

    if 0 <= nueva_fila < len(matriz) and 0 <= nueva_col < len(matriz[0]):
        if matriz[nueva_fila][nueva_col] == 0:
            matriz[nueva_fila][nueva_col] = -1 * dato_selec
            return True, nueva_fila, nueva_col
        elif matriz[nueva_fila][nueva_col] == dato_selec and (nueva_fila, nueva_col) not in coordenadas_usdadas:
            return False, nueva_fila, nueva_col

        else:
            print("Movimiento no válido.")
    else:
        print("Movimiento fuera de los límites.")

    return True, fila, col

def mostrar_matriz():
    """
        Muestra el tablero de juego actual con los índices de fila y columna.

        La función imprime la matriz del tablero de juego, donde se muestra el valor de cada celda.
        Las filas y columnas se indexan a partir de 1. Las celdas con valor 0 se muestran como 
        guiones bajos ('_'), mientras que los valores positivos se muestran con el color correspondiente y
        si es negativo se muestra un # con el color correspondiente al número negativo.
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
            elif valor > 0:
                color = colores_pos.get(valor, Fore.WHITE)
                linea += f"{color}{valor:^3}{Style.RESET_ALL}"
            else:
                #Imprime # del color de acuerdo al valor para mostrar la conexión
                color = colores_neg.get(valor, Fore.WHITE)
                linea += f"{color} # {Style.RESET_ALL}"

        print(linea)

def coordenadas():
    """
        Pide al usuario que ingrese las coordenadas de una celda en el tablero de juego.

        La función verifica que las coordenadas sean válidas y que la celda no esté vacía ni
        haya sido utilizada previamente. Si las coordenadas son válidas, devuelve la fila y la
        columna como enteros. Si no lo son, imprime un mensaje de error y vuelve a pedir las
        coordenadas.

        Retorna:
            tuple: (int, int), donde el primer elemento es la fila y el segundo es la columna
    """
    while True:
        try:
            print("Ingresa las coordenadas:")
            fila = int(input("Fila: ")) - 1
            col = int(input("Columna: ")) - 1

            if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]):
                if matriz[fila][col] != 0 and (fila, col) not in coordenadas_usdadas:
                    coordenadas_usdadas.append((fila, col))
                    return fila, col
                else:
                    print("Esta casilla no es válida.")
            else:
                print("Coordenadas fuera de rango.")
        except ValueError:
            print("Por favor ingresa números válidos.")


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
    global num_iniciales

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
                num_iniciales += 1
        num_iniciales /= 2


def revisar_tablero_vacio():
    """
        Revisa si el tablero está vacío. Si lo está, imprime un mensaje y devuelve True.
        Si no lo está, devuelve False.
    """
    global terminado
    for fila in matriz:
        for valor in fila:
            if valor == 0:
                return False
    return True
