# Importando a classe Union
from typing import Union

# Criando a classe Vértice
class Vertice:
  def __init__(self, valor: int, vizinhos: set = set(), grau: int = 0, cor: str = "branco") -> None:
    self.valor = valor
    self.vizinhos = vizinhos
    self.grau = grau
    assert cor in ["branco", "cinza", "preto"], f"Cor só aceita as opções 'branco', 'cinza' e 'preto'. Você digitou {cor}"
    self.cor = cor

  def __repr__(self) -> str:
    return f"Vertice({self.valor})"
  
  def __eq__(self, outroVertice) -> bool:
    return self.valor == outroVertice.valor
  
  def __hash__(self):
    return hash((self.valor))