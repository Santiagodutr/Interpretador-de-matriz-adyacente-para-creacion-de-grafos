# Interpretador de Matriz de Adyacencia para Grafos

Programa en Python con interfaz gráfica para trabajar con matrices de adyacencia y generar representaciones de grafos.

## Características

- ✅ Ingreso de matriz de adyacencia mediante celdas editables
- ✅ Tamaño de matriz ajustable (2x2 hasta 10x10)
- ✅ Soporte para grafos dirigidos y no dirigidos
- ✅ Validaciones de integridad de datos
- ✅ Representación matemática del grafo (vértices y aristas)
- ✅ Representación gráfica del grafo
- ✅ Visualización de conceptos:
  - Nodos adyacentes
  - Caminos
  - Ciclos
- ✅ Grafos dirigidos con doble flecha cuando dos nodos se apuntan mutuamente

## Instalación

```bash
python main.py
```

> **Nota:** tkinter viene incluido con Python por defecto en la mayoría de instalaciones.

## Uso

1. **Configurar el grafo:**
   - Ajusta el tamaño de la matriz usando el spinbox
   - Marca "Grafo Dirigido" si deseas un grafo con direcciones

2. **Ingresar la matriz:**
   - Completa las celdas con los pesos de las aristas
   - Usa 0 para indicar que no hay conexión
   - La diagonal siempre es 0 (no se permiten loops)

3. **Generar el grafo:**
   - Haz clic en "Generar Grafo"
   - El programa validará la matriz automáticamente

4. **Visualizar resultados:**
   - **Pestaña "Representación Gráfica":** Muestra el grafo visualmente
   - **Pestaña "Representación Matemática":** Muestra V (vértices) y E (aristas)
   - **Pestaña "Conceptos del Grafo":** Muestra ejemplos de nodos adyacentes, caminos y ciclos

## Validaciones Implementadas

- ✅ Matriz debe ser cuadrada
- ✅ Todos los elementos deben ser números
- ✅ Los pesos no pueden ser negativos
- ✅ La diagonal debe ser cero (sin loops)
- ✅ Para grafos no dirigidos, la matriz debe ser simétrica

## Características Especiales

### Grafos Dirigidos
- Cuando dos nodos se apuntan mutuamente, se dibujan dos flechas curvadas
- Cada flecha muestra su peso correspondiente

### Grafos No Dirigidos
- Las aristas se representan como líneas simples
- El peso se muestra en el centro de la arista
