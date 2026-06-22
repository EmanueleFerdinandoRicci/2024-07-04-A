from dataclasses import dataclass

from model.sighting import Sighting


@dataclass
class Arco:
    s1: Sighting
    s2: Sighting