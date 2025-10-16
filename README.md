# Interpretador de Matriz Adyacente para Creación de Grafos

Este programa permite crear y visualizar grafos a partir de matrices de adyacencia, aplicando el algoritmo de Dijkstra para encontrar caminos mínimos.

## Características

- ✅ Interfaz gráfica intuitiva con Tkinter
- ✅ Soporte para grafos dirigidos y no dirigidos
- ✅ Matriz de adyacencia editable (2-10 nodos)
- ✅ Visualización gráfica del grafo con NetworkX y Matplotlib
- ✅ Implementación del algoritmo de Dijkstra
- ✅ Muestra distancias mínimas y caminos más cortos

## Instalación

1. Asegúrate de tener Python 3.7 o superior instalado

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el programa:
```bash
python main.py
```

### Instrucciones:

1. **Selecciona el número de nodos** (2-10) usando el selector
2. **Marca la casilla "Grafo Dirigido"** si deseas un grafo dirigido
3. **Completa la matriz de adyacencia** con los pesos de las aristas
   - 0 significa que no hay conexión
   - Valores > 0 representan el peso de la arista
4. **Haz clic en "Procesar Grafo"** para visualizar el grafo y calcular caminos mínimos
5. **Usa "Limpiar Matriz"** para resetear todos los valores a 0

## Ejemplo

Para un grafo de 4 nodos con las siguientes conexiones:
- Nodo 0 → Nodo 1 (peso: 5)
- Nodo 0 → Nodo 2 (peso: 3)
- Nodo 1 → Nodo 3 (peso: 2)
- Nodo 2 → Nodo 3 (peso: 4)

Matriz de adyacencia:
```
    0  1  2  3
0   0  5  3  0
1   0  0  0  2
2   0  0  0  4
3   0  0  0  0
```

El programa mostrará el grafo visualmente y calculará los caminos más cortos desde el nodo 0.

## Tecnologías

- **Python 3.x**
- **Tkinter** - Interfaz gráfica
- **NetworkX** - Creación y manipulación de grafos
- **Matplotlib** - Visualización de grafos
- **NumPy** - Manejo de matrices

## Licencia

Este proyecto es de uso libre para fines educativos.
