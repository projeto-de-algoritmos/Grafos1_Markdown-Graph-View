from LinkedList import LinkedList
from Note import Note
from collections import deque

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        return f"({str(self.node1)}, {str(self.node2)})"

    def __repr__(self):
        return str(self)

class Graph:
    def __init__(self):
        self.adj_list = {}

    def __str__(self):
        result = ''
        for node, neighbors in self.adj_list.items():
            result += str(node) + ': '
            for neighbor in neighbors:
                result += str(neighbor) + '->'
            result += '\n'
        return result

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = LinkedList()

    def add_edge(self, edge):
        if edge.node1 not in self.adj_list:
            self.add_node(edge.node1)
        if edge.node2 not in self.adj_list:
            self.add_node(edge.node2)
        self.adj_list[edge.node1].add_node(edge.node2)

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
    
    node1 = notas[0]
    node2 = notas[1]

    path = nosso_grafo.bfs(node1, node2)
    
    for i in path:
        print(i)