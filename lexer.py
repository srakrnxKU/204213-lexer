"""
Lexer programme for Theory of Computation course,
Sirakorn Lamyai (5910500023)
Department of Computer Engineering, Kasetsart U.
"""


class FiniteAutomata:
    def __init__(self, k, sigma, moves, start):
        self.k = k
        self.sigma = set(sigma)
        self.moves = moves
        self.start = start
        self.state = start

    def move(self, inp):
        move = [i for i in self.moves if i[0] == self.state and i[1] == inp]
        if len(move) == 0:
            self.state = self.start
            return False
        self.state = move[0][2]
        return move[0][3]
