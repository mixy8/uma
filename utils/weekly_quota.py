import argparse
from datetime import datetime, timedelta
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Generate weekly quotas with cumulative days")
    parser.add_argument("--start", required=True, help="Start date/time (YYYY-MM-DD HH:MM)")
    parser.add_argument("--end", required=True, help="End date/time (YYYY-MM-DD HH:MM)")
    parser.add_argument("--daily_quota", type=float, help="Daily quota (ignored if weekly_quota is given)")
    parser.add_argument("--weekly_quota", help="Comma-delimited weekly quotas (overrides daily_quota)")
    parser.add_argument("--relative_end", action="store_true", help="Show second timestamp as relative time in Discord")
    return parser.parse_args()

def to_discord_ts(dt, relative=False):
    ts = int(dt.timestamp())
    return f"<t:{ts}{':R' if relative else ''}>"

def main():
    args = parse_args()

    start_dt = datetime.strptime(args.start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(args.end, "%Y-%m-%d %H:%M")

    weekly_quotas = []
    if args.weekly_quota:
        weekly_quotas = [float(x) * 7 for x in args.weekly_quota.split(",")]

    print(f"{'Week':<5} {'Start':<22} → {'End':<22} {'Days':<5} {'Quota/Wk':<6} {'Accumulated'}")
    print("-" * 76)

    current_dt = start_dt
    week_index = 0
    accumulated_quota = 0
    accumulated_days = 0

    while current_dt < end_dt:
        week_start = current_dt
        week_end = min(week_start + timedelta(days=7), end_dt)

        days_this_week = (week_end - week_start).days
        accumulated_days += days_this_week

        if weekly_quotas:
            quota = int(weekly_quotas[week_index])
        else:
            quota = int(math.ceil(days_this_week * args.daily_quota))

        accumulated_quota += quota

        print(
            f"{week_index+1:<5} "
            f"{to_discord_ts(week_start):<22} → "
            f"{to_discord_ts(week_end, args.relative_end):<22} "
            f"{accumulated_days:<5} "
            f"{quota:<8} "
            f"{accumulated_quota}m"
        )

        current_dt = week_end
        week_index += 1

if __name__ == "__main__":
    main()

