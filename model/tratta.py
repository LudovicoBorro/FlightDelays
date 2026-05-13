from dataclasses import dataclass
from model.airport import Airport

@dataclass
class Tratta:
    aeroportoP: Airport
    aeroportoA: Airport
    peso: int

    def __hash__(self):
        hash((self.aeroportoA, self.aeroportoP))

    def __eq__(self, other):
        return self.aeroportoP == other.aeroportoP and self.aeroportoA == other.aeroportoA

    def __str__(self):
        pass