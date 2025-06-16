# settings.py
from dataclasses import dataclass


@dataclass
class Configurations:
    DIVISAODEGRADIENTE: float = None
    ENDERECO_USB: str = "/dev/ttyACM0"


conf = Configurations()
