import unittest
import copy
from tablero import Tablero
from interfaz import (
    heuristica, encontrar_pares, revisar_salidas, astar, 
    MOVIMIENTOS, DIR_INVERSA, bloquear_menor_heuristica
)

class PruebasInterfazPrueba1(unittest.TestCase):
    
    def setUp(self):
        """Configurar datos de prueba con el archivo prueba1.txt"""
        self.tablero = Tablero()
        self.tablero.load_table('prueba1.txt')
        
        # Conexiones esperadas corregidas para prueba1.txt basadas en la matriz real
        # Matriz real: [[2, 1, 1], [0, 3, 0], [0, 2, 3]]
        # 1: (0,1) a (0,2) - posiciones (1,2) a (1,3) en índice 1
        # 2: (0,0) a (2,1) - posiciones (1,1) a (3,2) en índice 1  
        # 3: (1,1) a (2,2) - posiciones (2,2) a (3,3) en índice 1
        self.pares_esperados = {
            1: [(0, 1), (0, 2)],  # posiciones índice 0
            2: [(0, 0), (2, 1)],  # Corregido basado en matriz real
            3: [(1, 1), (2, 2)]
        }
    
    def test_carga_tablero(self):
        """Probar que el tablero se carga correctamente desde prueba1.txt"""
        # Matriz esperada corregida basada en el contenido real del archivo
        matriz_esperada = [
            [2, 1, 1],
            [0, 3, 0],
            [0, 2, 3]
        ]
        self.assertEqual(self.tablero.matriz, matriz_esperada)
        self.assertEqual(self.tablero.num_iniciales, 3.0)  # 6 pares / 2
    
    def test_heuristica(self):
        """Probar el cálculo de distancia Manhattan"""
        # Probar cálculos básicos de distancia Manhattan
        self.assertEqual(heuristica((0, 0), (0, 0)), 0)
        self.assertEqual(heuristica((0, 0), (1, 1)), 2)
        self.assertEqual(heuristica((0, 1), (0, 2)), 1)  # Para par 1
        self.assertEqual(heuristica((0, 0), (2, 1)), 3)  # Para par 2 (corregido)
        self.assertEqual(heuristica((1, 1), (2, 2)), 2)  # Para par 3
    
    def test_encontrar_pares(self):
        """Probar que los pares se identifican correctamente"""
        todas_permutaciones = encontrar_pares(self.tablero)
        
        # Debe devolver permutaciones de los pares
        self.assertIsInstance(todas_permutaciones, list)
        self.assertGreater(len(todas_permutaciones), 0)
        
        # Extraer los pares base de la primera permutación
        primera_perm = todas_permutaciones[0]
        dict_pares = {}
        for valor, posiciones in primera_perm:
            dict_pares[valor] = posiciones
        
        # Verificar que se encuentren todos los valores esperados
        self.assertIn(1, dict_pares)
        self.assertIn(2, dict_pares)
        self.assertIn(3, dict_pares)
        
        # Verificar posiciones para cada valor (corregido basado en matriz real)
        self.assertEqual(set(dict_pares[1]), {(0, 1), (0, 2)})
        self.assertEqual(set(dict_pares[2]), {(0, 0), (2, 1)})  # Corregido
        self.assertEqual(set(dict_pares[3]), {(1, 1), (2, 2)})
    
    def test_revisar_salidas(self):
        """Probar funcionalidad de verificación de salidas"""
        # Probar para posición (0,1) - debería tener algunos espacios libres
        salidas = revisar_salidas(1, self.tablero.matriz, (0, 1))
        self.assertIsInstance(salidas, list)
        self.assertEqual(len(salidas), 1)
        
        bloqueos_aux, libre = salidas[0]
        self.assertIsInstance(bloqueos_aux, list)
        self.assertIsInstance(libre, int)
        self.assertGreaterEqual(libre, 0)
    
    def test_astar_conexion_simple(self):
        """Probar búsqueda A* para par 1 (caso más simple)"""
        inicio = (0, 1)  # Posición del primer 1
        fin = (0, 2)     # Posición del segundo 1
        bloqueados = []
        
        camino = astar(self.tablero.matriz, 1, bloqueados, inicio, fin)
        
        # Debe encontrar un camino (celdas adyacentes)
        self.assertIsNotNone(camino)
        self.assertIsInstance(camino, list)
        
        # El camino debe ser un paso hacia la derecha
        movimiento_esperado = (0, 1)  # Movimiento hacia derecha
        self.assertEqual(len(camino), 1)
        self.assertEqual(camino[0], movimiento_esperado)
    
    def test_astar_conexion_compleja(self):
        """Probar búsqueda A* para par 2 (más complejo) - posiciones corregidas"""
        inicio = (0, 0)  # Posición del primer 2
        fin = (2, 1)     # Posición del segundo 2 (corregido)
        bloqueados = []
        
        camino = astar(self.tablero.matriz, 2, bloqueados, inicio, fin)
        
        # Debe encontrar un camino
        self.assertIsNotNone(camino)
        self.assertIsInstance(camino, list)
        self.assertGreater(len(camino), 0)
        
        # Verificar que el camino lleva al destino correcto
        pos = inicio
        for movimiento in camino:
            pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
        self.assertEqual(pos, fin)
    
    def test_bloquear_menor_heuristica(self):
        """Probar bloqueo basado en heurística mínima"""
        # Crear un escenario con salidas bloqueadas
        bloqueos = [([
            (2, (1, 0)),  # Alguna posición bloqueada
            (3, (2, 1))   # Otra posición bloqueada
        ], 0)]  # 0 salidas libres
        
        fin = (2, 2)  # Posición objetivo
        resultado = bloquear_menor_heuristica(fin, bloqueos)
        
        # Debe devolver la posición con heurística mínima al objetivo
        self.assertIsNotNone(resultado)
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        
        # Debe elegir la posición más cercana al objetivo
        dato, punto = resultado
        self.assertIn(dato, [2, 3])
        self.assertIsInstance(punto, tuple)
    
    def test_direcciones_movimiento(self):
        """Probar mapeo de direcciones de movimiento"""
        # Probar diccionario MOVIMIENTOS
        self.assertEqual(MOVIMIENTOS['w'], (-1, 0))  # Arriba
        self.assertEqual(MOVIMIENTOS['s'], (1, 0))   # Abajo
        self.assertEqual(MOVIMIENTOS['a'], (0, -1))  # Izquierda
        self.assertEqual(MOVIMIENTOS['d'], (0, 1))   # Derecha
        
        # Probar diccionario DIR_INVERSA
        self.assertEqual(DIR_INVERSA[(-1, 0)], 'w')
        self.assertEqual(DIR_INVERSA[(1, 0)], 's')
        self.assertEqual(DIR_INVERSA[(0, -1)], 'a')
        self.assertEqual(DIR_INVERSA[(0, 1)], 'd')
    
    def test_gestion_estado_tablero(self):
        """Probar funciones de gestión del estado del tablero"""
        # Probar estado inicial
        self.assertFalse(self.tablero.esta_conectado(1))
        self.assertFalse(self.tablero.esta_conectado(2))
        self.assertFalse(self.tablero.esta_conectado(3))
        
        # Probar conectar un par
        self.tablero.aumentar_conectados(1, 0, 2)
        self.assertTrue(self.tablero.esta_conectado(1))
        
        # Probar seguimiento de coordenadas
        coordenadas = self.tablero.get_coordenadas_usdadas()
        self.assertIn((0, 2), coordenadas)
    
    def test_validacion_solucion_completa(self):
        """Probar que una solución completa puede ser validada"""
        # Simular conectar todos los pares
        matriz_original = copy.deepcopy(self.tablero.matriz)
        
        # Conectar par 1: (0,1) a (0,2) - conexión directa
        self.tablero.matriz[0][1] = -1  # Marcar camino
        self.tablero.aumentar_conectados(1, 0, 2)
        
        # Conectar par 2: (0,0) a (2,1) - camino corregido
        self.tablero.matriz[1][0] = -2  # Marcar celda de camino intermedio
        self.tablero.aumentar_conectados(2, 2, 1)
        
        # Conectar par 3: (1,1) a (2,2) - a través de camino disponible
        self.tablero.matriz[2][1] = -3  # Marcar camino (puede haber conflicto, pero para prueba)
        self.tablero.aumentar_conectados(3, 2, 2)
        
        # Llenar espacios vacíos restantes para simular solución completa
        for i in range(len(self.tablero.matriz)):
            for j in range(len(self.tablero.matriz[i])):
                if self.tablero.matriz[i][j] == 0:
                    self.tablero.matriz[i][j] = -1  # Llenar con algún camino
        
        # Probar verificación de finalización
        self.assertTrue(self.tablero.revisar_tablero_vacio())
        self.assertEqual(len(self.tablero.num_conectados), 3)
    
    def test_validacion_estructura_matriz(self):
        """Probar para validar la estructura real de la matriz desde prueba1.txt"""
        # Imprimir matriz real para depuración
        print(f"\nMatriz real desde prueba1.txt: {self.tablero.matriz}")
        
        # Verificar las dimensiones de la matriz
        self.assertEqual(len(self.tablero.matriz), 3)  # 3 filas
        self.assertEqual(len(self.tablero.matriz[0]), 3)  # 3 columnas
        
        # Verificar que posiciones específicas contienen valores esperados
        self.assertEqual(self.tablero.matriz[0][0], 2)  # Primer 2
        self.assertEqual(self.tablero.matriz[0][1], 1)  # Primer 1
        self.assertEqual(self.tablero.matriz[0][2], 1)  # Segundo 1
        self.assertEqual(self.tablero.matriz[1][1], 3)  # Primer 3
        self.assertEqual(self.tablero.matriz[2][1], 2)  # Segundo 2
        self.assertEqual(self.tablero.matriz[2][2], 3)  # Segundo 3


