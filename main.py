# Importando a classe Grafo
from Grafo import Grafo
from Vertice import Vertice
from Aresta import Aresta

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
grafo.adicionaVertice(Vertice(9))
grafo.adicionaAresta(Aresta(Vertice(9), Vertice(1)))
grafo.removeVertice(Vertice(9))