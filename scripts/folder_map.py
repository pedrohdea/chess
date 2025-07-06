import os

def gerar_mapa_pasta(diretorio_base, arquivo_saida):
    with open(arquivo_saida, "w", encoding="utf-8") as f_out:
        for root, dirs, files in os.walk(diretorio_base):
            nivel = root.replace(diretorio_base, "").count(os.sep)
            indent = "│   " * nivel + "├── "
            f_out.write(f"{indent}{os.path.basename(root)}/\n")
            sub_indent = "│   " * (nivel + 1)
            for file in files:
                f_out.write(f"{sub_indent}├── {file}\n")

# Caminho da pasta que você quer mapear
diretorio = "."

# Nome do arquivo de saída
arquivo_saida = "mapa_da_pasta.txt"

gerar_mapa_pasta(diretorio, arquivo_saida)
