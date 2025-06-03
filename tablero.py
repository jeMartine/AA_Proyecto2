from colorama import Fore, Style, init
import copy

init(autoreset=True)

class Tablero:
    colores_disponibles = [
        Fore.BLUE, Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW,
        Fore.LIGHTBLUE_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
        Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX,
        Fore.WHITE, Fore.LIGHTWHITE_EX
    ]

    def obtener_color(self, valor):
        if valor == 0:
            return Fore.WHITE
        index = abs(valor) - 1
        return self.colores_disponibles[index % len(self.colores_disponibles)]

    def __init__(self):
        self.matriz = []
        self.tablero_original = []
        self.coordenadas_usdadas = []
        self.num_conectados = []
        self.num_iniciales = 0
        self.terminado = False

    def dato_seleccionado(self, fila, col):
        return self.matriz[fila][col]

    def aumentar_conectados(self, dato, fila, col):
        self.num_conectados.append(dato)
        self.coordenadas_usdadas.append((fila, col))

    def esta_conectado(self, dato):
        if dato in self.num_conectados:
            return True
        return False

    def get_num_iniciales(self):
        return self.num_iniciales

    def get_coordenadas_usdadas(self):
        return self.coordenadas_usdadas

    def get_terminado(self):
        return self.terminado

    def check_terminado(self):
        #print(f"Check terminado :{self.num_conectados}, {self.num_iniciales}, {self.revisar_tablero_vacio()}")
        if len(self.num_conectados) == self.num_iniciales and self.revisar_tablero_vacio():
            self.terminado = True 
        return self.terminado

    def revisar_moviento(self, fila, col, dir, dato_selec):
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

        if 0 <= nueva_fila < len(self.matriz) and 0 <= nueva_col < len(self.matriz[0]):
            if self.matriz[nueva_fila][nueva_col] == 0:
                self.matriz[nueva_fila][nueva_col] = -1 * dato_selec
                return True, nueva_fila, nueva_col
            elif self.matriz[nueva_fila][nueva_col] == dato_selec and (nueva_fila, nueva_col) not in self.coordenadas_usdadas:
                return False, nueva_fila, nueva_col

            else:
                print("Movimiento no válido.")
        else:
            print("Movimiento fuera de los límites.")

        return True, fila, col
    
    def coordenadas(self):
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

                if (0 <= fila < len(self.matriz) and
                    0 <= col < len(self.matriz[0])):

                    if (self.matriz[fila][col] != 0 and
                       (fila, col) not in self.coordenadas_usdadas):
                        
                        self.coordenadas_usdadas.append((fila, col))
                        return fila, col
                    else:
                        print("Esta casilla no es válida.")
                else:
                    print("Coordenadas fuera de rango.")
            except ValueError:
                print("Por favor ingresa números válidos.")


    def mostrar_matriz(self):
        print("\nTablero de juego:")
        encabezado = "     "
        for j in range(len(self.matriz[0])):
            encabezado += f"{j+1:^3}"
        print(encabezado)

        for i, fila in enumerate(self.matriz):
            linea = f"{i+1:^5}"
            for valor in fila:
                if valor == 0:
                    linea += " _ "
                elif valor > 0:
                    color = self.obtener_color(valor)
                    linea += f"{color}{valor:^3}{Style.RESET_ALL}"
                else:
                    color = self.obtener_color(valor)
                    linea += f"{color} # {Style.RESET_ALL}"
            print(linea)
    def load_cero_in_matriz(self, filas, columnas):
        self.matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    def load_table(self, arch_name):
        with open(arch_name, 'r') as f:
            linea_dimensiones = f.readline().strip().replace(" ", "")
            filas = int(linea_dimensiones.split(",")[0])
            columnas = int(linea_dimensiones.split(",")[1])
            self.load_cero_in_matriz(filas, columnas)

            for line in f:
                line = line.strip().replace(" ", "")
                fila = int(line.split(",")[0]) - 1
                colu = int(line.split(",")[1]) - 1
                data = int(line.split(",")[2])
                self.matriz[fila][colu] = data
                self.num_iniciales += 1
            self.tablero_original = copy.deepcopy(self.matriz)
            self.num_iniciales /= 2

    def revisar_tablero_vacio(self):
        #print(f"matriz: {self.matriz}")
        for fila in self.matriz:
            for valor in fila:
                if valor == 0:
                    return False
        return True


    def reset_estado(self):
        self.matriz = copy.deepcopy(self.tablero_original)
        self.coordenadas_usdadas = []
        self.num_conectados = 0
        self.terminado = False