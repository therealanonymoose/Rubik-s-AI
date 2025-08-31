import json, os, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def expand_lbl_moves(moves: list[str]) -> list[str]:
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

def extract(data: str, scr_type: str="str", sol_type: str="list") -> list[dict]:
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
            "scramble": scramble if scr_type == "str" else scramble.split(),
            "solution": solution if sol_type == "list" else ' '.join(solution)
        })
    
    return results

if __name__ == "__main__":
    extracted_data = extract("exports/zz.json", sol_type="str")
    print(extracted_data)