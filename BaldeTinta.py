from PIL import Image
import numpy as np
from collections import deque

# 250 500
def preenchimentoBFS(imagem, linha, coluna, nova_cor):
    cor_original = imagem[linha][coluna]

    if cor_original == nova_cor:
        return imagem

    fila = deque([(linha, coluna)])
    imagem[linha][coluna] = nova_cor

    direcoes = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    while fila:
        x, y = fila.popleft()

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(imagem) and 0 <= ny < len(imagem[0]) and imagem[nx][ny] == cor_original:
                imagem[nx][ny] = nova_cor
                fila.append((nx, ny))

    return imagem

def ler_matriz_do_arquivo(nome_arquivo="entrada.txt"):
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    matriz = []
    for linha in linhas:
        matriz.append(list(map(int, linha.split())))

    return matriz

def entrada_parametros():
    linha, coluna = map(int, input("Informe as coordenadas do ponto inicial (linha, coluna): ").split())
    nova_cor = int(input("Informe a nova cor: "))
    return linha, coluna, nova_cor

def salvar_matriz_em_txt(matriz, nome_arquivo="saida.txt"):
    with open(nome_arquivo, "w") as arquivo:
        for linha in matriz:
            arquivo.write(" ".join(map(str, linha)) + "\n")


img = Image.open('imgs/UNIFOR_logo.png')
img = img.convert('L')
arr = np.asarray(img)
np.savetxt('entrada.txt', arr, fmt='%d')


imagem = ler_matriz_do_arquivo()

linha, coluna, nova_cor = entrada_parametros()

imagem_resultante = preenchimentoBFS(imagem, linha, coluna, nova_cor)

salvar_matriz_em_txt(imagem_resultante)


arr = np.loadtxt('saida.txt', dtype=np.uint8)
img = Image.fromarray(arr, mode='L')
img.save('imgs/imagem_reconstruida.png')
img.show()