import time

print("15 min Testing long job started")

for minute in range(1, 16):  # 15 minutes
    time.sleep(60)  # Sleep for 1 minute
    print(f"{minute} minute(s) passed...")

print("15 min Testing long job ended")

