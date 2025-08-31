# Parse script that turns the output from the modified app into a json ready for training
# Uses PyCuber to manipulate cube, encode states, and save dataset

import pycuber as pc
import json, random, re, os
from utils.extract import extract
from utils.encode import encode_cube_array, encode_cube_vector  # PyCuber cube -> 6x3x3 int array
from utils.export import save_dataset  # write to data jsonimport json
from utils.solvecheck import is_valid_solution as check

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
random.seed(42)  # For reproducibility

def generate_dataset(data: str, type: str="vector") -> list[dict]:
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

            moves = solve["solution"] + [""] # Forces one more iteration to make the last move in each entry a solved cube
            steps = []

            for move in moves:
                if MOVE_IDS[str(move)] < 45: # not rotation
                    if type == "vector":
                        state = encode_cube_vector(cube)
                    else:
                        state = encode_cube_array(cube)
                    steps.append({"state": state, "move": MOVE_IDS[str(move)]})
                cube(move)

            dataset.append({
                "method": solve["method"],
                "steps": steps
            })

    return dataset

def main() -> None:
    data = "zz.json"
    data_structure = "array"
    dataset = generate_dataset(data, data_structure)
    dest = f"zz_{data_structure}.json"
    save_dataset(dataset, os.path.join(BASE_DIR, "data", dest))
    print(f"Dataset generation complete! Saved to {dest}")

if __name__ == "__main__":
    main()
