import networkx as nx
import matplotlib.pyplot as plt

# Definimos los estados y sus conexiones con costos
estados = {
    "Aguascalientes": {"Jalisco": 200, "Zacatecas": 150},
    "Jalisco": {"Aguascalientes": 200, "Michoacán": 250, "Guanajuato": 100},
    "Zacatecas": {"Aguascalientes": 150, "San Luis P.": 300},
    "San Luis P.": {"Zacatecas": 300, "Guanajuato": 200, "Querétaro": 350},
    "Guanajuato": {"Jalisco": 100, "San Luis P.": 200, "Querétaro": 150},
    "Querétaro": {"San Luis P.": 350, "Guanajuato": 150, "Michoacán": 400},
    "Michoacán": {"Jalisco": 250, "Querétaro": 400}
}

# Crear el grafo y agregar las conexiones con los costos
grafo = nx.Graph()
for estado, conexiones in estados.items():
    for vecino, costo in conexiones.items():
        grafo.add_edge(estado, vecino, weight=costo)

# Para calcular el costo total de un recorrido dado
def costo(ruta):
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo_total += grafo[ruta[i]][ruta[i + 1]]['weight']
    return costo_total

# Método para encontrar recorridos sin repetir estados
def regreso_sinrep(estado_actual, visitados, ruta, costo_actual):
    if len(visitados) == len(estados):
        return ruta + [estado_actual], costo_actual

    mejor_ruta, mejor_costo = None, float('inf')
    for vecino in grafo[estado_actual]:
        if vecino not in visitados:
            nueva_ruta, nuevo_costo = regreso_sinrep(
                vecino, visitados | {vecino}, ruta + [estado_actual], costo_actual + grafo[estado_actual][vecino]['weight']
            )
            if nueva_ruta and nuevo_costo < mejor_costo:
                mejor_ruta, mejor_costo = nueva_ruta, nuevo_costo
    return mejor_ruta, mejor_costo

# Método para encontrar recorridos con repetición de al menos un estado
def regreso_conrep(estado_actual, visitados, ruta, costo_actual):
    if len(ruta) >= len(estados) and estado_actual == ruta[0]:  # Condición para cerrar el ciclo
        return ruta + [estado_actual], costo_actual

    mejor_ruta, mejor_costo = None, float('inf')
    for vecino in grafo[estado_actual]:
        if len(ruta) < len(estados) or (vecino == ruta[0] and len(visitados) > len(estados)):
            nueva_ruta, nuevo_costo = regreso_conrep(
                vecino, visitados + [vecino], ruta + [estado_actual], costo_actual + grafo[estado_actual][vecino]['weight']
            )
            if nueva_ruta and nuevo_costo < mejor_costo:
                mejor_ruta, mejor_costo = nueva_ruta, nuevo_costo
    return mejor_ruta, mejor_costo

def regreso_conrepeticion():
    estados_lista = list(estados.keys())
    total_costs = []
    print("Recorridos con repetición de al menos un estado:")

    for recorrido in grafo(estados_lista, repeat=8):
        if len(set(recorrido)) >= 7:  # Asegura que al menos 7 estados diferentes estén presentes
            costo = costo(recorrido)
            if costo is not None:  # Solo imprimir recorridos válidos
                total_costs.append(costo)
                print(f"Recorrido: {' -> '.join(recorrido)} | Costo Total: {costo}")
    print(f"\nCosto total de recorridos con repetición: {sum(total_costs) if total_costs else 'No hay recorridos válidos'}")


# Dibuja el grafo con etiquetas de costos
def dibujar_grafo():
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=10)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.title("Grafo de Estados con Costos de Traslado")
    plt.show()

# Función principal para manejar el menú
def menu():
    estado_inicio = "Aguascalientes"
    while True:
        print("\nMenú:")
        print("1. Recorrido sin repetir estados")
        print("2. Recorrido permitiendo repetición de estados")
        print("3. Mostrar grafo")
        print("4. Salir")
        opcion = input("Elige una opción (1-4): ")

        if opcion == '1':
            ruta, costo_total = regreso_sinrep(estado_inicio, {estado_inicio}, [], 0)
            print("Recorrido sin repetir: ", ruta)
            print("Costo total sin repetir: ", costo_total)
        elif opcion == '2':
            ruta, costo_total = regreso_conrep(estado_inicio, [estado_inicio], [], 0)
            print("Recorrido con repetición: ", ruta)
            print("Costo total con repetición: ", costo_total)
        elif opcion == '3':
            dibujar_grafo()
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

menu()
