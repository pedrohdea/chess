# Reimportando bibliotecas após reset
import os
import matplotlib.pyplot as plt
from collections import Counter

# # Aplicar nos 3 conjuntos
# ("dataset/train/images", "dataset/train/labels")
# ("dataset/valid/images", "dataset/valid/labels")
# ("dataset/test/images", "dataset/test/labels")

# Recriar função de contagem e plot
labels_dir = "dataset/train/labels"  # Corrigido para o ambiente atual

# Contar quantos objetos há por imagem
objetos_por_imagem = []
if os.path.exists(labels_dir):
    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(labels_dir, filename)) as f:
                count = sum(1 for _ in f)
                count = 32 if count > 32 else count
                objetos_por_imagem.append(count)

    # Gerar histograma
    plt.figure(figsize=(8, 5))
    plt.hist(objetos_por_imagem, bins=range(0, max(objetos_por_imagem)+2), edgecolor='black', align='left')
    plt.title("Distribuição de Objetos por Imagem")
    plt.xlabel("Número de Objetos")
    plt.ylabel("Quantidade de Imagens")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Contar quantas imagens têm X objetos
    contagem = Counter(objetos_por_imagem)

    # Ordenar pelo número de objetos
    objetos = sorted(contagem.keys())
    frequencias = [contagem[qtd] for qtd in objetos]

    # Gerar gráfico de barras
    plt.figure(figsize=(8, 5))
    plt.bar(objetos, frequencias, color='skyblue', edgecolor='black')
    plt.title("Quantidade de Imagens por Número de Objetos")
    plt.xlabel("Número de Objetos na Imagem")
    plt.ylabel("Quantidade de Imagens")
    plt.xticks(objetos)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
else:
    print("Diretório de labels não encontrado. Por favor, envie a pasta 'train/labels'.")
