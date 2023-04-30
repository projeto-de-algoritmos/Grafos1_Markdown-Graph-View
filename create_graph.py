import os
import re
import networkx as nx

def criar_grafo(diretorio):
    # Cria um grafo vazio
    grafo = nx.Graph()

    # Obtém a lista de arquivos no diretório
    lista_arquivos = os.listdir(diretorio)

    # Itera sobre a lista de arquivos e cria um nó para cada um
    for nome_arquivo in lista_arquivos:
        # Cria um nó com o nome do arquivo
        grafo.add_node(nome_arquivo)

        # Abre o arquivo e procura por links para outros arquivos
        with open(os.path.join(diretorio, nome_arquivo), "r") as arquivo:
            conteudo = arquivo.read()
            # Encontra todos os links para outros arquivos markdown
            padrao_links = r"\[\[(.*?)\]\]"
            links_encontrados = re.findall(padrao_links, conteudo)
            # Cria uma aresta para cada link encontrado
            for link in links_encontrados:
                if link in lista_arquivos:
                    grafo.add_edge(nome_arquivo, link)

    return grafo
