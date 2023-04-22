from models.Note import Note

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        print(self.data)

class LinkedList:
    def __init__(self):
        self.head = None
        self.len = 0

    def __str__(self):
        curr_node = self.head
        result = f"{len(self)} elementos:\n"
        counter = 0
        while curr_node is not None:
            result += str(counter) + " - " + str(curr_node.data) + '\n'
            counter += 1
            curr_node = curr_node.next
        return result

    def __len__(self):
        return self.len
    
    def __iter__(self):
        self.curr_node = self.head
        return self

    def __next__(self):
        if self.curr_node is None:
            raise StopIteration
        data = self.curr_node.data
        self.curr_node = self.curr_node.next
        return data
    
    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            curr_node = self.head
            while curr_node.next is not None:
                curr_node = curr_node.next
            curr_node.next = new_node
        self.len += 1


if __name__ == '__main__':
    node_1 = Note('Bancos de dados relacionais')
    node_2 = Note('Declaracoes')
    node_3 = Note('Instroducoa ao SQL')
    node_4 = Note('Tipo de dado')

    lista = LinkedList()
    lista.add_node(node_1)
    lista.add_node(node_2)
    lista.add_node(node_3)
    lista.add_node(node_4)

    print(lista)