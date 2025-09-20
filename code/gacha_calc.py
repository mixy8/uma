import random
import argparse
from typing import List
from tabulate import tabulate
import matplotlib.ticker as ticker

PITY = 70
SOFT_PITY_START = 58
SOFT_PITY_INCREMENT = .045
RATE = .01

def soft_pity_calc(i: int) -> float:
    # Pity rate for a SSR
    if i < SOFT_PITY_START:
        return RATE
    if i == PITY:
        return 1.0
    return RATE + (i - SOFT_PITY_START + 1) * SOFT_PITY_INCREMENT

def gacha_until_rate_up(fifty_fifty: bool) -> int:
    """
    Returns the random variable pull count needed to get the target rate up
    """
    # soft_count is used to determine the soft pity probability increase at SOFT_PITY_START
    count = soft_count = 0
    rolled_qiqi = False
    for _ in range(PITY * 2):
        soft_count, count = soft_count + 1, count + 1
        # Rolled an SSR
        if random.random() < soft_pity_calc(soft_count):
            # 50/50 pity or won 50/50
            if not fifty_fifty or rolled_qiqi or random.random() < .5:
                return count
            else:
                rolled_qiqi = True
                soft_count = 0
    # return count
    

def sim(trials: int) -> List[int]:
    """
    Given a number of trials, output an array where the ith value is the amount of people
    that have gotten their wife at that pull
    """
    # pulls_to_gacha[i] += 1 if received morry's wife at the ith pull
    pulls_to_gacha = [0 for _ in range(PITY * 2 + 1)]
    for _ in range(trials):
        pulls_to_gacha[gacha_until_rate_up(False)] += 1
    return pulls_to_gacha


def gacha_table(sim_results: List[int]) -> None:
    """
    Takes the output of sim(trials) and prints a table with:
    - Pull number
    - Number of players who got the target at that pull
    - Cumulative % of players who have obtained the target by that pull
    """
    total_players = sum(sim_results)
    cumulative = 0

    table = []
    for pull, count in enumerate(sim_results):
        if count == 0:
            continue  # skip pulls with zero counts
        cumulative += count
        cumulative_pct = cumulative / total_players * 100
        table.append([pull, count, round(cumulative_pct, 4)])

    print(tabulate(table, headers=["Pull", "Count", "Cumulative %"], tablefmt="pretty"))

def gacha_plot_seaborn(sim_results: List[int], filename_prefix="gacha") -> None:
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    # Helper to save 4K
    def save_4k(fig, filename: str):
        width_in = 3840 / 200  # 200 DPI → 19.2 in
        height_in = 2160 / 200 # 200 DPI → 10.8 in
        fig.set_size_inches(width_in, height_in)
        fig.savefig(filename, dpi=200, bbox_inches="tight")
        plt.close(fig)

    total_players = sum(sim_results)
    cumulative = 0
    pulls, counts, cumulative_pcts = [], [], []

    for pull, count in enumerate(sim_results):
        if count == 0:
            continue
        cumulative += count
        pulls.append(pull)
        counts.append(count)
        cumulative_pcts.append(cumulative / total_players * 100)

    # Prettier theme
    sns.set_theme(style="ticks", palette="pastel")

    # --- Distribution line plot ---
    fig, ax = plt.subplots()
    sns.lineplot(x=pulls, y=counts, marker="o", color="tab:blue", ax=ax)
    ax.set_xlabel("Pull number", fontsize=16)
    ax.set_ylabel("Number of players", fontsize=16)
    ax.set_title("Distribution of pulls until rate-up", fontsize=20)

    # Secondary axis for %
    ax2 = ax.twinx()
    ax2.set_ylabel("Percentage of players", fontsize=16)
    ax2.set_ylim(0, max(counts) / sum(counts) * 100 * 1.1)
    ax2.yaxis.set_major_formatter(lambda y, _: f"{y:.1f}%")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.setp(ax.get_xticklabels(), rotation=45, fontsize=12)

    save_4k(fig, f"{filename_prefix}_distribution.png")

    # --- Cumulative line plot ---
    fig, ax = plt.subplots()
    sns.lineplot(x=pulls, y=cumulative_pcts, marker="o", color="tab:green", ax=ax)
    ax.set_xlabel("Pull number", fontsize=16)
    ax.set_ylabel("Cumulative % of players", fontsize=16)
    ax.set_title("Cumulative probability of obtaining rate-up", fontsize=20)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.setp(ax.get_xticklabels(), rotation=45, fontsize=12)

    save_4k(fig, f"{filename_prefix}_cumulative.png")

        
def main():
    parser = argparse.ArgumentParser(
        description="morry"
    )
    parser.add_argument(
        "trials", 
        type=int, 
        help="Number of times to gacha sim"
    )
    args = parser.parse_args()

    # gacha_table(sim(args.trials))
    gacha_plot_seaborn(sim(args.trials))

    # print(soft_pity_calc(58))
    # print(soft_pity_calc(69))
    # print(soft_pity_calc(70))


if __name__ == "__main__":
    main()
