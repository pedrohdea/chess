import os
import random
import shutil

# Pastas de origem combinadas
pasta_base = "dataset"
subpastas = ["train", "valid", "test"]

# Pasta de saída
pasta_saida = "new_dataset"

# métricas
PERCENT_TRAIN = 0.8 # 80%
PERCENT_VAL = 0.1 # 10%
PERCENT_TEST =  1.0 - (PERCENT_TRAIN + PERCENT_VAL) # 10%


# Função para juntar todas as imagens
def coletar_imagens():
    imagens = []
    for sub in subpastas:
        pasta_imgs = os.path.join(pasta_base, sub, "images")
        for f in os.listdir(pasta_imgs):
            if f.endswith(".jpg"):
                imagens.append(os.path.join(pasta_imgs, f))
    return imagens

# Lista de imagens embaralhada
imagens = coletar_imagens()
random.shuffle(imagens)

# Cálculo das quantidades
total = len(imagens)
qtde_train = int(total * PERCENT_TRAIN) # 80%
qtde_val = int(total * PERCENT_VAL) # 10%
qtde_test = total - qtde_train - qtde_val

# Separar listas
splits = {
    "train": imagens[:qtde_train],
    "val": imagens[qtde_train:qtde_train + qtde_val],
    "test": imagens[qtde_train + qtde_val:]
}

# Criar diretórios de saída
for split in splits:
    os.makedirs(os.path.join(pasta_saida, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(pasta_saida, split, "labels"), exist_ok=True)

# Copiar arquivos
for split, lista_imgs in splits.items():
    for caminho_img in lista_imgs:
        nome_img = os.path.basename(caminho_img)
        nome_lbl = nome_img.replace(".jpg", ".txt")

        # Procurar a label correspondente na estrutura original
        for sub in subpastas:
            possivel_lbl = os.path.join(pasta_base, sub, "labels", nome_lbl)
            if os.path.exists(possivel_lbl):
                src_lbl = possivel_lbl
                break
        else:
            print(f"⚠️ Label não encontrada para {nome_img}, ignorando.")
            continue

        # Destinos
        dst_img = os.path.join(pasta_saida, split, "images", nome_img)
        dst_lbl = os.path.join(pasta_saida, split, "labels", nome_lbl)

        shutil.copy2(caminho_img, dst_img)
        shutil.copy2(src_lbl, dst_lbl)

print("✅ Divisão aleatória finalizada em:", pasta_saida)
