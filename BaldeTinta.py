from collections import deque

# 250 500
def preenchimentoBFS(imagem, linha, coluna, nova_cor):
    cor_original = imagem[linha][coluna]

    if cor_original == nova_cor:
        return imagem

    fila = deque([(linha, coluna)])
    imagem[linha][coluna] = nova_cor

    # Vizinhança 8-conectada (horizontal, vertical e diagonal)
    direcoes = [
        (-1, 0), (1, 0), (0, -1), (0, 1),  # Vizinhos ortogonais
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Vizinhos diagonais
    ]

    while fila:
        x, y = fila.popleft()

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(imagem) and 0 <= ny < len(imagem[0]) and imagem[nx][ny] == cor_original:
                imagem[nx][ny] = nova_cor
                fila.append((nx, ny))

    return imagem

# Função para ler a matriz de um arquivo TXT
def ler_matriz_do_arquivo(nome_arquivo="entrada.txt"):
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()

    matriz = []
    for linha in linhas:
        matriz.append(list(map(int, linha.split())))

    return matriz

# Função para ler o ponto inicial e a nova cor
def entrada_parametros():
    linha, coluna = map(int, input("Informe as coordenadas do ponto inicial (linha, coluna): ").split())
    nova_cor = int(input("Informe a nova cor: "))
    return linha, coluna, nova_cor

# Função para salvar a matriz em um arquivo TXT
def salvar_matriz_em_txt(matriz, nome_arquivo="saida.txt"):
    with open(nome_arquivo, "w") as arquivo:
        for linha in matriz:
            arquivo.write(" ".join(map(str, linha)) + "\n")

# Lê a matriz do arquivo de entrada
imagem = ler_matriz_do_arquivo()

# Lê os parâmetros do preenchimento
linha, coluna, nova_cor = entrada_parametros()

# Aplica a ferramenta Balde de Tinta usando BFS com vizinhança 8-conectada
imagem_resultante = preenchimentoBFS(imagem, linha, coluna, nova_cor)

# Salva a matriz resultante no arquivo TXT
salvar_matriz_em_txt(imagem_resultante)

print(f"Matriz resultante salva em 'saida.txt'.")
