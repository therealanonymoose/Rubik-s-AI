# Main script to generate Rubik's Cube solves for CFOP, Roux, and ZZ methods
# Uses PyCuber to manipulate cube, encode states, and save dataset

import pycuber as pc
import json
import random
from utils.encode import encode_cube  # PyCuber cube -> 6x3x3 int array
from utils.export import save_dataset  # write to data json

from solvers.cfop_solver import solve as cfop_solver

# Configuration
NUM_SOLVES_PER_METHOD: int = 10  # 500
METHODS: list[str] = ["CFOP", "Roux", "ZZ"]

with open("ref/rotations.json", "r") as f:
    ROTATIONS: list[pc.Formula] = [pc.Formula(r) for r in json.load(f)]
with open("ref/move_mapping.json", "r") as f:
    MOVE_IDS: dict[str, int] = json.load(f)

# Methods
def scramble(cube: pc.Cube) -> pc.Formula:
    alg = pc.Formula().random()
    cube(alg)
    return alg

def solve(cube: pc.Cube, method: str) -> pc.Formula:
    # Apply a method-style solve using methods in solvers/
    # Returns a list of moves (formula) in Singmaster notation
    if method == "CFOP":
        return cfop_solver(cube)
    return []

def generate_dataset() -> list[dict]:
    dataset: list[dict] = []
    for method in METHODS:
        for _ in range(NUM_SOLVES_PER_METHOD):
            cube: pc.Cube = pc.Cube()
            scramble_alg = scramble(cube)

            moves: pc.Formula = solve(cube, method)
            steps: list[dict[str, object]] = []

            rotated_cube: pc.Cube = pc.Cube()
            rotated_cube(random.choice(ROTATIONS))
            rotated_cube(scramble_alg)  # Apply a random rotation to the cube

            for move in moves:
                state: list = encode_cube(rotated_cube)  # 6x3x3 int array
                steps.append({"state": state, "move": MOVE_IDS[str(move)]})
                rotated_cube(move)

            dataset.append({
                "method": method,
                "steps": steps
            })
            print(f"Generated solve for {method}")

    return dataset

def main() -> None:
    dataset: list[dict] = generate_dataset()
    save_dataset(dataset, "data/solves.json")
    print("Dataset generation complete! Saved to data/solves.json")

if __name__ == "__main__":
    main()
