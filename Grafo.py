# Importando módulos
import re
from typing import Union
from Vertice import Vertice
from Aresta import Aresta

# Criando a classe Grafo
class Grafo:

  def __init__(self, vertices: Union[None, set[Vertice]] = None, arestas: Union[None, set[Aresta]] = None, direcionado: bool = True) -> None:
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
    vertices = set(map(int, numerosVertices.split(", ")))

    # Extrai as tuplas para A
    tuplasArestas = re.findall(r"\((\d+), (\d+)\)", grafo)
    arestas = set(Aresta(vertice1 = Vertice(valor = int(x), grau = 0), vertice2 = Vertice(valor = int(y), grau = 0), direcionado = self.direcionado) for x, y in tuplasArestas)

    # Construir os objetos de Vertice e Aresta
    conjuntoVertices = set()
    for aresta in arestas:
      v1 = aresta.vertice1
      v2 = aresta.vertice2
      conjuntoVertices.add(v1)
      conjuntoVertices.add(v2)

    return conjuntoVertices, arestas
  
  def _vizinhosDoVertice(self, vertice: Vertice) -> set[Vertice]:
    vizinhos = set()
    for aresta in self.arestas:
      if vertice == aresta.vertice1:
        vizinhos.add(aresta.vertice2)
      elif vertice == aresta.vertice2:
        vizinhos.add(aresta.vertice1)
    return vizinhos
  
  def _verificaArestasValidas(self, vertices: set[Vertice], arestas: set[Aresta]) -> tuple[bool, set[Vertice]]:
    # Verificando os vértices únicos que estão compondo as arestas
    verticesEstranhos, verticesArestas = set(), set()
    for aresta in arestas:
      verticesArestas.add(aresta.vertice1)
      verticesArestas.add(aresta.vertice2)

    # Se houver vértices que estão nas arestas, mas não estão nos vértices, armazenamos em verticesEstranhos
    verticesEstranhos = verticesArestas.difference(vertices)

    return verticesArestas.issubset(vertices), verticesEstranhos
  
  def _salvaArquivo(self, vertices: set[Vertice], arestas: set[Aresta]) -> None:
    conjuntoVertices = set()
    for vertice in vertices:
      conjuntoVertices.add(vertice.valor)
    
    conjuntoArestas = set()
    for aresta in arestas:
      conjuntoArestas.add((aresta.vertice1.valor, aresta.vertice2.valor))

    grafo = f"V = {conjuntoVertices}; A = {conjuntoArestas};"
    with open(f'{self.nomeArquivo_}_resultado.txt', 'w') as file:
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
        for aresta in self.arestas:
          aux.add(Aresta(vertice1 = aresta.vertice2, vertice2 = aresta.vertice1, direcionado = self.direcionado))
        self.arestas = self.arestas.union(aux)

      # Adicionar vizinhos
      for vertice in self.vertices:
        vertice.vizinhos = self._vizinhosDoVertice(vertice)

      # Adiciona o número de graus no vértice
      for vertice in self.vertices:
        vertice.grau = self.verGrau(vertice)

      # Atualiza o número de vértices e arestas
      self.nVertices = len(self.vertices)
      self.nArestas = len(self.arestas)

    else:
      raise SyntaxError(f"Formato do arquivo incorreto.")
    
  def adicionaVertice(self, vertice: Vertice) -> None:
    # Verifica o grau do vértice
    if vertice.grau != 0:
      raise ValueError(f"O grau de um novo vértice deve ser 0.")
    
    # Se o vértice existe, não prosseguimos com a operação
    if vertice in self.vertices:
      print(f"Vértice {vertice} já foi adicionado")
    else:
      if type(vertice) == Vertice:
        self.vertices.add(vertice)
        print(f"Vértice {vertice} adicionado com sucesso")
        self._salvaArquivo(self.vertices, self.arestas)

        self.nVertices += 1

  def removeVertice(self, vertice: Vertice) -> None:
    if vertice not in self.vertices:
      raise ValueError(f"Você não pode excluir um vértice que ainda não foi adicionado.")
    # Removendo o vértice
    self.vertices.remove(vertice)
    print(f"Vértice {vertice} removido com sucesso.")
    self.nVertices -= 1

    # Excluindo todas as arestas que estavam ligadas ao vértice excluído
    excluirArestas = set()
    for aresta in self.arestas:
      if vertice == aresta.vertice1 or vertice == aresta.vertice2:
        excluirArestas.add(aresta)
        self.nArestas -= 1
    self.arestas = self.arestas.difference(excluirArestas)

    # Atualiza os graus
    for vertice in self.vertices:
      vertice.grau = self.verGrau(vertice)

    # Salva arquivo
    self._salvaArquivo(self.vertices, self.arestas)
  
  def adicionaAresta(self, aresta: Aresta) -> None:
    if aresta in self.arestas:
      print(f"Aresta {aresta} já pertence ao grafo.")
    else:
      # Verificando o tipo da aresta
      if type(aresta) == Aresta:
        if aresta.vertice1 in self.vertices and aresta.vertice2 in self.vertices:
          self.arestas.add(aresta)
          self.nArestas += 1

          # Se for não direcionado, adicionamos o outro par de aresta complementar (para ter ida e volta)
          if not self.direcionado:
            self.arestas.add(Aresta(vertice1 = aresta.vertice2, vertice2 = aresta.vertice1, direcionado = self.direcionado))
            self.nArestas += 1
            print(f"Arestas {aresta} e {Aresta(vertice1 = aresta.vertice2, vertice2 = aresta.vertice1)} adicionadas com sucesso.")
          else:
            print(f"Aresta {aresta} adicionada com sucesso.")

          # Atualiza os graus
          for vertice in self.vertices:
            vertice.grau = self.verGrau(vertice)
          
          # Salva o arquivo
          self._salvaArquivo(self.vertices, self.arestas)
        else:
          verticesNaoPertencentes = {aresta.vertice1, aresta.vertice2}.difference(self.vertices)
          raise ValueError(f"O(s) vértice(s) {verticesNaoPertencentes} não pertence(m) ao grafo.")
      else:
        raise TypeError("As arestas precisam ser do tipo Aresta!")

  def removeAresta(self, aresta: Aresta) -> None:
    if aresta not in self.arestas:
      raise ValueError(f"Você não pode excluir uma aresta que ainda não foi adicionada.")
    
    # Removendo a aresta
    self.arestas.remove(aresta)
    self.nArestas -= 1
    
    # Se o grafo for não direcionado, excluímos a aresta complementar (para não ter nem ida nem volta)
    if not self.direcionado:
      self.vertices.remove(Aresta(vertice1 = aresta.vertice2, vertice2 = aresta.vertice1))
      self.nArestas -= 1
      print(f"Arestas {aresta} e {Aresta(vertice1 = aresta.vertice2, vertice2 = aresta.vertice1)} removidas com sucesso.")
    else:
      print(f"Aresta {aresta} removida com sucesso.")

    # Atualiza os graus
    for vertice in self.vertices:
      vertice.grau = self.verGrau(vertice)

    # Salva o arquivo
    self._salvaArquivo(self.vertices, self.arestas)

  def verGrau(self, vertice: Vertice) -> int:
    if vertice not in self.vertices:
      raise ValueError(f"Vértice {vertice} não pertence ao grafo.")
    
    # Percorrendo as arestas e contando as vezes que o vértice está presente
    grau = 0
    for aresta in self.arestas:
      grau += 1 if vertice in (aresta.vertice1, aresta.vertice2) else 0
    
    # Se for direcionado, retornamos o grau. Se for não direcionado, dividimos por 2, pois contamos duas vezes
    return grau if self.direcionado else int(grau/2)

  def listaAdjacencia(self) -> dict:
    # Inicializamos um dicionário para cada vértice e um conjunto vazio associado a ele
    lista = {vertice: set() for vertice in self.vertices}
    for aresta in self.arestas:
      lista[aresta.vertice1].add(aresta.vertice2)
    return lista
  
  def matrizAdjacencia(self) -> list[list[int]]:
    # Inicializando uma matriz nxn, sendo n o número de vértices
    matriz = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
    for aresta in self.arestas:
      matriz[aresta.vertice1.valor-1][aresta.vertice2.valor-1] = 1
    return matriz