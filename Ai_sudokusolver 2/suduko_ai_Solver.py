#28 Upadted newer version tested 27th April 2025 

from collections import deque

#LOADING THE PUZZLE WITH PATH
def load_puzzle_from_file(path):
    puzzle = []
    with open(path, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            puzzle.append(row)
    return puzzle

class Sudoku_AI_Solver:
    def __init__(self, board):
        self.board = board
        self.variables = [(i, j) for i in range(9) for j in range(9)]
        self.domains = {}
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.domains[(i, j)] = [self.board[i][j]]
                else:
                    self.domains[(i, j)] = list(range(1, 10))

    def enforce_node_consistency(self):
        for var in self.variables:
            row, col = var
            value = self.board[row][col]
            if value != 0:
                self.domains[var] = [value]

    def neighbors(self, cell):
        i, j = cell
        neighbors = set()
        # Row and column
        for k in range(9):
            if k != j:
                neighbors.add((i, k))
            if k != i:
                neighbors.add((k, j))
        # Box
        box_row = (i // 3) * 3
        box_col = (j // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != cell:
                    neighbors.add((r, c))
        return neighbors

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi][:]:
            if not any(x != y for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def ac3(self):
        queue = deque([(xi, xj) for xi in self.variables for xj in self.neighbors(xi)])
        while queue:
            xi, xj = queue.popleft()
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False  # Domain wiped out, failure
                for xk in self.neighbors(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def assignment_complete(self, assignment):
        return len(assignment) == len(self.variables)

    def consistent(self, assignment):
        for (var, value) in assignment.items():
            for neighbor in self.neighbors(var):
                if neighbor in assignment and assignment[neighbor] == value:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None

    def solve(self):
        self.enforce_node_consistency()
        if not self.ac3():
            return None
        assignment = {}
        for var in self.variables:
            if len(self.domains[var]) == 1:
                assignment[var] = self.domains[var][0]
        return self.backtrack(assignment)

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[i][j] if self.board[i][j] != 0 else ".", end=" ")
            print()

if __name__ == "__main__":
    puzzle_path = r"C:\Users\mitch\OneDrive\Desktop\Ai_sudokusolver 2\sudoku_hard.txt"
    puzzle = load_puzzle_from_file(puzzle_path)

    print("Loaded puzzle:")
    for row in puzzle:
        print(row)

    solver = Sudoku_AI_Solver(puzzle)
    solution = solver.solve()

    if solution:
        print("\nSolved puzzle:")
        for (row, col), value in solution.items():
            solver.board[row][col] = value
        solver.print_board()
    else:
        print("No solution found.")
