import json, os, random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#random.seed(42)  # For reproducibility

def sample_solves(dataset: str, start: int, n: int) -> list[dict]:
    with open(os.path.join(BASE_DIR, "data", dataset), "r") as f:
        data = json.load(f)
    return data[start:start+n]

def sample_random_solves(dataset: str, n: int) -> list[dict]:
    with open(os.path.join(BASE_DIR, "data", dataset), "r") as f:
        data = json.load(f)
    return random.sample(data, n)

if __name__ == "__main__":
    file = "zz.json"
    print(sample_random_solves(file, 1))
