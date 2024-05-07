# Importando a classe vértice e a Uninion
from Vertice import Vertice
from typing import Union

# Criando a classe Aresta
class Aresta:
  def __init__(self, vertice1: Vertice, vertice2: Vertice, peso: Union[None, int] = None, direcionado: bool = True) -> None:
    self.vertice1 = vertice1
    self.vertice2 = vertice2
    self.peso = peso
    self.direcionado = direcionado

  def __repr__(self) -> str:
    return f"{self.vertice1} -> {self.vertice2}"
  
  def __eq__(self, outraAresta) -> bool:
    return self.vertice1 == outraAresta.vertice1 and self.vertice2 == outraAresta.vertice2
  
  def __hash__(self) -> int:
    return hash((self.vertice1, self.vertice2))