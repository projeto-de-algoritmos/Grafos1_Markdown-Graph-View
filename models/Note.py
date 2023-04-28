class Note:
    def __init__(self, x, y, filename: str, color=(255, 255, 255), radius=10):
        self.filename = filename
        self.next = None

        self.x = x
        self.y = y
        self.color = color
        self.dragging = False # flag to indicate if node is being dragged
        self.radius = radius
    
    def __str__(self):
        return self.filename

    def update_position(self, new_x, new_y, screen):
        # Check if the new position would cause the circle to collide with the border
        if new_x - self.radius < 0:
            new_x = self.radius
        elif new_x + self.radius > screen.get_width():
            new_x = screen.get_width() - self.radius
        if new_y - self.radius < 0:
            new_y = self.radius
        elif new_y + self.radius > screen.get_height():
            new_y = screen.get_height() - self.radius

        # Update the circle's position
        self.x = new_x
        self.y = new_y

    
if __name__ == '__main__':
    nota = Note('Bancos de dados relacionais')
    print(nota)
