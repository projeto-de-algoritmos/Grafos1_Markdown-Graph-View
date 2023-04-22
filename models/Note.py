class Note:
    def __init__(self, filename: str):
        self.filename = filename
        self.next = None

    def __str__(self):
        return self.filename
    
if __name__ == '__main__':
    nota = Note('Bancos de dados relacionais')
    print(nota)
