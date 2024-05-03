# Importando módulos
import re
from typing import Union

# Criando a classe Grafo
class Grafo:

  def __init__(self, vertices: Union[None, set] = None, arestas: Union[None, set] = None, direcionado: bool = True) -> None:
    self.vertices = vertices
    self.arestas = arestas
    self.direcionado = direcionado
    self.nVertices = len(vertices) if vertices else 0
    self.nArestas = len(arestas) if arestas else 0

  def __str__(self) -> str:
    return f"Vértices: {self.vertices}\nArestas: {self.arestas}"

  def _verificaFormato(self, grafo: str) -> bool:
    # Extraindo o padrão do formato requerido
    padrao = r"V = \{\d+(?:, \d+)*\}; A = \{\(\d+, \d+\)(?:, \(\d+, \d+\))*\};"
    return bool(re.match(padrao, grafo))
  
  def _extrairValoresDoGrafo(self, grafo: str) -> Union[None, tuple[set, set]]:
    # Se o formato do grafo não for válido, retorna None
    if not self._verificaFormato(grafo):
        return None 
    
    # Extrai os números para V
    numerosVertices = re.search(r"V = \{([^}]*)\}", grafo).group(1)
    vertices = set(map(int, numerosVertices.split(",")))

    # Extrai as tuplas para A
    tuplasArestas = re.findall(r"\((\d+), (\d+)\)", grafo)
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
  
  def _salvaArquivo(self, vertices: set, arestas: set[tuple[int, int]]) -> None:
    grafo = f"V = {vertices}; A = {arestas};"
    with open(f'{self.nomeArquivo_}.txt', 'w') as file:
      file.write(grafo)
      file.close()

  def lerArquivo(self, nomeArquivo: str) -> None:
    # Deixando o nome do arquivo sem o .txt
    self.nomeArquivo_ = nomeArquivo[:-4] if nomeArquivo[-4:] == '.txt' else nomeArquivo
    with open(f'{self.nomeArquivo_}.txt', 'r') as file:
      grafo = file.read()
      file.close()

    # Verificando se o formato do grafo é válido
    if self._verificaFormato(grafo):
      self.vertices, self.arestas = self._extrairValoresDoGrafo(grafo)
      grafoValido, verticesEstanhos = self._verificaArestasValidas(self.vertices, self.arestas)

      # Se as arestas não condizem com os vértices, então o grafo não é válido
      if not grafoValido: 
        raise ValueError(f"O grafo não é válido. Há arestas com vértices estranhos: {verticesEstanhos}")
      
      # Verifica direcionamento e, se for não direcionado, adiciona as arestas
      if not self.direcionado:
        aux = set()
        for v1, v2 in self.arestas:
          aux.add((v2, v1))
        self.arestas = self.arestas.union(aux)

      # Atualiza o número de vértices e arestas
      self.nVertices = len(self.vertices)
      self.nArestas = len(self.arestas)

    else:
      raise SyntaxError(f"Formato do arquivo incorreto.")
    
  def adicionaVertice(self, vertice: int) -> None:
    # Se o vértice existe, não prosseguimos com a operação
    if vertice in self.vertices:
      print(f"Vértice {vertice} já foi adicionado")
    else:
      if type(vertice) == int:
        self.vertices.add(vertice)
        print(f"Vértice {vertice} adicionado com sucesso")
        self._salvaArquivo(self.vertices, self.arestas)

        self.nVertices += 1


  def removeVertice(self, vertice: int) -> None:
    if vertice not in self.vertices:
      raise ValueError(f"Você não pode excluir um vértice que ainda não foi adicionado.")
    # Removendo o vértice
    self.vertices.remove(vertice)
    print(f"Vértice {vertice} removido com sucesso.")
    self.nVertices -= 1

    # Excluindo todas as arestas que estavam ligadas ao vértice excluído
    excluirArestas = set()
    for v1, v2 in self.arestas:
      if vertice == v1 or vertice == v2:
        excluirArestas.add((v1, v2))
        self.nArestas -= 1
    self.arestas = self.arestas.difference(excluirArestas)

    self._salvaArquivo(self.vertices, self.arestas)
  
  def adicionaAresta(self, aresta: tuple[int, int]) -> None:
    if aresta in self.arestas:
      print(f"Aresta {aresta} já foi adicionada.")
    else:
      # Verificando o tipo da aresta
      if type(aresta) == tuple:
        if len(aresta) == 2 and type(aresta[0]) == int and type(aresta[1]) == int:
          self.arestas.add(aresta)
          self.nArestas += 1

          # Se for não direcionado, adicionamos o outro par de aresta complementar (para ter ida e volta)
          if not self.direcionado:
            self.arestas.add((aresta[1], aresta[0]))
            self.nArestas += 1
            print(f"Arestas {aresta} e {(aresta[1], aresta[0])} adicionadas com sucesso.")
          else:
            print(f"Aresta {aresta} adicionada com sucesso")

          self._salvaArquivo(self.vertices, self.arestas)

        else:
          raise ValueError("Apenas dois inteiros são válidos por tupla.")
      else:
        raise TypeError("As arestas precisam ser tuplas! Siga o formato (n1,n2), com n1 e n2 inteiros.")

  def removeAresta(self, aresta: tuple[int, int]) -> None:
    if aresta not in self.arestas:
      raise ValueError(f"Você não pode excluir uma aresta que ainda não foi adicionada.")
    
    # Removendo a aresta
    self.vertices.remove(aresta)
    self.nArestas -= 1
    
    # Se o grafo for não direcionado, excluímos a aresta complementar (para não ter nem ida nem volta)
    if not self.direcionado:
      self.vertices.remove((aresta[1], aresta[0]))
      self.nArestas -= 1
      print(f"Arestas {aresta} e {(aresta[1], aresta[0])} removidas com sucesso.")
    else:
      print(f"Aresta {aresta} removida com sucesso.")

    self._salvaArquivo(self.vertices, self.arestas)

  def verGrau(self, vertice: int) -> int:
    if vertice not in self.vertices:
      raise ValueError(f"Vértice {vertice} não pertence ao grafo.")
    
    # Percorrendo as arestas e contando as vezes que o vértice está presente
    grau = 0
    for aresta in self.arestas:
      grau += 1 if vertice in aresta else 0
    
    # Se for direcionado, retornamos o grau. Se for não direcionado, dividimos por 2, pois contamos duas vezes
    return grau if self.direcionado else int(grau/2)

  def listaAdjacencia(self) -> dict:
    # Inicializamos um dicionário para cada vértice e um conjunto vazio associado a ele
    lista = {vertice: set() for vertice in self.vertices}
    for v1, v2 in self.arestas:
      lista[v1].add(v2)
    return lista
  
  def matrizAdjacencia(self) -> list[list]:
    # Inicializando uma matriz nxn, sendo n o número de vértices
    matriz = [[0]*len(self.vertices)]*len(self.vertices)
    for v1, v2 in self.arestas:
      matriz[v1-1][v2-1] = 1
    return matriz