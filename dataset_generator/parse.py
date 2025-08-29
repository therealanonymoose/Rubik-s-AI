# Parse script that turns the output from the modified app into a json ready for training
# Uses PyCuber to manipulate cube, encode states, and save dataset

import pycuber as pc
import json, random, re, os
from utils.encode import encode_cube  # PyCuber cube -> 6x3x3 int array
from utils.export import save_dataset  # write to data jsonimport json
from utils.solvecheck import is_valid_solution as check

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
random.seed(42)  # For reproducibility

def expand_lbl_moves(moves):
    all_moves = []

    for s in moves:
        # Find all groups with optional repetition or single moves
        tokens = re.findall(r'\([^\)]+\)\d*|[^\s]+', s)
        for t in tokens:
            # Match parenthesis with repetition, e.g. (R' D')2
            m = re.match(r'\((.*?)\)(\d*)', t)
            if m:
                group, count = m.groups()
                count = int(count) if count else 1
                moves_in_group = group.split()
                all_moves.extend(moves_in_group * count)
            else:
                # Single move, just strip parentheses if any
                all_moves.append(t.strip("()"))
    
    return all_moves

def extract(data: str) -> list[dict]:
    # Get Scramble and Solution strings from solves.json
    with open(os.path.join(BASE_DIR, data), "r") as f:
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

        if method == "LBL":
            best_match = re.search(r"cross in layer.*?Metric:", report, re.DOTALL)
            section = best_match.group(0) if best_match else "Unknown solution"
        else:
            # Extract the "Best solve" section
            best_match = re.search(r"Best.*?Metric:", report, re.DOTALL)
            section = best_match.group(0) if best_match else "Unknown solution"
        # Extract all move strings inside <span ...>...</span>
        moves = re.findall(r"<span[^>]*>([^<]+)</span>", section)

        # Clean moves (remove leading/trailing spaces)
        # If LBL, expand parentheses; eg (R U)2 = R U R U
        if method == "LBL":
            solution = expand_lbl_moves(moves)
        else:
            solution = [move for m in moves if m.strip() for move in m.strip().split()]
        results.append({
            "method": method,
            "scramble": scramble,
            "solution": solution
        })
    
    return results

def generate_dataset(data: str) -> list[dict]:
    with open(os.path.join(BASE_DIR, "ref", "rotations.json"), "r") as f:
        ROTATIONS = [pc.Formula(r) for r in json.load(f)]
    with open(os.path.join(BASE_DIR, "ref", "move_mapping.json"), "r") as f:
        MOVE_IDS = json.load(f)

    dataset = []
    solves = extract("exports/" + data)

    for solve in solves:
        if check(solve["scramble"], solve["solution"]):
            cube = pc.Cube()
            cube(random.choice(ROTATIONS)) # Apply a random rotation to the cube
            cube(solve["scramble"])

            moves = solve["solution"]
            moves.append("") # Forces one more iteration to make the last move in each entry a solved cube
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
    dataset: list[dict] = generate_dataset("lbl+cfop+roux+zz+petrus.json")
    file = "lbl+cfop+roux+zz+petrus_compact.json"
    save_dataset(dataset, os.path.join(BASE_DIR, "data", file))
    print(f"Dataset generation complete! Saved to {file}")

if __name__ == "__main__":
    main()
