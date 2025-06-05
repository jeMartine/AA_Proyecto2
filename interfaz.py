import sys
from Tablero import *
import heapq
from collections import deque, OrderedDict
import copy
from itertools import permutations
import time



# Direcciones y movimientos
MOVIMIENTOS = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
}

DIR_INVERSA = {
    (-1, 0): 'w',
    (1, 0): 's',
    (0, -1): 'a',
    (0, 1): 'd',
}

def heuristica(a, b):
    # Distancia de Manhattan
    #print(f"Heuristica usada a: {a}, b:{b} = {abs(a[0] - b[0]) + abs(a[1] - b[1])}")
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def encontrar_pares(tablero):
    #Encuentra las posiciones en la matriz de los valores que deben ser conectados
    posiciones = {}
    for i, fila in enumerate(tablero.matriz):
        for j, val in enumerate(fila):
            if val > 0:
                if val not in posiciones:
                    posiciones[val] = []
                posiciones[val].append((i, j))

    return permutaciones(posiciones)

def permutaciones(diccionario):
    pares = [(k, diccionario[k]) for k in diccionario]
    return list(permutations(pares))


def revisar_salidas(dat, tablero, coord):
    f, c = coord
    fila = len(tablero)
    colu = len(tablero[0])
    bloqueados = []
    libre =0
    bloquedos_aux=[]

    for df, dc in MOVIMIENTOS.values():
        nf, nc = f + df, c + dc

        if (0 <= nf < fila and 0 <= nc < colu):# revisar limites
            dato_revisar = tablero[nf][nc]
            if dato_revisar == 0:
                libre += 1
            if dato_revisar < 0 and dato_revisar != -dat:  # solo bloquea si es otro dato
                bloquedos_aux.append((abs(dato_revisar), (nf, nc)))

    bloqueados.append((bloquedos_aux, libre))
    return bloqueados


def astar(tablero_original, dato, bloqueados,  inicio, fin):
    heap = [] #lista abierta donde almaceno nuevos nodos                   
    heapq.heappush(heap, (0 + heuristica(inicio, fin), 0, inicio, [])) # f, g , nodo_inicial, lista de movimientos
    visitados = set() #Lista con las posiciones visitadas (reconstruye el camino final)

    while heap:
        f, g, actual, camino = heapq.heappop(heap)
        #Punto (f, c) actual que estoy revisando
        if actual in visitados:
            continue
        visitados.add(actual)

        #El nodo que estoy revisando, es el nodo objetivo
        if actual == fin:
            return camino  #los movimientos necesarios para llegar del nodo inicial al final

        
        #revisar vecinos
        for delta in MOVIMIENTOS.values():
            
            nueva_pos = (actual[0] + delta[0], actual[1] + delta[1])

            #Dentro de los límites del tablero, no lo haya visitado y no esté bloqueado
            if (0 <= nueva_pos[0] < len(tablero_original) and
                0 <= nueva_pos[1] < len(tablero_original[0]) and
                nueva_pos not in visitados and
                ((dato,nueva_pos)) not in bloqueados):

                celda = tablero_original[nueva_pos[0]][nueva_pos[1]]
                #Revisar que esté libre la nueva posición o que sea la posición objetivo
                if celda == 0 or nueva_pos == fin:
                    #Actualizar costos
                    nuevo_g = g + 1#Costo de 1 paso al pasar a la nueva posición
                    nuevo_f = nuevo_g + heuristica(nueva_pos, fin) #nuevo valor del nodo en el que me paro
                    heapq.heappush(heap, (nuevo_f, nuevo_g, nueva_pos, camino + [delta]))


            
    return None  # No se encontró camino

#Revisar que en cada iteración, al menos cada número que deba ser conectado esté libre a su al rededor

def salidas_pares(bloqueados, copia, pares):
    for dat, (inicio, fin) in copy.deepcopy(pares):
        for punto in [inicio, fin]:
            bloqueos = revisar_salidas(dat, copia.matriz, punto)

            tupla_bloqueo = bloquear_menor_heuristica(fin, bloqueos)

            if tupla_bloqueo is not None and not copia.esta_conectado(dat):
                desespero = revisar_movimiento_desde_bloqueo(copia.matriz, tupla_bloqueo[1])
                if desespero is not None:
                    bloqueados.append(desespero)
                bloqueados.append(tupla_bloqueo)
                return True
    return False

