import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpretador de Matriz Adyacente para Grafos")
        self.root.geometry("1200x700")
        
        # Variables
        self.num_nodos = tk.IntVar(value=4)
        self.es_dirigido = tk.BooleanVar(value=False)
        self.entries = []
        self.G = None
        self.pos = None  # Guardar posiciones de los nodos
        self.nodo_origen = tk.StringVar()
        self.nodo_destino = tk.StringVar()
        self.camino_actual = []  # Almacenar el camino actual
        self.algoritmo = tk.StringVar(value="Dijkstra")
        
        # Crear interfaz
        self.crear_interfaz()
        self.crear_tabla()
    
    def crear_interfaz(self):
        # Frame superior para controles
        frame_control = ttk.Frame(self.root, padding="10")
        frame_control.pack(side=tk.TOP, fill=tk.X)
        
        # Control de número de nodos
        ttk.Label(frame_control, text="Número de nodos:").pack(side=tk.LEFT, padx=5)
        spinbox = ttk.Spinbox(frame_control, from_=2, to=10, textvariable=self.num_nodos, 
                              width=10, command=self.crear_tabla)
        spinbox.pack(side=tk.LEFT, padx=5)
        
        # Checkbox para grafo dirigido
        ttk.Checkbutton(frame_control, text="Grafo Dirigido", 
                        variable=self.es_dirigido).pack(side=tk.LEFT, padx=20)
        
        # Selección de algoritmo
        ttk.Label(frame_control, text="Algoritmo:").pack(side=tk.LEFT, padx=5)
        self.combo_algoritmo = ttk.Combobox(frame_control, textvariable=self.algoritmo,
                                            values=("Dijkstra", "Bellman-Ford"),
                                            state='readonly', width=15)
        self.combo_algoritmo.pack(side=tk.LEFT, padx=5)
        
        # Botón procesar
        ttk.Button(frame_control, text="Procesar Grafo", 
                  command=self.procesar_grafo).pack(side=tk.LEFT, padx=20)
        
        # Botón limpiar
        ttk.Button(frame_control, text="Limpiar Matriz", 
                  command=self.limpiar_matriz).pack(side=tk.LEFT, padx=5)
        
        # Frame para selección de camino más corto
        frame_camino = ttk.LabelFrame(frame_control, text="Camino Más Corto", padding="5")
        frame_camino.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(frame_camino, text="Origen:").pack(side=tk.LEFT, padx=2)
        self.combo_origen = ttk.Combobox(frame_camino, textvariable=self.nodo_origen, 
                                         width=5, state='readonly')
        self.combo_origen.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(frame_camino, text="Destino:").pack(side=tk.LEFT, padx=2)
        self.combo_destino = ttk.Combobox(frame_camino, textvariable=self.nodo_destino, 
                                          width=5, state='readonly')
        self.combo_destino.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(frame_camino, text="Mostrar Camino", 
                  command=self.mostrar_camino_mas_corto).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_camino, text="Limpiar Camino", 
                  command=self.limpiar_camino).pack(side=tk.LEFT, padx=2)
        
        # Frame principal dividido
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo para la tabla
        frame_izquierdo = ttk.Frame(frame_principal)
        frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        ttk.Label(frame_izquierdo, text="Matriz de Adyacencia:", 
                 font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Canvas con scrollbar para la tabla
        canvas_frame = ttk.Frame(frame_izquierdo)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_tabla = tk.Canvas(canvas_frame, width=350, height=350)
        scrollbar_y = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas_tabla.yview)
        scrollbar_x = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas_tabla.xview)
        
        self.frame_tabla = ttk.Frame(self.canvas_tabla)
        self.canvas_tabla.create_window((0, 0), window=self.frame_tabla, anchor=tk.NW)
        
        self.canvas_tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame derecho dividido en grafo y resultados
        frame_derecho = ttk.Frame(frame_principal)
        frame_derecho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Frame para el grafo
        frame_grafo = ttk.LabelFrame(frame_derecho, text="Visualización del Grafo", padding="5")
        frame_grafo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas_grafo = FigureCanvasTkAgg(self.figure, frame_grafo)
        self.canvas_grafo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame para resultados
        self.frame_resultados = ttk.LabelFrame(frame_derecho, text="Resultados - Caminos más cortos", padding="5")
        self.frame_resultados.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        
        # Text widget con scrollbar para resultados
        scrollbar_resultados = ttk.Scrollbar(self.frame_resultados)
        scrollbar_resultados.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_resultados = tk.Text(self.frame_resultados, height=10, width=50, 
                                       yscrollcommand=scrollbar_resultados.set,
                                       font=('Courier', 9))
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resultados.config(command=self.text_resultados.yview)
    
    def validar_numero(self, texto):
        """Valida que el texto sea un número entero.

        Reglas:
        - Si el algoritmo seleccionado es 'Bellman-Ford' se permiten números negativos (entrada puede ser '-' mientras el usuario escribe).
        - Si el algoritmo seleccionado es 'Dijkstra' solo se permiten enteros no negativos.
        - Se permite cadena vacía mientras se edita.
        """
        # Permitir vacío (edición intermedia)
        if texto == "":
            return True

        algoritmo = self.algoritmo.get() if hasattr(self, 'algoritmo') else 'Dijkstra'

        if algoritmo == 'Bellman-Ford':
            # Permitir '-' mientras el usuario escribe un número negativo
            if texto == "-":
                return True
            # Permitir números con opcional signo negativo
            return texto.lstrip('-').isdigit()
        else:
            # Dijkstra: solo enteros no negativos
            return texto.isdigit()
    
    def crear_tabla(self):
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        self.entries = []
        
        n = self.num_nodos.get()
        
        # Registrar la función de validación
        vcmd = (self.root.register(self.validar_numero), '%P')
        
        # Etiquetas de columnas
        ttk.Label(self.frame_tabla, text="", width=3).grid(row=0, column=0, padx=2, pady=2)
        for j in range(n):
            ttk.Label(self.frame_tabla, text=str(j), width=5, 
                     font=('Arial', 9, 'bold')).grid(row=0, column=j+1, padx=2, pady=2)
        
        # Crear entradas con validación
        for i in range(n):
            # Etiqueta de fila
            ttk.Label(self.frame_tabla, text=str(i), width=3, 
                     font=('Arial', 9, 'bold')).grid(row=i+1, column=0, padx=2, pady=2)
            
            fila = []
            for j in range(n):
                entry = ttk.Entry(self.frame_tabla, width=6, justify=tk.CENTER,
                                validate='key', validatecommand=vcmd)
                entry.insert(0, "0")
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                fila.append(entry)
            self.entries.append(fila)
        
        # Actualizar el canvas
        self.frame_tabla.update_idletasks()
        self.canvas_tabla.configure(scrollregion=self.canvas_tabla.bbox("all"))
    
    def limpiar_matriz(self):
        for fila in self.entries:
            for entry in fila:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
    
    def obtener_matriz(self):
        n = self.num_nodos.get()
        matriz = np.zeros((n, n), dtype=int)
        
        try:
            for i in range(n):
                for j in range(n):
                    valor = int(self.entries[i][j].get())
                    matriz[i, j] = valor
            return matriz
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la matriz: {e}")
            return None

    def calcular_rutas_minimas(self, inicio):
        """Calcula las distancias mínimas según el algoritmo seleccionado"""
        algoritmo = self.algoritmo.get()
        if algoritmo == "Dijkstra":
            distancias, previos = self.dijkstra(inicio)
            return algoritmo, distancias, previos
        elif algoritmo == "Bellman-Ford":
            distancias, previos, ciclo_negativo = self.bellman_ford(inicio)
            if ciclo_negativo:
                messagebox.showerror(
                    "Error",
                    "El grafo contiene un ciclo de peso negativo. Bellman-Ford no puede calcular distancias mínimas en este caso."
                )
                return None
            return algoritmo, distancias, previos
        else:
            messagebox.showerror("Error", f"Algoritmo desconocido: {algoritmo}")
            return None
    
    def graficar_grafo(self, matriz, destacar_camino=None, bucles_destacados=None):
        self.ax.clear()
        
        if self.es_dirigido.get():
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                peso = matriz[i, j]
                if peso != 0:
                    if self.es_dirigido.get() or i <= j:
                        self.G.add_edge(i, j, weight=peso)
        
        if len(self.G.nodes) == 0:
            self.ax.text(0.5, 0.5, 'Grafo vacío', ha='center', va='center', 
                        transform=self.ax.transAxes, fontsize=14)
            self.canvas_grafo.draw()
            return
        
        # Guardar las posiciones para mantener consistencia
        if self.pos is None:
            self.pos = nx.spring_layout(self.G, seed=42)
        
        pos = self.pos
        
        # Actualizar los comboboxes con los nodos disponibles
        nodos_disponibles = [str(n) for n in sorted(self.G.nodes)]
        self.combo_origen['values'] = nodos_disponibles
        self.combo_destino['values'] = nodos_disponibles
        if nodos_disponibles:
            if not self.nodo_origen.get() or self.nodo_origen.get() not in nodos_disponibles:
                self.combo_origen.set(nodos_disponibles[0])
            if not self.nodo_destino.get() or self.nodo_destino.get() not in nodos_disponibles:
                self.combo_destino.set(nodos_disponibles[-1] if len(nodos_disponibles) > 1 else nodos_disponibles[0])
        
        bucles_destacados = set() if bucles_destacados is None else set(bucles_destacados)

        # Preparar aristas del camino más corto si se proporciona
        aristas_camino = set()
        if destacar_camino:
            for i in range(len(destacar_camino) - 1):
                u, v = destacar_camino[i], destacar_camino[i + 1]
                # Para grafos dirigidos, solo agregamos la dirección exacta del camino
                aristas_camino.add((u, v))
                # Para grafos no dirigidos, también agregamos la inversa
                if not self.es_dirigido.get():
                    aristas_camino.add((v, u))
        
        # Configurar flechas solo para grafos dirigidos
        if self.es_dirigido.get():
            # Dibujar nodos
            nx.draw_networkx_nodes(self.G, pos, ax=self.ax, 
                                  node_color='lightcoral', node_size=600)
            nx.draw_networkx_labels(self.G, pos, ax=self.ax, 
                                   font_size=12, font_weight='bold')
            
            # Detectar aristas bidireccionales y bucles
            aristas_simples = []
            aristas_bidireccionales = []
            bucles = []
            aristas_simples_camino = []
            aristas_bidireccionales_camino = []
            bucles_camino = []
            
            # Rastrear qué aristas bidireccionales ya procesamos
            procesadas = set()
            
            for (u, v, data) in self.G.edges(data=True):
                if u == v:  # Bucle (self-loop)
                    if (u, v) in aristas_camino or u in bucles_destacados:
                        bucles_camino.append((u, v))
                    else:
                        bucles.append((u, v))
                elif self.G.has_edge(v, u):  # Bidireccional (existe arista en ambas direcciones)
                    # Evitar procesar la misma arista bidireccional dos veces
                    if (v, u) in procesadas:
                        continue
                    procesadas.add((u, v))
                    
                    # Verificar si cada dirección está en el camino
                    u_a_v_en_camino = (u, v) in aristas_camino
                    v_a_u_en_camino = (v, u) in aristas_camino
                    
                    # Dibujar dirección u -> v
                    if u_a_v_en_camino:
                        aristas_bidireccionales_camino.append((u, v))
                    else:
                        aristas_bidireccionales.append((u, v))
                    
                    # Dibujar dirección v -> u
                    if v_a_u_en_camino:
                        aristas_bidireccionales_camino.append((v, u))
                    else:
                        aristas_bidireccionales.append((v, u))
                        
                else:  # Simple (solo existe en una dirección)
                    if (u, v) in aristas_camino:
                        aristas_simples_camino.append((u, v))
                    else:
                        aristas_simples.append((u, v))
            
            # Dibujar aristas simples normales (sin curva)
            if aristas_simples:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_simples,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0',
                                      width=1.5)
            
            # Dibujar aristas simples del camino (sin curva)
            if aristas_simples_camino:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_simples_camino,
                                      edge_color='red',
                                      arrows=True,
                                      arrowsize=25,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0',
                                      width=3.5)
            
            # Dibujar aristas bidireccionales normales (con curva)
            if aristas_bidireccionales:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_bidireccionales,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0.3',
                                      width=1.5)
            
            # Dibujar aristas bidireccionales del camino (con curva)
            if aristas_bidireccionales_camino:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_bidireccionales_camino,
                                      edge_color='red',
                                      arrows=True,
                                      arrowsize=25,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0.3',
                                      width=3.5)
            
            # Dibujar bucles normales (self-loops)
            if bucles:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=bucles,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=2.5',
                                      min_source_margin=15,
                                      min_target_margin=15,
                                      width=1.5)
            
            # Dibujar bucles del camino (self-loops)
            if bucles_camino:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=bucles_camino,
                                      edge_color='red',
                                      arrows=True,
                                      arrowsize=25,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=2.5',
                                      min_source_margin=15,
                                      min_target_margin=15,
                                      width=3.5)
            
            # Dibujar etiquetas de pesos con posiciones ajustadas
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            
            # Para aristas bidireccionales, ajustar posición de etiquetas
            label_pos = {}
            for edge, weight in edge_labels.items():
                u, v = edge
                if u == v:  # Bucle
                    # Posicionar etiqueta arriba del nodo
                    x, y = pos[u]
                    label_pos[edge] = (x, y + 0.15)
                elif self.G.has_edge(v, u) and u != v:  # Bidireccional
                    # Calcular posición desplazada para la etiqueta
                    x1, y1 = pos[u]
                    x2, y2 = pos[v]
                    # Vector perpendicular
                    dx = x2 - x1
                    dy = y2 - y1
                    length = np.sqrt(dx**2 + dy**2)
                    if length > 0:
                        # Perpendicular normalizado
                        px = -dy / length
                        py = dx / length
                        # Desplazar etiqueta
                        offset = 0.08
                        label_x = (x1 + x2) / 2 + px * offset
                        label_y = (y1 + y2) / 2 + py * offset
                        label_pos[edge] = (label_x, label_y)
                    else:
                        label_pos[edge] = ((x1 + x2) / 2, (y1 + y2) / 2)
                else:  # Arista simple
                    x1, y1 = pos[u]
                    x2, y2 = pos[v]
                    label_pos[edge] = ((x1 + x2) / 2, (y1 + y2) / 2)
            
            # Dibujar etiquetas
            for edge, weight in edge_labels.items():
                x, y = label_pos[edge]
                es_camino = edge in aristas_camino or (edge[0] == edge[1] and edge[0] in bucles_destacados)
                self.ax.text(x, y, str(weight), 
                           fontsize=10 if es_camino else 9, 
                           ha='center', 
                           va='center',
                           fontweight='bold' if es_camino else 'normal',
                           bbox=dict(boxstyle="round,pad=0.3", 
                                   facecolor='yellow' if es_camino else 'white', 
                                   edgecolor='red' if es_camino else 'none', 
                                   alpha=0.9 if es_camino else 0.8))
        else:
            # Separar aristas normales, destacadas y bucles
            aristas_normales = []
            aristas_destacadas = []
            bucles_normales = []
            bucles_destacados_und = []
            for u, v in self.G.edges():
                if u == v:
                    if (u, v) in aristas_camino or (v, u) in aristas_camino or u in bucles_destacados:
                        bucles_destacados_und.append((u, v))
                    else:
                        bucles_normales.append((u, v))
                elif (u, v) in aristas_camino or (v, u) in aristas_camino:
                    aristas_destacadas.append((u, v))
                else:
                    aristas_normales.append((u, v))
            
            # Dibujar nodos
            nx.draw_networkx_nodes(self.G, pos, ax=self.ax, 
                                  node_color='lightcoral', node_size=600)
            nx.draw_networkx_labels(self.G, pos, ax=self.ax, 
                                   font_size=12, font_weight='bold')
            
            # Dibujar aristas normales
            if aristas_normales:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_normales,
                                      edge_color='gray',
                                      width=1.5)
            
            # Dibujar aristas del camino más corto
            if aristas_destacadas:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_destacadas,
                                      edge_color='red',
                                      width=3.5)
            
            if bucles_normales:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=bucles_normales,
                                      edge_color='gray',
                                      width=1.5,
                                      connectionstyle='arc3,rad=0.2')

            if bucles_destacados_und:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=bucles_destacados_und,
                                      edge_color='red',
                                      width=3.5,
                                      connectionstyle='arc3,rad=0.2')

            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            
            # Dibujar etiquetas con estilo diferente para el camino y bucles destacados
            for edge, weight in edge_labels.items():
                u, v = edge
                es_camino = edge in aristas_camino or (v, u) in aristas_camino or (u == v and u in bucles_destacados)
                x = (pos[u][0] + pos[v][0]) / 2
                y = (pos[u][1] + pos[v][1]) / 2
                self.ax.text(x, y, str(weight), 
                           fontsize=10 if es_camino else 9,
                           ha='center', 
                           va='center',
                           fontweight='bold' if es_camino else 'normal',
                           bbox=dict(boxstyle="round,pad=0.3", 
                                   facecolor='yellow' if es_camino else 'white', 
                                   edgecolor='red' if es_camino else 'gray',
                                   linewidth=2 if es_camino else 0,
                                   alpha=0.9 if es_camino else 0.8))
        
        titulo = "Grafo Dirigido" if self.es_dirigido.get() else "Grafo No Dirigido"
        if destacar_camino:
            # Calcular distancia total del camino
            if len(destacar_camino) == 1:
                # Si el camino es un solo nodo, verificar si tiene bucle
                nodo = destacar_camino[0]
                if self.G.has_edge(nodo, nodo):
                    distancia = self.G[nodo][nodo]['weight']
                else:
                    distancia = 0
            else:
                distancia = sum(self.G[destacar_camino[i]][destacar_camino[i+1]]['weight'] 
                              for i in range(len(destacar_camino) - 1))
            titulo += f" - Camino más corto: {' → '.join(map(str, destacar_camino))} (Distancia: {distancia})"
        self.ax.set_title(titulo, fontsize=11, fontweight='bold')
        self.ax.axis('off')
        
        self.canvas_grafo.draw()
    
    def dijkstra(self, inicio):
        if self.G is None or len(self.G.nodes) == 0:
            return None, None
        
        distancias = {nodo: float('inf') for nodo in self.G.nodes}
        distancias[inicio] = 0
        visitados = set()
        previos = {nodo: None for nodo in self.G.nodes}
        
        while len(visitados) < len(self.G.nodes):
            nodos_no_visitados = {n: distancias[n] for n in self.G.nodes if n not in visitados}
            if not nodos_no_visitados:
                break
            actual = min(nodos_no_visitados, key=nodos_no_visitados.get)
            visitados.add(actual)
            
            for vecino in self.G.neighbors(actual):
                peso = self.G[actual][vecino]['weight']
                if distancias[actual] + peso < distancias[vecino]:
                    distancias[vecino] = distancias[actual] + peso
                    previos[vecino] = actual
        
        return distancias, previos

    def bellman_ford(self, inicio):
        if self.G is None or len(self.G.nodes) == 0:
            return None, None, False
        
        distancias = {nodo: float('inf') for nodo in self.G.nodes}
        distancias[inicio] = 0
        previos = {nodo: None for nodo in self.G.nodes}
        aristas = [(u, v, data['weight']) for u, v, data in self.G.edges(data=True)]
        num_nodos = len(self.G.nodes)
        
        for _ in range(num_nodos - 1):
            actualizado = False
            for u, v, peso in aristas:
                if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    previos[v] = u
                    actualizado = True
            if not actualizado:
                break
        
        # Verificar ciclos negativos
        for u, v, peso in aristas:
            if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                return distancias, previos, True
        
        return distancias, previos, False
    
    def mostrar_resultados(self, distancias, previos, inicio, algoritmo):
        self.text_resultados.delete(1.0, tk.END)
        self.frame_resultados.configure(text=f"Resultados - Algoritmo {algoritmo}")

        if distancias is None:
            self.text_resultados.insert(tk.END, "No hay nodos en el grafo\n")
            return

        # Representación matemática del grafo
        nodos = sorted(self.G.nodes)
        aristas = sorted(self.G.edges)

        representacion = "V = { " + ', '.join(str(n) for n in nodos) + " }\n"
        representacion += "A = { " + ', '.join(f"({u},{v})" for u, v in aristas) + " }\n\n"
        self.text_resultados.insert(tk.END, representacion)

        self.text_resultados.insert(tk.END, "╔═══════════════════════════════════════════╗\n")
        self.text_resultados.insert(
            tk.END,
            f"║  ALGORITMO DE {algoritmo.upper()} - Nodo inicial: {inicio}  ║\n"
        )
        self.text_resultados.insert(tk.END, "╚═══════════════════════════════════════════╝\n\n")

        self.text_resultados.insert(tk.END, "DISTANCIAS MÍNIMAS:\n")
        self.text_resultados.insert(tk.END, "─" * 45 + "\n")
        for nodo in sorted(distancias.keys()):
            distancia = distancias[nodo]
            if distancia == float('inf'):
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: ∞ (No alcanzable)\n")
            else:
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: {distancia}\n")

        # Evidencias del concepto de camino, ciclo y nodos adyacentes
        self.text_resultados.insert(tk.END, "\n" + "═" * 45 + "\n")
        self.text_resultados.insert(tk.END, "EVIDENCIAS DE CONCEPTOS:\n")
        self.text_resultados.insert(tk.END, "═" * 45 + "\n")

        self.text_resultados.insert(tk.END, f"● Caminos desde el nodo inicial ({inicio}):\n")
        for destino in sorted(distancias.keys()):
            if destino != inicio:
                if distancias[destino] < float('inf'):
                    path = []
                    actual = destino
                    while actual is not None:
                        path.append(actual)
                        actual = previos[actual]
                    path.reverse()
                    camino_str = ' → '.join(map(str, path))
                    self.text_resultados.insert(tk.END, f"   - A {destino}: {camino_str}\n")
                else:
                    self.text_resultados.insert(tk.END, f"   - A {destino}: No alcanzable\n")

        if self.es_dirigido.get():
            ciclos = list(nx.simple_cycles(self.G))
        else:
            ciclos = list(nx.cycle_basis(self.G))
            ciclos = [c + [c[0]] for c in ciclos if len(c) > 1]

        if ciclos:
            self.text_resultados.insert(tk.END, "\n● Ciclos detectados:\n")
            for i, ciclo in enumerate(ciclos, 1):
                ciclo_str = ' → '.join(map(str, ciclo))
                self.text_resultados.insert(tk.END, f"   - Ciclo {i}: {ciclo_str}\n")
        else:
            self.text_resultados.insert(tk.END, "\n● Ciclos detectados: Ninguno\n")

        self.text_resultados.insert(tk.END, "\n● Nodos adyacentes:\n")
        for nodo in sorted(self.G.nodes):
            adyacentes = list(self.G.neighbors(nodo))
            if adyacentes:
                ady_str = ', '.join(map(str, sorted(adyacentes)))
                self.text_resultados.insert(tk.END, f"   - Nodo {nodo}: {ady_str}\n")
            else:
                self.text_resultados.insert(tk.END, f"   - Nodo {nodo}: Ninguno\n")

    def reconstruir_camino(self, previos, inicio, destino):
        """Reconstruye el camino desde inicio hasta destino usando el diccionario de previos"""
        if previos[destino] is None and inicio != destino:
            return None  # No hay camino
        
        camino = []
        actual = destino
        while actual is not None:
            camino.append(actual)
            actual = previos[actual]
        camino.reverse()
        return camino
    
    def mostrar_camino_mas_corto(self):
        """Calcula y muestra el camino más corto entre dos nodos seleccionados"""
        if self.G is None or len(self.G.nodes) == 0:
            messagebox.showwarning("Advertencia", "Primero debe procesar un grafo")
            return
        
        try:
            origen = int(self.nodo_origen.get())
            destino = int(self.nodo_destino.get())
        except ValueError:
            messagebox.showerror("Error", "Seleccione nodos válidos")
            return
        
        if origen not in self.G.nodes or destino not in self.G.nodes:
            messagebox.showerror("Error", "Los nodos seleccionados no existen en el grafo")
            return
        
        matriz = self.obtener_matriz()
        if matriz is None:
            return

        algoritmo_seleccionado = self.algoritmo.get()
        if algoritmo_seleccionado == "Dijkstra" and np.any(matriz < 0):
            messagebox.showerror(
                "Error",
                "Dijkstra no admite pesos negativos. Seleccione Bellman-Ford o elimine los pesos negativos."
            )
            return

        resultado = self.calcular_rutas_minimas(origen)
        if resultado is None:
            return
        algoritmo_usado, distancias, previos = resultado
        if distancias is None or distancias[destino] == float('inf'):
            messagebox.showinfo(
                "Información",
                f"No existe un camino desde el nodo {origen} hasta el nodo {destino}"
            )
            return

        self.camino_actual = self.reconstruir_camino(previos, origen, destino)
        if not self.camino_actual:
            messagebox.showinfo(
                "Información",
                f"No existe un camino desde el nodo {origen} hasta el nodo {destino}"
            )
            return

        bucles_resaltar = set()
        if origen == destino and self.G.has_edge(origen, origen):
            bucles_resaltar.add(origen)

        # Redibujar el grafo con el camino destacado
        self.graficar_grafo(matriz, destacar_camino=self.camino_actual, bucles_destacados=bucles_resaltar)

        # Calcular la distancia total del camino
        if origen == destino:
            if self.G.has_edge(origen, origen):
                distancia_total = self.G[origen][origen]['weight']
            else:
                distancia_total = 0
        else:
            distancia_total = distancias[destino]
        
        camino_str = ' → '.join(map(str, self.camino_actual))
        
        mensaje = f"\n{'═' * 45}\n"
        mensaje += f"CAMINO MÁS CORTO:\n"
        mensaje += f"{'═' * 45}\n"
        mensaje += f"Origen: {origen}\n"
        mensaje += f"Destino: {destino}\n"
        mensaje += f"Algoritmo: {algoritmo_usado}\n"
        mensaje += f"Camino: {camino_str}\n"
        mensaje += f"Distancia total: {distancia_total}\n"
        mensaje += f"{'═' * 45}\n"
        
        self.text_resultados.insert(tk.END, mensaje)
        self.text_resultados.see(tk.END)
    
    def limpiar_camino(self):
        """Limpia el camino destacado y vuelve a mostrar el grafo normal"""
        self.camino_actual = []
        matriz = self.obtener_matriz()
        if matriz is not None:
            self.graficar_grafo(matriz)


    
    def procesar_grafo(self):
        matriz = self.obtener_matriz()
        if matriz is None:
            return
        
        if self.algoritmo.get() == "Dijkstra" and np.any(matriz < 0):
            messagebox.showerror(
                "Error",
                "Dijkstra no admite pesos negativos. Seleccione Bellman-Ford o elimine los pesos negativos."
            )
            return
        
        # Resetear posiciones y camino al procesar un nuevo grafo
        self.pos = None
        self.camino_actual = []
        
        self.graficar_grafo(matriz)
        
        if self.G is None or len(self.G.nodes) == 0:
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, "El grafo está vacío. Agregue conexiones con pesos > 0")
            return
        
        inicio = 0  # Nodo inicial fijo
        resultado = self.calcular_rutas_minimas(inicio)
        if resultado is None:
            return
        algoritmo, distancias, previos = resultado
        self.mostrar_resultados(distancias, previos, inicio, algoritmo)

def main():
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
