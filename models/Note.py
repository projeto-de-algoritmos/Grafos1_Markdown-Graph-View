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

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    
if __name__ == '__main__':
    nota = Note('Bancos de dados relacionais')
    print(nota)
