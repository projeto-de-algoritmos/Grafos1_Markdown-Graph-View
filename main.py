import pygame
import sys
import math
import random
import re
import pathlib
import random

from pygame.locals import *
from models.Graph import Graph, Edge
from models.Note import Note

pygame.init()

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)

def color_connected_components(graph):
    visited = set()
    colors = {}
    color_index = 0

    def dfs(node, color):
        visited.add(node)
        colors[node] = (color[0], color[1], color[2], 255)
        for neighbor in graph.adj_list[node]:
            if neighbor not in visited:
                dfs(neighbor, color)

    for node in graph.get_nodes():
        if node not in visited:
            color = tuple(random.randint(0, 255) for i in range(4))  # generate a unique color for each connected component
            dfs(node, color)
            color_index += 1
    
    return colors

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
    print(grafo_dict)
    return grafo

main_graph = criar_grafo ("./arquivos_teste")

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

