from PIL import Image
import numpy as np
from queue import Queue


class Node:
    def __init__(self, item):
        self.item = item
        self.next = None


class Bag:
    def __init__(self):
        self.first = None

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
        self.adj = {}
        self.pixel_colors = {}
        self.create_graph(imagem)

    def create_graph(self, imagem):
        height, width = len(imagem), len(imagem[0])
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for x in range(height):
            for y in range(width):
                self.adj[(x, y)] = Bag()
                self.pixel_colors[(x, y)] = imagem[x][y]

        for x in range(height):
            for y in range(width):
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in self.adj:
                        self.adj[(x, y)].add((nx, ny))


class BreadthFirstPaths:
    def __init__(self, graph, start, new_color):
        self.graph = graph
        self.start = start
        self.new_color = new_color
        self.bfs()

    def bfs(self):
        x, y = self.start
        original_color = self.graph.pixel_colors[(x, y)]
        if original_color == self.new_color:
            return

        queue = Queue()
        queue.put((x, y))
        visited = set()
        visited.add((x, y))

        self.graph.pixel_colors[(x, y)] = self.new_color

        while not queue.empty():
            vx, vy = queue.get()

            for nx, ny in self.graph.adj[(vx, vy)]:
                if (nx, ny) not in visited and self.graph.pixel_colors[(nx, ny)] == original_color:
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
img.save('imgs/imagem_grayscale.png')

imagem = ler_matriz_do_arquivo()
graph = Graph(imagem)

linha, coluna, nova_cor = entrada_parametros()
bfs = BreadthFirstPaths(graph, (linha, coluna), nova_cor)

salvar_matriz_em_txt(graph)

arr = np.loadtxt('saida.txt', dtype=np.uint8)
img = Image.fromarray(arr, mode='L')
img.save('imgs/imagem_reconstruida.png')
img.show()