def revisar_movimiento_desde_bloqueo(tablero, bloqueado):
    f,c = bloqueado
    fila = len(tablero)
    colu = len(tablero[0])
    aux = []
    salidas =0
    for df, dc in MOVIMIENTOS.values():
        nf, nc = f + df, c + dc
        if (0 <= nf < fila and 0 <= nc < colu and ((nf, nc)) is not bloqueado):# revisar limites
            dato_revisar = tablero[nf][nc]
            if dato_revisar == 0:
                salidas +=1

            if dato_revisar < 0:
                aux.append((abs(dato_revisar),((nf,nc))))
                print(f"Siguiente bloqueado dato {dato_revisar} por camino {((nf,nc))}")

    if salidas == 0:
        return aux[0]

    return None

def bloquear_menor_heuristica(fin, bloqueos):
    for bloqueos_aux, libre in bloqueos:
        if libre == 0:
            menor = None
            min_heur = float('inf')

            for dato, punto in bloqueos_aux:
                #bloquear la menor heuristica
                h = heuristica(fin, punto)

                if h<min_heur:
                    min_heur = h
                    menor = (dato, punto)
            return menor
        
    return None


def jugar_sintetico(arch_name):
    tablero_original = Tablero()
    tablero_original.load_table(arch_name)

    inicio = time.time()
    tablero_original=jugar(tablero_original)
    fin = time.time()

    print(f"Tiempo de ejecución: {fin - inicio:.7f} segundos")
    

    if tablero_original is not None:
        tablero_original.mostrar_matriz()
        print("El jugador sintético ha encontrado una solución")

    else:
        print("No se encontró una solución válida.")

def jugar(tablero_original):

    todas_permutaciones = encontrar_pares(tablero_original)

    for perm_index, perm in enumerate(todas_permutaciones):
        pares = list(perm)  # Convertir la permutación a una lista de pares
        tablero_temp = copy.deepcopy(tablero_original)
        bloqueados = []
        i = 0

        while i < len(pares):
            dato = pares[i][0]
            inicio, fin = pares[i][1]
            copia = copy.deepcopy(tablero_temp.matriz)

            camino = astar(copia, dato, bloqueados, inicio, fin)

            print(f"Calculando camino con {dato}")

            if not camino:
                print(f"No se encontró camino para {dato}")
                break  # Esta permutación falla, pasamos a la siguiente

            fila, col = inicio
            tablero_temp.coordenadas_usdadas.append(inicio)

            for mov in camino:
                direccion = DIR_INVERSA[mov]
                _, fila, col = tablero_temp.revisar_moviento(fila, col, direccion, dato)

            tablero_temp.mostrar_matriz()
            print(f"Se han conectado las casillas de {dato}")
            tablero_temp.aumentar_conectados(dato, fin[0], fin[1])
            i += 1

            if salidas_pares(bloqueados, tablero_temp, pares):
                tablero_temp = copy.deepcopy(tablero_original)
                i = 0

        if tablero_temp.check_terminado():
            return  tablero_temp

    return None



def juego(arch_name):
    """
        Controla el flujo del juego principal. Muestra el tablero, recibe las 
        coordenadas del jugador y permite el movimiento de las piezas en el 
        tablero. El juego continúa hasta que todas las piezas estén conectadas 
        correctamente.

        Durante el turno del jugador, el tablero se muestra y el jugador ingresa 
        una dirección para mover una pieza seleccionada. Si las piezas se conectan 
        correctamente, el juego termina con un mensaje de victoria.

        Utiliza las funciones:
        - mostrar_matriz(): para mostrar el estado actual del tablero.
        - coordenadas(): para obtener las coordenadas de la celda seleccionada.
        - revisar_moviento(): para verificar y realizar movimientos en el tablero.
    """
    tablero_manual = Tablero()
    tablero_manual.load_table(arch_name)
    while not tablero_manual.get_terminado():
        tablero_manual.mostrar_matriz()
        print("Juega tu turno.")

        fila, col = tablero_manual.coordenadas()
        dato_selec= tablero_manual.dato_seleccionado(fila, col)
        estado = True

        while estado:
            tablero_manual.mostrar_matriz()
            print("Mover con: a (izq), w (arriba), s (abajo), d (der)")
            
            mov = input(": ").lower()
            estado, fila, col= tablero_manual.revisar_moviento(fila, col, mov, dato_selec)

            if estado!= True:
                print(f"Se han conectado las casillas de {dato_selec}")
                tablero_manual.aumentar_conectados(dato_selec,fila, col)
                
                if tablero_manual.check_terminado():
                    print("¡Has ganado!")


if __name__ == '__main__':

    entrada = sys.argv
    if len(entrada) == 0:
        print("Recuerde: python interfaz.py <archivo de entrada>")
    else:
        if len(entrada)>2 and entrada[2]=="auto":
            jugar_sintetico(entrada[1])
        else:
            juego(entrada[1])
