from models.LinkedList import LinkedList
from models.Note import Note
from collections import deque

class Edge:
    def __init__(self, start_node, end_node, color=(255, 255, 255)):
        self.start_node = start_node
        self.end_node = end_node
        self.color = color
        self.spring_constant = 0.01

    def __str__(self):
        return f"({str(self.start_node)}, {str(self.end_node)})"

    def __repr__(self):
        return str(self)

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.edge_list = []

    def __str__(self):
        result = ''
        for node, neighbors in self.adj_list.items():
            result += str(node) + ': '
            for neighbor in neighbors:
                result += str(neighbor) + '->'
            result += '\n'
        return result

    def get_nodes(self):
        return list(self.adj_list.keys())

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = LinkedList()

    def add_edge(self, edge):
        self.edge_list.append(edge)
        if edge.start_node not in self.adj_list:
            self.add_node(edge.start_node)
        if edge.end_node not in self.adj_list:
            self.add_node(edge.end_node)
        self.adj_list[edge.start_node].add_node(edge.end_node)
        self.adj_list[edge.end_node].add_node(edge.start_node)

    def bfs(self, start_node, end_node):
        visited = set()
        queue = []
        parent = {}
        queue.append(start_node)
        visited.add(start_node)

        while queue:
            curr_node = queue.pop(0)
            if curr_node == end_node:
                path = []
                while curr_node != start_node:
                    path.append(curr_node)
                    curr_node = parent[curr_node]
                path.append(start_node)
                path.reverse()
                return path
            neighbors = self.adj_list[curr_node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = curr_node
        return None



if __name__ == '__main__':
    nosso_grafo = Graph()

    notas = [
        Note('Bancos de dados relacionais'),
        Note('Declaracoes'),
        Note('Instroducao ao SQL'),
        Note('Tipo de dado')
    ]

    arestas = [
        Edge(notas[0], notas[1]),
        Edge(notas[2], notas[3])
    ]

    for nota in notas:
        nosso_grafo.add_node(nota)

    for aresta in arestas:
        nosso_grafo.add_edge(aresta)

    print(str(nosso_grafo)  + "\n\n")
    
    start_node = notas[0]
    end_node = notas[1]

    path = nosso_grafo.bfs(start_node, end_node)
    
    for i in path:
        print(i)