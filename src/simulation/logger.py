def log_event(filename, message):
    with open(f"data/{filename}.txt", "a") as file:
        file.write(message + "\n")

def clear_logs():
    files = ["completion_times", "station_blockages", "train_arrivals", "train_delays", "train_schedules"]
    for f in files:
        with open(f"data/{f}.txt", "w") as file:
            file.truncate(0)       
    