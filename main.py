# Importando a classe Grafo
from graph import Grafo

# Inicializando o programa
opcao = ""

while opcao not in ["1", "2"]:
  opcao = input("O grafo é direcionado? (1 - Sim | 2 - Não): ")
  if opcao in ["1", "2"]:
    opcao = True if opcao == "1" else False
    break
  else:
    print(f"Os valores válidos são apenas '1' e '2', você digitou '{opcao}'. Tente novamente.")

grafo = Grafo(direcionado = opcao)
grafo.lerArquivo("grafo.txt")
grafo.adicionaVertice(3)
grafo.adicionaVertice(6)
print(grafo)
grafo.adicionaAresta((6, 1))
print(grafo)
grafo.adicionaAresta((2, 6))
print(grafo)
grafo.removeVertice((6))
print(grafo)
print(grafo.nVertices)
print(grafo.nArestas)
print(grafo.verGrau(1))