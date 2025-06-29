# settings.py
from dataclasses import dataclass


@dataclass
class Configurations:
    DIVISAODEGRADIENTE: float = 0.5
    ENDERECO_USB: str = "/dev/ttyACM0"


conf = Configurations()
