# Parse script that turns the output from the modified app into a json ready for training
# Uses PyCuber to manipulate cube, encode states, and save dataset

import pycuber as pc
import json
import random
import re
from utils.encode import encode_cube  # PyCuber cube -> 6x3x3 int array
from utils.export import save_dataset  # write to data jsonimport json
from utils.solvecheck import is_valid_solution as check


def extract(dataset: str) -> list[dict]:
    # Get Scramble and Solution strings from solves.json
    with open(dataset, "r") as f:
        data = json.load(f)

    results = []

    for solve in data:
        report = solve["report"]

        # Extract the method name from the "id" field
        method_match = re.match(r"(.+?) solve", solve["id"])
        method = method_match.group(1) if method_match else "Unknown method"

        # Extract the scramble
        scramble_match = re.search(r"Scramble: \[([^\]]+)\]", report)
        scramble = scramble_match.group(1) if scramble_match else "Unknown scramble"

        # Extract the "Best solve" section
        best_match = re.search(r"Best.*?Metric:", report, re.DOTALL)
        section = best_match.group(0) if best_match else "Unknown solution"
        # Extract all move strings inside <span ...>...</span>
        moves = re.findall(r"<span[^>]*>([^<]+)</span>", section)
        # Clean moves (remove leading/trailing spaces)
        moves = [move for m in moves if m.strip() for move in m.strip().split()]
        results.append({
            "method": method,
            "scramble": scramble,
            "solution": moves
        })
    
    return results

def generate_dataset() -> list[dict]:
    with open("ref/rotations.json", "r") as f:
        ROTATIONS = [pc.Formula(r) for r in json.load(f)]
    with open("ref/move_mapping.json", "r") as f:
        MOVE_IDS = json.load(f)

    dataset = []
    solves = extract("solves.json")

    for solve in solves:
        if check(solve["scramble"], solve["solution"]):
            cube = pc.Cube()
            cube(random.choice(ROTATIONS)) # Apply a random rotation to the cube
            cube(solve["scramble"])

            moves = solve["solution"]
            steps = []

            for move in moves:
                state = encode_cube(cube)  # 6x3x3 int array
                steps.append({"state": state, "move": MOVE_IDS[str(move)]})
                cube(move)

            dataset.append({
                "method": solve["method"],
                "steps": steps
            })

    return dataset

def main() -> None:
    dataset: list[dict] = generate_dataset()
    save_dataset(dataset, "data.json")
    print("Dataset generation complete! Saved to data.json")

if __name__ == "__main__":
    main()
