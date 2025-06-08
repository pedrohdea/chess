# Usa a imagem oficial com YOLOv8 + Python pré-instalado
FROM ultralytics/ultralytics:latest

# Define diretório de trabalho
WORKDIR /workspace

# Copia o dataset (opcional — melhor montar via volume)
# COPY ./dataset /workspace/dataset

# Comando padrão: apenas abre shell
CMD ["bash"]
