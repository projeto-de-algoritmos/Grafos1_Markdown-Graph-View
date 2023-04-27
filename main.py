import pygame
import sys
import math
import random

from models.Graph import Graph, Edge
from models.Note import Note


pygame.init()

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH), pygame.RESIZABLE)

def draw_nodes(screen, graph: Graph):
    for node, neighbors in graph.adj_list.items():
        pygame.draw.circle(screen, node.color, (node.x, node.y), node.radius)
        font = pygame.font.SysFont(None, 20)
        label = font.render(node.filename, True, (255,255,255))
        screen.blit(label, (node.x - label.get_width() // 2, node.y - 20 - label.get_height()))

def draw_arrow(screen, edge):
    start_node = edge.start_node
    end_node = edge.end_node

    angle = math.atan2(end_node.y - start_node.y, end_node.x - start_node.x)

    start_x = start_node.x + start_node.radius * math.cos(angle)
    start_y = start_node.y + start_node.radius * math.sin(angle)
    end_x = end_node.x - end_node.radius * math.cos(angle)
    end_y = end_node.y - end_node.radius * math.sin(angle)

    # draw the line
    pygame.draw.line(screen, edge.color, (start_x, start_y), (end_x, end_y), 1)

    # draw the arrowhead
    arrow_size = 5
    arrow_angle = math.pi / 6
    dx = arrow_size * math.cos(angle + arrow_angle)
    dy = arrow_size * math.sin(angle + arrow_angle)
    point1 = (end_x - dx, end_y - dy)
    dx = arrow_size * math.cos(angle - arrow_angle)
    dy = arrow_size * math.sin(angle - arrow_angle)
    point2 = (end_x - dx, end_y - dy)
    pygame.draw.polygon(screen, edge.color, [point1, point2, (end_x, end_y)])

def draw_edges(screen, graph: Graph):
    for edge in graph.edge_list:
        draw_arrow(screen, edge)

def update_node_positions(screen, graph: Graph, min_distance=100):

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

        if node1.x - node1.radius < 0:
            node1.x = node1.radius
        elif node1.x + node1.radius > screen.get_width():
            node1.x = screen.get_width() - node1.radius
        if node1.y - node1.radius < 0:
            node1.y = node1.radius
        elif node1.y + node1.radius > screen.get_height():
            node1.y = screen.get_height() - node1.radius

def handle_events(screen, graph: Graph):
    node_list = graph.get_nodes()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for node in node_list:
                if node.dragging == False:
                    if event.button == 1:
                        if node.x - node.radius <= event.pos[0] <= node.x + node.radius and node.y - node.radius <= event.pos[1] <= node.y + node.radius:
                            node.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for node in node_list:
                if node.dragging == True:
                    node.dragging = False
                    
        elif event.type == pygame.MOUSEMOTION:
            for node in node_list:
                if node.dragging == True:
                    node.update_position(event.pos[0], event.pos[1], screen)
            update_node_positions(screen, graph)
        
        elif event.type == pygame.VIDEORESIZE:
            # If the screen is resized, update the screen size
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

def color_connected_components(graph):
    visited = set()
    colors = {}
    color_index = 0

    def dfs(node, color):
        visited.add(node)
        colors[node] = color
        for neighbor in graph.adj_list[node]:
            if neighbor not in visited:
                dfs(neighbor, color)

    for node in graph.get_nodes():
        if node not in visited:
            color = tuple(random.sample(range(0, 256), 3))  # generate a unique color for each connected component
            dfs(node, color)
            color_index += 1
    
    return colors


main_graph = Graph()

notas = [
    
    Note(100, 110, 'Bancos de dados relacionais'), 
    Note(110, 120, 'Declaracoes'), 
    Note(120, 130, 'Instroducao ao SQL'), 
    Note(130, 140, 'Tipo de dado'), 

    Note(130, 260, 'Estutura de Dados'), 
    Note(135, 260, 'Arrays'), 
    Note(140, 260, 'Listas'), 
    Note(145, 260, 'Pilhas'), 
    Note(150, 260, 'Filas'), 
    Note(155, 260, 'Arvores'), 
    Note(160, 200, 'Grafos'), 
    Note(165, 220, 'Direcionados'), 
    Note(170, 240, 'Nao Direcionados'), 

    Note(190, 120, 'Calculo 1'), 
    Note(195, 140, 'Derivada'), 
    Note(200, 160, 'Limite'), 
    Note(205, 140, 'Integral'),
    Note(210, 120, 'Calculo 2'), 
    Note(215, 140, 'Series de Potencia'),
    Note(220, 160, 'Formula de Taylor'),
    Note(225, 140, 'Transformada de Laplace'),

    Note(200, 180, 'Pratica de Eletronica Digital 1'),
    Note(180, 100, 'Teoria de Eletronica Digital 1'),
    Note(190, 120, 'Sistemas Numericos'),
    Note(160, 100, 'Binario'),
    Note(170, 140, 'Decimal'),
    Note(180, 150, 'Hexadecimal'),
    Note(170, 100, 'Portas Logicas'),
    Note(180, 100, 'Flip-flops'),
    Note(140, 160, 'Registradores'),
    Note(160, 130, 'Contadores Digitais'),

    Note(300, 200, 'Introducao a Engenharia'),
    Note(320, 210, 'Software'),
    Note(325, 220, 'Eletronica'),
    Note(330, 230, 'Aeroespacial'),
    Note(335, 240, 'Energia'),
    Note(340, 250, 'Automotiva'),

    Note(360, 255, 'Probabilidade e Estatistica Aplicada a Engenharia'),
    Note(180, 150, 'Inferencia Estatistica'), 
    Note(190, 120, 'Probabilidade'),  
    Note(160, 130, 'Distribuicoes de Probabilidade'), 
    Note(240, 100, 'Analise Exploratoria de Dados'), 
    Note(170, 140, 'Estatistica Descritiva'),  
    Note(180, 150, 'Inferencia Estatistica'), 
    Note(170, 100, 'Regressao'), 
    Note(190, 120, 'Analise de Variancia'), 
    Note(180, 100, 'Séries Temporais'),

    Note(300, 200, 'Engenharia Economica'),
    Note(320, 210, 'Desconto'),
    Note(325, 220, 'Analise de Investimento'),
    Note(330, 230, 'Analise de Risco'),

]

arestas = [
    Edge(notas[0], notas[1]),
    Edge(notas[1], notas[0]),
    Edge(notas[2], notas[1]),
    Edge(notas[2], notas[3]),
    Edge(notas[3], notas[1]),

    Edge(notas[4], notas[5]),
    Edge(notas[4], notas[6]),
    Edge(notas[4], notas[7]),
    Edge(notas[4], notas[8]),
    Edge(notas[4], notas[9]),
    Edge(notas[4], notas[10]),
    Edge(notas[10], notas[11]),
    Edge(notas[10], notas[12]),

    Edge(notas[13], notas[14]),
    Edge(notas[14], notas[15]),
    Edge(notas[14], notas[16]),
    Edge(notas[13], notas[17]),
    Edge(notas[17], notas[18]),
    Edge(notas[17], notas[19]),
    Edge(notas[17], notas[20]),

    Edge(notas[21], notas[22]),
    Edge(notas[22], notas[21]),
    Edge(notas[22], notas[23]),
    Edge(notas[23], notas[24]),
    Edge(notas[23], notas[25]),
    Edge(notas[23], notas[26]),
    Edge(notas[22], notas[27]),
    Edge(notas[22], notas[28]),
    Edge(notas[22], notas[29]),
    Edge(notas[22], notas[30]),

    Edge(notas[31], notas[32]),
    Edge(notas[31], notas[33]),
    Edge(notas[31], notas[34]),
    Edge(notas[31], notas[35]),
    Edge(notas[31], notas[36]),

    Edge(notas[37], notas[38]),
    Edge(notas[37], notas[39]),
    Edge(notas[37], notas[40]),
    Edge(notas[39], notas[38]),
    Edge(notas[39], notas[40]),
    Edge(notas[37], notas[41]),
    Edge(notas[37], notas[42]),
    Edge(notas[37], notas[43]),
    Edge(notas[37], notas[44]),
    Edge(notas[37], notas[45]),
    Edge(notas[37], notas[46]),

    Edge(notas[47], notas[48]),
    Edge(notas[47], notas[49]),
    Edge(notas[47], notas[50]),

]

for nota in notas:
    main_graph.add_node(nota)

for aresta in arestas:
    main_graph.add_edge(aresta)

running = True
colors = color_connected_components(main_graph)

import asyncio

async def paint_nodes(graph, colors):
    for node in graph.get_nodes():
        color = colors[node]
        node.color = color
        await asyncio.sleep(0.5)  # Add a delay between color updates

async def main_loop(graph):
    paint_task = asyncio.create_task(paint_nodes(graph, colors))
    while running:
        handle_events(screen, main_graph)
        screen.fill((0, 0, 0))
        draw_edges(screen, main_graph)
        draw_nodes(screen, main_graph)
        pygame.display.update()
        if paint_task.done():
            await paint_task  # Wait for paint_nodes() to finish
        await asyncio.sleep(0.001)  # Add a small delay between loop iterations

asyncio.run(main_loop(main_graph))

# Quit pygame
pygame.quit()