# Saves the generated dataset to JSON
import json

def save_dataset(dataset: list, filename: str, compact=True) -> None:
    # Save dataset (solve list) to JSON file
    with open(filename, "w") as f:
        if compact:
            json.dump(dataset, f, separators=(",", ":"))
        else:
            json.dump(dataset, f, indent=2)