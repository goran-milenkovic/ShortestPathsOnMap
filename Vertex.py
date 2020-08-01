class Vertex:
    """ each vertex is 2-tupple (row,column) where row is given number 
        and column is also number mapped from given column letter by ord(letter) -64
        mapping: A -> 1, B -> 2...
        I assumed that column is represented with one big letter, otherwise
        is sum of all letters
     """

    def __init__(self, i, j):
        self.vertex = (i, j)

    # vertex hash required for comparing vertices based on row and column of cell
    def __hash__(self):
        return hash((self.vertex[0], self.vertex[1]))

    # modified equal method for vertex
    def __eq__(self, other):
        return self.vertex[0] == other.vertex[0] and self.vertex[1] == other.vertex[1]

    # modified string representation of vertex
    def __str__(self):
        return f"({self.vertex[0]},{self.vertex[1]})"
