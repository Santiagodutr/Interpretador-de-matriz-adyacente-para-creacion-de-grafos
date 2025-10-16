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
        
        # Botón procesar
        ttk.Button(frame_control, text="Procesar Grafo", 
                  command=self.procesar_grafo).pack(side=tk.LEFT, padx=20)
        
        # Botón limpiar
        ttk.Button(frame_control, text="Limpiar Matriz", 
                  command=self.limpiar_matriz).pack(side=tk.LEFT, padx=5)
        
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
        frame_resultados = ttk.LabelFrame(frame_derecho, text="Resultados - Algoritmo de Dijkstra", padding="5")
        frame_resultados.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        
        # Text widget con scrollbar para resultados
        scrollbar_resultados = ttk.Scrollbar(frame_resultados)
        scrollbar_resultados.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_resultados = tk.Text(frame_resultados, height=10, width=50, 
                                       yscrollcommand=scrollbar_resultados.set,
                                       font=('Courier', 9))
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resultados.config(command=self.text_resultados.yview)
    
    def crear_tabla(self):
        # Limpiar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()
        self.entries = []
        
        n = self.num_nodos.get()
        
        # Etiquetas de columnas
        ttk.Label(self.frame_tabla, text="", width=3).grid(row=0, column=0, padx=2, pady=2)
        for j in range(n):
            ttk.Label(self.frame_tabla, text=str(j), width=5, 
                     font=('Arial', 9, 'bold')).grid(row=0, column=j+1, padx=2, pady=2)
        
        # Crear entradas
        for i in range(n):
            # Etiqueta de fila
            ttk.Label(self.frame_tabla, text=str(i), width=3, 
                     font=('Arial', 9, 'bold')).grid(row=i+1, column=0, padx=2, pady=2)
            
            fila = []
            for j in range(n):
                entry = ttk.Entry(self.frame_tabla, width=6, justify=tk.CENTER)
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
                    if valor < 0:
                        raise ValueError("Los pesos deben ser >= 0")
                    matriz[i, j] = valor
            return matriz
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la matriz: {e}")
            return None
    
    def graficar_grafo(self, matriz):
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
        
        pos = nx.spring_layout(self.G, seed=42)
        
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
            
            for (u, v, data) in self.G.edges(data=True):
                if u == v:  # Bucle (self-loop)
                    bucles.append((u, v))
                elif self.G.has_edge(v, u) and u < v:  # Bidireccional
                    aristas_bidireccionales.append((u, v))
                    aristas_bidireccionales.append((v, u))
                elif not self.G.has_edge(v, u):  # Simple
                    aristas_simples.append((u, v))
            
            # Dibujar aristas simples (sin curva)
            if aristas_simples:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_simples,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0')
            
            # Dibujar aristas bidireccionales (con curva)
            if aristas_bidireccionales:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=aristas_bidireccionales,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=0.3')
            
            # Dibujar bucles (self-loops)
            if bucles:
                nx.draw_networkx_edges(self.G, pos, ax=self.ax,
                                      edgelist=bucles,
                                      edge_color='gray',
                                      arrows=True,
                                      arrowsize=20,
                                      arrowstyle='->',
                                      connectionstyle='arc3,rad=2.5',
                                      min_source_margin=15,
                                      min_target_margin=15)
            
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
                self.ax.text(x, y, str(weight), 
                           fontsize=9, 
                           ha='center', 
                           va='center',
                           bbox=dict(boxstyle="round,pad=0.3", 
                                   facecolor='white', 
                                   edgecolor='none', 
                                   alpha=0.8))
        else:
            nx.draw(self.G, pos, ax=self.ax, with_labels=True, 
                   node_color='lightcoral', node_size=600, 
                   font_size=12, font_weight='bold', arrows=False,
                   edge_color='gray')
            
            edge_labels = nx.get_edge_attributes(self.G, 'weight')
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax)
        
        titulo = "Grafo Dirigido" if self.es_dirigido.get() else "Grafo No Dirigido"
        self.ax.set_title(titulo, fontsize=12, fontweight='bold')
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
    
    def mostrar_resultados(self, distancias, previos, inicio):
        self.text_resultados.delete(1.0, tk.END)
        
        if distancias is None:
            self.text_resultados.insert(tk.END, "No hay nodos en el grafo\n")
            return
        
        self.text_resultados.insert(tk.END, f"╔═══════════════════════════════════════════╗\n")
        self.text_resultados.insert(tk.END, f"║  ALGORITMO DE DIJKSTRA - Nodo inicial: {inicio}  ║\n")
        self.text_resultados.insert(tk.END, f"╚═══════════════════════════════════════════╝\n\n")
        
        self.text_resultados.insert(tk.END, "DISTANCIAS MÍNIMAS:\n")
        self.text_resultados.insert(tk.END, "─" * 45 + "\n")
        for nodo in sorted(distancias.keys()):
            distancia = distancias[nodo]
            if distancia == float('inf'):
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: ∞ (No alcanzable)\n")
            else:
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: {distancia}\n")
        
        self.text_resultados.insert(tk.END, "\n" + "─" * 45 + "\n")
        self.text_resultados.insert(tk.END, "CAMINOS MÁS CORTOS:\n")
        self.text_resultados.insert(tk.END, "─" * 45 + "\n")
        
        for nodo in sorted(previos.keys()):
            if nodo == inicio:
                continue
            
            path = []
            actual = nodo
            while actual is not None:
                path.append(actual)
                actual = previos[actual]
            path.reverse()
            
            if len(path) == 1 and path[0] != inicio:
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: No hay camino\n")
            else:
                camino_str = ' → '.join(map(str, path))
                self.text_resultados.insert(tk.END, f"  Nodo {nodo}: {camino_str}\n")
    
    def procesar_grafo(self):
        matriz = self.obtener_matriz()
        if matriz is None:
            return
        
        self.graficar_grafo(matriz)
        
        if self.G is None or len(self.G.nodes) == 0:
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, "El grafo está vacío. Agregue conexiones con pesos > 0")
            return
        
        inicio = 0  # Nodo inicial fijo
        distancias, previos = self.dijkstra(inicio)
        self.mostrar_resultados(distancias, previos, inicio)

def main():
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
