import requests
import pandas as pd
import time
from datetime import datetime
import os

def format_timestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    # Check if file exists to handle headers properly
    file_exists = os.path.exists(filename)
    df.to_csv(filename, mode='a', index=False, header=not file_exists)

filename = "/home/briancooke/queue_times_backup.csv"

while True:
    print(f"Fetching queue times at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    parks_url = "https://queue-times.com/parks.json"
    parks_response = requests.get(parks_url)
    parks_data = parks_response.json()

    parks = [{'id': park['id'], 'name': park['name']} for group in parks_data for park in group['parks']]

    queue_times_list = []

    for park in parks:
        park_id = park['id']
        park_name = park['name']
        queue_times_url = f"https://queue-times.com/parks/{park_id}/queue_times.json"

        response = requests.get(queue_times_url)
        if response.status_code == 200:
            queue_data = response.json()
            for land in queue_data.get('lands', []):
                land_name = land.get('name', 'Unknown')
                for ride in land.get('rides', []):
                    formatted_time = format_timestamp(ride['last_updated']) if ride['last_updated'] else "Unknown"
                    queue_times_list.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'park_name': park_name,
                        'ride_name': ride['name'],
                        'ride_type': land_name,
                        'wait_time': ride['wait_time'],
                        'is_open': ride['is_open'],
                        'last_updated': formatted_time
                    })

    if queue_times_list:
        save_to_csv(queue_times_list, filename)
        print(f"Data saved to {filename}")
    else:
        print("No queue times found.")

    print("Sleeping for 15 minutes...\n")
    time.sleep(900)  
