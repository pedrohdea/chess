import numpy as np

def get_vertices(box):
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    x = x1 + w / 2
    y = y1 + h / 2
    return int(x), int(y), int(w), int(h)


class Peca:
    def __init__(self, det: np.ndarray):
        # Corrige as coordenadas da predição ONNX para o espaço original da imagem
        x1, y1, x2, y2 = det[0:4]

        w = x2 - x1
        h = y2 - y1
        x = x1
        y = y1

        self.vertice = (int(x), int(y), int(w), int(h))
        self.area = int(w) * int(h)
        self.multi = x * y
        self.confidence = det[4]
        self.class_id = int(det[5])

    @property
    def x(self):
        return self.vertice[0]

    @property
    def y(self):
        return self.vertice[1]

    @property
    def w(self):
        return self.vertice[2]

    @property
    def h(self):
        return self.vertice[3]

    @property
    def center(self) -> tuple[int, int]:
        cx = self.x + self.w // 2
        cy = self.y + self.h // 2
        return cx, cy

    def __repr__(self) -> str:
        return f"<{self.vertice}>"

    def __eq__(self, other) -> bool:
        return self.multi == other.multi

    def __gt__(self, other) -> bool:
        return self.multi > other.multi

    def __lt__(self, other) -> bool:
        return self.multi < other.multi
