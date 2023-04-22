import pygame
import sys

pygame.init()

class Node:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.color = (255, 255, 255)
        self.dragging = False # flag to indicate if node is being dragged

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.color = (255, 255, 255)
        self.spring_constant = 0.01 # add spring constant attribute

    def change_color(self, new_color):
        self.color = new_color

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

node_list = [
    Node(100, 100, "Note 1"),
    Node(120, 100, "Note 2"),
    Node(140, 100, "Note 3"),
    Node(160, 100, 'Note 4'),
    Node(180, 100, 'Note 5'),
    Node(150, 100, 'Note 6'),
    Node(160, 100, 'Note 7'),
    Node(170, 100, 'Note 8'),
    Node(180, 100, 'Note 9'),
]

edge_list = [
    Edge(node_list[0], node_list[1]),
    Edge(node_list[0], node_list[2]),
    Edge(node_list[1], node_list[2]),
    Edge(node_list[2], node_list[3]),
    Edge(node_list[2], node_list[5]),
    Edge(node_list[3], node_list[4]),
    Edge(node_list[3], node_list[5]),
    Edge(node_list[4], node_list[6]),
    Edge(node_list[4], node_list[7]),
    Edge(node_list[8], node_list[1])
]

edge_list[0].change_color((255, 255, 0))

def draw_nodes(node_list):
    for node in node_list:
        pygame.draw.circle(screen, node.color, (node.x, node.y), 15)
        font = pygame.font.SysFont(None, 20)
        label = font.render(node.label, True, (255,255,255))
        screen.blit(label, (node.x - label.get_width() // 2, node.y - 20 - label.get_height()))



def draw_edges(edge_list):
    for edge in edge_list:
        pygame.draw.line(screen, edge.color, (edge.start_node.x, edge.start_node.y), (edge.end_node.x, edge.end_node.y), 2)

def update_node_positions(node_list, min_distance=50):
    # calculate force vectors between nodes
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


def handle_events(node_list):
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
    update_node_positions(node_list)

while True:
    handle_events(node_list)
    screen.fill((0, 0, 0))
    draw_nodes(node_list)
    draw_edges(edge_list)
    pygame.display.update()