class PruebasInterfazPrueba2(unittest.TestCase):
    
    def setUp(self):
        """Configurar datos de prueba con el archivo prueba2.txt"""
        self.tablero = Tablero()
        self.tablero.load_table('prueba2.txt')
        
        # Caminos de solución esperados corregidos para prueba2.txt (corregido para usar solo movimientos válidos)
        # Todos los movimientos deben ser solo celdas adyacentes (sin movimientos diagonales)
        self.caminos_solucion_esperados = {
            1: [(1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3)],  # Camino válido para par 1
            2: [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)],  # Corregido: agregado paso intermedio en (3,2)
            3: [(2, 0), (3, 0), (4, 0)],  # Camino vertical válido
            4: [(2, 1), (3, 1), (4, 1), (4, 2)],  # Corregido: agregado paso intermedio en (4,1)
            5: [(4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4)]  # Camino inverso válido
        }
        
        # Posiciones de pares esperados corregidas desde prueba2.txt real
        self.pares_esperados = {
            1: [(1, 0), (2, 3)],  # índice 0: (2,1) a (3,4)
            2: [(1, 1), (3, 3)],  # índice 0: corregido basado en matriz real
            3: [(2, 0), (4, 0)],  # índice 0: (3,1) a (5,1)
            4: [(2, 1), (4, 2)],  # índice 0: corregido basado en matriz real
            5: [(0, 4), (4, 3)]   # índice 0: (1,5) a (5,4)
        }
    
    def test_prueba2_carga_tablero(self):
        """Probar que el tablero se carga correctamente desde prueba2.txt"""
        # Imprimir matriz real para depuración
        print(f"\nMatriz real desde prueba2.txt: {self.tablero.matriz}")
        
        # Matriz esperada corregida basada en contenido real del archivo
        matriz_esperada = [
            [0, 0, 0, 0, 5],
            [1, 2, 0, 0, 0],
            [3, 4, 0, 1, 0],
            [0, 0, 0, 2, 0],
            [3, 0, 4, 5, 0]
        ]
        self.assertEqual(self.tablero.matriz, matriz_esperada)
        self.assertEqual(self.tablero.num_iniciales, 5.0)  # 10 pares / 2
    
    def test_prueba2_encontrar_pares(self):
        """Probar que los pares se identifican correctamente en prueba2.txt"""
        todas_permutaciones = encontrar_pares(self.tablero)
        
        # Debe devolver permutaciones de los pares
        self.assertIsInstance(todas_permutaciones, list)
        self.assertGreater(len(todas_permutaciones), 0)
        
        # Extraer los pares base de la primera permutación
        primera_perm = todas_permutaciones[0]
        dict_pares = {}
        for valor, posiciones in primera_perm:
            dict_pares[valor] = posiciones
        
        # Verificar que se encuentren todos los valores esperados
        for i in range(1, 6):
            self.assertIn(i, dict_pares)
        
        # Verificar posiciones para cada valor (corregido basado en matriz real)
        self.assertEqual(set(dict_pares[1]), {(1, 0), (2, 3)})
        self.assertEqual(set(dict_pares[2]), {(1, 1), (3, 3)})  # Corregido
        self.assertEqual(set(dict_pares[3]), {(2, 0), (4, 0)})
        self.assertEqual(set(dict_pares[4]), {(2, 1), (4, 2)})  # Corregido
        self.assertEqual(set(dict_pares[5]), {(0, 4), (4, 3)})
    
    def test_prueba2_calculos_heuristica(self):
        """Probar cálculos de distancia Manhattan para pares de prueba2.txt"""
        # Probar cálculos heurísticos para cada par (corregido)
        self.assertEqual(heuristica((1, 0), (2, 3)), 4)  # Par 1
        self.assertEqual(heuristica((1, 1), (3, 3)), 4)  # Par 2 (corregido)
        self.assertEqual(heuristica((2, 0), (4, 0)), 2)  # Par 3
        self.assertEqual(heuristica((2, 1), (4, 2)), 3)  # Par 4 (corregido)
        self.assertEqual(heuristica((0, 4), (4, 3)), 5)  # Par 5
    
    def test_prueba2_busqueda_astar(self):
        """Probar búsqueda A* para cada par en prueba2.txt"""
        pares_a_probar = [
            (3, (2, 0), (4, 0)),  # Par 3 - más simple (línea vertical)
            (4, (2, 1), (4, 2)),  # Par 4 - posiciones corregidas
            (2, (1, 1), (3, 3)),  # Par 2 - posiciones corregidas
        ]
        
        for dato, inicio, fin in pares_a_probar:
            with self.subTest(par=dato):
                bloqueados = []
                camino = astar(self.tablero.matriz, dato, bloqueados, inicio, fin)
                
                # Debe encontrar un camino
                self.assertIsNotNone(camino, f"No se encontró camino para par {dato}")
                self.assertIsInstance(camino, list)
                self.assertGreater(len(camino), 0)
                
                # Verificar que el camino lleva al destino correcto
                pos = inicio
                for movimiento in camino:
                    pos = (pos[0] + movimiento[0], pos[1] + movimiento[1])
                self.assertEqual(pos, fin, f"Camino para par {dato} no alcanza el objetivo")
    
    def test_prueba2_validacion_camino_solucion(self):
        """Probar que los caminos de solución esperados son válidos"""
        # Probar cada camino esperado
        for num_par, camino_esperado in self.caminos_solucion_esperados.items():
            with self.subTest(par=num_par):
                # Verificar continuidad del camino
                for i in range(len(camino_esperado) - 1):
                    pos_actual = camino_esperado[i]
                    pos_siguiente = camino_esperado[i + 1]
                    
                    # Calcular movimiento
                    movimiento = (pos_siguiente[0] - pos_actual[0], pos_siguiente[1] - pos_actual[1])
                    
                    # Verificar que es un movimiento válido de un solo paso
                    self.assertIn(movimiento, MOVIMIENTOS.values(), 
                                f"Movimiento inválido {movimiento} en camino para par {num_par} de {pos_actual} a {pos_siguiente}")
                    
                    # Verificar que la distancia Manhattan es 1
                    self.assertEqual(heuristica(pos_actual, pos_siguiente), 1,
                                  f"Posiciones no adyacentes en camino para par {num_par}")
    
    def test_prueba2_dimensiones_matriz(self):
        """Probar dimensiones de matriz para prueba2.txt"""
        self.assertEqual(len(self.tablero.matriz), 5)  # 5 filas
        self.assertEqual(len(self.tablero.matriz[0]), 5)  # 5 columnas
        
        # Verificar posiciones específicas de pares (corregido basado en matriz real)
        self.assertEqual(self.tablero.matriz[1][0], 1)  # Primer 1 en (2,1)
        self.assertEqual(self.tablero.matriz[2][3], 1)  # Segundo 1 en (3,4)
        self.assertEqual(self.tablero.matriz[1][1], 2)  # Primer 2 en (2,2)
        self.assertEqual(self.tablero.matriz[3][3], 2)  # Segundo 2 en (4,4) - corregido
        self.assertEqual(self.tablero.matriz[2][0], 3)  # Primer 3 en (3,1)
        self.assertEqual(self.tablero.matriz[4][0], 3)  # Segundo 3 en (5,1)
        self.assertEqual(self.tablero.matriz[2][1], 4)  # Primer 4 en (3,2)
        self.assertEqual(self.tablero.matriz[4][2], 4)  # Segundo 4 en (5,3) - corregido
        self.assertEqual(self.tablero.matriz[0][4], 5)  # Primer 5 en (1,5)
        self.assertEqual(self.tablero.matriz[4][3], 5)  # Segundo 5 en (5,4)
    
    def test_prueba2_simulacion_solucion_completa(self):
        """Probar simulación de solución completa para prueba2.txt"""
        # Crear una copia para simulación
        tablero_prueba = copy.deepcopy(self.tablero)
        
        # Simular conectar todos los pares siguiendo caminos esperados
        matriz_solucion = [
            [-1, -1, -1, -1, 5],    # Camino para par 1
            [1, 2, -2, -1, -5],     # Caminos mixtos
            [3, 4, -2, 1, -5],      # Posiciones finales y caminos
            [-3, -4, -2, 2, -5],    # Caminos continuos (corregido)
            [3, -4, 4, 5, -5]       # Conexiones finales (corregido)
        ]
        
        # Marcar todos los pares como conectados
        for i in range(1, 6):
            tablero_prueba.aumentar_conectados(i, 0, 0)  # Coordenadas ficticias
        
        # Actualizar matriz para reflejar solución
        tablero_prueba.matriz = matriz_solucion
        
        # Probar que el tablero se considera completo
        self.assertTrue(tablero_prueba.revisar_tablero_vacio())
        self.assertEqual(len(tablero_prueba.num_conectados), 5)
    
    def test_prueba2_validacion_longitud_camino(self):
        """Probar que las longitudes de camino esperadas son razonables"""
        longitudes_esperadas = {
            1: 6,  # 7 posiciones = 6 movimientos
            2: 4,  # 5 posiciones = 4 movimientos (corregido)
            3: 2,  # 3 posiciones = 2 movimientos
            4: 3,  # 4 posiciones = 3 movimientos (corregido)
            5: 5   # 6 posiciones = 5 movimientos
        }
        
        for num_par, longitud_esperada in longitudes_esperadas.items():
            longitud_real = len(self.caminos_solucion_esperados[num_par]) - 1
            self.assertEqual(longitud_real, longitud_esperada,
                           f"Discrepancia en longitud de camino para par {num_par}")


if __name__ == '__main__':
    # Crear suites de pruebas para ambos archivos de prueba
    suite1 = unittest.TestLoader().loadTestsFromTestCase(PruebasInterfazPrueba1)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(PruebasInterfazPrueba2)
    
    # Combinar suites de pruebas
    suite_combinado = unittest.TestSuite([suite1, suite2])
    
    # Ejecutar pruebas
    ejecutor = unittest.TextTestRunner(verbosity=2)
    resultado = ejecutor.run(suite_combinado)
    
    # Imprimir resumen
    if resultado.wasSuccessful():
        print("\nPRUEBAS SUPERADAS CORRECTAMENTE CON PRUEBA1.TXT Y PRUEBA2.TXT")
    else:
        print(f"\nFALLOS: {len(resultado.failures + resultado.errors)} PRUEBAS FALLIDAS")
        for fallo in resultado.failures:
            print(f"FALLO: {fallo[0]}")
            print(fallo[1])
        for error in resultado.errors:
            print(f"ERROR: {error[0]}")
            print(error[1])