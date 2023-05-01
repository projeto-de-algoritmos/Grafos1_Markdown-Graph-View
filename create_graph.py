from models.Graph import Graph, Edge
import pathlib
import re
from models.Note import Note
import random

def criar_grafo(arquivos_teste):
    # Cria um grafo vazio
    grafo = Graph()

    # Obtém a lista de arquivos no diretório
    lista_arquivos = [path for path in pathlib.Path(arquivos_teste).rglob("*.md")]

    grafo_dict = {}
    # Itera sobre a lista de arquivos e cria um nó para cada um
    for nome_arquivo in lista_arquivos:

        # Abre o arquivo e procura por links para outros arquivos
        with open(str(nome_arquivo), "r") as arquivo:
            conteudo = arquivo.read()
            # Encontra todos os links para outros arquivos markdown
            padrao_links = r"\[\[(.*?)\]\]"
            referencias = re.findall(padrao_links, conteudo)

        grafo_dict[nome_arquivo.name[:-3]] = (Note(random.randint(5, 550),random.randint(5, 550), nome_arquivo.name[:-3]), referencias)

    for valor in grafo_dict.values():
         grafo.add_node(valor[0])
         for referencia in valor[1]:
              aresta = Edge(valor[0], grafo_dict[referencia][0])
              grafo.add_edge(aresta)
    return grafo