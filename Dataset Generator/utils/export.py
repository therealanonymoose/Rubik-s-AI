# Saves the generated dataset to JSON
import json

def save_dataset(dataset: list, filename: str) -> None:
    # Save dataset (solve list) to JSON file
    with open(filename, "w") as f:
        #json.dump(dataset, f, indent=2)
        json.dump(dataset, f, separators=(",", ":")) # more compact