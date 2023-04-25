import pygame
import pygame_gui
import sys
import math

from models.Graph import Graph, Edge
from models.Note import Note


pygame.init()

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

def draw_nodes(graph: Graph):
    for node, neighbors in graph.adj_list.items():
        pygame.draw.circle(screen, node.color, (node.x, node.y), node.radius)
        if node.text is not None: # if the node has text
            font = pygame.font.SysFont(None, 20)
            if node.color != WHITE:
                text_surface = font.render(node.text, True, WHITE)
            else:
                text_surface = font.render(node.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(node.x, node.y)) # get the rectangle that centers the text surface on the node position
            screen.blit(text_surface, text_rect) # blit the text surface onto the screen at the text rectangle position
        font = pygame.font.SysFont(None, 20)
        label = font.render(node.filename, True, (255,255,255))
        screen.blit(label, (node.x - label.get_width() // 2, node.y - 20 - label.get_height()))


def draw_arrow(screen, edge):
    start_node = edge.start_node
    end_node = edge.end_node

    # calculate the angle between the two nodes
    angle = math.atan2(end_node.y - start_node.y, end_node.x - start_node.x)

    # calculate the coordinates of the start and end points of the arrow
    start_x = start_node.x + start_node.radius * math.cos(angle)
    start_y = start_node.y + start_node.radius * math.sin(angle)
    end_x = end_node.x - end_node.radius * math.cos(angle)
    end_y = end_node.y - end_node.radius * math.sin(angle)

    # draw the line
    pygame.draw.line(screen, edge.color, (start_x, start_y), (end_x, end_y), 1)

    # draw the arrowhead
    arrow_size = 10
    arrow_angle = math.pi / 6
    dx = arrow_size * math.cos(angle + arrow_angle)
    dy = arrow_size * math.sin(angle + arrow_angle)
    point1 = (end_x - dx, end_y - dy)
    dx = arrow_size * math.cos(angle - arrow_angle)
    dy = arrow_size * math.sin(angle - arrow_angle)
    point2 = (end_x - dx, end_y - dy)
    pygame.draw.polygon(screen, edge.color, [point1, point2, (end_x, end_y)])


def draw_edges(graph: Graph):
    for edge in graph.edge_list:
        draw_arrow(screen, edge)


def update_node_positions(graph: Graph, min_distance=100):
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

def handle_events(graph: Graph, counter: int):
    node_list = graph.get_nodes()
    edge_list = graph.edge_list
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for node in node_list:
                if node.dragging == False:
                    if event.button == 1:
                        if node.x - node.radius <= event.pos[0] <= node.x + node.radius and node.y - node.radius <= event.pos[1] <= node.y + node.radius:
                            if node.color == GREEN:
                                node.text = None
                                counter-=1
                            node.dragging = True
                            node.color = RED # change node color when it is being dragged
                    elif event.button == 3:
                        if node.x - node.radius <= event.pos[0] <= node.x + node.radius and node.y - node.radius <= event.pos[1] <= node.y + node.radius:
                                if node.color == GREEN:
                                    node.color = WHITE 
                                    node.text = None
                                    counter-=1
                                else:
                                    if counter <= 2:
                                        node.color = GREEN # change node color to green on right-click
                                        node.text = str(counter) # set node COUNTER to current value of counter
                                        return counter + 1
        elif event.type == pygame.MOUSEBUTTONUP:
            for node in node_list:
                if node.dragging == True:
                    node.dragging = False
                    if node.color == RED:
                        node.color = WHITE
                    
        elif event.type == pygame.MOUSEMOTION:
            for node in node_list:
                if node.dragging == True:
                    node.update_position(event.pos[0], event.pos[1])
            update_node_positions(graph)
        elif event.type == pygame.VIDEORESIZE:
            # If the screen is resized, update the screen size
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    return counter

main_graph = Graph()

notas = [
    Note(100, 120, 'Bancos de dados relacionais'),
    Note(120, 140, 'Declaracoes'),
    Note(140, 160, 'Instroducao ao SQL'),
    Note(160, 180, 'Tipo de dado'),
    Note(180, 200, 'Node2'),
    Note(200, 220, 'Node3'),
    Note(220, 240, 'Node4'),
    Note(240, 260, 'Node5'),
    Note(260, 260, 'Node5'),
    Note(280, 260, 'Node5'),
    Note(300, 260, 'Node5'),
    Note(320, 260, 'Node5'),
]

arestas = [
    Edge(notas[0], notas[1]),
    Edge(notas[1], notas[0]),
    Edge(notas[2], notas[1]),
    Edge(notas[2], notas[3]),
    Edge(notas[3], notas[1]),
    Edge(notas[4], notas[1]),
    Edge(notas[2], notas[6]),
    Edge(notas[5], notas[6]),
    Edge(notas[7], notas[6]),
]

for nota in notas:
    main_graph.add_node(nota)

for aresta in arestas:
    main_graph.add_edge(aresta)


running = True
counter = 1
while True:
    counter = handle_events(main_graph, counter)
    screen.fill((0, 0, 0))
    draw_edges(main_graph)
    draw_nodes(main_graph)
    pygame.display.update()

# Quit pygame
pygame.quit()