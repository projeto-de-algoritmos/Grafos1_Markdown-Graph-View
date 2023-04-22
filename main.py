import pygame
import sys

from models.Graph import Graph, Edge
from models.Note import Note

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_nodes(graph: Graph):
    for node, neighbors in graph.adj_list.items():
        pygame.draw.circle(screen, node.color, (node.x, node.y), node.size)
        font = pygame.font.SysFont(None, 20)
        label = font.render(node.filename, True, (255,255,255))
        screen.blit(label, (node.x - label.get_width() // 2, node.y - 20 - label.get_height()))

def draw_edges(graph: Graph):
    for edge in graph.edge_list:
        pygame.draw.line(screen, edge.color, (edge.node1.x, edge.node1.y), (edge.node2.x, edge.node2.y), 2)

def update_node_positions(graph: Graph, min_distance=50):
    # calculate force vectors between nodes
    node_list = graph.get_nodes()
    for i in range(len(node_list)):
        for j in range(i+1, len(node_list)):
            node1 = node_list[i]
            node2 = node_list[j]
            dx = node1.x - node2.x
            dy = node1.y - node2.y
            dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            if dist < min_distance:
                force = 1000 / dist ** 2 # adjust the force factor as needed
                node1_x_force = force * dx / dist
                node1_y_force = force * dy / dist
                node2_x_force = -node1_x_force
                node2_y_force = -node1_y_force
                node1.x += node1_x_force
                node1.y += node1_y_force
                node2.x += node2_x_force
                node2.y += node2_y_force


def handle_events(graph: Graph):
    node_list = graph.get_nodes()
    edge_list = graph.edge_list
    node_color = (255, 255, 255) # initialize node_color variable
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for node in node_list:
                if node.dragging == False:
                    if event.button == 1:
                        if node.x - 20 <= event.pos[0] <= node.x + 20 and node.y - 20 <= event.pos[1] <= node.y + 20:
                            node.dragging = True
                            node_color = node.color
                            node.color = (255, 0, 0) # change node color when it is being dragged
                    elif event.button == 3:
                        # right-click to delete node
                        if node.x - 20 <= event.pos[0] <= node.x + 20 and node.y - 20 <= event.pos[1] <= node.y + 20:
                            node_list.remove(node)
                            # remove edges connected to the deleted node
                            for edge in edge_list:
                                if edge.start_node == node or edge.end_node == node:
                                    edge_list.remove(edge)
        elif event.type == pygame.MOUSEBUTTONUP:
            for node in node_list:
                if node.dragging == True:
                    node.dragging = False
                    node.color = node_color
        elif event.type == pygame.MOUSEMOTION:
            for node in node_list:
                if node.dragging == True:
                    node.update_position(event.pos[0], event.pos[1])
    # update node positions based on repelling forces
    update_node_positions(graph)


main_graph = Graph()

notas = [
    Note(100, 120, 'Bancos de dados relacionais'),
    Note(120, 140, 'Declaracoes'),
    Note(140, 160, 'Instroducao ao SQL'),
    Note(160, 180, 'Tipo de dado')
]

arestas = [
    Edge(notas[0], notas[1]),
    Edge(notas[2], notas[3])
]

for nota in notas:
    main_graph.add_node(nota)

for aresta in arestas:
    main_graph.add_edge(aresta)

while True:
    handle_events(main_graph)
    screen.fill((0, 0, 0))
    draw_nodes(main_graph)
    draw_edges(main_graph)
    pygame.display.update()
