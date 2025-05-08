from timelord import TimeLord
import datetime

tl = TimeLord()

# Mark location (must match a settlement or POI name from world.json)
tl.mark_location("Rynn", "Aetherholt")

# Get starting time
base_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

# Simulate 24 hourly ticks with biome-aware events
print("--- JOURNAL ENTRIES ---")
for i in range(24):
    tick_time = base_time + datetime.timedelta(hours=i)
    timestamp, event = tl.simulate_hourly_tick(custom_time=tick_time)
    print(f"[{timestamp}] {event}")

# Simulate 10 combat rounds
print("\n--- COMBAT ROUND SIMULATION ---")
for round_num in range(10):
    timestamp, event = tl.simulate_round_tick(base_time, round_number=round_num)
    print(f"[Round {round_num+1} | {timestamp}] {event}")

# Time skip summary
rynn_summary = tl.restore_passage("Rynn")
print("\n--- TIME SKIP SUMMARY ---")
print(rynn_summary)
