import numpy as np
import matplotlib

matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import math


def analyze(values: list):
    if not values:
        print("No data to analyze.")
        return

    v = np.array(values, dtype=np.float64)
    mean = np.mean(v)
    min = np.min(v)
    max = np.max(v)

    v_sorted = np.sort(v)
    n = len(v)
    index = np.arange(1, n + 1)
    gini = (np.sum((2 * index - n - 1) * v_sorted)) / (n * np.sum(v_sorted))

    print("Finantial Report (Satoshis)")
    print("=" * 40)
    print(f"mean:  {mean:,.2f}")
    print(f"min: {min:,.2f}")
    print(f"max: {max:,.2f}")
    print(f"gini:   {gini:.4f} (0 = total equality, 1 = total inequality)")

    first_digit = [int(str(int(val))[0]) for val in v if val > 0]
    count = {i: 0 for i in range(1, 10)}
    for d in first_digit:
        count[d] += 1

    total_valid = len(first_digit)
    freq = [(count[i] / total_valid) * 100 for i in range(1, 10)]

    freq_benford = [math.log10(1 + 1 / i) * 100 for i in range(1, 10)]

    plt.figure(figsize=(20, 20))
    digits = list(range(1, 10))

    plt.bar(digits, freq, color="blue", alpha=0.7, label="Real Data Distribution")
    plt.plot(
        digits,
        freq_benford,
        color="red",
        marker="o",
        linestyle="dashed",
        linewidth=2,
        label="Benford Distribution",
    )
    plt.xticks(digits)
    plt.xlabel("First Digit", fontsize=12, fontweight="bold")
    plt.ylabel("Frequency (%)", fontsize=12, fontweight="bold")
    plt.title(
        "Análise da Lei de Benford - Pagamentos ao Faraó",
        fontsize=14,
        fontweight="bold",
    )
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.savefig("benford_farao.png", dpi=300, bbox_inches="tight")
    print("benford_farao.png saved")
