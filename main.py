# Main script to generate Rubik's Cube solves for CFOP, Roux, and ZZ methods
# Uses PyCuber to manipulate cube, encode states, and save dataset

import pycuber as pc
import json
from utils.encode import encode_cube  # PyCuber cube -> 6x3x3 int array
from utils.export import save_dataset  # write to data json

from solvers.cfop_solver import solve as cfop_solver

# Configuration
NUM_SOLVES_PER_METHOD = 10 #500
METHODS = ["CFOP", "Roux", "ZZ"]

with open("ref/move_mapping.json", "r") as f:
    MOVE_IDS= json.load(f)

def scramble(cube: pc.Cube):
    alg = pc.Formula().random()
    cube(alg)

def solve(cube: pc.Cube, method: str) -> pc.Formula:
    # Apply a method-style solve using methods in solvers/
    # Returns a list of moves (formula) in Singmaster notation
    if method == "CFOP":
        return cfop_solver(cube)
    return []

def generate_dataset():
    dataset = []
    for method in METHODS:
        for _ in range(NUM_SOLVES_PER_METHOD):
            cube = pc.Cube()
            scramble(cube)

            moves = solve(cube, method)
            steps = []

            for move in moves:
                state = encode_cube(cube)  # 6x3x3 int array
                steps.append({"state": state, "move": MOVE_IDS[str(move)]})
                cube(move)

            dataset.append({
                "method": method,
                "steps": steps
            })
            print(f"Generated solve for {method}")

    return dataset

def main():
    dataset = generate_dataset()
    save_dataset(dataset, "data/solves.json")
    print("Dataset generation complete! Saved to data/solves.json")

if __name__ == "__main__":
    main()
