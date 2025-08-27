# Script to check how many unknown solutions exist in the dataset

from parse import extract # Run from Dataset Generator to resolve imports: ./myenv/bin/python -m utils.check_unknown

def check(data: str, print_unknown=False) -> int:
    solves = extract("exports/" + data)
    count = 0
    counts = {}

    for i, solve in enumerate(solves):
        if not solve["solution"]:
            if print_unknown:
                print(f"Unknown solution found in entry {i}: {solve}")
            count += 1
            counts[solve["method"]] = counts.get(solve["method"], 0) + 1

    if print_unknown:
        for method, c in counts.items():
            print(f"{method} has {c} unknown solutions")

    return count

if __name__ == "__main__":
    unknown_count = check("lbl+cfop+roux+zz+petrus.json", True)
    print(f"Total unknown solutions: {unknown_count}")