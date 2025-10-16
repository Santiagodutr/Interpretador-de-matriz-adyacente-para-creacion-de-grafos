"""
Módulo para operaciones con grafos a partir de matrices de adyacencia
"""

class Grafo:
    def __init__(self, matriz, dirigido=False):
        """
        Inicializa un grafo con su matriz de adyacencia
        
        Args:
            matriz: Lista de listas representando la matriz de adyacencia
            dirigido: Boolean indicando si el grafo es dirigido
        """
        self.matriz = matriz
        self.dirigido = dirigido
        self.n_nodos = len(matriz)
        self.nodos = [chr(65 + i) for i in range(self.n_nodos)]  # A, B, C, ...
    
    def validar_matriz(self):
        """
        Valida que la matriz de adyacencia sea correcta
        
        Returns:
            tuple: (es_valida, mensaje_error)
        """
        # Verificar que sea cuadrada
        if len(self.matriz) != len(self.matriz[0]):
            return False, "La matriz debe ser cuadrada"
        
        # Verificar que todos los elementos sean números
        for i in range(len(self.matriz)):
            if len(self.matriz[i]) != self.n_nodos:
                return False, "La matriz debe ser cuadrada"
            for j in range(len(self.matriz[i])):
                try:
                    val = float(self.matriz[i][j])
                    if val < 0:
                        return False, "Los pesos no pueden ser negativos"
                except (ValueError, TypeError):
                    return False, "Todos los elementos deben ser números"
        
        # Permitir loops (auto-conexiones en la diagonal)
        
        # Si es no dirigido, verificar simetría
        if not self.dirigido:
            for i in range(self.n_nodos):
                for j in range(self.n_nodos):
                    if self.matriz[i][j] != self.matriz[j][i]:
                        return False, "Para grafos no dirigidos, la matriz debe ser simétrica"
        
        return True, "Matriz válida"
    
    def obtener_representacion_matematica(self):
        """
        Genera la representación matemática del grafo
        
        Returns:
            str: Representación matemática con vértices y aristas
        """
        # Conjunto de vértices
        vertices = f"V = {{{', '.join(self.nodos)}}}"
        
        # Conjunto de aristas
        aristas = []
        for i in range(self.n_nodos):
            for j in range(self.n_nodos):
                peso = self.matriz[i][j]
                if peso != 0:
                    if self.dirigido:
                        aristas.append(f"({self.nodos[i]}, {self.nodos[j]}, {peso})")
                    else:
                        # Para no dirigidos, solo agregar una vez
                        if i <= j:
                            aristas.append(f"({self.nodos[i]}, {self.nodos[j]}, {peso})")
        
        tipo = "Dirigido" if self.dirigido else "No Dirigido"
        aristas_str = f"E = {{{', '.join(aristas)}}}"
        
        return f"Grafo {tipo}\n\n{vertices}\n{aristas_str}"
    
    def obtener_nodos_adyacentes(self, nodo_idx):
        """
        Obtiene los nodos adyacentes a un nodo dado
        
        Args:
            nodo_idx: Índice del nodo
            
        Returns:
            list: Lista de tuplas (nodo, peso)
        """
        adyacentes = []
        for j in range(self.n_nodos):
            if self.matriz[nodo_idx][j] != 0:
                adyacentes.append((self.nodos[j], self.matriz[nodo_idx][j]))
        return adyacentes
    
    def encontrar_camino(self, inicio, fin, visitados=None):
        """
        Encuentra un camino entre dos nodos usando DFS
        
        Args:
            inicio: Índice del nodo inicial
            fin: Índice del nodo final
            visitados: Set de nodos visitados
            
        Returns:
            list: Lista de índices representando el camino, o None si no existe
        """
        if visitados is None:
            visitados = set()
        
        visitados.add(inicio)
        
        if inicio == fin:
            return [inicio]
        
        for j in range(self.n_nodos):
            if self.matriz[inicio][j] != 0 and j not in visitados:
                camino = self.encontrar_camino(j, fin, visitados.copy())
                if camino:
                    return [inicio] + camino
        
        return None
    
    def encontrar_ciclo(self):
        """
        Encuentra un ciclo en el grafo
        
        Returns:
            list: Lista de índices representando el ciclo, o None si no existe
        """
        def dfs_ciclo(nodo, padre, visitados, camino):
            visitados.add(nodo)
            camino.append(nodo)
            
            for vecino in range(self.n_nodos):
                if self.matriz[nodo][vecino] != 0:
                    if vecino in visitados and vecino != padre:
                        # Encontramos un ciclo
                        idx = camino.index(vecino)
                        return camino[idx:] + [vecino]
                    elif vecino not in visitados:
                        resultado = dfs_ciclo(vecino, nodo, visitados, camino[:])
                        if resultado:
                            return resultado
            
            return None
        
        for i in range(self.n_nodos):
            resultado = dfs_ciclo(i, -1, set(), [])
            if resultado and len(resultado) > 2:  # Un ciclo debe tener al menos 3 nodos
                return resultado
        
        return None
    
    def obtener_todas_aristas(self):
        """
        Obtiene todas las aristas del grafo
        
        Returns:
            list: Lista de tuplas (i, j, peso)
        """
        aristas = []
        for i in range(self.n_nodos):
            for j in range(self.n_nodos):
                if self.matriz[i][j] != 0:
                    if self.dirigido:
                        aristas.append((i, j, self.matriz[i][j]))
                    else:
                        if i <= j:  # Para no dirigidos, solo una vez
                            aristas.append((i, j, self.matriz[i][j]))
        return aristas
