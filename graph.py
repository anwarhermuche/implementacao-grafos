# Importando módulos
import re
from typing import Union

# Criando a classe Grafo
class Grafo:

  def __init__(self, vertices: Union[None, set] = None, arestas: Union[None, set] = None, direcionado: bool = True) -> None:
    self.vertices = vertices
    self.arestas = arestas
    self.direcionado = direcionado

  def _verificaFormato(self, grafo: str) -> bool:
    # Extraindo o padrão do formato requerido
    padrao = r"V = \{\d+(?:,\d+)*\}; A = \{\(\d+,\d+\)(?:,\(\d+,\d+\))*\};"
    return bool(re.match(padrao, grafo))
  
  def _extrairValoresDoGrafo(self, grafo: str) -> Union[None, tuple[set, set]]:
    # Se o formato do grafo não for válido, retorna None
    if not self._verificaFormato(grafo):
        return None 
    
    # Extrai os números para V
    numerosVertices = re.search(r"V = \{([^}]*)\}", grafo).group(1)
    vertices = set(map(int, numerosVertices.split(",")))

    # Extrai as tuplas para A
    tuplasArestas = re.findall(r"\((\d+),(\d+)\)", grafo)
    arestas = set((int(x), int(y)) for x, y in tuplasArestas)

    return vertices, arestas
  
  def _verificaArestasValidas(self, vertices: set, arestas: set) -> tuple[bool, set]:
    # Verificando os vértices únicos que estão compondo as arestas
    verticesEstranhos, verticesArestas = set(), set()
    for v1, v2 in arestas:
      verticesArestas.add(v1)
      verticesArestas.add(v2)

    # Se houver vértices que estão nas arestas, mas não estão nos vértices, armazenamos em verticesEstranhos
    verticesEstranhos = verticesArestas.difference(vertices)

    return verticesArestas.issubset(vertices), verticesEstranhos

  def lerArquivo(self, nomeArquivo: str) -> None:
    nomeArquivo = nomeArquivo[:-4] if nomeArquivo[-4:] == '.txt' else nomeArquivo
    with open(f'{nomeArquivo}.txt', 'r') as file:
      grafo = file.read()

    if self._verificaFormato(grafo):
      self.vertices, self.arestas = self._extrairValoresDoGrafo(grafo)
      grafoValido, verticesEstanhos = self._verificaArestasValidas(self.vertices, self.arestas)

      # Verificamos se o grafo é válido
      if not grafoValido: 
        raise ValueError(f"O grafo não é válido. Há arestas com vértices estranhos: {verticesEstanhos}")
      
      # Verifica direcionamento e, se for não direcionado, adiciona as arestas
      if not self.direcionado:
        aux = set()
        for v1, v2 in self.arestas:
          aux.add((v2, v1))
        self.arestas = self.arestas.union(aux)

    else:
      raise SyntaxError(f"Formato do arquivo incorreto.")
    
    
  def adicionaNoh(self, vertice: int) -> None:
    if type(vertice) == int:
      self.vertices.add(vertice)
  
  def adicionaAresta(self, aresta: tuple[int, int]) -> None:
    if type(aresta) == tuple:
      if len(aresta) == 2 and type(aresta[0]) == int and type(aresta[1]) == int:
        self.arestas.add(aresta)

  def listaAdjacencia(self) -> dict:
    lista = {vertice: set() for vertice in self.vertices}
    for v1, v2 in self.arestas:
      lista[v1].add(v2)
    return lista
  
  def matrizAdjacencia(self) -> list[list]:
    matriz = [[0]*len(self.vertices)]*len(self.vertices)
    for v1, v2 in self.arestas:
      matriz[v1-1][v2-1] = 1
    return matriz