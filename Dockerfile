FROM chennavarri/ubuntu_opencv_python
FROM ultralytics/ultralytics:latest

WORKDIR /app
COPY . /app/

ENV DISPLAY=10.202.5.30:0

# Copia o dataset (opcional — melhor montar via volume)
COPY ./dataset /workspace/dataset