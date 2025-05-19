import sys
import tablero



def juego():
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

    while not tablero.get_terminado():
        tablero.mostrar_matriz()
        print("Juega tu turno.")

        fila, col = tablero.coordenadas()
        dato_selec= tablero.dato_seleccionado(fila, col)
        estado = True

        while estado:
            tablero.mostrar_matriz()
            print("Mover con: a (izq), w (arriba), s (abajo), d (der)")
            
            mov = input(": ").lower()
            estado, fila, col= tablero.revisar_moviento(fila, col, mov, dato_selec)

            if estado!= True:
                print(f"Se han conectado las casillas de {dato_selec}")
                tablero.aumentar_conectados(fila, col)
                
                if tablero.check_terminado():
                    print("¡Has ganado!")


if __name__ == '__main__':

    entrada = sys.argv
    if len(entrada) == 0:
        print("Recuerde: python interfaz.py <archivo de entrada>")
    else:
        tablero.load_table(entrada[1])
        juego()
    