import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from extract import extract  # your custom extractor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def analyze_solves(filename: str):
    data = extract("exports/" + filename)
    
    # Flatten data into a table: one row per solve
    records = []
    for solve in data:
        method = solve["method"]
        moves = solve["solution"]  # list of moves
        step_types = solve.get("step_types", ["Unknown"] * len(moves))  # optional step labels
        records.append({
            "method": method,
            "num_moves": len(moves),
            "moves": moves,
            "step_types": step_types
        })
    
    df = pd.DataFrame(records)
    
    # Stats per method
    stats = df.groupby("method")["num_moves"].agg(["mean", "std"]).reset_index()
    stats.rename(columns={"mean": "avg_moves", "std": "stdev_moves"}, inplace=True)
    
    # Move frequency
    move_freq = {}
    for method, group in df.groupby("method"):
        all_moves = [move for moves_list in group["moves"] for move in moves_list]
        freq = pd.Series(all_moves).value_counts().sort_index()
        move_freq[method] = freq

    # Average moves per step type
    step_freq = {}
    for method, group in df.groupby("method"):
        all_steps = [step for steps_list in group["step_types"] for step in steps_list]
        step_counts = pd.Series(all_steps).value_counts()
        step_freq[method] = step_counts
    
    return stats, move_freq, step_freq


def plot_avg_moves(stats: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    sns.barplot(x="method", y="avg_moves", data=stats, palette="Set2", hue="method", errorbar=None)
    plt.errorbar(x=range(len(stats)), y=stats["avg_moves"], yerr=stats["stdev_moves"].values,
                 fmt='none', c='black', capsize=5)
    plt.title("Average Moves per Solve by Method")
    plt.ylabel("Average Moves")
    plt.xlabel("Method")
    plt.tight_layout()
    plt.show(block=False)


def plot_move_frequency(move_freq: dict):
    # Convert move_freq dict into a DataFrame
    all_moves = sorted({move for freq in move_freq.values() for move in freq.index})
    heatmap_data = pd.DataFrame(index=all_moves)

    for method, freq in move_freq.items():
        heatmap_data[method] = freq

    # Fill missing values with 0
    heatmap_data = heatmap_data.fillna(0).astype(int)

    # Convert to percentage per method (column-wise)
    heatmap_percent = heatmap_data.div(heatmap_data.sum(axis=0), axis=1) * 100

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_percent, cmap="viridis", linewidths=0.5, annot=True, fmt=".1f")
    plt.title("Move Frequency (%) per Method")
    plt.xlabel("Method")
    plt.ylabel("Move")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    stats, move_freq, step_freq = analyze_solves("all.json")
    
    print("Stats per method:\n", stats)
    print("\nMove frequency per method:")
    for method, freq in move_freq.items():
        print(f"\nMethod: {method}\n{freq}")
    
    # Plotting
    plot_avg_moves(stats)
    plot_move_frequency(move_freq)
