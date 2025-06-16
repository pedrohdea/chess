import os

def contar_imagens_e_objetos(imagens_dir, labels_dir):
    total_imagens = len([f for f in os.listdir(imagens_dir) if f.endswith(('.jpg', '.png'))])
    total_objetos = 0
    for label_file in os.listdir(labels_dir):
        if label_file.endswith('.txt'):
            with open(os.path.join(labels_dir, label_file)) as f:
                total_objetos += sum(1 for _ in f)
    return total_imagens, total_objetos

# Caminhos corrigidos
train_imgs, train_objs = contar_imagens_e_objetos("dataset/train/images", "dataset/train/labels")
val_imgs, val_objs = contar_imagens_e_objetos("dataset/valid/images", "dataset/valid/labels")
test_imgs = len([f for f in os.listdir("dataset/test/images") if f.endswith(('.jpg', '.png'))])

print(f"Treino: {train_imgs} imagens, {train_objs} objetos")
print(f"Validação: {val_imgs} imagens, {val_objs} objetos")
print(f"Teste: {test_imgs} imagens")

import os
import hashlib

def calcular_hash_arquivo(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def remover_duplicatas_em_pasta(imagens_dir, labels_dir):
    print(f"\nVerificando duplicatas em: {imagens_dir}")
    hash_imagens = {}
    imagens_removidas = []

    # 1. Verificar imagens duplicadas
    for nome in os.listdir(imagens_dir):
        if nome.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(imagens_dir, nome)
            hash_val = calcular_hash_arquivo(path)
            if hash_val in hash_imagens:
                os.remove(path)
                imagens_removidas.append(nome)
                # Remover label correspondente
                label_path = os.path.join(labels_dir, nome.rsplit('.', 1)[0] + '.txt')
                if os.path.exists(label_path):
                    os.remove(label_path)
            else:
                hash_imagens[hash_val] = nome

    print(f"{len(imagens_removidas)} imagens duplicadas removidas.")

    # 2. Verificar labels duplicados
    print(f"Verificando duplicatas em: {labels_dir}")
    hash_labels = {}
    labels_removidas = []

    for nome in os.listdir(labels_dir):
        if nome.endswith('.txt'):
            path = os.path.join(labels_dir, nome)
            hash_val = calcular_hash_arquivo(path)
            if hash_val in hash_labels:
                os.remove(path)
                labels_removidas.append(nome)
            else:
                hash_labels[hash_val] = nome

    print(f"{len(labels_removidas)} arquivos .txt duplicados removidos.")

# Aplicar nos 3 conjuntos
remover_duplicatas_em_pasta("dataset/train/images", "dataset/train/labels")
remover_duplicatas_em_pasta("dataset/valid/images", "dataset/valid/labels")
remover_duplicatas_em_pasta("dataset/test/images", "dataset/test/labels")
