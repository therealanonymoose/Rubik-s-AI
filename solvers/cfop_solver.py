# Uses PyCuber's CFOPSolver to generate a CFOP-style solution

import pycuber as pc
from pycuber.solver import CFOPSolver

def solve(cube: pc.Cube) -> pc.Formula:
    # Solves the cube using CFOP method and returns a list of moves in Singmaster notation
    solver: CFOPSolver = CFOPSolver(cube)
    return solver.solve(suppress_progress_messages=True)


# Example usage
if __name__ == "__main__":
    c = pc.Cube()
    scramble = pc.Formula().random()
    c(scramble)
    moves = solve(c)
    print("Scramble:", scramble)
    print("CFOP solution:", moves)

    import utils.solvecheck as sc
    print("Solved:", sc.is_solved(c))
