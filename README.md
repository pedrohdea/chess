# Xadrez Automatizado com OpenCV e Arduino

Este projeto tem como objetivo construir um sistema de xadrez físico automatizado que utiliza **visão computacional (OpenCV)** para detectar movimentos no tabuleiro e **Stockfish**, uma poderosa engine de xadrez, para calcular a melhor jogada. O sistema então **sinaliza a jogada da máquina através de LEDs** controlados por um microcontrolador (ex: Arduino ou ESP32).

---

## Funcionalidades

- Detecção de movimento das peças no tabuleiro usando OpenCV;
- Reconhecimento da jogada realizada pelo jogador humano;
- Cálculo da melhor jogada via engine **Stockfish**;
- Indicação visual da jogada da máquina com **LEDs** conectados ao Arduino.

---

## Requisitos

- Python 3.8+
- [Stockfish Chess Engine](https://stockfishchess.org/download/linux/)
- OpenCV
- Arduino IDE
- Docker (opcional para uso em ambiente isolado)

---

## Instalação

1. Instale o Stockfish:

```bash
sudo apt install stockfish
```

Ou baixe diretamente do site:  [https://stockfishchess.org/download/linux/](https://stockfishchess.org/download/linux/)

2. Instale as dependências do Python:

```bash
. install.sh
```

(O script `install.sh` deve conter os comandos para instalar `opencv-python`, `numpy`, `python-chess`, `pyserial`, etc.)

---

## Treinamento e Detecção de Peças (OpenCV)

Você pode usar ferramentas como `opencv_createsamples` e `opencv_traincascade` para treinar detectores em cascata para as peças de xadrez:

```bash
opencv_createsamples -info pos.dat -w 24 -h 24 -num 1000 -vec pos.vec

opencv_traincascade -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 200 -numNeg 100

# Exemplo com menos imagens (rápido para testes)
opencv_traincascade -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -numPos 20 -numNeg 500 -numStages 10
```

Você também pode utilizar a API do **Roboflow** para detecção de imagens:

```bash
base64 negativas/1701128875.2898896.jpg | curl -d @- "https://detect.roboflow.com/chess-4jvm8/1?api_key=Yc9P3iOmEuSts3mFZLd3"
```

## Treinamento com ROBOFLOW:
```
yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=100 imgsz=640,360 augment=True
```
---

## Uso com Docker

Se desejar isolar o ambiente com Docker:

```bash
docker compose run opencv
cd app/
```

---

## Referências

- [Chessboard Detection - GitHub](https://github.com/prashantdukecyfi/Chessboard-Detection)
- [Tutorial de Cascade Classifier - OpenCV](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)
- [Vídeo explicativo (YouTube)](https://www.youtube.com/watch?v=XrCAvs9AePM)

---

## Autor

Pedro Henrique de Assumpção  
Engenharia de Controle e Automação – IFRS Campus Farroupilha