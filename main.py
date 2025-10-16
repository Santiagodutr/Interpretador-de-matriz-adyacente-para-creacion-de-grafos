# Nueva versión basada en tu código de Jupyter, adaptada a Tkinter y matplotlib
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MatrizAdyacencia:
    def __init__(self, parent, n):
        self.parent = parent
        self.n = n
        self.entries = []
        self.frame = ttk.Frame(parent)
        self.crear_tabla(n)

    def crear_tabla(self, n):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.entries = []
        for i in range(n):
            fila = []
            for j in range(n):
                entry = ttk.Entry(self.frame, width=4, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            self.entries.append(fila)

    def get_matriz(self):
        matriz = np.zeros((self.n, self.n), dtype=int)
        for i in range(self.n):
            for j in range(self.n):
                val = self.entries[i][j].get()
                try:
                    v = int(val)
                    if v < 0:
                        raise ValueError
                    matriz[i, j] = v
                except:
                    return None
        return matriz

    def set_size(self, n):
        self.n = n
        self.crear_tabla(n)

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpretador de Matriz de Adyacencia")
        self.root.geometry("1000x700")

        self.nodos = tk.IntVar(value=4)
        self.dirigido = tk.BooleanVar(value=False)

        self.frame_top = ttk.Frame(root)
        self.frame_top.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(self.frame_top, text="Nodos:").pack(side=tk.LEFT)
        self.spin_nodos = ttk.Spinbox(self.frame_top, from_=2, to=10, textvariable=self.nodos, width=5, command=self.actualizar_tabla)
        self.spin_nodos.pack(side=tk.LEFT, padx=5)

        self.check_dirigido = ttk.Checkbutton(self.frame_top, text="Dirigido", variable=self.dirigido)
        self.check_dirigido.pack(side=tk.LEFT, padx=10)

        self.boton_procesar = ttk.Button(self.frame_top, text="Procesar grafo", command=self.procesar_grafo)
        self.boton_procesar.pack(side=tk.LEFT, padx=10)

        self.frame_matriz = ttk.LabelFrame(root, text="Matriz de Adyacencia")
        self.frame_matriz.pack(fill=tk.X, padx=10, pady=10)

        self.matriz_widget = MatrizAdyacencia(self.frame_matriz, self.nodos.get())
        self.matriz_widget.frame.pack()

        self.frame_resultados = ttk.Notebook(root)
        self.frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tab_grafico = ttk.Frame(self.frame_resultados)
        self.tab_texto = ttk.Frame(self.frame_resultados)
        self.frame_resultados.add(self.tab_grafico, text="Gráfico")
        self.frame_resultados.add(self.tab_texto, text="Resultados")

        self.text_resultados = tk.Text(self.tab_texto, wrap=tk.WORD, font=("Consolas", 11))
        self.text_resultados.pack(fill=tk.BOTH, expand=True)

        self.canvas_grafico = None

    def actualizar_tabla(self):
        n = self.nodos.get()
        self.matriz_widget.set_size(n)

    def procesar_grafo(self):
        matriz = self.matriz_widget.get_matriz()
        if matriz is None:
            messagebox.showerror("Error", "La matriz contiene valores inválidos o negativos.")
            return
        dirigido = self.dirigido.get()
        if dirigido:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        n = len(matriz)
        for i in range(n):
            for j in range(n):
                peso = matriz[i, j]
                if peso != 0:
                    if dirigido or i <= j:
                        G.add_edge(i, j, weight=peso)
        self.mostrar_grafico(G, dirigido)
        self.mostrar_resultados(G, matriz)

    def mostrar_grafico(self, G, dirigido):
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()
        fig, ax = plt.subplots(figsize=(7, 5))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightcoral', node_size=600, font_size=12, font_weight='bold', ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        titulo = "Grafo Dirigido" if dirigido else "Grafo No Dirigido"
        ax.set_title(titulo)
        ax.axis('off')
        self.canvas_grafico = FigureCanvasTkAgg(fig, master=self.tab_grafico)
        self.canvas_grafico.draw()
        self.canvas_grafico.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)

    def dijkstra(self, G, inicio):
        distancias = {nodo: float('inf') for nodo in G.nodes}
        distancias[inicio] = 0
        visitados = set()
        previos = {nodo: None for nodo in G.nodes}
        while len(visitados) < len(G.nodes):
            nodos_no_visitados = {n: distancias[n] for n in G.nodes if n not in visitados}
            if not nodos_no_visitados:
                break
            actual = min(nodos_no_visitados, key=nodos_no_visitados.get)
            visitados.add(actual)
            for vecino in G.neighbors(actual):
                peso = G[actual][vecino]['weight']
                if distancias[actual] + peso < distancias[vecino]:
                    distancias[vecino] = distancias[actual] + peso
                    previos[vecino] = actual
        return distancias, previos

    def mostrar_caminos(self, previos, inicio):
        resultados = []
        for nodo in previos:
            if nodo == inicio:
                continue
            path = []
            actual = nodo
            while actual is not None:
                path.append(actual)
                actual = previos[actual]
            path.reverse()
            if len(path) == 1 and path[0] != inicio:
                resultados.append(f"No hay camino al nodo {nodo}")
            else:
                resultados.append(f"Camino a {nodo}: {' -> '.join(map(str, path))}")
        return resultados

    def mostrar_resultados(self, G, matriz):
        self.text_resultados.delete(1.0, tk.END)
        inicio = 0
        if inicio not in G.nodes:
            self.text_resultados.insert(tk.END, "Nodo inicial no válido\n")
            return
        distancias, previos = self.dijkstra(G, inicio)
        self.text_resultados.insert(tk.END, f"Distancias mínimas desde el nodo {inicio}:\n")
        for nodo, distancia in distancias.items():
            self.text_resultados.insert(tk.END, f" Nodo {nodo}: {distancia}\n")
        self.text_resultados.insert(tk.END, "\nCaminos más cortos:\n")
        caminos = self.mostrar_caminos(previos, inicio)
        for c in caminos:
            self.text_resultados.insert(tk.END, c + "\n")

def main():
    root = tk.Tk()
    app = GrafoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
