

# Criando a classe Vértice
class Vertice:
  def __init__(self, valor: int, vizinhos: set, grau: int = 0) -> None:
    self.valor = valor
    self.vizinhos = vizinhos
    self.grau = grau