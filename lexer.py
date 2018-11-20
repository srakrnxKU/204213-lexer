"""
Lexer programme for Theory of Computation course,
Sirakorn Lamyai (5910500023)
Department of Computer Engineering, Kasetsart U.
"""


class FiniteAutomata:
    def __init__(self, k, sigma, moves, start, finals):
        self.k = k
        self.sigma = set(sigma)
        self.moves = moves
        self.start = start
        self.finals = set(finals)
        self.states = set([start])
        self.epsilon_move()

    def is_accepted(self):
        return len(self.states.intersection(self.finals)) > 0

    def epsilon_move(self):
        n_states_before = 1
        n_states_after = 0
        while n_states_before != n_states_after:
            n_states_before = len(self.states)
            for move in self.moves:
                if move[0] in self.states and move[1] == "":
                    self.states.add(move[2])
            n_states_after = len(self.states)

    def move(self, inp):
        new_states = []
        for state in self.states:
            possible_states = [i[2] for i in self.moves if i[0] == state and i[1] == inp]
            new_states += possible_states
        self.states = set(new_states)
        self.epsilon_move()
        return self.states
