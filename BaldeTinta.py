from PIL import Image
import numpy as np
from queue import Queue


class Node:
    def __init__(self, item):
        self.item = item  # Vértice vizinho (coordenada (x, y))
        self.next = None  # Ponteiro para o próximo nó


class Bag:
    def __init__(self):
        self.first = None  # Primeiro nó da lista

    def add(self, item):
        new_node = Node(item)
        new_node.next = self.first
        self.first = new_node

    def __iter__(self):
        current = self.first
        while current:
            yield current.item
            current = current.next


class Graph:
    def __init__(self, imagem):
        self.adj = {}  # Dicionário {(x, y): Bag} -> Lista de adjacência
        self.pixel_colors = {}  # Dicionário {(x, y): cor}
        self.create_graph(imagem)

    def create_graph(self, imagem):
        height, width = len(imagem), len(imagem[0])
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        # Criar os vértices e armazenar cores
        for x in range(height):
            for y in range(width):
                self.adj[(x, y)] = Bag()  # Cada pixel é um vértice no dicionário
                self.pixel_colors[(x, y)] = imagem[x][y]  # Armazena a cor original do pixel

        # Criar as conexões entre os vértices vizinhos
        for x in range(height):
            for y in range(width):
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in self.adj:  # Verifica se o vizinho está dentro da imagem
                        self.adj[(x, y)].add((nx, ny))


class BreadthFirstPaths:
    def __init__(self, graph, start, new_color):
        self.graph = graph
        self.start = start  # Vértice inicial
        self.new_color = new_color
        self.bfs()

    def bfs(self):
        x, y = self.start
        original_color = self.graph.pixel_colors[(x, y)]
        if original_color == self.new_color:
            return  # Se já estiver na cor desejada, não faz nada

        queue = Queue()
        queue.put((x, y))
        visited = set()
        visited.add((x, y))

        # Modifica a cor do vértice inicial
        self.graph.pixel_colors[(x, y)] = self.new_color

        while not queue.empty():
            vx, vy = queue.get()

            for nx, ny in self.graph.adj[(vx, vy)]:
                if (nx, ny) not in visited and self.graph.pixel_colors[(nx, ny)] == original_color:
                    # Modifica a cor do vértice no grafo
                    self.graph.pixel_colors[(nx, ny)] = self.new_color
                    visited.add((nx, ny))
                    queue.put((nx, ny))


def ler_matriz_do_arquivo(nome_arquivo="entrada.txt"):
    with open(nome_arquivo, "r") as arquivo:
        return [list(map(int, linha.split())) for linha in arquivo.readlines()]


def salvar_matriz_em_txt(graph, nome_arquivo="saida.txt"):
    height = max(x for x, y in graph.pixel_colors.keys()) + 1
    width = max(y for x, y in graph.pixel_colors.keys()) + 1
    matriz = [[0] * width for _ in range(height)]

    for (x, y), color in graph.pixel_colors.items():
        matriz[x][y] = color

    with open(nome_arquivo, "w") as arquivo:
        for linha in matriz:
            arquivo.write(" ".join(map(str, linha)) + "\n")


def entrada_parametros():
    linha, coluna = map(int, input("Informe as coordenadas do ponto inicial (linha, coluna): ").split())
    nova_cor = int(input("Informe a nova cor: "))
    return linha, coluna, nova_cor


img = Image.open('imgs/imagem.png').convert('L')
arr = np.asarray(img)
np.savetxt('entrada.txt', arr, fmt='%d')

imagem = ler_matriz_do_arquivo()
graph = Graph(imagem)

linha, coluna, nova_cor = entrada_parametros()
bfs = BreadthFirstPaths(graph, (linha, coluna), nova_cor)

salvar_matriz_em_txt(graph)

arr = np.loadtxt('saida.txt', dtype=np.uint8)
img = Image.fromarray(arr, mode='L')
img.save('imgs/imagem_reconstruida.png')
img.show()