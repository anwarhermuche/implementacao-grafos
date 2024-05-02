# Inicializando o programa
opcao = ""

while opcao not in ["1", "2"]:
  opcao = input("O grafo é direcionado? (1 - Sim | 2 - Não): ")
  if opcao in ["1", "2"]:
    break
  else:
    print(f"Os valores válidos são apenas '1' e '2', você digitou '{opcao}'. Tente novamente.")

# Lendo o arquivo
with open('grafo.txt', 'r') as file:
  grafo = file.read()

# Conjunto de vértices e tuplas de arestas
try:
  vertices, arestas = grafo.split('; ')
  vertices = eval(vertices.split('= ')[1])
  arestas = eval(arestas.split('= ')[1][:-1])
except Exception as erro:
  print("Formato do arquivo inválido. Certifique-se de que ele segue o seguinte formato:\nV = {n1, n2, ..., n}; A = {(v1, v2), (v3, v4), ..., (vn, vk)}\n")
  print(f"Erro: {erro}")

# TODO: Verificar se os vértices das arestas são válidos

# Verificando se o grafo é não direcionado. Se sim, adicionamos as arestas
if opcao == "2":
  aux = set()
  for v1, v2 in arestas:
    aux.add((v2, v1))
  arestas = arestas.union(aux)

# Faz a matriz de adjacência
def matrizAdjacencia(vertices, arestas):
  matriz = [[0]*len(vertices)]*len(vertices)
  for v1, v2 in arestas:
    matriz[v1-1][v2-1] = 1
  return matriz

# Faz a lista de adjacência
def listaAdjacencia(vertices, arestas):
  lista = {vertice: set() for vertice in vertices}
  for v1, v2 in arestas:
    lista[v1].add(v2)
  return lista

print(matrizAdjacencia(vertices, arestas))
print(listaAdjacencia(vertices, arestas))
print({'oi', 'ola', 'tudo bem', '1'})
