import lexer

k = [1, 2, 3]
sigma = ['a', 'b']
moves = [(1, '', 2), (2, 'a', 2), (2, 'b', 3), (3, 'a', 1), (3, 'a', 3)]
start = 1
finals = [2]
l = lexer.FiniteAutomata(k, sigma, moves, start, finals)

