# Importando a classe vértice e a Uninion
from Vertice import Vertice
from typing import Union

# Criando a classe Aresta
class Aresta:

  def __init__(self, vertice1: Vertice, vertice2: Vertice, peso: int = Union[None, int], direcionado: bool = True) -> None:
    self.vertice1 = vertice1
    self.vertice2 = vertice2
    self.peso = peso
    self.direcionado = direcionado