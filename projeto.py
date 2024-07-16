import heapq
import PySimpleGUI as sg

def carregar_grafo(filename):
    grafo = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('#'):  # Ignorar linhas de comentário
                continue
            origem, destino = line.strip().split('\t')
            if origem not in grafo:
                grafo[origem] = []
            grafo[origem].append(destino)
    return grafo

def dijkstra(grafo, origem):
    distancias = {vertice: float('inf') for vertice in grafo}
    predecessores = {vertice: None for vertice in grafo}
    distancias[origem] = 0
    fila = [(0, origem)]
    
    while fila:
        distancia_atual, vertice_atual = heapq.heappop(fila)
        
        if distancia_atual > distancias[vertice_atual]:
            continue
        
        if vertice_atual in grafo:
            for vizinho in grafo[vertice_atual]:
                distancia = distancia_atual + 1  # Peso igual a 1
                
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    predecessores[vizinho] = vertice_atual
                    heapq.heappush(fila, (distancia, vizinho))
    
    return distancias, predecessores

def menor_caminho(grafo, origem, destino):
    distancias, predecessores = dijkstra(grafo, origem)
    
    if destino not in predecessores:
        return float('inf'), None
    
    caminho = []
    vertice_atual = destino
    while vertice_atual is not None:
        caminho.append(vertice_atual)
        vertice_atual = predecessores[vertice_atual]
    
    caminho.reverse()
    peso_menor_caminho = distancias[destino]
    
    return peso_menor_caminho, caminho

def main():
    # Carregar o grafo a partir do arquivo
    grafo = carregar_grafo('roadNet-CA.txt')

    # Layout da GUI
    layout = [
        [sg.Text('Origem:'), sg.InputText(key='origem')],
        [sg.Text('Destino:'), sg.InputText(key='destino')],
        [sg.Button('Calcular menor caminho'), sg.Button('Sair')],
        [sg.Text(size=(40, 2), key='output')]
    ]

    # Criar janela
    window = sg.Window('Rede rodoviária da Califórnia', layout)

    # Loop de eventos
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

        if event == 'Calcular menor caminho':
            origem = values['origem'].strip()
            destino = values['destino'].strip()

            if origem not in grafo:
                window['output'].update(f"Vértice {origem} não encontrado no grafo.")
                continue
            if destino not in grafo:
                window['output'].update(f"Vértice {destino} não encontrado no grafo.")
                continue

            peso_menor_caminho, caminho = menor_caminho(grafo, origem, destino)
            if peso_menor_caminho == float('inf'):
                window['output'].update(f"Não há caminho entre {origem} e {destino}.")
            else:
                window['output'].update(f"O menor caminho de {origem} a {destino} tem peso {peso_menor_caminho}.")
                window['output'].update(f"Caminho: {' -> '.join(caminho)}")

    window.close()

if __name__ == "__main__":
    main()
